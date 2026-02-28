"""Shared UI components: heatmap builder for app and help page."""

import plotly.graph_objects as go

from interaction_engine import GAMBITS, FRICTION_MATRIX

# Gambit type colors for tree viz: Structuralist, Relationalist, Assertive
TYPE_COLORS = {
    "Structuralist": "rgb(70, 130, 180)",   # steel blue
    "Relationalist": "rgb(60, 179, 113)",   # medium sea green
    "Assertive": "rgb(178, 34, 34)",         # firebrick
}
DEFAULT_COLOR = "rgb(220, 220, 220)"  # light gray for internal nodes


def build_friction_matrix_figure(
    highlight_gambit_a: str | None = None,
    highlight_gambit_b: str | None = None,
    compact: bool = False,
) -> go.Figure:
    """Build the 81-cell friction matrix heatmap. Optionally highlight one cell."""
    z = [[FRICTION_MATRIX[ga][gb] for gb in GAMBITS] for ga in GAMBITS]
    colorscale = [
        [0.0, "rgb(40, 120, 60)"],
        [0.25, "rgb(120, 160, 80)"],
        [0.5, "rgb(200, 180, 80)"],
        [0.75, "rgb(200, 100, 60)"],
        [1.0, "rgb(160, 50, 50)"],
    ]
    text_size = 8 if compact else 11
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=list(GAMBITS),
        y=list(GAMBITS),
        colorscale=colorscale,
        zmin=0,
        zmax=10,
        text=z,
        texttemplate="%{text}",
        textfont={"size": text_size},
        hoverongaps=False,
    ))
    if highlight_gambit_a and highlight_gambit_b:
        idx_a = list(GAMBITS).index(highlight_gambit_a)
        idx_b = list(GAMBITS).index(highlight_gambit_b)
        fig.add_shape(
            type="rect",
            x0=idx_b - 0.5, x1=idx_b + 0.5,
            y0=idx_a - 0.5, y1=idx_a + 0.5,
            line=dict(color="white", width=3),
            fillcolor="rgba(0,0,0,0)",
        )
    height = 320 if compact else 500
    margin = dict(l=60, r=30, t=15, b=60) if compact else dict(l=80, r=40, t=20, b=80)
    fig.update_layout(
        xaxis_title="B's Response (Gambit)",
        yaxis_title="A's Gambit",
        height=height,
        margin=margin,
    )
    tickangle = -90 if compact else -45
    fig.update_xaxes(tickangle=tickangle)
    return fig


def _flatten_tree(node: dict, parent_id: str, ids: list, labels: list, parents: list, colors: list) -> None:
    """Recursively flatten tree into Plotly Sunburst/Icicle format."""
    name = node.get("name", "?")
    node_id = f"{parent_id}-{name}" if parent_id else name
    node_type = node.get("type")
    children = node.get("children", [])

    ids.append(node_id)
    labels.append(name)
    parents.append(parent_id)
    colors.append(TYPE_COLORS.get(node_type, DEFAULT_COLOR) if node_type else DEFAULT_COLOR)

    for child in children:
        _flatten_tree(child, node_id, ids, labels, parents, colors)


def build_predictive_tree_figure(tree_data: dict, chart_type: str = "sunburst") -> go.Figure:
    """Build Plotly Sunburst or Icicle from predictive logic tree JSON."""
    ids, labels, parents, colors = [], [], [], []
    root_id = tree_data.get("name", "Root")
    _flatten_tree(tree_data, "", ids, labels, parents, colors)

    if chart_type == "icicle":
        trace = go.Icicle(
            ids=ids,
            labels=labels,
            parents=parents,
            marker=dict(colors=colors),
        )
    else:
        trace = go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            marker=dict(colors=colors),
        )

    fig = go.Figure(trace)
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        height=600,
    )
    return fig
