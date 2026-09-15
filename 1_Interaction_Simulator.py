"""
Streamlit UI for the Interaction Engine.
Run with: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

from interaction_engine import (
    GAMBITS,
    PRIMARY_NEEDS,
    WORLDVIEWS,
    NEED_TO_WORLDVIEWS,
    WORLDVIEW_TO_GAMBITS,
    NEED_DEFINITIONS,
    WORLDVIEW_DEFINITIONS,
    GAMBIT_DEFINITIONS,
    GAMBIT_METADATA,
    PersonData,
    calculate_interaction,
    _friction_band,
)
from ui_components import build_friction_matrix_figure

st.set_page_config(
    page_title="Interaction Engine",
    page_icon="⚡",
    layout="wide",
)

# Inject custom CSS (Streamlit does not auto-load .streamlit/style.css)
_css_dir = Path(__file__).resolve().parent
_css_path = _css_dir / ".streamlit" / "style.css"
if not _css_path.exists():
    _css_path = _css_dir.parent / ".streamlit" / "style.css"
if _css_path.exists():
    st.markdown(f"<style>{_css_path.read_text()}</style>", unsafe_allow_html=True)

st.title("Interaction Engine")
st.caption("Select an initiating gambit and a response below to see the friction score of the interaction.")

# ---------------------------------------------------------------------------
# Dialog: About & Glossary
# ---------------------------------------------------------------------------
@st.dialog("About & Glossary", width="large")
def about_glossary_dialog():
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
            if meta and meta.get("sub_tactics"):
                tactic_names = ", ".join(t["token"] for t in meta["sub_tactics"])
                st.caption(f"*Includes: {tactic_names}*")
            
    with tab4:
        st.markdown("""
        - **0–2 (Harmonic):** Needs are met; connection flows.
        - **3–6 (Dissonant):** "Category Error." Misunderstandings, clinical coldness, or mild frustration.
        - **7–10 (Combustive):** Conflict. Ego-clashes, abandonment, or betrayal of vulnerability.
        """)

# ---------------------------------------------------------------------------
# Sidebar: Compact mode + footer
# ---------------------------------------------------------------------------
with st.sidebar:
    if st.button("📖 About & Glossary", use_container_width=True):
        about_glossary_dialog()
    st.divider()
    st.checkbox("Compact mode", value=False, key="compact_mode")
    st.divider()
    st.caption("Run: `streamlit run 1_Interaction_Simulator.py`")

# ---------------------------------------------------------------------------
# Two-column character panels
# ---------------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Person A (initiates)")
    need_a = st.selectbox(
        "Primary Need", PRIMARY_NEEDS, key="need_a",
        format_func=lambda x: f"{x} — {NEED_DEFINITIONS[x]}"
    )
    
    wv_a = st.selectbox(
        "Worldview", WORLDVIEWS, key="wv_a",
        format_func=lambda x: f"{x} — {WORLDVIEW_DEFINITIONS[x]}"
    )
    
    gambit_a = st.selectbox(
        "Gambit", GAMBITS, key="gambit_a",
        format_func=lambda x: f"{x} — {GAMBIT_DEFINITIONS[x]}"
    )

with col_b:
    st.subheader("Person B (responds)")
    need_b = st.selectbox(
        "Primary Need", PRIMARY_NEEDS, key="need_b",
        format_func=lambda x: f"{x} — {NEED_DEFINITIONS[x]}"
    )
    
    wv_b = st.selectbox(
        "Worldview", WORLDVIEWS, key="wv_b",
        format_func=lambda x: f"{x} — {WORLDVIEW_DEFINITIONS[x]}"
    )
    
    gambit_b = st.selectbox(
        "Gambit", GAMBITS, key="gambit_b",
        format_func=lambda x: f"{x} — {GAMBIT_DEFINITIONS[x]}"
    )

# ---------------------------------------------------------------------------
# Calculate and display result
# ---------------------------------------------------------------------------
person_a = PersonData(primary_need=need_a, worldview=wv_a, gambit=gambit_a)
person_b = PersonData(primary_need=need_b, worldview=wv_b, gambit=gambit_b)
score, flavor = calculate_interaction(person_a, person_b)
band = _friction_band(score)

st.divider()
st.metric(
    "Friction Score", score, delta=None,
    help="Scale 0-10: 0-2 = Harmonic, 3-6 = Dissonant, 7-10 = Combustive"
)
st.write(f"**Band:** {band}")
st.info(flavor)

st.divider()

col_meta_a, col_meta_b = st.columns(2)

with col_meta_a:
    meta = GAMBIT_METADATA.get(gambit_a)
    if meta:
        st.markdown(f"**A's Gambit ({gambit_a}) Metadata**")
        st.write(f"**Status Delta:** {meta['status_delta']}")
        st.write(f"**Structural Impact:** {meta['structural_impact']}")
        if meta['sub_tactics']:
            st.write("**Sub-Tactics:**")
            for t in meta['sub_tactics']:
                st.caption(f"- **{t['token']}**: {t['definition']}")

with col_meta_b:
    meta = GAMBIT_METADATA.get(gambit_b)
    if meta:
        st.markdown(f"**B's Gambit ({gambit_b}) Metadata**")
        st.write(f"**Status Delta:** {meta['status_delta']}")
        st.write(f"**Structural Impact:** {meta['structural_impact']}")
        if meta['sub_tactics']:
            st.write("**Sub-Tactics:**")
            for t in meta['sub_tactics']:
                st.caption(f"- **{t['token']}**: {t['definition']}")

# ---------------------------------------------------------------------------
# 81-cell Friction Matrix heatmap (Plotly)
# ---------------------------------------------------------------------------
st.subheader("81 Friction Matrix")
st.caption("Rows = A's Gambit, Columns = B's Response. Current pair highlighted.")

compact = st.session_state.get("compact_mode", False)
fig = build_friction_matrix_figure(
    highlight_gambit_a=gambit_a,
    highlight_gambit_b=gambit_b,
    compact=compact,
)
st.plotly_chart(fig, use_container_width=True)
