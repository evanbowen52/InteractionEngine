"""
Streamlit UI for the Interaction Engine.
Run with: streamlit run app.py
"""

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

st.title("Interaction Engine")
st.caption("Periodic Table of Interaction · 64 Friction Matrix · Rule of Three")

# ---------------------------------------------------------------------------
# Sidebar: Rule of Three reference + definitions
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Rule of Three")
    need = st.selectbox("Need → Worldviews", PRIMARY_NEEDS, key="ref_need")
    st.write("Likely worldviews:", ", ".join(NEED_TO_WORLDVIEWS[need]))
    st.caption(NEED_DEFINITIONS[need])
    st.divider()
    wv = st.selectbox("Worldview → Gambits", WORLDVIEWS, key="ref_wv")
    st.write("Likely gambits:", ", ".join(WORLDVIEW_TO_GAMBITS[wv]))
    st.caption(WORLDVIEW_DEFINITIONS[wv])
    st.divider()
    gambit_ref = st.selectbox("Gambit → Definition", list(GAMBIT_DEFINITIONS), key="ref_gambit")
    st.caption(GAMBIT_DEFINITIONS[gambit_ref])

# ---------------------------------------------------------------------------
# Two-column character panels
# ---------------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Person A (initiates)")
    need_a = st.selectbox("Primary Need", PRIMARY_NEEDS, key="need_a")
    wv_a = st.selectbox("Worldview", WORLDVIEWS, key="wv_a")
    gambit_a = st.selectbox("Gambit", GAMBITS, key="gambit_a")

with col_b:
    st.subheader("Person B (responds)")
    need_b = st.selectbox("Primary Need", PRIMARY_NEEDS, key="need_b")
    wv_b = st.selectbox("Worldview", WORLDVIEWS, key="wv_b")
    gambit_b = st.selectbox("Gambit", GAMBITS, key="gambit_b")

# ---------------------------------------------------------------------------
# Calculate and display result
# ---------------------------------------------------------------------------
person_a = PersonData(primary_need=need_a, worldview=wv_a, gambit=gambit_a)
person_b = PersonData(primary_need=need_b, worldview=wv_b, gambit=gambit_b)
score, flavor = calculate_interaction(person_a, person_b)
band = _friction_band(score)

st.divider()
st.metric("Friction Score", score, delta=None)
st.write(f"**Band:** {band}")
st.info(flavor)

# ---------------------------------------------------------------------------
# 64-cell Friction Matrix heatmap (Plotly)
# ---------------------------------------------------------------------------
st.subheader("81 Friction Matrix")
st.caption("Rows = A's Gambit, Columns = B's Response. Current pair highlighted.")

fig = build_friction_matrix_figure(highlight_gambit_a=gambit_a, highlight_gambit_b=gambit_b)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# How to run (footer)
# ---------------------------------------------------------------------------
st.sidebar.divider()
st.sidebar.caption("Run: `streamlit run app.py`")
