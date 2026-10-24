---
name: linkedin-plan
description: >-
  Plan the LinkedIn week for each of your businesses: which post goes out which day, the
  angle drawn from what really happened, the topic it covers, and who to engage with.
  Rotates topics from founder-context so no topic repeats too soon, and reads what you
  already posted from the per-business log. Use it when someone says "plan my LinkedIn
  week", "what should I post this week", "content calendar for LinkedIn", "I have nothing
  to post", "plan posts for both my businesses", or "what's next on LinkedIn". Writes a
  plan file per business. It never schedules or posts anything.
---

> Based on li-plan by Jake Schincariol (MIT). Changed by Aya Taleb: one plan per business from founder-context, topic rotation from the post log, a weekly budget across ventures.

# linkedin-plan

Decides what gets written this week, per business. The other skills write. The user posts.
Run it once a week, on the same day.

Tool paths: `<this skill>` is the folder this SKILL.md is in (the "base directory" you
were given). Sibling skills sit next to it, so `<this skill>/../linkedin-hooks/` is the
hooks skill. Run tools with full paths built from that folder, not from the current
working directory, or they will look missing.

## 1. Load the businesses

Read `~/.founder/businesses/*.md` (one file per business) and
`~/.founder/active`. A project-local `founder/context.md` overrides both and means
one business only. If nothing exists, ask once for the business name, who it serves, 3 to
5 topics, tone, and proof, and offer the founder-context skill to save it. Never invent
topics or proof.

Ask which businesses to plan this week if the user did not say. Default: the active one.

For each business, its folder is `~/.founder/social/linkedin/<slug>/`. Read if present:
- `posts.csv`: what was posted (date, type, topic, pattern, first line).
- `plan.md`: last week's plan, to see what was skipped.
- `audit.md`: what linkedin-audit found works. Follow its three changes.

## 2. Ask what happened

Posts come from real events, not from topics. Ask once, in one batched message:

- What happened this week in each business? A customer moment, a number, a mistake, a
  thing you built or changed, a conversation, an argument.
- How many posts can you really write and post this week, across everything?
- Any date that matters (a launch, an event, a holiday when your buyers are away)?

If the user has nothing, say so plainly and still write a short plan from proof in the
business file, marked "draft until you add this week's news". A thin week is better with
two good posts than four weak ones. If the user said "this week", plan the rest of this
week from today; do not move it to next week without asking.

## 3. Set the weekly budget

A solo founder running several ventures cannot post four times for each. Split the posts
the user said they can do. A sensible start: 3 posts a week for the main business, 1 to 2
for a second one, and 0 to 1 for others. Say the split and why in one line.
Never put two businesses' posts on the same day from the same profile; it reads scattered.

## 4. Rotate topics

Each business file lists its topics. Pick each slot's topic with this rule:
1. Start with the topic posted least recently in `posts.csv` (never posted counts as oldest).
2. Skip a topic that was posted in the last 7 days, unless the user's news is about it.
3. A real event beats rotation. Say when you broke the rotation and why.

Then mix post types across the week, never the same type two days in a row:

| type | job |
| --- | --- |
| proof | something that happened, with a real number |
| teach | one thing the reader can do today |
| opinion | a position some of the audience will disagree with |
| story | a scene, a person, and what it cost |
| offer | what you sell, said plainly, at most once a week |

For each slot give: day and time, business, type, topic, the angle (a specific moment,
not a topic), and a hook direction for linkedin-post. "Office lunch" is a topic.
"The Tuesday the taco truck broke down and the office manager ordered pizza for 40" is an angle.

## 5. When to post

For a B2B audience in one timezone, Tuesday to Thursday mornings in the buyer's timezone
is a reasonable default. Say plainly that time matters far less than the hook. For local
or consumer businesses, ask when their buyers scroll (lunch breaks, evenings) and use that.

## 6. Who to engage with

Comments on other people's posts put the founder in front of new readers. Per business,
list up to 10 people or pages, split into: buyers (people who could pay), peers (same
stage or field), and bigger accounts the buyers follow. Take names only from the user,
from `warm-leads.csv`, or from `sales/leads.csv`. If you have none, ask for them. Never
make up people. Suggest 15 minutes a day of comments using linkedin-comment.

## 7. Write the plan

Write `~/.founder/social/linkedin/<slug>/plan.md` for each business:

```
# <Business> LinkedIn plan, week of <YYYY-MM-DD>

| day | time | type | topic | angle | hook direction | status |
| --- | --- | --- | --- | --- | --- | --- |
| Tue | 8:15 | proof | <topic> | <angle> | <pattern> | planned |

Topics rotated: <topic> (last posted <date>), ...
Engage: <names and why>, or "ask user for names"
Budget this week: <n> posts for this business, <n> total across businesses
```

Show a short combined view across businesses in chat. End with:
"Nothing is scheduled. You post each one yourself. Say 'write Tuesday' and linkedin-post
will draft it."

When the user gave news, use it in as many slots as it honestly fits (a launch can carry a
proof post and a teach post). Fill the rest from proof in the business file, and say which
slots came from the file.

## 8. Log what was posted

When the user says a planned post went out, mark it `posted` in `plan.md` and make sure it
has a row in `posts.csv` (linkedin-post's `<this skill>/../linkedin-post/scripts/postlog.py add` does this). When a slot
is skipped, mark it `skipped` so next week's rotation sees it.

## When the user asks you to schedule or auto-post

Say no in the first lines: plans are text, nothing is scheduled or connected to any tool,
and the user posts each one by hand. Then plan.

## Never

- Never schedule, post, or log in to LinkedIn for the user. Plans are text.
- Never put two businesses in one post.
- Never invent events, numbers, or people for the plan.

## What runs next

linkedin-post for each slot, linkedin-comment for the engage list, and linkedin-audit
once a month to tune the plan.
