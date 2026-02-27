"""
Person-N Interaction Simulator
Based on the 'Periodic Table of Interaction' and 64-cell Friction Matrix.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 1. THE 81 FRICTION MATRIX (A's Gambit → B's Response → Score)
# ---------------------------------------------------------------------------

GAMBITS = (
    "Tether", "Shield", "Gavel", "Tool", "Blueprint", "Gift", "Mirror", "Probe", "Challenge"
)

FRICTION_MATRIX: dict[str, dict[str, int]] = {
    "Tether":    {"Tether": 2, "Shield": 8, "Gavel": 9, "Tool": 6, "Blueprint": 5, "Gift": 2, "Mirror": 0, "Probe": 4, "Challenge": 9},
    "Shield":    {"Tether": 7, "Shield": 5, "Gavel": 8, "Tool": 4, "Blueprint": 4, "Gift": 8, "Mirror": 6, "Probe": 7, "Challenge": 8},
    "Gavel":     {"Tether": 6, "Shield": 9, "Gavel": 10, "Tool": 7, "Blueprint": 4, "Gift": 8, "Mirror": 2, "Probe": 5, "Challenge": 10},
    "Tool":      {"Tether": 5, "Shield": 4, "Gavel": 7, "Tool": 0, "Blueprint": 1, "Gift": 3, "Mirror": 2, "Probe": 2, "Challenge": 4},
    "Blueprint": {"Tether": 4, "Shield": 5, "Gavel": 6, "Tool": 1, "Blueprint": 0, "Gift": 4, "Mirror": 2, "Probe": 3, "Challenge": 5},
    "Gift":      {"Tether": 3, "Shield": 9, "Gavel": 10, "Tool": 6, "Blueprint": 5, "Gift": 0, "Mirror": 0, "Probe": 4, "Challenge": 10},
    "Mirror":    {"Tether": 0, "Shield": 7, "Gavel": 8, "Tool": 5, "Blueprint": 4, "Gift": 0, "Mirror": 0, "Probe": 3, "Challenge": 5},
    "Probe":     {"Tether": 5, "Shield": 8, "Gavel": 7, "Tool": 2, "Blueprint": 3, "Gift": 4, "Mirror": 2, "Probe": 1, "Challenge": 7},
    "Challenge": {"Tether": 7, "Shield": 9, "Gavel": 10, "Tool": 4, "Blueprint": 5, "Gift": 10, "Mirror": 5, "Probe": 7, "Challenge": 10},
}

# ---------------------------------------------------------------------------
# 2. RULE OF THREE: Need → Worldviews → Gambits
# ---------------------------------------------------------------------------

PRIMARY_NEEDS = (
    "Safety", "Autonomy", "Competence", "Significance",
    "Order", "Belonging", "Meaning"
)

WORLDVIEWS = (
    "Survival", "Deficiency", "Identity", "Operational",
    "Unity", "Ludenic", "Sacred"
)

# Need → most likely Worldviews (ordered by likelihood)
NEED_TO_WORLDVIEWS: dict[str, tuple[str, ...]] = {
    "Safety":     ("Survival", "Deficiency", "Operational"),
    "Autonomy":   ("Identity", "Operational", "Ludenic"),
    "Competence": ("Operational", "Identity", "Unity"),
    "Significance": ("Identity", "Deficiency", "Sacred"),
    "Order":      ("Operational", "Survival", "Unity"),
    "Belonging":  ("Unity", "Deficiency", "Ludenic"),
    "Meaning":    ("Sacred", "Unity", "Identity"),
}

# Worldview → most likely Gambits
WORLDVIEW_TO_GAMBITS: dict[str, tuple[str, ...]] = {
    "Survival":   ("Tether", "Shield", "Probe"),
    "Deficiency": ("Tether", "Gift", "Shield"),
    "Identity":   ("Gavel", "Challenge", "Probe", "Shield"),
    "Operational": ("Tool", "Blueprint", "Probe"),
    "Unity":      ("Mirror", "Gift", "Tether"),
    "Ludenic":    ("Gift", "Probe", "Mirror"),
    "Sacred":     ("Gift", "Mirror", "Tether"),
}

# Definitions (from SYSTEM_DEFINITION.md) for UI reference
NEED_DEFINITIONS: dict[str, str] = {
    "Safety": "Physical security or psychological \"face\" saving.",
    "Autonomy": "The need for choice; avoiding being \"done to.\"",
    "Competence": "The need to feel capable/effective.",
    "Significance": "To be seen, to have status, to matter.",
    "Order": "To reduce entropy; predictability.",
    "Belonging": "Acceptance without performance.",
    "Meaning": "Purpose, justice, or \"righting the scales.\"",
}
WORLDVIEW_DEFINITIONS: dict[str, str] = {
    "Survival": "The world is a threat (High Cortisol).",
    "Deficiency": "The world is a desert (Not enough love/time/resource).",
    "Identity": "The world is a ladder/courtroom (Status/Who is right?).",
    "Operational": "The world is a machine (Tools/Logistics).",
    "Unity": "The world is a shared garden (Collaboration/Flow).",
    "Ludenic": "The world is a playground (Play/Low-stakes).",
    "Sacred": "The world is a temple (Awe/Grief/Birth).",
}
GAMBIT_DEFINITIONS: dict[str, str] = {
    "Tether": "A reach for grounding/reassurance.",
    "Shield": "Deflecting or setting a boundary.",
    "Gavel": "Passing judgment or declaring \"Truth.\"",
    "Tool": "Providing data or proposing structure.",
    "Blueprint": "Providing data or proposing structure (systematic).",
    "Gift": "Vulnerability, wit, or insight.",
    "Mirror": "Reflecting the other's state/validation.",
    "Probe": "Questioning to test a model.",
    "Challenge": "A direct hit to status or autonomy.",
}

# ---------------------------------------------------------------------------
# 3. NARRATIVE FLAVORS (signature pairings + band descriptions)
# ---------------------------------------------------------------------------

def _friction_band(score: int) -> str:
    if score <= 2:
        return "Harmonic"
    if score <= 6:
        return "Dissonant"
    return "Combustive"

# Signature (Gambit A, Response B) → narrative flavor
NARRATIVE_FLAVORS: dict[tuple[str, str], str] = {
    ("Gift", "Gavel"):   "Betrayal of Vulnerability",
    ("Gift", "Shield"):  "Vulnerability Deflected",
    ("Gift", "Challenge"): "Vulnerability Dismissed; Status Hit",
    ("Tether", "Gavel"): "Reassurance Met with Judgment",
    ("Tether", "Shield"): "Reach Rejected",
    ("Tether", "Challenge"): "Reach Rejected; Autonomy Hit",
    ("Shield", "Gavel"): "Boundary Overruled",
    ("Shield", "Challenge"): "Boundary Challenged",
    ("Gavel", "Gavel"):  "Ego Clash; Truth vs Truth",
    ("Gavel", "Shield"): "Judgment Blocked",
    ("Gavel", "Challenge"): "Truth vs Position; Full Clash",
    ("Challenge", "Gift"): "Status Hit on Vulnerability",
    ("Challenge", "Challenge"): "Power Clash",
    ("Mirror", "Gavel"): "Validation Dismissed",
    ("Mirror", "Shield"): "Reflection Deflected",
    ("Mirror", "Challenge"): "Validation Feels Patronizing",
    ("Tool", "Tool"):    "Alignment; Data Meets Data",
    ("Blueprint", "Blueprint"): "Structure in Sync",
    ("Tether", "Tether"): "Mutual Grounding",
    ("Gift", "Gift"):    "Vulnerability Reciprocated",
    ("Gift", "Mirror"):  "Vulnerability Seen",
    ("Mirror", "Mirror"): "Mutual Recognition",
    ("Probe", "Probe"):  "Curiosity Aligned",
}

def _default_flavor(gambit_a: str, gambit_b: str, score: int) -> str:
    band = _friction_band(score)
    if score <= 2:
        return f"Connection flows; needs met ({band})"
    if score <= 6:
        return f"Category error; misunderstanding or mild frustration ({band})"
    return f"Conflict; ego-clash or breach of trust ({band})"


# ---------------------------------------------------------------------------
# 4. PERSON DATA & CALCULATE INTERACTION
# ---------------------------------------------------------------------------

@dataclass
class PersonData:
    """One person's interaction profile."""
    primary_need: str
    worldview: str
    gambit: str

    def __post_init__(self) -> None:
        if self.primary_need not in PRIMARY_NEEDS:
            raise ValueError(f"Unknown primary_need: {self.primary_need}")
        if self.worldview not in WORLDVIEWS:
            raise ValueError(f"Unknown worldview: {self.worldview}")
        if self.gambit not in GAMBITS:
            raise ValueError(f"Unknown gambit: {self.gambit}")


def calculate_interaction(
    person_a_data: PersonData,
    person_b_data: PersonData,
) -> tuple[int, str]:
    """
    Compute Friction Score and Narrative Flavor when A's gambit meets B's response.

    Convention: A initiates with their Gambit; B's "response" is represented
    by B's Gambit. So we use A.gambit → B.gambit.
    """
    gambit_a = person_a_data.gambit
    gambit_b = person_b_data.gambit

    if gambit_a not in FRICTION_MATRIX or gambit_b not in FRICTION_MATRIX[gambit_a]:
        raise ValueError(f"Unknown gambit pair: {gambit_a!r} vs {gambit_b!r}")

    friction_score = FRICTION_MATRIX[gambit_a][gambit_b]
    key = (gambit_a, gambit_b)
    narrative = NARRATIVE_FLAVORS.get(key, _default_flavor(gambit_a, gambit_b, friction_score))

    return friction_score, f"Friction {friction_score}: {narrative}"


# ---------------------------------------------------------------------------
# 5. SAMPLE SCENE: Escalation from Friction 2 to Friction 10
# ---------------------------------------------------------------------------

def run_sample_scene() -> None:
    """
    Two characters start at Friction 2 and, through mismatched
    gambits, escalate to Friction 10.
    """
    # Beat 1: Tether + Tether → Friction 2 (harmonic)
    alice_start = PersonData(
        primary_need="Belonging",
        worldview="Unity",
        gambit="Tether",
    )
    bob_start = PersonData(
        primary_need="Belonging",
        worldview="Unity",
        gambit="Tether",
    )

    # Beat 2: Tether + Shield → Friction 8 (combustive)
    alice_mid = PersonData("Belonging", "Unity", "Tether")
    bob_mid = PersonData("Belonging", "Deficiency", "Shield")

    # Beat 3: Gift + Gavel → Friction 10 (combustive)
    alice_end = PersonData("Belonging", "Unity", "Gift")
    bob_end = PersonData("Significance", "Identity", "Gavel")

    scene = [
        ("Alice", alice_start, "Bob", bob_start, "Both reach for grounding - mild harmony (Friction 2)."),
        ("Alice", alice_mid, "Bob", bob_mid, "Alice reaches out; Bob deflects."),
        ("Alice", alice_end, "Bob", bob_end, "Alice offers vulnerability; Bob brings down the gavel."),
    ]

    print("=" * 60)
    print("SAMPLE SCENE: Friction 2 -> 8 -> 10")
    print("=" * 60)

    for name_a, data_a, name_b, data_b, beat in scene:
        score, flavor = calculate_interaction(data_a, data_b)
        band = _friction_band(score)
        print(f"\n{beat}")
        print(f"  [{name_a}] Need={data_a.primary_need}, Worldview={data_a.worldview}, Gambit={data_a.gambit}")
        print(f"  [{name_b}] Need={data_b.primary_need}, Worldview={data_b.worldview}, Gambit={data_b.gambit}")
        print(f"  -> {flavor} ({band})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_sample_scene()
