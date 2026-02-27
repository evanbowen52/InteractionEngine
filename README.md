# Interaction Engine

A **Person-N interaction simulator** based on the "Periodic Table of Interaction" and the 64-cell Friction Matrix. Characters are defined by **Primary Need**, **Worldview**, and **Gambit**; dialogue tension is computed when A's gambit meets B's response.

## Quick start

**CLI (sample scene):**
```bash
python interaction_engine.py
```

**Web UI (sliders + 64-matrix heatmap):**

If you created a venv (e.g. `.venv`) when prompted, use it so dependencies stay in one place:

```bash
# From project root: d:\_EVAN\Dev\InteractionEngine

# 1. Activate the venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 2. Install deps into the venv
pip install -r requirements.txt

# 3. Run the UI
streamlit run app.py
```

Then open the URL in your browser (e.g. http://localhost:8501).

If you don't use a venv, run `pip install -r requirements.txt` and `streamlit run app.py` from any terminal (that uses your system Python).

## Usage

```python
from interaction_engine import PersonData, calculate_interaction

alice = PersonData(primary_need="Belonging", worldview="Unity", gambit="Gift")
bob   = PersonData(primary_need="Significance", worldview="Identity", gambit="Gavel")

score, flavor = calculate_interaction(alice, bob)
# score == 10, flavor == "Friction 10: Betrayal of Vulnerability"
```

## Files

- **SYSTEM_DEFINITION.md** — Full spec: Needs, Worldviews, Gambits, Friction Matrix, Rule of Three.
- **interaction_engine.py** — Matrix, `calculate_interaction()`, narrative flavors, Rule of Three maps, sample scene.
- **app.py** — Streamlit UI: two character panels (Need / Worldview / Gambit), friction result, and interactive 64-cell heatmap.

## Sculpting characters

Adjust **Need** sliders; the engine uses **Rule of Three** logic so that Need constrains likely Worldviews and Worldview constrains likely Gambits. You can still set any valid `(primary_need, worldview, gambit)` for full control.

## UI stack

The included UI is **Streamlit + Plotly** (Python-only, no Node/D3). Run with `streamlit run app.py` for:

- Two character panels (Need, Worldview, Gambit dropdowns)
- Live friction score and narrative flavor
- Interactive 64-cell heatmap (A’s gambit vs B’s response) with the current pair highlighted

For a custom, D3-style front end (e.g. force-directed graph of gambits, or a bespoke matrix), you’d add a separate web app (e.g. React + D3 or vanilla JS) and either call a small Python API or load a JSON export of the matrix.

---

## Python and the venv (two sets of Python)

You do have two Pythons in play when you use a venv:

| What | Where | When it is used |
|------|--------|------------------|
| **System Python** | `C:\Python313\` (3.13.2) | Default `python` / `pip` when the venv is **not** activated; other projects. |
| **Project venv** | `d:\_EVAN\Dev\InteractionEngine\.venv\` | After you run `.\.venv\Scripts\Activate.ps1` in this project; `python` and `pip` then point into `.venv`. |

The venv was created from your system Python but is isolated (`include-system-site-packages = false`), so packages you install with `pip` after activating the venv go only into `.venv\Lib\site-packages`. That keeps this project's dependencies (e.g. streamlit, plotly) separate from the rest of your system.

**To avoid confusion:** Activate the venv first (`.\.venv\Scripts\Activate.ps1`), then run `pip install -r requirements.txt` and `streamlit run app.py`. In Cursor, use **Python: Select Interpreter** and choose `.venv\Scripts\python.exe` so the IDE uses the same environment.
