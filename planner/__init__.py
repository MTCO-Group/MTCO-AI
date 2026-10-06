"""
MTCO AI Roadmap planner component
Version 1.3

1.3: the Work Diary gains a trend under the calendar: emails (blue) and work
entries (green) for each day of the month shown, as two slim panels on one
shared date axis (emails run near a hundred a day and work near ten, so one
scale would flatten work and a second axis would mislead). Hover a day for
its numbers, click to open it. Day counts no longer include the email line.

1.2: the AI Summit picker is gone; workflow carries the Nathan Workflow
entries ({"entries": {"YYYY-MM-DD": [...]}}) to the Planner calendar. The
calendar is read only, so the only value coming back is still the plan.

1.1: the AI Summit picker rides in the same component. summit carries the
programme and everyone's saved picks in; a save comes back as
{"kind": "summit", "name": ..., "keys": [...], "nonce": n}, and the What's
Next plan now says {"kind": "plan", ...} so the app can tell them apart.

A two way Streamlit component. It shows the dashboard exactly as it is (in a
nested frame, untouched), adds the What's Next button, and returns the plan
back to Python when someone saves an arrangement. Two way is the whole point:
st.components.v1.html can only send, so the drag order could never get back
to the server to be written to GitHub.
"""
from pathlib import Path

import streamlit.components.v1 as components

_FRONTEND = Path(__file__).parent / "frontend"
_component = components.declare_component("mtco_planner", path=str(_FRONTEND))


def planner(dashboard_html, roadmap, plan, can_save, saved_at="", height=900, key=None,
            workflow=None):
    """Render the board. Returns None until someone saves, then the plan
    {"kind": "plan", "lanes": {"now": [...], "next": [...], "later": [...]}, "nonce": n}."""
    return _component(dashboard_html=dashboard_html, roadmap=roadmap, plan=plan,
                      can_save=bool(can_save), saved_at=saved_at, height=height,
                      workflow=workflow or {"entries": {}},
                      key=key, default=None)
