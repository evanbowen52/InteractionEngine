"""
Help page: definitions (each term once), Rule of Three relationships, 64 Friction Matrix.
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
)
from ui_components import build_friction_matrix_figure

st.set_page_config(
    page_title="Help · Interaction Engine",
    page_icon="⚡",
    layout="wide",
)

st.title("Help")
st.caption("Periodic Table of Interaction · Definitions and Reference")

# ---------------------------------------------------------------------------
# 1. Definitions (each term defined once)
# ---------------------------------------------------------------------------
st.header("Definitions")

st.subheader("Primary Needs (The Gravity)")
st.table([["Need", "Definition"]] + [[n, NEED_DEFINITIONS[n]] for n in PRIMARY_NEEDS])

st.subheader("Worldviews (The Filter)")
st.table([["Worldview", "Definition"]] + [[w, WORLDVIEW_DEFINITIONS[w]] for w in WORLDVIEWS])

st.subheader("Gambits (The Throw)")
st.table([["Gambit", "Definition"]] + [[g, GAMBIT_DEFINITIONS[g]] for g in GAMBITS])

st.divider()

# ---------------------------------------------------------------------------
# 2. Rule of Three relationships (compact, no duplicate definitions)
# ---------------------------------------------------------------------------
st.header("Rule of Three")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Need → Likely Worldviews")
    st.table(
        [["Need", "Likely Worldviews"]]
        + [[n, ", ".join(NEED_TO_WORLDVIEWS[n])] for n in PRIMARY_NEEDS]
    )

with col2:
    st.subheader("Worldview → Likely Gambits")
    st.table(
        [["Worldview", "Likely Gambits"]]
        + [[w, ", ".join(WORLDVIEW_TO_GAMBITS[w])] for w in WORLDVIEWS]
    )

st.divider()

# ---------------------------------------------------------------------------
# 3. 64 Friction Matrix (no highlight on help page)
# ---------------------------------------------------------------------------
st.header("81 Friction Matrix")
st.caption("Rows = A's Gambit, Columns = B's Response. 0–2 Harmonic, 3–6 Dissonant, 7–10 Combustive.")

fig = build_friction_matrix_figure()
st.plotly_chart(fig, use_container_width=True)
