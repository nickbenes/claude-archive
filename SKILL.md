---
name: archive-claude-chats
description: Archive all Claude.ai chats, projects (metadata + knowledge files), and account memory to local Markdown/JSON, sorted chronologically by folder name. Use when the user wants to back up, consolidate, search, or migrate their Claude.ai chat history.
---

# archive-claude-chats

Archives a Claude.ai account's full chat history using the internal JSON API (not a
browser extension or page-scrape), via [browser-harness](https://github.com/browser-use/browser-harness)
as the authenticated-browser bridge. See [README.md](README.md) for the full technical
writeup — this file is the condensed skill entry point.

## When to use this

The user asks to back up, export, consolidate, or migrate their Claude.ai chat
history, project knowledge bases, or saved memory.

## Prerequisites (check before running)

1. `browser-harness` must be installed and on `$PATH`. If `which browser-harness`
   fails, point the user to https://github.com/browser-use/browser-harness — its
   README has an LLM-installable setup prompt.
2. The user's Chrome must have a tab logged into claude.ai (any tab; doesn't need
   to be focused). If archiving a *different* Claude.ai account than whatever the
   current Claude Code session is authenticated as, that's fine — this script only
   reads the browser's session cookie, never the CLI's own credentials.

## Running it

```bash
python3 archive_api.py --output <destination-folder> [--max N]
```

Ask the user where they want the archive written — do not assume
`~/gdrive/ObsidianVault/` or any other personal path. A sensible default is
`~/claude-archive`, but confirm rather than guessing, since this is a new directory
creation the user will want to know about in advance.

Use `--max 3` first for any new user/setup to confirm the pipeline works (session
cookie valid, browser-harness reachable) before running the full archive, since a
full run can take a few minutes and there's no resume-from-partial-run support yet.

## What it produces

See [README.md](README.md#output-structure) for the full directory layout. In short:
one timestamp-prefixed folder per chat (sorts chronologically by name), a
`_projects/` folder with each project's metadata and knowledge files, and a
`_memory.md` with the account's Settings → Capabilities memory.

## Troubleshooting

- **A chat fails with a `TimeoutError` traceback from browser-harness**: the script
  already retries each chat up to 3 times with increasing timeouts. If a chat still
  fails after that, it's usually one with an unusually large number of attached
  files/images — safe to re-run just that chat afterward rather than the whole
  archive (see the retry pattern in README.md).
- **Everything fails immediately**: check that `browser-harness` can actually reach
  a running, logged-in Chrome (`browser-harness <<< 'print(page_info())'` as a smoke
  test) before assuming the archive script itself is broken.
- **Only some chats show up**: the internal API occasionally changes; if pagination
  looks broken, re-check the `chat_conversations?limit=&offset=` shape against
  what the network tab shows for a real `/recents` page load.
