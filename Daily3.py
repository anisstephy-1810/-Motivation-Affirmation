import streamlit as st
import google.generativeai as genai

# ---------------------------
# Configuration
# ---------------------------
GEMINI_API_KEY = "AIzaSyDnH78k_Sj1y0fziRvS6VKkYe8u0lGsLyw"  # Replace this with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🌟 Motivation & Affirmation Generator", layout="centered")
st.title("🌟 Motivation & Affirmation Generator")

# Input: User scenario
scenario = st.text_area("💬 Describe your current situation or feeling:",
                        placeholder="E.g., I'm feeling anxious about my exams...")

# Input: Type of message
motivation_type = st.selectbox("💡 What kind of support do you need?",
                               ["Motivation", "Daily Affirmation", "Confidence Booster", "Self-Love Reminder", "Stress Relief"])

# Initialize session state
if 'output' not in st.session_state:
    st.session_state.output = ""

# ---------------------------
# Prompt creation
# ---------------------------
def create_prompt(scenario_text, type_text, variation=False):
    base_tone = "uplifting" if not variation else "gentle, poetic or calming"
    return (
        f"You are a supportive coach. Based on the user's situation below, write a short and {base_tone} "
        f"{type_text.lower()} in 2-3 sentences.\n\n"
        f"Scenario: {scenario_text}\n"
        f"Output:"
    )

# ---------------------------
# Output generation
# ---------------------------
def generate_response(scenario_text, type_text, variation=False):
    prompt = create_prompt(scenario_text, type_text, variation)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# ---------------------------
# Generate Button
# ---------------------------
if st.button("✨ Generate"):
    if scenario.strip() == "":
        st.warning("Please describe your scenario first.")
    else:
        result = generate_response(scenario, motivation_type)
        st.session_state.output = result

# ---------------------------
# Regenerate Button
# ---------------------------
if st.session_state.output:
    if st.button("🔁 Regenerate with New Tone"):
        result = generate_response(scenario, motivation_type, variation=True)
        st.session_state.output = result

# ---------------------------
# Show Output
# ---------------------------
if st.session_state.output:
    st.markdown("### 🌈 Here's your Motivation / Affirmation:")
    st.success(st.session_state.output)
