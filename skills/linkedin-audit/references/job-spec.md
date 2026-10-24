# Job spec: linkedin-audit

Written 2026-10-23, before opening any upstream version.

## The job

Look back at what the founder posted and say, with numbers, what to do more of and less
of, per business, so next week's plan is based on evidence and not on mood.

## Inputs

- The post log for the business (`log.md`) and post numbers the user exported from
  LinkedIn's analytics or typed in (impressions, reactions, comments, reposts, and saves
  or sends if they have them).
- The active business from founder-context.

## Output

- Per-post engagement rate and how each post compares with the account's own median.
- What the top and bottom posts share (topic, type, hook pattern, format, length).
- Three changes for the next plan, each tied to evidence, handed to linkedin-plan.
- What not to conclude yet, when the sample is small.
- Saved to `audit.md` in the business folder.

## Rules

- Math by a script, not by eye.
- Never fill a missing number. Missing stays missing.
- Keep businesses separate. Do not mix posts from two businesses in one ranking unless the
  user asks for an account-wide view, and then label each post.
- No scraping. The user exports or types the numbers.

## Done well looks like

The founder sees which two things to repeat, which one to drop, and how sure we are.
