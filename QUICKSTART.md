# Quick Start: Claude.ai Archive Automation

## 1-Minute Setup

```bash
# Go to the skill directory
cd ~/dev/claude-archive-skill

# Run the automation (will process all your chats)
python archive-automation.py
```

That's it! Your chats will be exported to:
```
~/gdrive/ObsidianVault/Claude-archive/
```

## What Happens

The script will:
1. ✓ Connect to your browser
2. ✓ Load Claude.ai and find all your chats
3. ✓ Export each one via the ai-chat-exporter extension
4. ✓ Save as markdown in chronologically-named folders
5. ✓ Extract timestamps and organize them
6. ✓ Create metadata.json for each chat

Progress updates every 5 chats processed.

## Output Example

After running, you'll have a structure like:

```
Claude-archive/
├── 20260701_094600_Third_grade_Pokemon_selection/
│   ├── conversation.md       ← Full chat export
│   └── metadata.json         ← Chat info & timestamp
├── 20260629_143000_Organizing_disparate_projects/
│   ├── conversation.md
│   └── metadata.json
├── 20260625_114500_Something_else/
│   ├── conversation.md
│   └── metadata.json
└── ... (more chats)
```

**Folders are automatically sorted chronologically!**

## Common Commands

```bash
# Archive only first 10 chats (for testing)
python archive-automation.py --max 10

# Archive to different location
python archive-automation.py --output ~/Downloads/my-archive

# Both options
python archive-automation.py --max 20 --output /tmp/test-archive
```

## Troubleshooting

### "browser-harness command not found"
- Restart Claude Code
- Or run from the directory: `cd ~/dev/claude-archive-skill && python archive-automation.py`

### "No chats found"
- Make sure you're logged into Claude.ai
- Open https://claude.ai/recents in your browser first
- Check that you actually have chats there

### Extension not triggering
- Verify ai-chat-exporter is installed: https://www.ai-chat-exporter.net/
- Test it manually once on one chat to confirm it works

## Next Steps

After archiving:

### 1. Explore Your History
```bash
# Count how many chats you have
ls -1 ~/gdrive/ObsidianVault/Claude-archive | wc -l

# See the oldest chat
ls -1 ~/gdrive/ObsidianVault/Claude-archive | head -1

# See the newest chat
ls -1 ~/gdrive/ObsidianVault/Claude-archive | tail -1
```

### 2. Search Your Chats
```bash
# Find all chats about "Pokemon"
grep -r "Pokemon" ~/gdrive/ObsidianVault/Claude-archive

# Find chats from specific date
ls ~/gdrive/ObsidianVault/Claude-archive/202606*
```

### 3. Create an Index
```bash
# List all chat titles
find ~/gdrive/ObsidianVault/Claude-archive -name metadata.json | \
  xargs grep '"title"' | \
  cut -d: -f2 | \
  sort > ~/my-claude-index.txt
```

### 4. Analyze Your Archive
```bash
# See stats
echo "Total chats: $(ls -1 ~/gdrive/ObsidianVault/Claude-archive | wc -l)"
echo "Total words: $(find ~/gdrive/ObsidianVault/Claude-archive -name conversation.md -exec wc -w {} + | tail -1 | awk '{print $1}')"
echo "Total files: $(find ~/gdrive/ObsidianVault/Claude-archive -type f | wc -l)"
```

## Features You're Getting

- ✓ **Chronological Organization**: Folders sorted by date
- ✓ **Automatic Timestamps**: Extracted from chat content
- ✓ **Metadata**: Each chat has title, ID, URL, export date
- ✓ **Full Chat Text**: All conversations preserved as markdown
- ✓ **Progress Tracking**: Updates every 5 chats
- ✓ **Error Handling**: Continues if one chat fails
- ✓ **Local Processing**: Everything stays on your machine

## Future Enhancements

The skill is designed to be extensible. Planned additions:

- [ ] Artifact extraction (PDFs, images)
- [ ] Full-text search index
- [ ] Duplicate detection
- [ ] Topic clustering
- [ ] Sentiment analysis
- [ ] Word cloud generation
- [ ] Integration with Obsidian

## File Structure

Inside the skill directory:

```
claude-archive-skill/
├── archive-automation.py    ← Main script you run
├── SKILL.md                 ← Claude Code documentation
├── README.md                ← Full documentation
├── QUICKSTART.md            ← This file
└── (future: tests, config, etc.)
```

## Performance

- ~30 seconds per chat (including page load & export)
- ~2 chats per minute
- 100 chats = ~50 minutes
- 500 chats = ~4 hours

**Pro tip**: Run overnight for large archives!

## Support

### If something breaks:

1. **Error in script**: Check Python version: `python --version` (need 3.8+)
2. **Browser issues**: Close all browsers, restart once
3. **Extension issues**: Verify at https://www.ai-chat-exporter.net/
4. **Path issues**: Use absolute paths: `python /full/path/archive-automation.py`

### Getting help:

- Check the main [README.md](README.md) for detailed troubleshooting
- Review [SKILL.md](SKILL.md) for technical details
- Check browser console (F12) for errors

## Privacy Reminder

- ✓ All processing is local
- ✓ No uploads to any server
- ✓ All files stay in your archive directory
- ✓ ai-chat-exporter is open source

## Tips & Tricks

**Backup before archiving**: Important chats? Keep a backup first.

**Test run**: Try `--max 5` first to see if it works:
```bash
python archive-automation.py --max 5
```

**Schedule it**: Run via cron for periodic updates:
```bash
0 2 * * * cd ~/dev/claude-archive-skill && python archive-automation.py >> ~/archive.log 2>&1
```

**Version control**: Your archive folder works great with git:
```bash
cd ~/gdrive/ObsidianVault/Claude-archive
git init
git add .
git commit -m "Initial Claude archive export"
```

---

**Ready to archive?** Run it now:
```bash
python ~/dev/claude-archive-skill/archive-automation.py
```

Questions? See the full docs in [README.md](README.md)
