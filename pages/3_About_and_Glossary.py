"""
Help page: definitions (each term once), Rule of Three relationships, Friction Matrix.
"""

from pathlib import Path
import streamlit as st

from interaction_engine import (
    GAMBITS,
    PRIMARY_NEEDS,
    WORLDVIEWS,
    NEED_DEFINITIONS,
    WORLDVIEW_DEFINITIONS,
    GAMBIT_DEFINITIONS,
    GAMBIT_METADATA
)

st.set_page_config(
    page_title="About & Glossary · Interaction Engine",
    page_icon="⚡",
    layout="wide",
)

# Inject custom CSS
_css_dir = Path(__file__).resolve().parent
_css_path = _css_dir / ".streamlit" / "style.css"
if not _css_path.exists():
    _css_path = _css_dir.parent / ".streamlit" / "style.css"
if _css_path.exists():
    st.markdown(f"<style>{_css_path.read_text()}</style>", unsafe_allow_html=True)

st.title("About & Glossary")
st.caption("The theoretical foundation and definitions for the Interaction Engine.")

st.markdown("""
### The Periodic Table of Interaction
This system predicts the narrative outcome of an interaction based on underlying psychological states. 
Every interaction is governed by a **Rule of Three**:

1. **Primary Need (The Gravity):** The fundamental psychological driver. A character's core Need limits how they can perceive the situation.
2. **Worldview (The Filter):** The lens through which they view the world, heavily shaped by their Need.
3. **Gambit (The Throw):** The specific tactical move they execute based on their Worldview.

When Person A throws a Gambit and Person B responds with their own Gambit, the resulting combination dictates the **Friction Score (0-10)** and the narrative outcome.
""")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Needs", "Worldviews", "Gambits", "Friction Scale"])

with tab1:
    for need, desc in NEED_DEFINITIONS.items():
        st.markdown(f"**{need}**: {desc}")
        
with tab2:
    for wv, desc in WORLDVIEW_DEFINITIONS.items():
        st.markdown(f"**{wv}**: {desc}")
        
with tab3:
    for gambit, desc in GAMBIT_DEFINITIONS.items():
        st.markdown(f"**{gambit}**: {desc}")
        meta = GAMBIT_METADATA.get(gambit)
        if meta:
            st.caption(f"*Status Delta: {meta['status_delta']} | Impact: {meta['structural_impact']}*")
            if meta.get("sub_tactics"):
                tactic_names = ", ".join(t["token"] for t in meta["sub_tactics"])
                st.caption(f"*Tactics include: {tactic_names}*")
        st.write("") # spacing
        
with tab4:
    st.markdown("""
    - **0–2 (Harmonic):** Needs are met; connection flows.
    - **3–6 (Dissonant):** "Category Error." Misunderstandings, clinical coldness, or mild frustration.
    - **7–10 (Combustive):** Conflict. Ego-clashes, abandonment, or betrayal of vulnerability.
    """)