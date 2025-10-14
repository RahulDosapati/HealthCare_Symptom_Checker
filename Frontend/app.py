# frontend/app.py
import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api/diagnose")
LOGS_URL = os.getenv("LOGS_URL", "http://localhost:8000/api/logs")

# Page setup
st.set_page_config(page_title="Symptom Checker", layout="centered")

tab1, tab2 = st.tabs(["🩺 Symptom Checker", "📜 Database Logs"])

# ---------------------------
# 🩺 TAB 1 — Symptom Checker
# ---------------------------
with tab1:
    st.title("Healthcare Symptom Checker")
    st.caption("For **educational purposes only** — not a medical diagnosis.")

    symptoms = st.text_area(
        "Describe your symptoms:",
        placeholder="E.g., cough, fever, sore throat for 3 days",
    )
    user_id = st.text_input("User ID (optional):", "anonymous")

    if st.button("Check Symptoms"):
        if not symptoms.strip():
            st.error("Please enter your symptoms.")
        else:
            with st.spinner("Analyzing symptoms..."):
                try:
                    res = requests.post(API_URL, json={"text": symptoms, "user_id": user_id})
                    if res.status_code == 200:
                        data = res.json()
                        st.subheader("🧾 Result:")
                        st.write(data.get("result", "No response."))
                        st.caption(data.get("disclaimer", ""))
                    else:
                        st.error(f"API Error {res.status_code}: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

# ---------------------------
# 📜 TAB 2 — Database Logs
# ---------------------------
with tab2:
    st.title("Database Logs")
    st.caption("Displays the most recent queries stored in the backend database.")

    if st.button("🔄 Refresh Logs"):
        with st.spinner("Fetching logs..."):
            try:
                res = requests.get(LOGS_URL)
                if res.status_code == 200:
                    logs = res.json().get("logs", [])
                    if logs:
                        for log in logs:
                            with st.expander(f"🩹 {log['symptom'][:60]}"):
                                st.markdown(f"**ID:** {log['id']}")
                                st.markdown(f"**Symptom:** {log['symptom']}")
                                st.markdown(f"**created_at:** {log['created_at']}")
                                st.markdown(f"**Response:** {log['response']}")
                    else:
                        st.info("No logs available yet.")
                else:
                    st.error(f"API Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Error fetching logs: {e}")
