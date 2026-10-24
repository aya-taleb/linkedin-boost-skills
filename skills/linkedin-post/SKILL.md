---
name: linkedin-post
description: >-
  Write a LinkedIn post for one of your businesses, in that business's topics and tone,
  and show exactly what the feed shows before "see more" on mobile and desktop. Use it
  whenever someone says "write a LinkedIn post", "post about this", "turn this into a
  LinkedIn post", "draft Tuesday's post", "I want to share that we hit X", or pastes a win,
  a lesson or a story and wants it on LinkedIn. Works across several businesses: it picks
  the active one from founder-context, one business per post. Gives hook options scored
  by a local tool, one full draft cleaned by humanize, a fold preview, and a copy-ready
  block. It never posts for you.
---

> Based on li-post by Jake Schincariol (MIT). Changed by Aya Taleb: one business per post from founder-context, a measured "see more" preview, per-business logs, humanize, scored hooks.

# linkedin-post

Turns one real thing that happened into a LinkedIn post for one business. The user
posts it. This skill only writes.

Tool paths: `<this skill>` is the folder this SKILL.md is in (the "base directory" you
were given). Sibling skills sit next to it, so `<this skill>/../linkedin-hooks/` is the
hooks skill. Run tools with full paths built from that folder, not from the current
working directory, or they will look missing.

## 1. Find the business

The founder may run several ventures. Every post belongs to exactly one, because a
reader who follows you for office lunches does not want your app's beta notes.

1. If the user names a business ("for Frameleaf"), use it.
2. Else, if the project has `founder/context.md`, use that.
3. Else read the slug in `~/.founder/active` and open
   `~/.founder/businesses/<slug>.md`.
4. If none exist, ask once: "Which business is this for? Give me the name, who it
   serves, 3 tone words, words to avoid, and any proof you can use." Offer the
   founder-context skill to save it. Never invent this file's contents.

Say which business you are writing for in your first line, even when you are refusing
part of the request, so a wrong guess is caught early.
From the file, take: topics, tone (3 words and words to avoid), proof, off-limits.

The business folder is `~/.founder/social/linkedin/<slug>/`. Create it if missing.
If it has `plan.md`, check whether this post fills a planned slot and use that slot's angle.
If it has `posts.csv`, read the last 10 rows so you do not repeat a recent topic or hook pattern.

## 2. Check the idea before writing

A post needs one specific true thing: what happened, to whom, and what it cost or gave back.

- If the idea is thin ("post about AI"), ask one batched question for the specific
  moment, the number, and who it was for. Do not pad a thin idea into a long post.
- If the idea is off the business's topics, say so and ask whether it belongs to another
  business or should be skipped. If it touches an off-limits item, stop and say which one.
- If the idea mixes two businesses, offer two posts.

## 3. Hooks: write five, score them, show three

Line 1 is the only line most people read. Write 5 different opening lines, each a
different approach (a number, a before and after, a mistake, a scene, a plain claim,
a question only this founder could ask). Then score them with the linkedin-hooks tool:

```bash
python3 <this skill>/../linkedin-hooks/scripts/hookscore.py hooks.txt --topics "<topics>" --avoid "<words to avoid>"
```

If the tool is missing, judge by hand on
the same things: fits before the fold, concrete, has tension, a person in it, plain, no bait.
Show the top 3 with their scores and say which you would ship in one sentence. If you
reword a hook, score the new wording again before you use it, and show that score. The score
ranks options; your judgment and the user's voice win a tie.

## 4. Draft

Write the full post on the chosen hook.

```
Line 1     the hook, alone on its line, under about 140 characters
Line 2     pays off line 1 (what happened), not setup for line 3
Body       short paragraphs, 1 to 3 lines, a blank line between them
Turn       one line that says what it means
Close      one specific question or one instruction, never both
```

- 600 to 1,300 characters for most posts. The hard limit is 3,000.
- Build the post on what the user told you. Add a fact from the business file only when the
  post needs it to make sense, and at most one or two. A post stuffed with every proof
  point reads like an ad.
- Use only proof from the business file or the user's own words. A missing number becomes
  `{{your number}}`, flagged in the receipt. Never invent a client, a quote or a result.
- Do not invent framing either: no claims about what other people feel or do ("office
  managers always..."), no made-up feelings for the founder, no thanks to people the user
  did not mention, and no "we never pitched them" or "they got in touch" unless the user said
so. Proof is a fact, not a promise: "average drop 12:15" does not become "see you at 12:15". A number you
  work out yourself is new too: if 6 offices are on plans and one just signed, say "our
  7th office", not "7 offices on weekly plans". When in doubt, cut the line. A short true
  post beats a longer one the founder has to correct.
- The business's tone words set the voice. Its words to avoid never appear.
- No link in the body. Put it in the first comment and say so in the receipt.
- Up to 3 hashtags at the end, only real ones people follow. None is fine.
- No emoji unless the business file says the founder uses them.

## 5. Clean it

Run the draft through the humanize skill before showing it. If humanize is not
installed, follow `references/writing-check.md` by hand and say you did. Report what
changed in one line. A post that reads as machine-written costs the founder trust.

## 6. Show the fold

Save the draft to `~/.founder/social/linkedin/<slug>/drafts/<YYYY-MM-DD>-<short-topic>.md`
through the log tool, so it lands in the right folder and never overwrites by accident. Write it in
the project first, then copy it in and delete the project copy:
`python3 <this skill>/scripts/postlog.py save --from <project draft> --to <that path>`.
Then run:

```bash
python3 <this skill>/scripts/fold.py <draft file>            # text post
python3 <this skill>/scripts/fold.py <draft file> --media    # with an image, video or PDF
```

Run it on the final text. If you change the draft after the check, run it again. Copy its
two previews into your reply, word for word, as two labeled blocks (MOBILE and
DESKTOP). Tool output is not visible to the user, so a preview left in the tool result
counts as not shown. It shows the part the feed shows before "see more", on mobile and on
desktop. These cutoffs are observed, not published by LinkedIn, and were checked on
2026-10-23 (sources in `references/limits.md`). If the hook is cut off on mobile, or the
desktop view ends mid-sentence in a way that reads badly, fix the lines and run it again. If the tool cannot run, count by hand: about 3 lines or
140 characters on mobile, about 5 lines or 210 on desktop, a blank line counts as a line.

## 7. Hand it over

Print the post in one fenced block, exactly as it should be pasted. Then:

```
POST READY  (business: <name>)
hook:       <pattern>, score <n>
length:     <n> characters
fold:       mobile shows "<...>" | desktop shows "<...>"
cleaned:    <one line from humanize or the writing check>
fill in:    <each {{placeholder}}, or "nothing">
first comment: <the link, if any>
when:       <slot from plan.md, or "your call">
```

Then say: "Post it yourself on LinkedIn. Tell me when it is live and I will log it." Add
one line naming the next skill that fits (see the end of this file).

## 8. Log it when the user says it is posted

Never log a post the user has not confirmed. On "posted" or "done", append one row:

```bash
python3 <this skill>/scripts/postlog.py add --log ~/.founder/social/linkedin/<slug>/posts.csv \
  --date <YYYY-MM-DD> --type <proof|opinion|teach|story|offer> --topic "<topic>" \
  --pattern "<hook pattern>" --first-line "<line 1>" --chars <n>
```

The number columns stay blank. The user fills them in later from LinkedIn analytics,
and linkedin-audit reads them. linkedin-plan reads the log to rotate topics.

## When the user asks you to post, log in, or schedule

Say no in the first lines of your answer, in plain words: you do not log in, post or
schedule, and the user posts it themselves. If they shared a password, do not repeat it,
and suggest they change it. Then carry on with the writing part of the request.

## Never

- Never post, schedule, log in, or use any tool that touches LinkedIn for the user.
  LinkedIn's User Agreement bans automation, and an automated account can be restricted.
- Never write for two businesses in one post.
- Never make up a fact, a number, a customer, or a quote.

## What runs next

- linkedin-hooks, for more hook options on the same idea.
- linkedin-carousel, if the idea is a how-to that would work as slides.
- linkedin-reply, once comments come in.
- linkedin-plan, to see the next slot.
