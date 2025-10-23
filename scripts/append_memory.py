#!/usr/bin/env python3
"""
Memory Updater - Records a successful blog post in memory

Updates the memory JSON with:
- Post date
- Title slug
- Tone words (extracted from content)
- Used jokes/phrases (extracted from content)
- Content fingerprint (SHA256)

Usage:
    python append_memory.py <workflow-name> <date> <title-slug> <markdown-file>

Example:
    python append_memory.py ollama-pulse 2025-10-23 new-cloud-models docs/_posts/2025-10-23-ollama-pulse.md
"""

import sys
from pathlib import Path
from memory_manager import BlogMemory


def main():
    if len(sys.argv) != 5:
        print("Usage: python append_memory.py <workflow-name> <date> <title-slug> <markdown-file>")
        print("\nArguments:")
        print("  workflow-name: 'ollama-pulse' or 'ai-research-daily'")
        print("  date: Post date (YYYY-MM-DD)")
        print("  title-slug: URL-friendly title")
        print("  markdown-file: Path to published markdown")
        print("\nExample:")
        print("  python append_memory.py ollama-pulse 2025-10-23 new-cloud-models docs/_posts/2025-10-23-ollama-pulse.md")
        sys.exit(1)
    
    workflow = sys.argv[1]
    date = sys.argv[2]
    title_slug = sys.argv[3]
    md_file = Path(sys.argv[4])
    
    # Check file exists
    if not md_file.exists():
        print(f"❌ File not found: {md_file}")
        sys.exit(1)
    
    # Load content
    try:
        content = md_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    # Update memory
    memory = BlogMemory(workflow)
    memory.add_post(date, title_slug, content)
    
    print(f"\n✅ Memory updated successfully!")
    print(f"\n📊 Current Memory Status:")
    print(f"Total posts: {len(memory.memory['post_history'])}")
    print(f"Last run: {memory.memory['last_run']}")
    
    # Show recent context
    print(f"\n{memory.get_context_summary(max_entries=3)}")


if __name__ == "__main__":
    main()

