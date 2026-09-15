"""
Tree page: Predictive Logic tree (Need → Worldview → Gambit).
All 9 gambits per worldview; darker = more likely. Click for descriptions & friction.
"""

import json
from pathlib import Path

import streamlit as st
from streamlit_plotly_events import plotly_events

from interaction_engine import (
    GAMBITS,
    FRICTION_MATRIX,
    NEED_DEFINITIONS,
    WORLDVIEW_DEFINITIONS,
)
from ui_components import build_predictive_tree_figure

st.set_page_config(
    page_title="Tree · Interaction Engine",
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

st.title("Tree")
st.caption("Predictive Logic · Need → Worldview → Gambit · 67 behavioral paths")

# ---------------------------------------------------------------------------
# Load tree data
# ---------------------------------------------------------------------------
_data_dir = Path(__file__).resolve().parent.parent / "data"
_tree_path = _data_dir / "tree.json"

if not _tree_path.exists():
    st.error(f"Tree data not found: {_tree_path}")
    st.stop()

with open(_tree_path, encoding="utf-8") as f:
    tree_data = json.load(f)

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
st.subheader("Gambit types")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("**Structuralist** — cold/logic (Blues)")
with col2:
    st.markdown("**Relationalist** — warm/connection (Greens)")
with col3:
    st.markdown("**Assertive** — hot/high-friction (Reds)")
st.caption("Darker = more likely for that worldview. Click any segment.")

st.divider()

# ---------------------------------------------------------------------------
# Plotly Sunburst (clickable via streamlit-plotly-events)
# ---------------------------------------------------------------------------
fig, customdata = build_predictive_tree_figure(tree_data, "sunburst")
selected_points = plotly_events(
    fig,
    click_event=True,
    select_event=False,
    override_height=600,
    key="tree_click",
)

# ---------------------------------------------------------------------------
# Selected Need / Worldview description + Gambit friction row
# ---------------------------------------------------------------------------
need, worldview, gambit = None, None, None
if selected_points and len(selected_points) > 0:
    pt = selected_points[0]
    idx = pt.get("pointIndex", pt.get("pointNumber", -1))
    if 0 <= idx < len(customdata):
        cd = customdata[idx]
        if isinstance(cd, (list, tuple)) and len(cd) >= 3:
            need, worldview, gambit = cd[0], cd[1], cd[2]

if need or worldview or gambit:
    st.divider()
    st.subheader("Selection")

    # Need + Worldview descriptions
    if need:
        st.markdown(f"**{need}** (Need)")
        st.caption(NEED_DEFINITIONS.get(need, ""))
    if worldview:
        st.markdown(f"**{worldview}** (Worldview)")
        st.caption(WORLDVIEW_DEFINITIONS.get(worldview, ""))

    # Gambit: friction row (A's gambit → B's responses)
    if gambit and gambit in FRICTION_MATRIX:
        st.markdown(f"**{gambit}** (Gambit) — Friction when B responds with each gambit:")
        row = FRICTION_MATRIX[gambit]
        cols = st.columns(len(GAMBITS))
        for i, gb in enumerate(GAMBITS):
            with cols[i]:
                score = row.get(gb, "—")
                st.metric(gb, score)
else:
    st.caption("Click a segment above to see Need/Worldview descriptions, or click a Gambit for friction values.")

st.divider()

# ---------------------------------------------------------------------------
# Expandable tree (fallback / detail view)
# ---------------------------------------------------------------------------
def render_node(node: dict, depth: int = 0) -> None:
    """Render a tree node: expander for branches, bullet for leaves."""
    name = node.get("name", "?")
    node_type = node.get("type")
    children = node.get("children", [])

    if not children:
        type_label = f" ({node_type})" if node_type else ""
        st.markdown(f"- **{name}**{type_label}")
        return

    with st.expander(name, expanded=(depth < 2)):
        for child in children:
            render_node(child, depth + 1)


with st.expander("Expandable tree view", expanded=False):
    st.caption("Path context for duplicate Gambits (e.g. Shield).")
    for child in tree_data.get("children", []):
        render_node(child)

# ---------------------------------------------------------------------------
# Raw JSON (collapsed)
# ---------------------------------------------------------------------------
with st.expander("Raw JSON", expanded=False):
    st.json(tree_data)
