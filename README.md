# MTCO AI Roadmap

Working folder for the MTCO Group AI Roadmap dashboard, live at
https://mtco-ai.streamlit.app and deployed from the GitHub repo
Nathanjmcg/mtco-ai.

## Files
- `app.py` - Streamlit entry point. Reads dashboard.html, injects data/roadmap.json into it and renders it full page.
- `dashboard.html` - the dashboard itself (logos, fonts and runtime inlined). Holds no project data.
- `data/roadmap.json` - the companies shown, the category list and every project. Ken appends proposals to the copy in the repo.
- `requirements.txt` - Streamlit only.
- `planner/` - the What's Next planner, a two way Streamlit component. `frontend/index.html` shows the board and the planner; `__init__.py` wires it to Python.
- `Publish App To GitHub.py` - pushes the files above to the repo. Run it after any change.
- `Publish App.cmd`, `Push Roadmap Data.cmd`, `Pull Roadmap Data.cmd` - double click versions of the same thing.

## Making a change live
1. Edit the file(s) in this folder.
2. Run `Publish App To GitHub.py` from a terminal with the full Python path.
3. Streamlit Cloud redeploys within a couple of minutes.

## Where the project data lives
`data/roadmap.json` in the repo is the single source of truth. Ken writes to it when
someone emails him an idea, so the publish script never overwrites it (it only creates
it if the repo has none). To edit a project by hand, edit it on GitHub or pull the file
down first.

Each project carries: id, company (mtco, kensite, aes, eventus, ats, thinkhire, fireflai),
name, stage (Proposed, Scoped, Planned, Building, Testing, Shipped), category (one of the
list in the file), owner, proposed_by, date (Mon YYYY), summary (one line, shown on the
card), scope (What it does), how (How it does it) and who (a list of {who, how} pairs).

## Ken
Staff on the proposers list, and guests granted the ai_roadmap ability, can email Ken an
idea. He works out the company and category, asks for anything he cannot infer, then files
it as Proposed and confirms with a link to the app.

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```

## What's Next planner
The button under the stage bracket opens a planner: every Proposed idea across the
group, dragged into Now, Next or Later to form the AI Manager's queue. Saving writes
a `plan` object into `data/roadmap.json` in the repo and nothing else, so a proposal
Ken filed a second earlier can never be lost by someone saving an arrangement.

Saving needs a GitHub token with contents write access to this repo, stored in the
app's Streamlit Cloud secrets as `github_token`:

    Streamlit Cloud > this app > Settings > Secrets
    github_token = "ghp_..."

Without it the planner still opens, read only, and says so on screen. Note the app is
public, so with the token in place anyone who has the link can rearrange the plan.
Every save is a commit, so the history in GitHub is the audit trail and any change can
be reverted.

Click any card (or focus it and press Enter) to expand it: the sheet shows the
full scope, how it works and who it helps, with buttons to place it in a lane
and arrows to step to the next card. A drag does not open it.

## Work Diary and Nathan Workflow
The What's Next view has a Work Diary button. The Work Diary holds the Nathan Workflow
widget: a month calendar, Monday first, where clicking a day slides out that day's work
entries. Keyboard: arrow keys move between days, Enter opens one, Page Up and Page Down
change month, Escape closes the day and then the Work Diary.

Each entry Ken has linked to a live roadmap project (stage past Proposed) shows
that project as a pill beside its title in the day panel, and the panel's foot
shows the week's pen: every project worked on that week with its count. Ken
links entries when Diary Taglines.py runs; to correct one, edit the entry's
"project" field (a roadmap id, or "" for none) and Ken will leave it alone.

Under the calendar a trend shows each day of the month: emails (blue, from the
"Emails: N received, M sent" entry) and work entries (green), on one date axis
in two panels. Hover a day for its numbers; click to open it.

The Work Diary header also carries a split flap board of the time Ken and our AI
have saved: plain white split flap tiles with a roller beside them that turns through Today,
This Week, This Month, This Quarter, This Year and All Time, shuffling the board
onto each period's figure. The numbers
are in data/Time Saved.json, written every minute by Push Time Saved.py on Ken's
machine from the Ken Time Saved Index (the same count as Ken Mission Control)
to the live-data branch, which the board reads every 90 seconds; main gets a
copy at most hourly so Streamlit Cloud is not pulled every minute.

The Work Diary header carries a GitHub activity heatmap: one block per month,
Monday to Sunday down and weeks across, shaded by the day's build commits
(from the "kind": "github" entries Diary GitHub Commits.py writes).
Diary GitHub Commits.py runs every five minutes on Ken's machine (Kensite Task
Runner) and covers yesterday and today; an open Work Diary re-reads the diary
every five minutes, so new commits appear without reloading the page. Hover a
day for the repos and counts, click it to open the day, click a month name to
show that month.

Entries are read from `data/Nathan Workflow.json` in the repo. That file does not exist
yet, so every day opens blank. Whatever writes the work logs later only needs to create it:

    {"entries": {"2026-10-06": [{"time": "09:30", "title": "...", "detail": "..."}]}}

`time` and `detail` are optional. The app is public, so anything in that file can be seen
by anyone with the link.

The AI Summit Barcelona picker was retired in app 2.3. Its data files
(`data/summit_programme.json`, `data/summit_picks.json`) are left in the repo untouched.
