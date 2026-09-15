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
# Sidebar: footer
# ---------------------------------------------------------------------------
with st.sidebar:
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

compact = st.checkbox("Compact view", value=False)
fig = build_friction_matrix_figure(
    highlight_gambit_a=gambit_a,
    highlight_gambit_b=gambit_b,
    compact=compact,
)
st.plotly_chart(fig, use_container_width=True)
