import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURE YOUR GEMINI API KEY
# ==========================================
# Replace the text below with the secret API Key you grabbed from Google AI Studio
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# ==========================================
# 2. STREAMLIT USER INTERFACE (UI)
# ==========================================
st.set_page_config(page_title="The Friction Fighter", page_icon="🛡️", layout="centered")

st.title("🛡️ The Friction Fighter")
st.subheader("Move past generic to-do lists. Get your behavioral battle plan.")
st.write("---")

# Input 1: The Chaos Brain-Dump
user_tasks = st.text_area(
    "Brain-dump everything on your plate right now (messy is fine!):",
    placeholder="e.g., I have an engineering assignment due at 5 PM, need to clean my room, and I'm totally overwhelmed..."
)

# Input 2: The Energy Slider (Matches Pillar #2 of your system instructions!)
energy_level = st.slider("What is your current physical/mental energy level right now?", 1, 10, 5)

st.write("---")

# ==========================================
# 3. CORE APPLICATION LOGIC
# ==========================================
if st.button("⚡ Generate My Battle Plan", type="primary"):
    if user_tasks.strip() == "":
        st.error("Please dump at least one task or deadline so the Friction Fighter can assist you!")
    else:
        with st.spinner("Analyzing energy metrics and breaking down mental friction..."):
            try:
                # Initialize the model using Gemini 1.5 Flash
                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash',
                    system_instruction="""You are "The Friction Fighter," a hyper-proactive, behavioral-science-backed productivity companion designed to save users from deadline panic. Your goal is to move beyond passive reminders and force "meaningful action" by eliminating the mental friction of starting a task.

You must strictly analyze the user's input based on three secret pillars:

1. THE ANTI-PROCRASTINATION "MICRO-STEP": For every major task the user provides, you must break the initial entry barrier down to a ridiculous, un-intimidating action that takes under 2 minutes.
2. CHRONOBIOLOGY ADAPTATION: You will receive the user's current energy level (on a scale of 1-10). If energy is low (1-4), intentionally defer high-cognition tasks and prioritize low-effort quick wins to build momentum. If energy is high (7-10), block out their hardest, most critical deadline tasks immediately.
3. ADVERSARIAL ACCOUNTABILITY (THE TWIST): You do not just list tasks. You must predict exactly *why* the user will fail or procrastinate on each specific item based on human nature, and explicitly write out a counter-strategy for them.

Output Format Requirements:
- Tone: Empathetic, direct, witty, and grounded. No corporate jargon.
- Format: Use clear markdown headers, bold text, and bullet points. Never give a giant wall of text.
- CRITICAL BEHAVIOR RULE: You must absolutely avoid generic or basic formatting. Do not output standard list structures like "1. Task, 2. Task". You must heavily lean into your persona as "The Friction Fighter", analyze energy levels first, and structure your response dynamically with clever conversational prose."""
                )
                
                # Construct the dynamic prompt integrating the slider value
                dynamic_prompt = f"User raw tasks/stress dump: '{user_tasks}'. Current user energy level: {energy_level}/10. Break down the friction and generate the custom battle plan."
                
                # Fire the request to Google AI Studio
                response = model.generate_content(dynamic_prompt)
                
                # Display the beautifully styled markdown result
                st.success("Your Actionable Plan is Ready:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred connecting to Google AI Studio: {e}")
