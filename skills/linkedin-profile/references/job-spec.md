# Job spec: linkedin-profile

Written 2026-10-23, before opening any upstream version.

## The job

Someone sees the founder's comment or post and taps the name. In a few seconds they
should know who this person helps, with what, why to believe them, and what to do next.
The founder runs several businesses from one profile, so it also has to decide what leads.

## Inputs

- Profile sections pasted by the user (headline, About, Featured, Experience, banner
  text), or their data export's profile file. No login, no scraping.
- All businesses from founder-context, and which one the profile should lead with now.

## Output

- A score built from the questions a visitor asks, with the reason for each lost point.
- Rewrites in fix-first order: headline (within the 220 character limit), the part of
  About that shows before "see more", the rest of About, Featured picks, an Experience
  entry per business, banner text, and the call to action.
- How to show several businesses without looking scattered.
- Saved to `profile.md` in the lead business's folder.

## Rules

- Never invent titles, results, clients or credentials. Placeholders for gaps.
- Field limits are dated and sourced.
- The user edits the profile by hand.

## Done well looks like

A buyer for the lead business gets it in five seconds, and the other ventures read as a
portfolio, not noise.
