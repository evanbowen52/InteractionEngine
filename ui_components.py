"""Shared UI components: heatmap builder for app and help page."""

import copy

import plotly.graph_objects as go

from interaction_engine import GAMBITS, FRICTION_MATRIX, GAMBIT_TYPES, WORLDVIEW_TO_GAMBITS

# Gambit type colors for tree viz: Structuralist, Relationalist, Assertive
TYPE_COLORS = {
    "Structuralist": "rgb(70, 130, 180)",   # steel blue
    "Relationalist": "rgb(60, 179, 113)",   # medium sea green
    "Assertive": "rgb(178, 34, 34)",         # firebrick
}
DEFAULT_COLOR = "rgb(220, 220, 220)"  # light gray for internal nodes
DIM_ALPHA = 0.35  # opacity for less-likely gambits


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


def _rgb_to_rgba(rgb: str, alpha: float) -> str:
    """Convert 'rgb(r,g,b)' to 'rgba(r,g,b,alpha)'."""
    if rgb.startswith("rgb("):
        inner = rgb[4:-1]  # "70, 130, 180"
        return f"rgba({inner}, {alpha})"
    return rgb


def expand_tree_for_viz(tree_data: dict) -> dict:
    """Expand each worldview to show all 9 gambits; likely ones stay full color, others dimmed."""
    tree = copy.deepcopy(tree_data)

    def expand_node(node: dict) -> None:
        children = node.get("children", [])
        if not children:
            return
        # Check if children are worldviews (have gambit children)
        first_child = children[0]
        if "children" in first_child and first_child["children"]:
            grandchild = first_child["children"][0]
            if "type" in grandchild:
                # This level is Need -> Worldview; expand each Worldview
                for wv_node in children:
                    wv_name = wv_node["name"]
                    likely = set(WORLDVIEW_TO_GAMBITS.get(wv_name, ()))
                    expanded = []
                    for g in GAMBITS:
                        g_type = GAMBIT_TYPES.get(g, "Structuralist")
                        expanded.append({
                            "name": g,
                            "type": g_type,
                            "likely": g in likely,
                        })
                    wv_node["children"] = expanded
                return
        for child in children:
            expand_node(child)

    expand_node(tree)
    return tree


def _flatten_tree(
    node: dict,
    parent_id: str,
    path: list[str],
    ids: list,
    labels: list,
    parents: list,
    colors: list,
    customdata: list,
) -> None:
    """Recursively flatten tree into Plotly Sunburst/Icicle format."""
    name = node.get("name", "?")
    node_id = f"{parent_id}-{name}" if parent_id else name
    node_type = node.get("type")
    children = node.get("children", [])
    is_likely = node.get("likely", True)  # default True for non-gambit nodes

    # Path: [root, need, worldview, gambit] - extract for customdata
    need = path[1] if len(path) >= 2 else None
    worldview = path[2] if len(path) >= 3 else None
    gambit = path[3] if len(path) >= 4 else None

    # Color: full for likely/internal, dimmed for less-likely gambits
    base_color = TYPE_COLORS.get(node_type, DEFAULT_COLOR) if node_type else DEFAULT_COLOR
    if not is_likely and node_type:
        color = _rgb_to_rgba(base_color, DIM_ALPHA)
    else:
        color = base_color

    ids.append(node_id)
    labels.append(name)
    parents.append(parent_id)
    colors.append(color)
    customdata.append([need, worldview, gambit])

    for child in children:
        _flatten_tree(child, node_id, path + [child.get("name", "?")], ids, labels, parents, colors, customdata)


def build_predictive_tree_figure(
    tree_data: dict, chart_type: str = "sunburst", expand_all_gambits: bool = True
) -> tuple[go.Figure, list]:
    """Build Plotly Sunburst or Icicle from predictive logic tree JSON.
    Returns (figure, customdata) for click handling.
    When expand_all_gambits=True, each worldview shows all 9 gambits (likely ones full color, others dimmed).
    """
    tree = expand_tree_for_viz(tree_data) if expand_all_gambits else tree_data
    ids, labels, parents, colors, customdata = [], [], [], [], []
    root_name = tree.get("name", "Root")
    _flatten_tree(tree, "", [root_name], ids, labels, parents, colors, customdata)

    if chart_type == "icicle":
        trace = go.Icicle(
            ids=ids,
            labels=labels,
            parents=parents,
            marker=dict(colors=colors),
            customdata=customdata,
        )
    else:
        trace = go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            marker=dict(colors=colors),
            customdata=customdata,
        )

    fig = go.Figure(trace)
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        height=600,
    )
    return fig, customdata
