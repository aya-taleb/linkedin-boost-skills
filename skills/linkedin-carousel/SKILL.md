---
name: linkedin-carousel
description: >-
  Turn one idea into a LinkedIn document post (the swipeable slides people call a
  carousel): slide copy with one idea per slide, a cover that earns the first swipe, the
  post text that sits above it with a "see more" check, and a ready-to-upload PDF built
  on your machine with no design app. Use it when someone says "make a LinkedIn
  carousel", "turn this into slides for LinkedIn", "document post", "PDF carousel",
  "swipe post", or has a how-to, a list, or a post that did well and wants it as slides.
  Works per business from founder-context. You upload it yourself.
---

# linkedin-carousel

One idea, 6 to 10 slides, readable on a phone. The user uploads the PDF as a document post.

Tool paths: `<this skill>` is the folder this SKILL.md is in (the "base directory" you
were given). Sibling skills sit next to it, so `<this skill>/../linkedin-hooks/` is the
hooks skill. Run tools with full paths built from that folder, not from the current
working directory, or they will look missing.

## 1. Business and idea

Find the business: a named one, else `founder/context.md`, else `~/.founder/active`
and `~/.founder/businesses/<slug>.md`. If none exist, ask once for who it serves,
topics, tone, words to avoid, and proof, and offer founder-context. Name the business first.

A carousel works when the idea has steps, a list, a before and after, or a short
framework. A single opinion or a story usually works better as a text post; say so and
offer linkedin-post. If the source is a past post, read it from the business folder's
`drafts/` or `posts.csv`, or ask the user to paste it.

Ask for brand colors if the business file does not list them. Default: white background,
near-black text, one accent color.

## 2. Plan the slides

- **Cover**: the promise in under 10 words, plus a short line under it. It is the hook,
  so run it through the linkedin-hooks tool if installed
  (`python3 <this skill>/../linkedin-hooks/scripts/hookscore.py --line "<cover>"`).
- **Slides 2 to n-1**: one idea each. A short title line (under about 8 words) and at most
  2 short lines of body. Aim for 40 words or fewer per slide; people read on phones.
- **Last slide**: exactly one action (save it, try step 1 on Monday, follow the founder for
  the next one, or reply with X). One, not two.
- 6 to 10 slides is the usual range. Cut any slide that repeats another.
- Only real facts from the business file or the user. A missing number stays as
  `{{your number}}` and is flagged. Never put a made-up stat on a slide. Advice lines are
  fine; claims about what people think or do ("nobody trusts a late lunch") are not, unless
  the user said them.
- Do not add facts about people in the user's story (that a teacher "uses it with her
  class", that a customer "came back"). Use only what the user wrote.
- Write as the founder, in their own role. Do not give them a persona ("as an office
  manager, I would...").

Show the plan as a numbered list and ask the user to OK it before building, unless they
said to go ahead.

## 3. Write the slides file

Write `~/.founder/social/linkedin/<slug>/carousels/<YYYY-MM-DD>-<topic>/slides.md`:

```
# Cover line
Line under it
> <business name or founder name>
---
# Slide title
Body line one.
Body line two.
---
...
```

Clean the slide text with the humanize skill, or `references/writing-check.md` by hand if
it is not installed, and say which.

## 4. Build the PDF

```bash
python3 <this skill>/scripts/slides_pdf.py slides.md --check
python3 <this skill>/scripts/slides_pdf.py slides.md --out carousel.pdf --bg "#FFFFFF" --fg "#111111" --accent "#E4572E"
```

The tool makes square 1080 pages with large type, numbers each slide, and warns about long
slides, placeholders, and LinkedIn's document limits (100 MB, 300 pages, checked
2026-10-23, `references/limits.md`). It uses a built-in font, so it is plain but clean.
For a designed version, also write `design-brief.md` in the same folder: size 1080 x 1080
(or 1080 x 1350), colors, fonts if known, and the slide text, for Canva or Figma.

If Python is not available, give the slide text and the design brief only, and say so.

## 5. The post text above it

Write a short post (about 300 to 800 characters) that makes people open the document: the hook in
line 1, why it matters, and one line telling them to swipe. Then check what shows before
"see more" with a document attached:

```bash
python3 <this skill>/../linkedin-post/scripts/fold.py post.md --media
```

Posts with a document show about 3 lines on both mobile and desktop. Save it as
`post.md` in the carousel folder and clean it the same way. If you change the post after
the check, run the check again; the preview must match the final text.

## 6. Hand over

```
CAROUSEL READY  (business: <name>)
slides:  <n>  | file: <path to carousel.pdf>
cover:   <line> (hook score <n>)
post:    <length> characters, fold shows "<...>"
fill in: <placeholders>, or "nothing"
```

Then: "Upload the PDF yourself as a document post on LinkedIn and add a title when it asks.
Tell me when it is live and I will log it." On "posted", log it with
`python3 <this skill>/../linkedin-post/scripts/postlog.py add ... --type teach` (or the right type) so
linkedin-plan and linkedin-audit see it.

## Never

- Never upload or post for the user.
- Never put an invented number, logo, or quote on a slide.
- Never use images or fonts the user does not have the rights to.
