# claude-archive

Archive your entire Claude.ai chat history — every conversation, every project's
knowledge base, and your saved memory — to local Markdown/JSON files, sorted
chronologically.

Unlike browser-extension exporters, this pulls from Claude.ai's own internal JSON
API (the one the web client itself calls), so you get:

- Every chat, fully paginated (not just what's rendered in the sidebar)
- Real per-message and per-chat timestamps (not scraped/guessed)
- Clean conversation text (no sidebar/nav noise)
- Text attachments inlined automatically (Claude already extracts their text)
- Code-execution output files (images, generated PDFs rendered as page previews) downloaded
- Every project's name, description, custom instructions, and knowledge-base files
- Your account-level "memory" (Settings → Capabilities)

## How it works

Claude.ai puts a Cloudflare bot check in front of its API, so plain `requests`/`curl`
calls get a 403 even with a valid session cookie. This script instead runs the exact
same `fetch()` calls *from inside your already-logged-in Chrome tab*, using
[browser-harness](https://github.com/browser-use/browser-harness) as the bridge — same-origin,
real browser TLS fingerprint, no bot check triggered. No login flow, no headless
browser to configure: it just uses whatever Chrome session you already have open.

## Prerequisites

1. **Python 3.8+** (stdlib only — no pip installs needed for this script itself)
2. **[browser-harness](https://github.com/browser-use/browser-harness)** installed and on your `$PATH`.
   Follow that repo's README (it has an LLM-installable setup prompt).
3. **Chrome open and logged into claude.ai** — any tab, doesn't need to be the active one.

## Usage

```bash
python3 archive_api.py --output ~/claude-archive
```

Options:

- `--output PATH` — where to write the archive (default: `~/claude-archive`)
- `--max N` — only process the first N chats (useful for a quick test run)

A full run of ~125 chats (with attachments/files) takes about 2-3 minutes.

## Output structure

```
claude-archive/
├── _memory.md                          # Your Settings → Capabilities memory
├── _projects/
│   └── <Project Name>/
│       ├── metadata.json               # name, description, custom instructions
│       └── <knowledge-file>.html        # each project doc, full content
└── 20260701_132222_Chat_title/
    ├── conversation.md                  # full chat, real timestamps per message
    ├── metadata.json                    # chat id, url, created/updated_at
    ├── attachments/                     # text files you uploaded (extracted text)
    │   └── some_file.txt
    └── files/                           # images/previews generated during the chat
        └── preview_0.png.webp
```

Folder names are prefixed `YYYYMMDD_HHMMSS_`, so a plain alphabetical sort of the
archive directory is also a chronological sort. Chats with no discoverable creation
timestamp (shouldn't normally happen) fall back to an `undated_` prefix.

## Known limitations

- **Requires a real, logged-in browser session** — this can't run on a headless
  server with no browser at all. It rides your existing Chrome session, so if you're
  not logged into claude.ai in some open Chrome tab, it has nothing to authenticate with.
- **Uses Claude.ai's internal API**, which is undocumented and could change without
  notice. If a run starts failing across the board, that's the first thing to check.
- **Multiple accounts**: it archives whichever account is logged into the browser tab
  browser-harness attaches to — independent of any other Claude account/session on
  the same machine (e.g. your Claude Code CLI login). See "Multiple accounts" below.
- Binary (non-image) attachments beyond what Claude's own text extraction covers
  aren't separately downloaded — only `extracted_content` text and code-execution
  image previews are pulled today.

## Multiple accounts / different email than Claude Code

The script authenticates purely off the browser's session cookie — it has no idea
what account your Claude Code CLI itself is logged in as, and doesn't need to. If you
want to archive a different Claude.ai account than the one Claude Code uses:

1. Open (or switch to) a Chrome profile/tab logged into that account at claude.ai
2. Point `browser-harness` at that Chrome instance (see its README for how it selects
   a running Chrome)
3. Run the script as normal — it'll pick up whatever account is in that tab

## Using this as a Claude Code skill

See [SKILL.md](SKILL.md) for how to install this as an invocable skill
(`/archive-claude-chats`) rather than running the script by hand.
