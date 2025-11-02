#!/usr/bin/env python3
"""
GrumpiBlogged - Idea Vault Blog Post Generator
"The Innovator" - Where tech ideation meets practical AI analysis

Persona: The Visionary Thinker 💡
- Forward-thinking: Always looking at what's next and what's possible
- Creative: Combines ideas in novel ways
- Practical dreamer: Balances vision with implementation reality
- Thought-provoking: Asks questions that challenge assumptions
- Connective: Links disparate concepts into cohesive narratives
- Inspiring: Motivates readers to think bigger

Voice Characteristics:
- Enthusiastic but grounded in reality
- "Imagine if...", "What if we could...", "The future where..."
- Explores possibilities while acknowledging constraints
- Bridges ideation and execution
"""
import json
import os
import sys
from datetime import datetime
import pytz
from pathlib import Path
import random
import requests
import base64

# Import memory system
from memory_manager import BlogMemory

# Import AI editing system
from ai_editor import AIEditor

# Import Report Translator
from report_translator import (
    generate_intro_hook,
    generate_metrics_snapshot,
    generate_findings_section,
    generate_patterns_analysis,
    generate_developer_framework,
    generate_priorities_watchlist
)

# Paths
IDEA_VAULT_REPO = "https://api.github.com/repos/Grumpified-OGGVCT/idea_vault"
POSTS_DIR = Path("docs/_posts")
DATA_DIR = Path("data/ideas")  # Local cache of Idea Vault data


def ensure_directories():
    """Create necessary directories if they don't exist"""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def fetch_idea_vault_data_from_github(date_override=None):
    """Fetch aggregated data from idea_vault GitHub repository
    
    Args:
        date_override: Optional date string (YYYY-MM-DD) for testing with historical data
    """
    target_date = date_override if date_override else get_today_date_str()
    
    # Try to fetch from GitHub (assuming similar structure to other repos)
    # Check both /docs and /data folders
    possible_paths = [
        f"docs/{target_date}.json",
        f"data/{target_date}.json",
        f"data/aggregated/{target_date}.json",
        f"docs/reports/{target_date}.json"
    ]
    
    aggregated = []
    insights = {}
    
    for path in possible_paths:
        try:
            url = f"{IDEA_VAULT_REPO}/contents/{path}"
            print(f"📡 Trying: {url}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.json()
                # Decode base64 content
                decoded = base64.b64decode(content['content']).decode('utf-8')
                data = json.loads(decoded)
                
                # Handle different data structures
                if isinstance(data, list):
                    aggregated = data
                elif isinstance(data, dict):
                    aggregated = data.get('ideas', data.get('items', []))
                    insights = data.get('insights', data.get('patterns', {}))
                
                print(f"✅ Loaded {len(aggregated)} items from GitHub ({path})")
                
                # Cache locally
                cache_file = DATA_DIR / f"{target_date}.json"
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump({'ideas': aggregated, 'insights': insights}, f, indent=2)
                
                break  # Found data, stop trying
                
        except Exception as e:
            print(f"⚠️  Path {path} not found: {e}")
            continue
    
    # If GitHub fetch failed, try local cache
    if not aggregated:
        print(f"📂 Trying local cache...")
        cache_file = DATA_DIR / f"{target_date}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                aggregated = cached_data.get('ideas', cached_data.get('items', []))
                insights = cached_data.get('insights', {})
            print(f"✅ Loaded {len(aggregated)} items from local cache")
    
    return aggregated, insights


def generate_visionary_opening(aggregated):
    """Generate The Visionary's opening based on ideas collected"""
    total_ideas = len(aggregated)
    
    openings = [
        f"💡 **What if we could...** Today's collection brings {total_ideas} ideas that could reshape how we think about AI and technology. Let's explore the possibilities.",
        f"💡 The future isn't written yet, and today's {total_ideas} concepts remind us why that's exciting. Let's imagine what's possible.",
        f"💡 **Vision meets execution.** {total_ideas} ideas landed today that bridge the gap between 'what if' and 'why not.' Let's dive in.",
        f"💡 Innovation starts with imagination. Today's {total_ideas} ideas span from wild dreams to practical implementations. Here's what caught my attention.",
        f"💡 The best ideas come from asking better questions. Today's {total_ideas} concepts do exactly that—they challenge us to think differently.",
    ]
    
    return random.choice(openings)


def generate_idea_commentary(entry):
    """Generate unique, visionary commentary for an idea/concept
    
    This is The Visionary's voice: forward-thinking, inspiring, practical
    """
    title = entry.get('title', 'Unknown Idea')
    summary = entry.get('summary', entry.get('description', ''))
    category = entry.get('category', 'general')
    
    # Analyze the idea
    summary_lower = summary.lower()
    
    # Identify idea characteristics
    is_automation = any(word in summary_lower for word in ['automate', 'automation', 'autonomous', 'auto-'])
    is_integration = any(word in summary_lower for word in ['integrate', 'integration', 'connect', 'combine'])
    is_efficiency = any(word in summary_lower for word in ['efficient', 'optimize', 'faster', 'streamline'])
    is_creative = any(word in summary_lower for word in ['creative', 'generate', 'create', 'design'])
    is_collaborative = any(word in summary_lower for word in ['collaborate', 'team', 'social', 'community'])
    is_accessibility = any(word in summary_lower for word in ['accessible', 'easy', 'simple', 'democratize'])
    
    # Generate commentary based on characteristics
    commentaries = []
    
    if is_automation:
        commentaries.append(f"**Automation potential**: {summary[:100]}... Imagine freeing humans from repetitive tasks to focus on creative work.")
    
    if is_integration:
        commentaries.append(f"**Integration vision**: {summary[:100]}... The power isn't in individual tools—it's in how they work together.")
    
    if is_efficiency:
        commentaries.append(f"**Efficiency multiplier**: {summary[:100]}... Time saved is time earned for innovation.")
    
    if is_creative:
        commentaries.append(f"**Creative amplification**: {summary[:100]}... Tools that enhance human creativity without replacing it.")
    
    if is_collaborative:
        commentaries.append(f"**Collaboration catalyst**: {summary[:100]}... The best innovations emerge when humans and AI work together.")
    
    if is_accessibility:
        commentaries.append(f"**Democratization driver**: {summary[:100]}... Making powerful capabilities available to everyone changes everything.")
    
    # Select and combine commentaries
    if commentaries:
        return ' '.join(commentaries[:2])
    else:
        # Fallback: generic visionary commentary
        return f"**The possibility**: {summary[:120]}... This is the kind of thinking that moves us forward."


def generate_ideas_section(aggregated):
    """Generate section about ideas with visionary analysis"""
    if not aggregated:
        return ""
    
    lines = []
    lines.append("## 💭 Today's Ideation Landscape\n\n")
    lines.append("*Curated concepts that bridge imagination and implementation.*\n\n")
    
    # Take top 5-7 most significant ideas
    top_ideas = aggregated[:7]
    
    for i, entry in enumerate(top_ideas, 1):
        title = entry.get('title', 'Unknown Idea')
        url = entry.get('url', '#')
        category = entry.get('category', 'General')
        
        lines.append(f"**{i}. {title}** ({category})")
        
        if url != '#':
            lines.append(f" — [Details]({url})")
        lines.append("\n\n")
        
        # Generate unique visionary commentary
        commentary = generate_idea_commentary(entry)
        lines.append(f"   {commentary}\n\n")
    
    return ''.join(lines)


def generate_vision_section(aggregated, insights):
    """Generate section on broader vision and future directions"""
    lines = []
    lines.append("## 🔮 The Vision Forward\n\n")
    
    lines.append("When we step back and look at today's ideas collectively, a pattern emerges: ")
    lines.append("we're not just building better tools—we're reimagining how humans and AI collaborate.\n\n")
    
    lines.append("**Key Themes**:\n\n")
    
    # Extract themes from insights or analyze aggregated ideas
    themes = insights.get('themes', [])
    if not themes and aggregated:
        # Auto-detect themes
        theme_keywords = {}
        for idea in aggregated:
            summary = idea.get('summary', idea.get('description', '')).lower()
            if 'automat' in summary:
                theme_keywords.setdefault('Automation', 0)
                theme_keywords['Automation'] += 1
            if 'creativ' in summary or 'generat' in summary:
                theme_keywords.setdefault('Creativity', 0)
                theme_keywords['Creativity'] += 1
            if 'collabor' in summary or 'team' in summary:
                theme_keywords.setdefault('Collaboration', 0)
                theme_keywords['Collaboration'] += 1
        
        themes = [{'name': k, 'count': v} for k, v in sorted(theme_keywords.items(), key=lambda x: x[1], reverse=True)]
    
    for theme in themes[:3]:
        theme_name = theme.get('name', 'Innovation') if isinstance(theme, dict) else theme
        lines.append(f"- **{theme_name}**: The future where this becomes second nature\n")
    
    lines.append("\n")
    lines.append("**What to watch**: The gap between idea and implementation is shrinking. ")
    lines.append("What seemed like science fiction last year is production-ready today. ")
    lines.append("These ideas aren't distant dreams—they're tomorrow's reality.\n\n")
    
    return ''.join(lines)


def generate_idea_vault_seo_section(aggregated):
    """Generate SEO-optimized keywords and hashtags for idea vault content"""
    # Core keywords
    keywords = ["AIIdeas", "TechInnovation", "FutureTech", "AIIdeation", "TechVision"]
    hashtags = ["#AIIdeas", "#TechInnovation", "#FutureTech", "#AIIdeation", "#TechVision"]
    
    # Analyze aggregated data for specific themes
    tech_keywords = set()
    for entry in aggregated[:10]:
        summary = (entry.get('summary', '') + ' ' + entry.get('description', '')).lower()
        
        if 'automat' in summary:
            tech_keywords.add('Automation')
            hashtags.append('#Automation')
        if 'ai' in summary:
            tech_keywords.add('ArtificialIntelligence')
            hashtags.append('#AI')
        if 'workflow' in summary:
            tech_keywords.add('Workflow')
            hashtags.append('#Workflow')
        if 'productivity' in summary:
            tech_keywords.add('Productivity')
            hashtags.append('#Productivity')
    
    keywords.extend(list(tech_keywords))
    
    # Add current year
    current_year = datetime.now().year
    keywords.append(f"Tech{current_year}")
    hashtags.append(f"#Tech{current_year}")
    
    # Add general trending hashtags
    trending_hashtags = [
        '#Innovation', '#TechTrends', '#FutureOfWork',
        '#AITools', '#TechIdeas', '#DigitalTransformation'
    ]
    hashtags.extend(trending_hashtags)
    
    # Deduplicate
    seen_kw = set()
    unique_keywords = []
    for kw in keywords:
        if kw.lower() not in seen_kw:
            seen_kw.add(kw.lower())
            unique_keywords.append(kw)
    
    seen_ht = set()
    unique_hashtags = []
    for ht in hashtags:
        if ht.lower() not in seen_ht:
            seen_ht.add(ht.lower())
            unique_hashtags.append(ht)
    
    # Limit
    unique_keywords = unique_keywords[:20]
    unique_hashtags = unique_hashtags[:25]
    
    # Format
    seo_section = "\n\n---\n\n"
    seo_section += "## 🔍 Keywords & Topics\n\n"
    seo_section += f"**Innovation Topics**: {', '.join(unique_keywords)}\n\n"
    seo_section += f"**Hashtags**: {' '.join(unique_hashtags)}\n\n"
    seo_section += "*These keywords help you discover related ideas and connect with the innovation community.*\n"
    
    return seo_section


def generate_idea_vault_support_section():
    """Generate support/donation section for Idea Vault posts"""
    section = """## 💰 Support The Innovator

If these daily ideas inspire your own projects, consider supporting:

### ☕ Ko-fi (Fiat/Card)

**[💝 Tip on Ko-fi](https://ko-fi.com/grumpified)** | Scan QR Code Below

<a href="https://ko-fi.com/grumpified"><img src="../assets/KofiTipQR_Code_GrumpiFied.png" alt="Ko-fi QR Code" width="200" height="200" /></a>

*Click the QR code or button above to support via Ko-fi*

### ⚡ Lightning Network (Bitcoin)

**Send Sats via Lightning:**

- [🔗 gossamerfalling850577@getalby.com](lightning:gossamerfalling850577@getalby.com)
- [🔗 havenhelpful360120@getalby.com](lightning:havenhelpful360120@getalby.com)

**Scan QR Codes:**

<a href="lightning:gossamerfalling850577@getalby.com"><img src="../assets/lightning_wallet_QR_Code.png" alt="Lightning Wallet 1 QR Code" width="200" height="200" /></a> <a href="lightning:havenhelpful360120@getalby.com"><img src="../assets/lightning_wallet_QR_Code_2.png" alt="Lightning Wallet 2 QR Code" width="200" height="200" /></a>

### 🎯 Why Support?

- **Keeps the ideation flowing** — Daily curation and synthesis of tech concepts
- **Funds practical experiments** — Testing ideas in real-world scenarios
- **Supports open innovation** — All content shared freely with the community
- **Enables deeper analysis** — More time for thoughtful idea development

*All support helps turn ideas into reality.*

<!-- Ko-fi Floating Widget -->
<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
<script>
  kofiWidgetOverlay.draw('grumpified', {
    'type': 'floating-chat',
    'floating-chat.donateButton.text': 'Tip The Innovator',
    'floating-chat.donateButton.background-color': '#FF6B35',
    'floating-chat.donateButton.text-color': '#fff'
  });
</script>

"""
    return section


def generate_blog_post(aggregated, insights):
    """Generate the complete blog post with The Visionary's voice"""
    if not aggregated:
        return None
    
    # Visionary persona
    persona = ("The Visionary", "💡", "Forward-Thinking Innovation")
    
    # Build report data structure
    report_insights = {
        'patterns': insights.get('patterns', {}),
        'inferences': insights.get('themes', [])
    }
    
    report_data = {
        'findings': aggregated,
        'insights': report_insights,
        'history': {},
        'persona': persona
    }
    
    # Use Report Translator approach
    post = generate_intro_hook(report_data, persona)
    post += generate_metrics_snapshot(report_data)
    post += generate_findings_section(report_data)
    post += generate_patterns_analysis(report_data)
    post += generate_developer_framework(report_data)
    post += generate_priorities_watchlist(report_data)
    
    # Support section
    post += generate_idea_vault_support_section()
    
    # Attribution
    post += "\n---\n\n"
    post += f"*Written by **The Visionary** 💡 — your guide to tech ideation and innovation. "
    post += f"Ideas sourced from [Idea Vault](https://grumpified-oggvct.github.io/idea_vault).*\n"
    
    return post


def save_blog_post(content, date_str):
    """Save the blog post as a Jekyll markdown file with AI editing"""
    filename = f"{date_str}-idea-vault.md"
    filepath = POSTS_DIR / filename
    
    title = f"The Innovator - Daily Tech Ideas ({date_str})"
    
    # AI EDITING
    print("\n🤖 Running AI-Powered Editing...")
    try:
        editor = AIEditor()
        
        ai_results = editor.edit_post(
            title=title,
            content=content,
            persona_name="The Visionary",
            author="The Innovator",
            enable_readability=True,
            enable_seo=True,
            enable_grammar=True,
            enable_fact_check=False
        )
        
        seo_data = ai_results.get('seo', {})
        readability_data = ai_results.get('readability', {})
        grammar_data = ai_results.get('grammar', {})
        
        tags = ["ideas", "innovation", "tech-vision", "ideation", "future-tech"]
        if seo_data and 'error' not in seo_data:
            seo_keywords = seo_data.get('keywords', [])[:5]
            for keyword in seo_keywords:
                if keyword not in tags and len(tags) < 12:
                    tags.append(keyword)
        
        meta_description = seo_data.get('meta_description', f"{title} - Visionary insights from The Innovator")
        keywords = ', '.join(tags[:10])
        
        print(f"  ✅ SEO Score: {seo_data.get('seo_score', 'N/A')}/100")
        print(f"  ✅ Readability: {readability_data.get('readability_level', 'N/A')}")
        if not grammar_data.get('skipped'):
            print(f"  ✅ Clarity: {grammar_data.get('clarity_score', 'N/A')}/100")
    
    except Exception as e:
        print(f"  ⚠️  AI editing skipped: {e}")
        tags = ["ideas", "innovation", "tech-vision", "ideation", "future-tech"]
        meta_description = f"{title} - Visionary insights from The Innovator"
        keywords = ', '.join(tags)
        seo_data = {}
        readability_data = {}
    
    # Create Jekyll front matter
    front_matter = f"""---
layout: post
title: "{title}"
date: {date_str} 10:00:00 -0600
categories: [ideas, innovation]
tags: {tags}
author: The Visionary
description: "{meta_description[:160]}"
keywords: "{keywords}"
readability_level: "{readability_data.get('readability_level', 'Standard')}"
seo_score: {seo_data.get('seo_score', 0)}
---

"""
    
    full_content = front_matter + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ Blog post saved: {filepath}")
    return filepath


def main():
    """Main execution function"""
    print("💡 The Innovator - Idea Vault Blog Generator")
    print("=" * 60)
    
    # Check for date override argument
    date_override = sys.argv[1] if len(sys.argv) > 1 else None
    if date_override:
        print(f"📅 Using date override: {date_override}")
    
    # Ensure directories exist
    ensure_directories()
    
    # Initialize memory system
    memory = BlogMemory('idea-vault')
    print(f"🧠 Memory loaded: {len(memory.memory['post_history'])} posts in history")
    
    # Fetch data from Idea Vault
    aggregated, insights = fetch_idea_vault_data_from_github(date_override)
    
    if not aggregated:
        print("❌ No data available. Cannot generate blog post.")
        return 1
    
    print(f"📊 Loaded {len(aggregated)} ideas")
    
    # Generate blog post
    print("✍️  Generating blog post...")
    blog_content = generate_blog_post(aggregated, insights)
    
    if not blog_content:
        print("❌ Failed to generate blog content")
        return 1
    
    # Save the post
    target_date = date_override if date_override else get_today_date_str()
    filepath = save_blog_post(blog_content, target_date)
    
    print("=" * 60)
    print("🎉 Blog post generation complete!")
    print(f"📄 File: {filepath}")
    print(f"📝 Length: {len(blog_content)} characters")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
