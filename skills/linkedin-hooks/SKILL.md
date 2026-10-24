---
name: linkedin-hooks
description: >-
  Write and score opening lines for a LinkedIn post before the full post gets written.
  A small local tool scores each hook 0 to 100 on six checks (fits before "see more" on a
  phone, concrete, tension, a person in it, plain words, no engagement bait) and the skill
  explains what to fix. Use it when someone says "give me hooks", "better first line",
  "which opening is best", "score these hooks", "my posts get no clicks on see more", or
  pastes a few first lines to compare. Reads the active business from founder-context so
  hooks fit its topics and avoid its banned words. Hands the winner to linkedin-post.
---

# linkedin-hooks

Line 1 decides whether anyone taps "see more". This skill writes options, scores them
with a local tool, and says why the winner wins. It does not write the full post.

Tool paths: `<this skill>` is the folder this SKILL.md is in (the "base directory" you
were given). Sibling skills sit next to it, so `<this skill>/../linkedin-hooks/` is the
hooks skill. Run tools with full paths built from that folder, not from the current
working directory, or they will look missing.

## 1. Business and idea

Find the business the same way every skill in this repo does: a named business, else
`founder/context.md`, else `~/.founder/active` and
`~/.founder/businesses/<slug>.md`. If none exist, ask once for topics, tone words,
words to avoid, and proof, and offer the founder-context skill. Never invent proof.

Name the business in your first line. Then get the one true thing the post is about.
If the user gave only a topic, ask what happened, with what number, for whom. A hook
without a fact under it is a promise the post cannot keep.

## 2. Write 6 to 8 options

Use different patterns from `references/patterns.md` (number, before-after, mistake,
scene, said-no, claim, question, overheard). Only use a pattern the facts support:
no "overheard" without real words, no "number" without a real number. When a number is
missing, write `{{your number}}` and keep going.

Write each hook as the founder would say it out loud, in the business's tone words.
Keep each under about 140 characters. Do not picture scenes, add feelings, or work out new
numbers ("9 on-time weeks") to make a hook stronger; those are made up even when flagged.
Use only what the user said or the business file holds. Habits and opinions count too:
"I count every late drop" or "I think parades are worse than rain" are made up unless the
user said them. Pick the top scorer unless you say why another one is better.

## 3. Score them

Save the options one per line to a temp file and run:

```bash
python3 <this skill>/scripts/hookscore.py hooks.txt --topics "<topic 1>,<topic 2>" --avoid "<words to avoid>"
```

The tool checks six things (weights in brackets):
- fold (15): fits before "see more" on mobile, about 140 characters.
- concrete (25): a number, a time, or a name.
- tension (20): something changed, cost, broke, or was refused.
- person (10): "I", "we" or "you" is in it.
- plain (20): no stock phrases, no vague words, no business words to avoid.
- no bait (10): no "Agree?", "comment below" and the like.

The tool is a heuristic written for this repo. It ranks options. It does not predict
reach, and a 95 can still be wrong for this audience. If Python is not available, score
by hand on the same six checks and say so.

## 4. Show the result

```
HOOKS for <business>, idea: <one line>

1. 92  <hook>        pattern: number
2. 85  <hook>        pattern: before-after
3. 78  <hook>        pattern: mistake
   (lower ones in one line each, with the main note)

Pick: #1. <one sentence on why, in plain words>
Fix before posting: <each {{placeholder}}>, or "nothing"
```

If the top hook scores under 70, say what is missing (usually a real number or a real
moment) and ask for it rather than polishing weak lines.

If the user pasted their own hooks, score theirs first and show them, then offer at most
3 improved versions that keep their words where they can. If one of their hooks names a
fact that is not in the business file (a family member, a customer, a number), ask them to
confirm it is real and OK to share before you pick it.

When you stop to ask for facts instead of writing hooks, still end with the handoff line,
so the user knows linkedin-post comes after.

## 5. Save and hand off

Append the scored list to `~/.founder/social/linkedin/<slug>/hooks.md` under a heading like
`## 2026-10-23, idea: <one line>` (a comma, not a dash), so linkedin-audit can later see
which patterns worked.

Next: "Say 'write it' and linkedin-post will draft the post on hook #1."

## Never

- Never write a hook that claims something the founder did not do or say.
- Never use engagement bait to lift a score. The tool penalizes it for a reason.
- Never post anything. The user posts.
