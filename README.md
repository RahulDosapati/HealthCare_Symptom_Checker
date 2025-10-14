# 🩺 Healthcare Symptom Checker

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
git clone https://github.com/RajeshAndra/Healthcare-Symptom-Checker.git
cd Healthcare-Symptom-Checker
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set your API key

Create a `.env` file in the root:

```
GEMINI_API_KEY=your_google_api_key_here
```

### 4️⃣ Run the backend

```bash
uvicorn backend.main:app --reload
```

### 5️⃣ Run the frontend

```bash
streamlit run frontend/app.py
```

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

