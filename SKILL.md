# claude-archive

**Export and archive all your Claude.ai chats with automatic timestamps and organization.**

This skill automates the complete process of downloading, organizing, and cataloging your entire Claude.ai chat history. Each chat is timestamped, organized chronologically, and includes metadata.

## Quick Start

```bash
# Archive all chats to default location (~/gdrive/ObsidianVault/Claude-archive)
python archive-automation.py

# Archive first 20 chats only
python archive-automation.py --max 20

# Archive to custom location  
python archive-automation.py --output ~/my-archive
```

## What You Get

- ✓ Complete chat history exported as markdown
- ✓ Chronological folder organization (YYYYMMDD_HHMMSS format)
- ✓ Extracted timestamps from chat content
- ✓ Metadata file for each chat (JSON)
- ✓ Progress tracking and reporting
- ✓ Error recovery and logging

## Prerequisites

1. **ai-chat-exporter browser extension** - [Get it here](https://www.ai-chat-exporter.net/)
   - Install in Chrome, Firefox, Edge, or Brave
   - Ensure it's enabled and logged into Claude.ai

2. **browser-harness** - Already included in Claude Code

3. **Python 3.8+** - Already on most systems

## How It Works

The skill:
1. Connects to your running browser
2. Navigates to Claude.ai/recents
3. Extracts list of all your chats
4. For each chat:
   - Opens it
   - Triggers the ai-chat-exporter extension
   - Captures the markdown export
   - Extracts timestamp information
   - Saves to timestamped folder with metadata
5. Reports progress every 5 chats

**Total time**: ~30 seconds per chat (varies with network/browser)

## Example Output

```
Claude-archive/
├── 20260701_094600_Third_grade_Pokemon_selection/
│   ├── conversation.md
│   └── metadata.json
├── 20260629_143000_Organizing_disparate_projects/
│   ├── conversation.md
│   └── metadata.json
├── 20260625_082300_Walmart_cart_integration_bug/
│   ├── conversation.md
│   ├── metadata.json
│   └── artifacts/
│       └── screenshot.png
└── undated_chat_without_timestamp/
    ├── conversation.md
    └── metadata.json
```

## Configuration

### Output Directory

Default: `~/gdrive/ObsidianVault/Claude-archive`

Change via `--output`:
```bash
python archive-automation.py --output ~/Downloads/my-chats
```

### Limit Number of Chats

Default: All chats

Limit via `--max`:
```bash
python archive-automation.py --max 50
```

### Resume or Incremental

Future version will support:
```bash
# Process only new chats since last run
python archive-automation.py --incremental

# Resume interrupted archive
python archive-automation.py --resume
```

## Advanced: Extracting Artifacts

The current version captures text content. Future versions will:
- Download PDF artifacts
- Save images and code snippets
- Organize in `artifacts/` subfolder per chat

## Customization

### Custom Timestamp Patterns

Edit `archive-automation.py` to add patterns for timestamps not in ISO 8601 format:

```python
def extract_timestamp(self, markdown):
    # Your custom timestamp extraction logic
    # Return datetime object or None
    pass
```

### Filter Chats

Add filtering logic:

```python
def process_chat(self, chat):
    # Skip chats with certain titles
    if "Draft" in chat['title']:
        return True  # Skip
    
    return super().process_chat(chat)
```

### Post-processing Hooks

Add custom processing after export:

```python
def on_chat_exported(self, folder, metadata):
    # Create index, sync to cloud, etc.
    pass
```

## Troubleshooting

### "Could not connect to browser"

The script tries to connect to an already-running browser. Ensure:
- Chrome/Firefox/Edge is open with Claude.ai loaded
- Or the script will launch a new browser instance

### "Extension not triggering"

- Verify ai-chat-exporter is installed: Visit your extensions page
- Test manually: Open a chat, click SELECT and EXPORT buttons
- Check browser console for errors: F12 → Console tab

### "No chats found"

- Confirm you're logged into Claude.ai
- Confirm chats are visible in https://claude.ai/recents
- Try in incognito/private mode to rule out extension conflicts

### "Timestamps not extracting"

Some chats may not have timestamps. They'll go to `undated_` folders.
To add custom timestamp patterns, edit `extract_timestamp()` method.

### "Files not saving"

- Check output directory is writable: `ls -ld /path/to/archive`
- Ensure sufficient disk space
- Try a temp directory first: `python archive-automation.py --output /tmp/test`

## Performance Tips

- **Faster on better hardware**: Close other apps
- **Faster on stable network**: WiFi tends to be more stable
- **Run at off-peak times**: Browser extensions are less laggy during low usage
- **Batch processing**: Process in chunks of 20-50, then merge results

Example: Process in 3 batches of 50
```bash
python archive-automation.py --max 50 --output ~/archive-batch-1
python archive-automation.py --max 50 --skip 50 --output ~/archive-batch-2
python archive-automation.py --max 50 --skip 100 --output ~/archive-batch-3
```

## What Gets Saved

### For Each Chat:

**conversation.md** - Full chat export with:
- All user messages
- All assistant responses
- Timestamps when available
- Formatted markdown

**metadata.json** - Chat information:
```json
{
  "title": "Chat title",
  "chat_id": "UUID",
  "url": "https://claude.ai/chat/...",
  "exported_at": "2026-07-01T21:30:00",
  "extracted_timestamp": "2026-06-29T14:30:00",
  "content_length": 5250
}
```

### Top-Level Archive:

- Chronologically sorted folders (YYYYMMDD_HHMMSS_title)
- All chats from oldest to newest
- Undated chats grouped at bottom

## Privacy

- All processing happens locally on your machine
- No cloud uploads
- No tracking or analytics
- Uses your existing Claude.ai session
- ai-chat-exporter is open-source - [review it here](https://github.com/theodo/ai-chat-exporter)

## Next Steps

After archiving:

1. **Explore your history**: Browse the Claude-archive folder
2. **Search**: Use grep/ripgrep to find specific topics
3. **Analyze**: Import metadata.json into a spreadsheet for stats
4. **Backup**: Copy to cloud storage or external drive
5. **Index**: Create a searchable index with tools like [meilisearch](https://www.meilisearch.com/)

## Creating a Searchable Index

```bash
# Create a file listing all chats
find Claude-archive -name metadata.json | while read f; do
  echo "=== $(dirname $f) ==="
  jq '.title' "$f"
done > Claude-archive-index.txt

# Or create a CSV for spreadsheet import
find Claude-archive -name metadata.json | while read f; do
  jq -r '[.title, .extracted_timestamp, .chat_id] | @csv' "$f"
done > Claude-archive-index.csv
```

## Feedback & Contributions

- Found a bug? Include: OS, Python version, browser, error output
- Have an idea? Describe the use case and expected behavior
- Want to contribute? Check CONTRIBUTING.md

## See Also

- [ai-chat-exporter](https://www.ai-chat-exporter.net/) - The browser extension this tool uses
- [Claude Code Docs](https://claude.com/code) - Claude Code documentation
- [jq](https://stedolan.github.io/jq/) - Useful for parsing metadata.json files

---

**Created for Claude.ai users** | MIT License
