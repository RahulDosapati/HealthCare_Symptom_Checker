
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Support Google Gemini via GEMINI_API_KEY. If not provided, fall back to a local heuristic generator
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

USE_GEMINI = bool(GEMINI_API_KEY)

if USE_GEMINI:
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)

        GENERATION_CONFIG = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GENERATION_CONFIG,
            system_instruction=(
                "You are a helpful, factual, and empathetic healthcare assistant. "
                "When given symptoms, suggest possible medical conditions, causes, and self-care steps. "
                "Always include a disclaimer that this is for educational purposes only and not a diagnosis. "
                "Use structured formatting with bullet points or numbered lists when possible."
            ),
        )
    except Exception as e:
        USE_GEMINI = False
        model = None
        print(f"Warning: Could not initialize Google Gemini client: {e}")
else:
    model = None


def _local_fallback_generator(symptom_text: str) -> str:
    """A conservative, rule-based fallback that returns safe, high-level suggestions.

    This is meant for local development when an LLM key isn't provided. It is intentionally
    non-medical and provides generic possibilities and clear disclaimers.
    """
    text = symptom_text.lower()
    candidates = []
    recs = [
        "Rest and stay hydrated",
        "Over-the-counter remedies may help symptom relief",
        "Monitor symptoms for 48-72 hours",
        "Seek urgent care if severe or worsening symptoms"
    ]

    if any(k in text for k in ["fever", "temperature"]):
        candidates.append("Viral infection (e.g., common cold, seasonal flu)")
    if any(k in text for k in ["cough", "sore throat", "runny", "sneeze"]):
        candidates.append("Upper respiratory tract infection")
    if any(k in text for k in ["chest pain", "shortness of breath", "difficulty breathing"]):
        candidates = ["Potentially serious condition — seek immediate medical attention"]

    if not candidates:
        candidates = ["Non-specific symptoms — consider general viral illnesses or allergic causes"]

    return (
        "Possible conditions:\n- "
        + "\n- ".join(candidates)
        + "\n\nRecommended next steps:\n- "
        + "\n- ".join(recs)
        + "\n\nDisclaimer: For educational purposes only. Not a medical diagnosis."
    )


def generate_diagnosis(symptom_text: str) -> str:
    """Generate a diagnosis string for given symptom text.

    Attempts to use Google Gemini if configured; otherwise returns a conservative fallback.
    """
    if not symptom_text or not symptom_text.strip():
        return "⚠️ Please provide a valid symptom description."

    if USE_GEMINI and model is not None:
        try:
            response = model.generate_content(
                [f"Symptoms: {symptom_text}\n\nSuggest probable conditions and next steps."]
            )
            return response.text.strip() if response and getattr(response, "text", None) else "⚠️ No response generated."
        except Exception as e:
            # fall back to local generator but include error info
            return f"⚠️ LLM error: {e}\n\n" + _local_fallback_generator(symptom_text)
    else:
        return _local_fallback_generator(symptom_text)


if __name__ == "__main__":
    print(generate_diagnosis("I have cough, mild fever, and sore throat for 2 days"))
