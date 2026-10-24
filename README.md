# linkedin-boost-skills

Claude skills that help a founder grow on LinkedIn, for each of their businesses, without handing over the account.

## What do you want to do?

| I want to... | run this |
| --- | --- |
| write a post for one of my businesses and see what shows before "see more" | /linkedin-post |
| plan this week's posts across my businesses | /linkedin-plan |
| find a better first line before I write the post | /linkedin-hooks |
| reach out to real leads without spamming anyone | /linkedin-dm |
| learn why some posts did well and do it my way | /linkedin-viral |
| leave a comment worth reading on someone's post | /linkedin-comment |
| answer the comments under my own post | /linkedin-reply |
| clear my LinkedIn inbox and spot the scams | /linkedin-inbox |
| turn an idea into a swipeable PDF post | /linkedin-carousel |
| get several posts out of a talk, podcast or newsletter | /linkedin-repurpose |
| fix my profile so visitors get it in five seconds | /linkedin-profile |
| see which posts worked and what to change | /linkedin-audit |

## Install

```
/plugin marketplace add aya-taleb/linkedin-boost-skills
/plugin install linkedin-boost-skills@linkedin-boost-skills
```

## Start here

Run `/founder-context` first and set up each business: who it serves, topics, tone, proof.
Every skill here reads it, so posts sound like that business and use only real facts.
Then run `/linkedin-plan` to plan the week, and `/linkedin-post` to write the first slot.

## Good to know

- Nothing here posts, messages, scrapes or logs in to LinkedIn. Skills write; you post and send by hand.
- One business per post. Logs and plans live in `~/.founder/social/linkedin/<business>/`.
- Nothing is made up. Missing numbers come back as `{{your number}}` for you to fill in.
- Outreach stays inside a daily invite limit (default 15), and every limit we use is dated and sourced in each skill's `references/limits.md`.
- The Python tools use the standard library only and run on your machine. The skills save their files in `~/.founder/social/linkedin/`, outside the protected `~/.claude` folder, so saves don't need approval each time.

## Credits

Made by Aya Taleb (github.com/aya-taleb). linkedin-post, linkedin-plan and linkedin-dm are built on Jake Schincariol's linkedin-agent-skill (MIT), and the other skills thank his pack for the ideas. See CREDITS.md. MIT.
