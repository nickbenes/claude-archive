#!/usr/bin/env python3
"""
Claude.ai Chat Archive Automation
Full end-to-end automation using browser-harness
"""

import json
import re
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import subprocess
import sys


class ClaudeArchiveBot:
    def __init__(self, archive_root: Path):
        self.archive_root = Path(archive_root)
        self.archive_root.mkdir(parents=True, exist_ok=True)
        self.processed = 0
        self.successful = 0
        self.failed = 0
        self.chats: List[Dict] = []

    def log(self, msg: str, level: str = "INFO"):
        """Log message with timestamp"""
        ts = datetime.now().strftime("%H:%M:%S")
        icons = {"✓": "✓", "✗": "✗", "⚠": "⚠", "•": "•"}
        icon = icons.get(level[0], "•")
        print(f"[{ts}] {icon} {msg}")

    def run_browser_harness(self, python_code: str) -> Optional[str]:
        """Execute Python code in browser-harness context"""
        try:
            result = subprocess.run(
                ["browser-harness"],
                input=python_code,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                self.log(f"Browser harness error: {result.stderr}", "✗")
                return None
        except Exception as e:
            self.log(f"Failed to run browser harness: {e}", "✗")
            return None

    def get_all_chats(self) -> List[Dict]:
        """Fetch all chats from recents page"""
        self.log("Fetching all chats from Claude.ai...", "•")

        code = """
import json

# Navigate to recents
goto_url("https://claude.ai/recents")
wait_for_load()

# Extract all chat links
chats = js('''
const chats = [];
const links = document.querySelectorAll('a[href*="/chat/"]');
links.forEach(link => {
    const href = link.getAttribute('href');
    const id = href.split('/chat/')[1];
    const title = link.textContent.trim();
    if (id && title) {
        chats.push({
            id: id,
            title: title,
            url: "https://claude.ai/chat/" + id
        });
    }
});
return JSON.stringify(chats);
''')

print(chats)
"""

        output = self.run_browser_harness(code)
        if output:
            try:
                self.chats = json.loads(output)
                self.log(f"Found {len(self.chats)} chats", "✓")
                return self.chats
            except json.JSONDecodeError:
                self.log(f"Could not parse chat list JSON", "✗")
                return []
        return []

    def sanitize_name(self, name: str, max_len: int = 100) -> str:
        """Sanitize folder name"""
        # Remove bad characters
        name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
        # Replace spaces with underscores
        name = re.sub(r'\s+', '_', name.strip())
        # Remove trailing special chars
        name = name.rstrip('._- ')
        # Limit length
        return (name[:max_len] if name else 'untitled')

    def extract_timestamp(self, markdown: str) -> Optional[datetime]:
        """Extract first timestamp found in markdown"""
        if not markdown:
            return None

        # ISO format
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})', markdown)
        if match:
            try:
                return datetime(
                    int(match.group(1)), int(match.group(2)), int(match.group(3)),
                    int(match.group(4)), int(match.group(5)), int(match.group(6))
                )
            except ValueError:
                pass
        return None

    def export_chat(self, chat: Dict) -> Optional[str]:
        """
        Export single chat using the browser.
        Returns markdown content.
        """
        chat_id = chat['id']

        # Use simpler JavaScript without complex escaping
        code = f"""
goto_url("https://claude.ai/chat/{chat_id}")
import time
time.sleep(3)

try:
    # Get page text content
    text = js("document.body.innerText")
    if text and len(text) > 50:
        print(text)
    else:
        print("No content")
except Exception as e:
    print(f"Error: {{str(e)[:100]}}")
"""

        output = self.run_browser_harness(code)
        return output if output else None

    def process_chat(self, chat: Dict) -> bool:
        """Process and save single chat"""
        self.processed += 1
        self.log(f"[{self.processed}/{len(self.chats)}] Exporting: {chat['title']}", "•")

        try:
            # Export the chat
            markdown = self.export_chat(chat)

            if not markdown or len(markdown) < 20:
                self.log(f"  Failed to export", "✗")
                self.failed += 1
                return False

            # Extract timestamp
            timestamp = self.extract_timestamp(markdown)

            # Create folder
            safe_title = self.sanitize_name(chat['title'], 80)

            if timestamp:
                folder_name = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{safe_title}"
            else:
                folder_name = f"undated_{safe_title}"

            session_dir = self.archive_root / folder_name
            session_dir.mkdir(parents=True, exist_ok=True)

            # Save markdown
            (session_dir / "conversation.md").write_text(markdown, encoding='utf-8')

            # Save metadata
            metadata = {
                "title": chat['title'],
                "chat_id": chat['id'],
                "url": chat['url'],
                "exported_at": datetime.now().isoformat(),
                "extracted_timestamp": timestamp.isoformat() if timestamp else None,
                "content_length": len(markdown)
            }
            (session_dir / "metadata.json").write_text(
                json.dumps(metadata, indent=2, default=str),
                encoding='utf-8'
            )

            self.log(f"  ✓ Saved to: {folder_name}", "✓")
            self.successful += 1
            return True

        except Exception as e:
            self.log(f"  Error: {e}", "✗")
            self.failed += 1
            return False

    def run(self, max_chats: Optional[int] = None):
        """Execute full archive workflow"""
        print("\n" + "="*70)
        print("  Claude.ai Chat Archive Automation")
        print("="*70 + "\n")

        # Get all chats
        self.get_all_chats()

        if not self.chats:
            self.log("No chats found!", "✗")
            return

        # Limit chats if needed
        chats_to_process = self.chats[:max_chats] if max_chats else self.chats

        self.log(f"Processing {len(chats_to_process)} chats...\n", "•")

        # Process each chat
        for i, chat in enumerate(chats_to_process):
            self.process_chat(chat)

            # Progress update every 5 chats
            if (self.processed % 5) == 0 and self.processed > 0:
                print("\n" + "="*70)
                self.log(f"Progress: {self.processed}/{len(chats_to_process)}", "•")
                self.log(f"Successful: {self.successful} | Failed: {self.failed}", "•")
                print("="*70 + "\n")

            # Small delay
            time.sleep(0.5)

        # Final report
        print("\n" + "="*70)
        self.log(f"Archive Complete!", "✓")
        self.log(f"Total processed: {self.processed}", "✓")
        self.log(f"Successful: {self.successful}", "✓")
        self.log(f"Failed: {self.failed}", "✓" if self.failed == 0 else "✗")
        self.log(f"Archive location: {self.archive_root}", "✓")
        print("="*70 + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automate Claude.ai chat archiving"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home() / "gdrive" / "ObsidianVault" / "Claude-archive",
        help="Archive output directory"
    )
    parser.add_argument(
        "--max",
        type=int,
        default=None,
        help="Maximum chats to process"
    )

    args = parser.parse_args()

    bot = ClaudeArchiveBot(args.output)
    bot.run(max_chats=args.max)


if __name__ == "__main__":
    main()
