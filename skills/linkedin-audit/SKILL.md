---
name: linkedin-audit
description: >-
  Look back at what you posted on LinkedIn for one business and say, with real numbers,
  what to repeat, what to drop, and how sure we are. A local script ranks each post
  against your own median (not raw impressions), then finds what the top posts share by
  type, topic, hook pattern and length, and hands three changes to next week's plan. Use
  it when someone says "audit my LinkedIn", "what's working on my LinkedIn", "which posts
  did best", "why are my posts flopping", "review last month's posts", or pastes or exports
  post numbers. For why one pasted post beat another on its writing, use linkedin-viral.
  Never scrapes; you export or type the numbers.
---

# linkedin-audit

Turns what was posted into what to post next. Every number comes from the user's own
analytics. Missing numbers stay missing.

Tool paths: `<this skill>` is the folder this SKILL.md is in (the "base directory" you
were given). Sibling skills sit next to it, so `<this skill>/../linkedin-hooks/` is the
hooks skill. Run tools with full paths built from that folder, not from the current
working directory, or they will look missing.

## 1. Business and numbers

Find the business: a named one, else `founder/context.md`, else `~/.founder/active`
and `~/.founder/businesses/<slug>.md`. If none exist, ask once and offer
founder-context. Audit one business at a time. If the user wants an account-wide view,
label every post with its business.

Get the numbers:
- `~/.founder/social/linkedin/<slug>/posts.csv` (written by linkedin-post), with impressions,
  reactions, comments, reposts, and saves or sends if they have them, typed in from LinkedIn
  analytics; or
- a CSV they export from LinkedIn's post analytics; or
- numbers pasted in chat. Put them into a CSV with the columns
  `date,type,topic,pattern,first_line,chars,impressions,reactions,comments,reposts,saves,sends`.

Never log in, scrape, or browse LinkedIn for the numbers. If the user has none, explain where
to find them (each post's analytics, or the Analytics tab) and stop.

## 2. Run the math

```bash
python3 <this skill>/scripts/audit.py <posts.csv>
```

It computes, per post: engagement rate (reactions + comments + reposts + saves + sends,
over impressions), the rate compared with the account's own median, reach compared with
the median, and a weighted rate where comments count 3x and reposts, saves and sends 2x.
It groups by type, topic, hook pattern and length band. Rows with no impressions are listed
as "no numbers yet" and left out. Do not do this math by eye. If Python is not available,
say so and show your arithmetic step by step.

## 3. Read the results

Write it for a busy founder:

- **Top 3 and bottom 3 posts**, copied from the script's ranking, in its order (bottom 3 are
  the last three rows). Do not
  re-rank by eye or retype numbers; paste the script's lines. Say which rate you ranked by
  (the script sorts by weighted rate).
- **What the top posts share**: type, topic, pattern, length, day. Only claim a pattern if
  at least 2 of the top posts share it and the bottom ones mostly do not.
- **How sure we are**: under 8 posts with numbers, say "early hints, not findings". Name
  other things that could explain a result (a holiday, a repost by a big account, a
  different time).
- **Comments**: if `comments.md` or `warm-leads.csv` exist, note which posts started real
  conversations or leads. That matters more than reactions.
- **Hooks**: if `hooks.md` exists, compare hook scores with results and say whether the
  scoring looks useful for this audience.

Never fill a missing number, never round a small sample into a trend, and never compare
with "industry benchmarks" unless the user gives a source.

## 4. Three changes

End with exactly three changes for the next plan, each tied to evidence:

```
1. More <x>: posts 3 and 7 did 2.4x and 1.9x the median rate, both <x>.
2. Less <y>: the 3 <y> posts sat under 0.6x.
3. Try <z>: not enough data on <z>; plan 2 posts to find out.
```

## 5. Save and hand off

Save to `~/.founder/social/linkedin/<slug>/audit.md` with the date, the script output, the
reading, and the three changes. Use the Write tool or Bash, then confirm the file exists
(for example `ls -l` on it). linkedin-plan reads this file. Tell the user:
"linkedin-plan will use these three changes next week."

## Never

- Never scrape or log in.
- Never invent or estimate a missing number.
- Never mix businesses in one ranking without labels.
