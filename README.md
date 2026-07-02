# Claude.ai Chat Archive Skill

Automate exporting and organizing all your Claude.ai chat history with proper timestamps and folder structure.

## What This Does

- **Discovers** all chats from your Claude.ai account
- **Exports** each chat as markdown using the ai-chat-exporter extension
- **Extracts** timestamps automatically
- **Organizes** chats chronologically into folders
- **Creates** metadata for each chat (title, date, URL)
- **Reports** progress every 5 chats

## Prerequisites

### Required
1. **ai-chat-exporter extension**: [Install here](https://www.ai-chat-exporter.net/)
2. **browser-harness**: Pre-installed in Claude Code
3. **Python 3.8+**: For the automation script

### Optional
- **Playwright**: For advanced browser automation
  ```bash
  pip install playwright
  playwright install chromium
  ```

## Installation

```bash
# Clone or copy the skill
cp -r claude-archive-skill ~/.claude/skills/claude-archive/

# Make scripts executable
chmod +x ~/.claude/skills/claude-archive/*.py
```

## Usage

### Method 1: Direct Python Script (Recommended)

```bash
# Basic usage - archives all chats
python ~/gdrive/ObsidianVault/archive-automation.py

# Limit to first 20 chats
python ~/gdrive/ObsidianVault/archive-automation.py --max 20

# Custom output directory
python ~/gdrive/ObsidianVault/archive-automation.py \
  --output ~/Downloads/my-claude-archive
```

### Method 2: Claude Code Integration

```
/claude-archive
```

Or use the skill directly in Claude Code for seamless integration.

## Output Structure

```
Claude-archive/
├── 20260701_094600_Third_grade_Pokemon_selection/
│   ├── conversation.md          # Full chat export
│   └── metadata.json            # Chat metadata
├── 20260629_143000_Organizing_disparate_projects/
│   ├── conversation.md
│   └── metadata.json
└── undated_Some_other_chat/
    ├── conversation.md
    └── metadata.json
```

### Folder Naming

- **Timestamped**: `YYYYMMDD_HHMMSS_Title` (if timestamp found in chat)
- **Undated**: `undated_Title` (if no timestamp in content)
- Titles are sanitized (spaces → underscores, special chars removed)
- Chronologically sortable (older chats first)

## Metadata Format

Each chat folder contains `metadata.json`:

```json
{
  "title": "Chat title as shown in Claude.ai",
  "chat_id": "unique-chat-uuid",
  "url": "https://claude.ai/chat/...",
  "exported_at": "2026-07-01T21:30:00.123456",
  "extracted_timestamp": "2026-06-29T14:30:00",
  "content_length": 5250
}
```

## How It Works

### Automation Flow

1. **Browser Setup**: Connects to running browser or launches new instance
2. **Chat Discovery**: Loads Claude.ai/recents and extracts all chat links
3. **Chat Export**:
   - Opens each chat
   - Waits for content to load
   - Exports via ai-chat-exporter extension
   - Captures markdown output
4. **Timestamp Extraction**: Finds timestamps in chat content (ISO 8601 format)
5. **Organization**: Creates chronologically-named folders and saves metadata
6. **Reporting**: Updates progress every 5 chats processed

### Browser Extension Integration

The tool works with the **ai-chat-exporter** extension by:
- Navigating to each chat URL
- Triggering the SELECT and EXPORT buttons via JavaScript
- Capturing the clipboard or download output
- Processing the markdown markdown for organization

## Performance

- **Speed**: ~30 seconds per chat (includes page load, export, file processing)
- **Throughput**: ~2 chats per minute
- **Example**: 100 chats = ~50 minutes

## Troubleshooting

### Extension not triggering
- Ensure ai-chat-exporter is installed and enabled
- Try manual export on one chat to verify it works
- Check browser console for errors

### Browser connection issues
- Kill existing browser processes: `pkill -f chromium; pkill -f firefox`
- Try the `--headless` flag to run browser in headless mode

### Files not downloading
- Check your Downloads folder for .md files
- Verify browser download settings aren't blocking .md files
- Try running with verbose logging

### Timestamps not extracting
- Add custom timestamp patterns to `extract_timestamp()` method
- Some chats may not have timestamps (will be in 'undated' folder)

## Advanced Usage

### Custom Archive Rules

Edit `archive-automation.py` to add custom processing:

```python
class CustomArchiver(ClaudeArchiveBot):
    def process_chat(self, chat):
        # Add custom logic here
        # Filter by title, process artifacts, etc.
        return super().process_chat(chat)
```

### Artifact Handling

Future versions will include automatic artifact extraction:
- Download PDFs, images, and other files
- Organize in `artifacts/` subfolder
- Link them in the markdown export

### Incremental Updates

```bash
# Process only new chats
python archive-automation.py --incremental

# Resume interrupted archive
python archive-automation.py --resume /path/to/archive
```

## Creating a Shareable Skill

To turn this into a Claude Code skill:

1. **Package**: Create a `.tar.gz` with all required files
2. **Manifest**: Add skill metadata (`skill.json`)
3. **Documentation**: Include comprehensive README (this file)
4. **Tests**: Add example usage and validation
5. **Share**: Submit to Claude Code skill registry

See the skill contributor guide for details.

## Privacy & Security

- **Local Processing**: All data is processed locally on your machine
- **No Cloud Uploads**: Archive stays in your specified directory
- **Authentication**: Uses your existing Claude.ai session
- **Browser Extension**: ai-chat-exporter is open source - verify before use

## Contributing

Found a bug or have a feature request?

- Report issues with:
  - Python version and OS
  - Browser version
  - ai-chat-exporter version
  - Full error output

- Contributions welcome:
  - Better timestamp extraction
  - Artifact handling
  - Performance optimizations
  - Documentation improvements

## License

MIT License - Use freely, modify, share, and contribute back.

---

**Made for the Claude community** | [ai-chat-exporter](https://www.ai-chat-exporter.net/) | [Claude Code Docs](https://claude.com/code)
