#!/usr/bin/env python3
"""
Memory Manager for AI-Generated Blog Posts

Provides persistent memory across blog generations to:
- Prevent duplicate content (SHA256 fingerprinting)
- Track used jokes/phrases (cooldown system)
- Maintain consistent tone (persona tracking)
- Build context for AI prompts
"""

import json
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
MEMORY_DIR = PROJECT_ROOT / "data" / "memory"
POSTS_DIR = PROJECT_ROOT / "docs" / "_posts"

# Ensure memory directory exists
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class BlogMemory:
    """Manages persistent memory for a blog workflow"""
    
    def __init__(self, workflow_name: str):
        """
        Initialize memory for a specific workflow
        
        Args:
            workflow_name: 'ollama-pulse' or 'ai-research-daily'
        """
        self.workflow_name = workflow_name
        self.memory_file = MEMORY_DIR / f"{workflow_name}_memory.json"
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load memory from JSON file"""
        if not self.memory_file.exists():
            return {
                "workflow": self.workflow_name,
                "last_run": None,
                "post_history": []
            }
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading memory: {e}")
            return {
                "workflow": self.workflow_name,
                "last_run": None,
                "post_history": []
            }
    
    def _save_memory(self):
        """Save memory to JSON file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, indent=2, fp=f)
            print(f"✅ Memory saved for {self.workflow_name}")
        except Exception as e:
            print(f"⚠️  Error saving memory: {e}")
    
    @staticmethod
    def fingerprint(text: str) -> str:
        """Generate SHA256 fingerprint of content"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def is_duplicate(self, content: str) -> bool:
        """
        Check if content is a duplicate of recent posts
        
        Args:
            content: Markdown content to check
            
        Returns:
            True if duplicate, False otherwise
        """
        fp = self.fingerprint(content)
        
        # Check last 7 posts
        recent = self.memory["post_history"][-7:]
        for entry in recent:
            if entry.get("content_fingerprint") == fp:
                print(f"⚠️  Duplicate content detected (matches {entry['date']})")
                return True
        
        return False
    
    def extract_tone_words(self, content: str) -> List[str]:
        """
        Extract tone indicators from content
        
        Args:
            content: Markdown content
            
        Returns:
            List of tone words
        """
        tone_indicators = {
            'technical', 'forward-looking', 'optimistic', 'analytical',
            'community', 'helpful', 'neutral', 'excited', 'cautious',
            'breakthrough', 'incremental', 'controversial', 'pedagogical',
            'rigorous', 'measured', 'curious', 'energetic', 'grounded',
            'inquisitive', 'reflective', 'balanced', 'insightful'
        }
        
        # Extract words from content
        words = set(re.findall(r'\b\w+\b', content.lower()))
        
        # Find matching tone indicators
        found_tones = list(words & tone_indicators)
        
        # If none found, infer from persona markers
        if not found_tones:
            if '💡' in content or 'hype' in content.lower():
                found_tones.append('energetic')
            elif '🛠️' in content or 'fix' in content.lower():
                found_tones.append('grounded')
            elif '🤔' in content or 'curious' in content.lower():
                found_tones.append('inquisitive')
            elif '📈' in content or 'trend' in content.lower():
                found_tones.append('reflective')
            elif '📚' in content or 'scholar' in content.lower():
                found_tones.append('pedagogical')
        
        return found_tones[:5]  # Limit to 5
    
    def extract_jokes_phrases(self, content: str) -> List[str]:
        """
        Extract memorable jokes/phrases from content
        
        Args:
            content: Markdown content
            
        Returns:
            List of joke/phrase identifiers
        """
        jokes = []
        
        # Common joke patterns
        patterns = [
            r'(?:LLM|GPU|AI|ML)[-\s](?:latté|golf|hype|brew|magic)',
            r'byte[-\s]brew',
            r'neural[-\s]network[-\s](?:ninja|wizard)',
            r'tensor[-\s](?:time|trouble)',
            r'gradient[-\s]descent[-\s](?:into|madness)',
            r'overfitting[-\s](?:to|the)',
            r'(?:my|your)[-\s]\d+[-\s]year[-\s]old',
            r'plot[-\s]twist',
            r'spoiler[-\s]alert',
            r'mic[-\s]drop',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            jokes.extend([m.lower().replace(' ', '-') for m in matches])
        
        # Extract quoted phrases (potential jokes)
        quoted = re.findall(r'"([^"]{10,50})"', content)
        for quote in quoted:
            if any(word in quote.lower() for word in ['llm', 'ai', 'model', 'gpu', 'neural']):
                # Create identifier from first 3 words
                words = quote.split()[:3]
                jokes.append('-'.join(words).lower())
        
        return list(set(jokes))[:10]  # Limit to 10, unique
    
    def get_joke_blacklist(self, cooldown_days: int = 7) -> Set[str]:
        """
        Get jokes that should not be reused (within cooldown period)
        
        Args:
            cooldown_days: Number of days to blacklist jokes
            
        Returns:
            Set of joke identifiers to avoid
        """
        cutoff = datetime.now() - timedelta(days=cooldown_days)
        blacklist = set()
        
        for entry in self.memory["post_history"]:
            try:
                post_date = datetime.fromisoformat(entry["date"])
                if post_date >= cutoff:
                    blacklist.update(entry.get("used_jokes", []))
            except (ValueError, KeyError):
                continue
        
        return blacklist
    
    def get_context_summary(self, max_entries: int = 5) -> str:
        """
        Generate context summary for AI prompt
        
        Args:
            max_entries: Maximum number of recent posts to include
            
        Returns:
            Formatted context string
        """
        recent = self.memory["post_history"][-max_entries:]
        
        if not recent:
            return "No prior context available."
        
        lines = ["**Recent Post History:**\n"]
        for entry in recent:
            tone = ', '.join(entry.get('tone_words', ['neutral']))
            jokes = entry.get('used_jokes', [])
            joke_str = f" | Jokes: {', '.join(jokes[:3])}" if jokes else ""
            lines.append(f"- {entry['date']}: {tone} tone{joke_str}")
        
        # Add joke blacklist
        blacklist = self.get_joke_blacklist()
        if blacklist:
            lines.append(f"\n**Avoid These Recent Jokes/Phrases:**")
            lines.append(f"{', '.join(list(blacklist)[:10])}")
        
        return '\n'.join(lines)
    
    def add_post(self, date: str, title_slug: str, content: str):
        """
        Add a new post to memory
        
        Args:
            date: Post date (YYYY-MM-DD)
            title_slug: URL-friendly title
            content: Full markdown content
        """
        entry = {
            "date": date,
            "title_slug": title_slug,
            "tone_words": self.extract_tone_words(content),
            "used_jokes": self.extract_jokes_phrases(content),
            "content_fingerprint": self.fingerprint(content)
        }
        
        self.memory["post_history"].append(entry)
        self.memory["last_run"] = datetime.now().isoformat()
        
        # Keep only last 30 entries (save space)
        self.memory["post_history"] = self.memory["post_history"][-30:]
        
        self._save_memory()
        
        print(f"✅ Added post to memory: {date} ({len(entry['tone_words'])} tones, {len(entry['used_jokes'])} jokes)")
    
    def should_post(self, content: str) -> Tuple[bool, str]:
        """
        Determine if content should be posted
        
        Args:
            content: Markdown content to check
            
        Returns:
            (should_post, reason)
        """
        # Check for duplicate
        if self.is_duplicate(content):
            return False, "Duplicate content detected"
        
        # Check if already posted today
        today = datetime.now().strftime("%Y-%m-%d")
        for entry in self.memory["post_history"][-3:]:  # Check last 3
            if entry["date"] == today:
                return False, f"Already posted today ({today})"
        
        return True, "Content is unique and ready to post"


def main():
    """Test the memory manager"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python memory_manager.py <workflow-name>")
        print("  workflow-name: 'ollama-pulse' or 'ai-research-daily'")
        sys.exit(1)
    
    workflow = sys.argv[1]
    memory = BlogMemory(workflow)
    
    print(f"\n📊 Memory Status for {workflow}")
    print(f"Total posts in memory: {len(memory.memory['post_history'])}")
    print(f"Last run: {memory.memory.get('last_run', 'Never')}")
    print(f"\n{memory.get_context_summary()}")
    
    # Show joke blacklist
    blacklist = memory.get_joke_blacklist()
    if blacklist:
        print(f"\n🚫 Joke Blacklist ({len(blacklist)} items):")
        for joke in list(blacklist)[:10]:
            print(f"  - {joke}")


if __name__ == "__main__":
    main()

