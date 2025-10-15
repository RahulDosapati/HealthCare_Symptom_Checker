# 🩺 Healthcare Symptom Checker

Author: Rahul  
GitHub: https://github.com/RahulDosapati/Healthcare_Symptom_Checker

An AI-powered web app that analyzes user-reported symptoms and provides **educational insights** on possible conditions and next steps.
Built using **Python, Streamlit, FastAPI, SQLite**, and **Google Gemini LLM**.

---

## 🚀 Features

* 🤖 **LLM-powered diagnosis suggestions** using Google Gemini
* 🧾 **Educational disclaimer** for safe, non-clinical use
* 💾 **SQLite database** to store query history
* 🌐 **Streamlit frontend** + **FastAPI backend**
* 📜 **View saved queries** directly in the app

---

## 🛠️ Tech Stack

| Layer          | Technology                            |
| -------------- | ------------------------------------- |
| Frontend       | Streamlit                             |
| Backend        | FastAPI                               |
| LLM            | Google Gemini (`google-generativeai`) |
| Database       | SQLite                                |
| Env Management | Python-dotenv                         |

---

## ⚙️ Setup

### 1️⃣ Clone the repo

```bash
git clone https://github.com/<your-github-username>/Healthcare-Symptom-Checker.git
cd Healthcare-Symptom-Checker
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set your API key

Create a `.env` file in the `Backend/` folder (or set environment variables):

```
GEMINI_API_KEY=your_google_api_key_here
```

If you do not provide a `GEMINI_API_KEY`, the backend will use a conservative local fallback generator for development. The fallback is intentionally non-diagnostic and returns general, high-level suggestions only.

### 4️⃣ Run the backend

```bash
cd Backend
uvicorn main:app --reload --port 8000
```

### 5️⃣ Run the frontend

```bash
streamlit run Frontend/app.py
```

Notes:
- The FastAPI backend listens on port 8000 by default. Adjust `API_URL` and `LOGS_URL` via environment variables in `Frontend/app.py` if needed.
- This project is for educational/demo purposes only. It is not medical advice and should never replace consultation with a qualified healthcare professional.

---

## 📤 Preparing to push this repo to your GitHub

Before pushing, replace the placeholders at the top of this README with your name and GitHub username.

Set your repo as the remote and push:

```bash
git remote remove origin || true
git remote add origin https://github.com/<your-github-username>/Healthcare-Symptom-Checker.git
git branch -M main
git push -u origin main
```

If you want your future commits to show your name and email locally, configure git:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

If you need to rewrite commit authorship in existing commits, do that carefully (this rewrites history). A simple approach for small repos:

```bash
# Replace author/email for all commits (rewrites history)
git filter-branch --env-filter '
OLD_EMAIL="old@example.com"
CORRECT_NAME="Your Name"
CORRECT_EMAIL="you@example.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then
	export GIT_COMMITTER_NAME="$CORRECT_NAME"
	export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then
	export GIT_AUTHOR_NAME="$CORRECT_NAME"
	export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

NOTE: Rewriting history is destructive — only do this if you understand git history rewriting and you control the remote repository.

---

## 🧠 API Endpoints

| Endpoint        | Method | Description                           |
| --------------- | ------ | ------------------------------------- |
| `/api/diagnose` | POST   | Generate diagnosis suggestions        |
| `/api/logs`     | GET    | Retrieve stored symptom-response logs |

---

## 🧾 Example Output

**Input:**

> “I have a sore throat and mild fever for 2 days.”

**Output:**

* Possible conditions: Common cold, mild viral infection
* Recommendations: Rest, hydrate, consult doctor if worsens
* Disclaimer: *Educational purpose only — not medical advice.*

