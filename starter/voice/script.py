# One short answer per slot prompt — matches the order CALM asks for.
USER_TURNS = [
    "Hello RxTwin, this is Pharmacist Divya.",
    "I need to log a compliance ticket please.",
    "Fridge B temperature alarm. It dropped to minus one Celsius.",
    "temperature",
    "urgent",
    "divya@rxlab.com",
]

RESUME_TURNS = [
    "Hey RxTwin, Pharmacist Divya is back on shift.",
    "Yes, we moved all the Shingrix vials to Fridge A safely.",
    "That is all for now. Thanks RxTwin.",
]

PRESENTATION_ACTS = [
    {"title": "Act 1 — Report temperature excursion", "turns": USER_TURNS, "new_session": False},
    {"title": "Act 2 — Shift resume (new session)", "turns": RESUME_TURNS, "new_session": True},
]

ALL_PRESENTATION_TURNS = USER_TURNS + RESUME_TURNS
