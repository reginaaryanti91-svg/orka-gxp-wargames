import os
from google import genai
from google.genai import types
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="GxP Compliance War Room", page_icon="🛡️", layout="centered"
)
st.title("🛡️ Inspector Vance — GxP War Game Console")
st.caption("Interactive AI Auditor testing 21 CFR Part 11 & CSA Compliance")

# 2. Retrieve Gemini API Key
api_key = None
if "gemini" in st.secrets and "GEMINI_API_KEY" in st.secrets["gemini"]:
  api_key = st.secrets["gemini"]["GEMINI_API_KEY"].strip()
elif "GEMINI_API_KEY" in os.environ:
  api_key = os.environ["GEMINI_API_KEY"].strip()

if not api_key:
  api_key = st.text_input("Enter your Gemini API Key:", type="password").strip()

if api_key:
  try:
    # Initialize client once
    client = genai.Client(api_key=api_key)

    system_instruction = """You are Inspector Alex Vance, a senior lead regulatory auditor 
        representing a joint task force of FDA, EMA, TGA, and HSA. You are conducting an audit 
        on 21 CFR Part 11, Computer Software Assurance (CSA), and AI model drift compliance.
        Keep responses sharp, concise, direct, and under 250 words to maintain fast engagement."""

    if "messages" not in st.session_state:
      st.session_state.messages = []

    # Render previous conversation history
    for msg in st.session_state.messages:
      with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

    # 3. Streamed User Input & Model Response
    if prompt := st.chat_input(
        "Present your strategy or remediation plan to the inspector..."
    ):
      # Display user message immediately
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      # Stream the assistant response chunk-by-chunk
      with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
          # Use generate_content_stream for instantaneous output
          # Use gemini-3.5-flash-lite for lowest latency
          stream = client.models.generate_content_stream(
              model="gemini-3.5-flash-lite",
              contents=prompt,
              config=types.GenerateContentConfig(
                  system_instruction=system_instruction,
                  temperature=0.3,
                  max_output_tokens=500,  # Limits lengthy outputs to reduce wait times
              ),
          )

          for chunk in stream:
            full_response += chunk.text
            response_placeholder.markdown(full_response + "▌")

          # Finalize output without cursor
          response_placeholder.markdown(full_response)
          st.session_state.messages.append(
              {"role": "assistant", "content": full_response}
          )
        except Exception as e:
          st.error(f"Audit Connection Error: {e}")
  except Exception as e:
    st.error(f"Initialization Error: {e}")
else:
  st.warning("Please enter your Gemini API Key to activate the war room.")
