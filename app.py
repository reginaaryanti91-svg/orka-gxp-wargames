import os
from google import genai
from google.genai import types
import streamlit as st

# Page setup
st.set_page_config(
    page_title="GxP Compliance War Room", page_icon="🛡️", layout="centered"
)
st.title("🛡️ Inspector Vance — GxP War Game Console")
st.caption(
    "Interactive Regulatory Auditor testing 21 CFR Part 11 & CSA Compliance"
)

# Secret API key retrieval
api_key = None
if "gemini" in st.secrets and "GEMINI_API_KEY" in st.secrets["gemini"]:
  api_key = st.secrets["gemini"]["GEMINI_API_KEY"].strip()
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"].strip()

if not api_key:
  api_key = st.text_input("Enter your Gemini API Key:", type="password").strip()

if api_key:
  try:
    # Initialize Google GenAI client
    client = genai.Client(api_key=api_key)

    system_instruction = """You are Inspector Alex Vance, a senior lead regulatory auditor 
        representing a joint task force of FDA, EMA, TGA, and HSA. You are conducting an audit 
        on 21 CFR Part 11, Computer Software Assurance (CSA), and AI model drift compliance."""

    if "messages" not in st.session_state:
      st.session_state.messages = []

    # Render history
    for msg in st.session_state.messages:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input(
        "Present your strategy or remediation plan to the inspector..."
    ):
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      with st.chat_message("assistant"):
        with st.spinner("Inspector Vance is reviewing your submission..."):
          # Updated to use gemini-3.8-flash
          response = client.models.generate_content(
              model="gemini-3.8-flash",
              contents=prompt,
              config=types.GenerateContentConfig(
                  system_instruction=system_instruction,
                  temperature=0.3,
              ),
          )
          reply = response.text
          st.markdown(reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": reply}
          )
  except Exception as e:
    st.error(f"Audit Connection Error: {e}")
else:
  st.warning("Please provide a valid Gemini API key to run the audit console.")
