import streamlit as st
from google import genai
from google.genai import types

# Page setup & branding
st.set_page_config(
    page_title="Inspector O.R.K.A. | GxP War Games",
    page_icon="⚖️",
    layout="wide",
)

# Sidebar with scenario briefs & instructions
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/orca.png", width=70)
    st.title("ORKA Life Science Partner")
    st.subheader("Session 3: GxP War Games")
    st.markdown("---")
    st.markdown("**War Games Scenarios:**")
    st.markdown("1. **Round 1:** CSA Risk Rationale & Silent Cloud Updates")
    st.markdown("2. **Round 2:** Non-Deterministic AI & Part 11 Audit Trail")
    st.markdown("3. **Round 3:** QC Raw Data Integrity & Peak Integration")
    st.markdown("---")
    if st.button("🔄 Reset Inspection Terminal", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = None
        st.rerun()

st.title("🚨 Inspector O.R.K.A. — Regulatory Terminal")
st.caption("Joint US FDA / EMA / TGA / HSA Enforcement Taskforce | 21 CFR Part 11 & CSA")

# Initialize Gemini Client using Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing `GEMINI_API_KEY` in Streamlit Secrets. Please configure it in settings.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are "Inspector O.R.K.A." (Operational Risk & Knowledge Auditor), a Lead Regulatory Examiner representing a harmonized enforcement taskforce from the US FDA, EMA, TGA, and Singapore HSA.
You are conducting an unannounced, high-stakes inspection of a biopharmaceutical consulting team during the GxP War Games.

YOUR RULES OF ENGAGEMENT:
1. Demeanor: Formal, skeptical, unyielding, authoritative. Never cheerlead, flatter, or give answers away.
2. Focus Areas: 21 CFR Part 11, FDA Computer Software Assurance (CSA), EU Annex 11, ALCOA+, and non-deterministic AI auditability.
3. Challenge Tactics:
   - Demand concrete SOP clauses, regulatory citations, and technical data architecture proof.
   - Attack buzzwords ('robust prompt', 'agile validation', 'ethical AI'). Demand to know how audit trails under 11.10(e) capture metadata and how 11.200 e-signatures are attributed.
   - Attack CSA categorizations: challenge teams when they attempt to classify patient safety or batch-release software as low-risk just to avoid scripted testing.

TURN EXECUTION FORMAT (Always use this exact structure):
1. **Auditor Reaction:** 1-2 sentence razor-sharp assessment of their argument.
2. **The Interrogation:** 1-2 technical challenge questions demanding specific proof or regulatory references.
3. **Audit Status Meter:**
   - Current Status: [Compliant / Conditional / Major Finding Imminent / Critical Form 483 Issued]
   - Compliance Risk: [Low / Moderate / Severe / Critical]
   - Observation Note: (One sentence identifying their biggest unaddressed vulnerability).

If the team says 'Inspector, conclude our session and provide our final score', provide a formal audit exit summary and a numerical Compliance Score from 0 to 100 based on their performance.
"""

# Maintain persistent multi-turn chat
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "**INSPECTION NOTICE:** I am **Inspector O.R.K.A.** representing the joint FDA/EMA/TGA/HSA audit taskforce.\n\n"
                "The regulatory examination has officially commenced. State your team name, the scenario you are addressing, "
                "and your technical compliance justification. Do not offer boilerplate generalities."
            ),
        }
    ]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt handling
if user_input := st.chat_input("Submit your compliance justification to Inspector O.R.K.A..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Format conversation history for Gemini API
    formatted_contents = []
    for m in st.session_state.messages:
        role = "model" if m["role"] == "assistant" else "user"
        formatted_contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

    with st.chat_message("assistant"):
        with st.spinner("Inspector O.R.K.A. is reviewing regulatory records..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2,
                    ),
                )
                inspector_response = response.text
                st.markdown(inspector_response)
                st.session_state.messages.append({"role": "assistant", "content": inspector_response})
            except Exception as e:
                st.error(f"Audit Connection Error: {str(e)}")
