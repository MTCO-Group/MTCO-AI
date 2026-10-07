"""
MTCO AI Roadmap planner component
Version 2.2

2.2: the Work Diary as designed on the canvas. The header reads "Work
Diary" with Diary in regular weight, and under it the Time Saved Clock: its
name and the period roller on one line (plain text with the green up and
down mark, no border, ending level with the last minute digit), the tiles
beneath. Three activity trackers sit in a row with level 20px headers: AI
Adoption Activity (emails Ken answered each complete week, Kensite and
AES, with week on week, month on month, last month's contacts and this
month so far), OpenRouter Activity (Ken's calls and charge for the roller's
period, linked to openrouter.ai; two placeholder key rows until the new
keys are settled) centred between its neighbours, and GitHub Activity
(linked to GitHub, four months of 14px days, no day labels or key, build
commits in the last 30 days). The supplied GitHub and OpenRouter logos are
inlined. "Nathan's WorkFlow" heads the calendar with no hint line; each day
shows its first entry and "+N more", and hovering or focusing a day opens a
pop-out of every entry that fades in from the top down over about two
seconds (Thursday to Sunday open to the left). A click still opens the day
panel, which counts "N Entries"; its project pills and the week's pen open
the project. Any roadmap project now opens in the detail sheet: a live one
shows its stage, a Time spent estimate from the diary (each linked entry
counts the gap since the previous entry that day, 10 to 90 minutes; the
first counts 30, an untimed one 20) and "Live project, so it is not queued
in What's Next." Section headings in the sheet are Kensite green.

2.1: the parchment is gone. Nathan: "a more stripped back version, much
more in keeping with the aesthetic of the dashboard as is". The tiles are
white with the calendar's 1px keyline and 8px corners, a hairline hinge
across the middle and Figtree figures in the page's near black; no
housing, pins or texture, and the colon is two Kensite green dots. The
flip, the shuffle and the roller are unchanged, with the falling leaf only
lightly shaded.

2.0: the flaps read as parchment and the roller sits quietly with the rest
of the page. Each leaf carries three layers of paper made in the browser
(long fibres, soft age staining and a fine tooth) over a warm base, with
burnt edges, and every tile is cut from a different part of the sheet so no
two share a grain; the figures are printed dark green. The roller is now a
plain pill like the page's own buttons (white, a 1px border, a green up and
down mark): the drum still turns behind it, but only the front label is
read and its neighbours fade out.

1.9: parchment flaps with dark green figures, and a period roller. The
leaves are warm paper with a fibre grain (an inline noise texture), the top
catching the light and the bottom in its shadow. The line of text under the
board and the This Week and This Month row are gone; instead a six sided
drum beside the board turns through Today, This Week, This Month, This
Quarter, This Year and All Time, on its own every eight seconds (held while
the pointer or focus is on it) or at a click. Each turn shuffles the board:
every flap flips rapidly through a run of digits, as if resetting, and
lands on that period's figure. A period the data does not carry is skipped.

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
