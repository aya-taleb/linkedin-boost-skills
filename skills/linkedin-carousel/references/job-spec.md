# Job spec: linkedin-carousel

Written 2026-10-23, before opening any upstream version.

## The job

Turn one idea into a LinkedIn document post: a short deck people swipe through, plus
the text that sits above it. The founder needs slide copy, a cover that earns the first
swipe, a clean PDF they can upload, and the post text.

## Inputs

- The idea or source (a post that did well, notes, a how-to).
- The active business from founder-context. Brand colors if the user has them.

## Output

- Slide plan: one idea per slide, short text, a cover and a last slide with one action.
- The caption post, with what shows before "see more".
- A PDF built locally by a stdlib tool from the slide file, so no design app is needed.
  A design brief for Canva or Figma if they want a nicer version.
- Files in `carousels/<date>-<topic>/` in the business folder. Logged when posted.

## Rules

- No made-up stats on slides. Placeholders stay visible.
- Readable on a phone: big text, high contrast, few words per slide.
- Check the file against LinkedIn's upload limits (dated and sourced).
- The user uploads. Nothing is posted for them.

## Done well looks like

A stranger swipes past slide 2, learns one useful thing, and the founder can upload the
PDF in the next five minutes.
