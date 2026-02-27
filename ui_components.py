"""Shared UI components: heatmap builder for app and help page."""

import plotly.graph_objects as go

from interaction_engine import GAMBITS, FRICTION_MATRIX


def build_friction_matrix_figure(
    highlight_gambit_a: str | None = None,
    highlight_gambit_b: str | None = None,
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
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=list(GAMBITS),
        y=list(GAMBITS),
        colorscale=colorscale,
        zmin=0,
        zmax=10,
        text=z,
        texttemplate="%{text}",
        textfont={"size": 11},
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
    fig.update_layout(
        xaxis_title="B's Response (Gambit)",
        yaxis_title="A's Gambit",
        height=500,
        margin=dict(l=80, r=40, t=20, b=80),
    )
    fig.update_xaxes(tickangle=-45)
    return fig
