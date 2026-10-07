"""
MTCO AI Roadmap planner component
Version 1.8

1.8: the time saved board looks and moves like a real split flap display.
Each tile is two halves on a hinge (a dark slot and a pin either side) in a
dark housing, set in Oswald; a change drops the old top leaf to flat and
lands the new bottom leaf over the old bottom, and a tile steps through
every digit between its old and new value (the tens of minutes only 0 to
5). The board fetches its own numbers every 90 seconds while the Work Diary
is open and the tab is visible: data/Time Saved.json on the live-data
branch through GitHub's API (conditional, so an unchanged file costs
nothing), else the raw file. Push Time Saved 1.1 writes that branch every
minute.

1.7: a split flap board at the top of the Work Diary, in Kensite green,
showing the time Ken and our AI have saved: hours and minutes all time,
with this week and this month beneath on wide screens, and a line saying
since when and when it was last worked out. The numbers come in as
workflow["time_saved"] (app 2.4, from data/Time Saved.json). Only a digit
that changes flips; the first showing rolls each digit up from 0, and
reduced motion sets them straight. Below 1180px wide the GitHub heatmap
gives way to it, below 760px both are hidden.

1.6: click a card in What's Next (or press Enter on it) to expand it into a
detail sheet: company, category, lane, owner and date proposed, then what it
does (scope), how it works and who it helps. A click that was really a drag
does not open it. With saving on, the sheet can place the card in Not placed,
Now, Next or Later (the same as dragging; Save plan still keeps it). Arrows
step through the cards, Escape closes and returns focus to the card. Read
only viewers can still open it. The proposer's email is never shown.

1.5: a GitHub activity heatmap in the Work Diary header, between the title
and the Back button. One small block per month (up to six, from the first
month with commits to this month), Monday to Sunday down and weeks across,
like GitHub's own graph. The shade is the day's build commits summed across
repos in four steps (1 to 3, 4 to 9, 10 to 19, 20 and over); commits Ken and
the apps make on their own show in the tooltip only. Click a day to open it,
click a month name to jump the calendar there. Hidden under 900px wide.

1.4: project pills. A diary entry Ken has linked to a live roadmap project
("project": id, set by Diary Taglines 1.1) shows that project as a small pill
to the right of its title in the day panel, tinted in its company's colour.
The foot of the day panel holds the week's pen: one pill per project linked
Monday to Sunday of that day's week, with its count, most first; clicking one
highlights that project's entries. The calendar itself is unchanged and no
new view or route is added. Project names come from the roadmap the app
already passes in.

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
