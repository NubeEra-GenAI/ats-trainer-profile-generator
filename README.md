# 📄 ATS-Friendly Trainer Profile Generator

Generate **professional, ATS-optimized trainer profiles** from requirement documents and your existing profile data — powered by **ChatGPT API** and a clean **Streamlit web app**.

---

## 🚀 Features
- 📝 Upload **requirements.docx** and **profile.docx**
- 🤖 Uses **ChatGPT (GPT-4o / GPT-4o-mini)** to rewrite your trainer profile
- 🎯 ATS-friendly structure with **categories + technology keywords**
- 📂 Download polished **.docx output** with professional formatting (Headings, Bullets)
- 🖥️ Easy to run via **Streamlit**

---

## 📂 Project Structure

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/ats-trainer-profile-generator.git
cd ats-trainer-profile-generator
```
### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```
```bash
export OPENAI_API_KEY="sk-xxxx"      # Linux/Mac
setx OPENAI_API_KEY "sk-xxxx"        # Windows PowerShell
```
### ▶️ Usage: Run the Streamlit app:
```bash
streamlit run app.py
```
- Upload requirements.docx (training request from client)

- Upload profile.docx (your current trainer profile)

- Click Generate Profile

- Download your new ATS-optimized trainer profile 🎉
