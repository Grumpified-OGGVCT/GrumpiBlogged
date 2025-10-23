#!/usr/bin/env python3
"""
Content Guard - Determines if a blog post should be published

Checks:
1. Content fingerprint (prevent duplicates)
2. Already posted today (prevent double-posting)
3. Content quality (basic validation)

Usage:
    python should_post.py <markdown-file> <workflow-name>

Exit codes:
    0 = Should post
    1 = Should NOT post
"""

import sys
from pathlib import Path
from memory_manager import BlogMemory


def validate_content(content: str) -> tuple[bool, str]:
    """
    Basic content validation
    
    Args:
        content: Markdown content
        
    Returns:
        (is_valid, reason)
    """
    # Check minimum length
    if len(content) < 500:
        return False, "Content too short (< 500 chars)"
    
    # Check for required sections
    required_markers = ['##', '---']  # Headers and front matter
    if not all(marker in content for marker in required_markers):
        return False, "Missing required sections (headers/front matter)"
    
    # Check for placeholder text
    placeholders = ['TODO', 'FIXME', '[INSERT', 'PLACEHOLDER']
    for placeholder in placeholders:
        if placeholder in content.upper():
            return False, f"Contains placeholder: {placeholder}"
    
    return True, "Content is valid"


def main():
    if len(sys.argv) != 3:
        print("Usage: python should_post.py <markdown-file> <workflow-name>")
        print("  markdown-file: Path to generated markdown")
        print("  workflow-name: 'ollama-pulse' or 'ai-research-daily'")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    workflow = sys.argv[2]
    
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
    
    # Validate content
    is_valid, reason = validate_content(content)
    if not is_valid:
        print(f"❌ Content validation failed: {reason}")
        sys.exit(1)
    
    # Check memory
    memory = BlogMemory(workflow)
    should_post, reason = memory.should_post(content)
    
    if should_post:
        print(f"✅ SHOULD POST: {reason}")
        print(f"\n📊 Memory Context:")
        print(memory.get_context_summary())
        sys.exit(0)
    else:
        print(f"⛔ SHOULD NOT POST: {reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()

