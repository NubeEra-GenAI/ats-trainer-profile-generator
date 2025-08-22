import streamlit as st
from openai import OpenAI
from docx import Document
from io import BytesIO
import os

# -----------------------
# OpenAI Config
# -----------------------
# Make sure you set your API key as an environment variable:
# export OPENAI_API_KEY="sk-..."
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------
# Helpers
# -----------------------
def read_docx(file):
    doc = Document(file)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text

def ask_chatgpt(requirements, profile_text):
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
- Output plain text only (no Markdown # or **).

REQUIREMENTS:
{requirements}

PROFILE DATA:
{profile_text}

Return only the rewritten profile text, structured and formatted as instructed.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # you can also use gpt-4o for more quality
        messages=[
            {"role": "system", "content": "You are a professional trainer profile generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def create_docx_clean(text):
    doc = Document()
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Section headings
        if line.upper() in [
            "SUMMARY", "KEY SKILLS", "INDUSTRIAL WORKING EXPERIENCE",
            "CORPORATE TRAINING EXPERIENCE", "RETAIL TRAINING EXPERIENCE",
            "MATERIAL EXPERIENCE", "CERTIFICATIONS", "EDUCATION", "PERSONAL DETAILS"
        ]:
            para = doc.add_paragraph(line)
            para.style = "Heading 1"
        # Bullets
        elif line.startswith(("-", "•")):
            clean = line.lstrip("-• ").strip()
            para = doc.add_paragraph(clean)
            para.style = "List Bullet"
        else:
            para = doc.add_paragraph(line)
            para.style = "Normal"

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# -----------------------
# Streamlit UI
# -----------------------
st.title("📄 ATS-Friendly Trainer Profile Generator (ChatGPT API)")

req_file = st.file_uploader("Upload Requirements Document (.docx)", type=["docx"])
profile_file = st.file_uploader("Upload Profile Document (.docx)", type=["docx"])

if st.button("Generate Profile"):
    if req_file and profile_file:
        with st.spinner("Processing with ChatGPT…"):
            requirements_text = read_docx(req_file)
            profile_text = read_docx(profile_file)

            rewritten_text = ask_chatgpt(requirements_text, profile_text)

            final_doc = create_docx_clean(rewritten_text)

            st.success("✅ ATS-friendly trainer profile generated!")
            st.download_button(
                label="📥 Download Final Profile",
                data=final_doc,
                file_name="trainer_profile_final.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    else:
        st.error("⚠️ Please upload both documents before generating.")
