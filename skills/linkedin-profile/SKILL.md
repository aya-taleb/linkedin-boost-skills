---
name: linkedin-profile
description: >-
  Review and rewrite your LinkedIn profile so a visitor knows in five seconds who you help,
  with what, why to believe you, and what to do next, even when you run several businesses
  from one profile. Scores the profile on the questions a visitor asks, explains every lost
  point, and rewrites in fix-first order: headline, the top of About, Featured, Experience,
  banner text, and the call to action. Use it when someone says "fix my LinkedIn profile",
  "rewrite my headline", "review my About section", "how do I show two businesses on
  LinkedIn", or pastes profile sections. You edit the profile yourself.
---

# linkedin-profile

People tap a name after a good post or comment. The profile has a few seconds to make them
stay, follow, or reach out. This skill makes those seconds count.

## 1. Businesses and the lead

Read every business file in `~/.founder/businesses/*.md` and the slug in
`~/.founder/active` (or `founder/context.md` for a single business). If none exist,
ask once for each business's offer, who it serves, stage, and proof, and offer
founder-context. Never invent titles, results, or clients.

Ask which business the profile should lead with right now, if the user did not say. Default
to the active business. A profile can only lead with one; the others still show, lower down.

## 2. Get the profile

The user pastes it. You need: headline, About, Featured items, Experience entries (title,
company, dates, description), banner text if any, and the custom button or link if set.
They can also use the profile file from LinkedIn's data export. Never log in or scrape.
Ask for anything missing in one message, and score what you have.

## 3. Score it

Score out of 100 on what a visitor asks, in this order. Each lost point gets a reason.

| question a visitor has | points | where they look |
| --- | --- | --- |
| Who do you help, and with what? | 25 | headline |
| Why should I believe you? | 20 | top of About, Featured, Experience |
| Is this for me? | 15 | About uses the buyer's words and problems |
| What do I do next? | 15 | a clear call to action, a link, the Featured slot |
| Are the other ventures confusing? | 10 | Experience, banner, About |
| Does it look cared for? | 15 | photo and banner present, no gaps, no stock phrases, consistent with recent posts |

For "looks cared for", ask the user whether a photo and banner are set if you cannot tell.
Do not guess.

## 4. Rewrite in fix-first order

Fix the biggest point loss first. For each section give the new text and one line on why.

- **Headline** (220 characters max; about 60 to 70 show in search, checked 2026-10-23,
  `references/limits.md`): who you help, with what, plus one proof or a short "also building".
  Offer 3 options and count each. Every option names the lead business in its first few
  words, because search shows only the start.
- Use titles exactly as the user or the profile gives them. Never upgrade, swap or merge a
  title, even to make it fit.
- **About, the top part**: about 300 characters show before "see more". Open with the
  buyer's problem or the result you deliver. Give that part on its own and count it.
- **About, the rest** (2,600 max): who you are, what you do for whom, proof, the other
  ventures in a short "I also run" line, and how to reach you.
- **Featured**: pick 2 or 3 items that prove the lead business (a post that did well, the
  product page, a case study). Ask the user what exists; do not invent items.
- **Experience**: one entry per business with a plain one-line description and a few lines
  on what it does, for whom, and proof. Past roles: keep what supports the lead business.
- **Banner**: one line of text and what it should show.
- **Call to action**: the custom button or link, pointing to the lead business.

**Several businesses**: lead with one in the headline and About. Show the rest as "also
building" in a short line and in Experience. Do not stack three ventures in the headline.

Every result, number, and title must be in the business files, the pasted profile, or what
the user said. Gaps become `{{placeholder}}` and are flagged. Do not write the buyer's
pains as specific details (spreadsheets, tools, habits) unless the business file names them;
use its own words for who it serves. Keep each fact as written: "6 offices since August"
and "late twice in 11 weeks" are two facts, not "6 offices in 11 weeks".

Clean every rewrite with the humanize skill, or `references/writing-check.md` by hand if it
is not installed, and say which. Avoid every business's words to avoid.

## 5. Show and save

```
PROFILE SCORE  <n>/100  (leading with: <business>)
lost points:  <question>: -<n>, <reason>   (one line each)

FIX FIRST: <section>
<new text>   [<count>/<limit>]
why: <one line>
...
FILL IN: <placeholders>
```

Save it to `~/.founder/social/linkedin/<lead-slug>/profile.md` with the date, with the Write
tool or Bash. Put the full rewritten text in the file, not a pointer to the chat. Save it even when you also ask questions; mark open items in the file.
Say which cleanup you used (humanize or the writing check).

End with: "Make these edits yourself on LinkedIn. Paste the new profile anytime and I will
score it again."

## Never

- Never log in or edit the profile for the user.
- Never invent a title, credential, client, or result.
- Never copy another person's profile text.
