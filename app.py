import streamlit as st
import docx
from docx import Document
import requests
import os
from io import BytesIO
import re
from openai import OpenAI


# -------------------------
# Config
# -------------------------
OPENROUTER_API_KEY = os.getenv(OPENROUTER_API_KEY)  # put your key here
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

# -----------------------
# Helpers
# -----------------------
def read_docx(file):
    doc = Document(file)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text

def ask_ai(requirements, profile_text):
    prompt = f"""
You are an expert CV/profile rewriting assistant.

TASK:
- Rewrite the trainer profile using the given requirements.
- Keep the document structure professional and ATS-friendly.
- Section order:
  1. Summary
  2. Key Skills (with categories AND representative technology keywords, e.g. Big Data (Spark, Kafka, Hadoop))
  3. Industrial Working Experience (per client: Client, Focus, Technologies (categories + key tools), Achievements)
  4. Corporate Training Experience
  5. Retail Training Experience
  6. Material Experience
  7. Certifications
  8. Education
  9. Personal Details
- Replace long raw tool dumps with concise categories, but keep keyword coverage for ATS.
- Output clean text (no Markdown hashes ###, no asterisks **).
- Use professional formatting that can be mapped to Word headings and bullet points.

REQUIREMENTS:
{requirements}

PROFILE DATA:
{profile_text}

Return only the rewritten profile text, structured and formatted as instructed.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional trainer profile generator."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    response.raise_for_status()
    response_json = response.json()

    return response_json["choices"][0]["message"]["content"]

def create_docx(text):
    doc = Document()
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Headings
        if re.match(r"^#{1,3}\s", line):
            clean = re.sub(r"^#+\s*", "", line)
            para = doc.add_paragraph(clean)
            para.style = "Heading 1"

        # Bold headings (e.g., **Client: MTData**)
        elif re.match(r"^\*\*.*\*\*$", line):
            clean = line.replace("**", "")
            para = doc.add_paragraph(clean)
            para.style = "Heading 2"

        # Bullet points
        elif line.startswith(("-", "•")):
            clean = line.lstrip("-• ").strip()
            para = doc.add_paragraph(clean)
            para.style = "List Bullet"

        # Normal text
        else:
            clean = line.replace("**", "")
            para = doc.add_paragraph(clean)
            para.style = "Normal"

    # Save to memory buffer (for Streamlit download)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
# -----------------------
# Streamlit UI
# -----------------------
st.title("📄 ATS-Friendly Trainer Profile Generator")

req_file = st.file_uploader("Upload Requirements Document (.docx)", type=["docx"])
profile_file = st.file_uploader("Upload Profile Document (.docx)", type=["docx"])

if st.button("Generate Profile"):
    if req_file and profile_file:
        with st.spinner("Processing..."):
            requirements_text = read_docx(req_file)
            profile_text = read_docx(profile_file)

            rewritten_text = ask_ai(requirements_text, profile_text)

            final_doc = create_docx(rewritten_text)

            st.success("✅ ATS-friendly trainer profile generated!")
            st.download_button(
                label="📥 Download Final Profile",
                data=final_doc,
                file_name="trainer_profile_final.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    else:
        st.error("⚠️ Please upload both documents before generating.")
