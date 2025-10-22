#!/usr/bin/env python3
"""
GrumpiBlogged - Daily Learning Blog Post Generator
Generates personal, reflective blog posts based on Ollama Pulse discoveries
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import random

# Paths
OLLAMA_PULSE_DATA = Path("../ollama_pulse/data")
POSTS_DIR = Path("_posts")


def ensure_posts_dir():
    """Create _posts directory if it doesn't exist"""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def load_ollama_pulse_data():
    """Load today's aggregated data and insights from Ollama Pulse"""
    today = get_today_date_str()
    agg_file = OLLAMA_PULSE_DATA / "aggregated" / f"{today}.json"
    insights_file = OLLAMA_PULSE_DATA / "insights" / f"{today}.json"
    
    aggregated = []
    if agg_file.exists():
        with open(agg_file, 'r', encoding='utf-8') as f:
            aggregated = json.load(f)
    
    insights = {}
    if insights_file.exists():
        with open(insights_file, 'r', encoding='utf-8') as f:
            insights = json.load(f)
    
    return aggregated, insights


def generate_opening(aggregated, insights):
    """Generate a personal opening paragraph"""
    openings = [
        f"Today was one of those days where the Ollama ecosystem just keeps surprising me. I tracked {len(aggregated)} new developments, and honestly, the pace of innovation is wild.",
        f"Another day, another deep dive into what's happening with Ollama. Today I found {len(aggregated)} interesting things worth talking about.",
        f"I spent today exploring the Ollama landscape, and wow - {len(aggregated)} discoveries later, I'm buzzing with ideas.",
        f"You know that feeling when you're tracking something and it just clicks? That's how today felt. {len(aggregated)} new items crossed my radar.",
    ]
    return random.choice(openings)


def generate_official_section(official):
    """Generate section about official updates"""
    if not official:
        return ""
    
    lines = ["\n## 📢 What the Ollama Team Shipped\n"]
    lines.append("The official updates today were particularly interesting:\n\n")
    
    for entry in official[:3]:
        title = entry.get('title', 'Unknown')
        url = entry.get('url', '#')
        lines.append(f"- **[{title}]({url})**: This caught my attention because it shows where the core team is focusing their energy.\n")
    
    return "".join(lines)


def generate_community_section(tools):
    """Generate section about community projects"""
    if not tools:
        return ""
    
    lines = ["\n## 🛠️ What the Community is Building\n"]
    lines.append("This is where it gets really exciting. The community is shipping some wild stuff:\n\n")
    
    for entry in tools[:5]:
        title = entry.get('title', 'Unknown')
        url = entry.get('url', '#')
        highlights = entry.get('highlights', [])
        source = entry.get('source', 'unknown')
        
        if highlights:
            highlight_text = ', '.join(highlights[:2])
            lines.append(f"- **[{title}]({url})** (via {source}): {highlight_text}\n")
        else:
            lines.append(f"- **[{title}]({url})** (via {source})\n")
    
    lines.append("\nSeeing what other developers are building always sparks new ideas for me.\n")
    return "".join(lines)


def generate_patterns_section(patterns):
    """Generate section about emerging patterns"""
    if not patterns:
        return ""
    
    lines = ["\n## 📈 Patterns I'm Noticing\n"]
    lines.append("When you track this stuff daily, patterns start to emerge:\n\n")
    
    for pattern_name, items in list(patterns.items())[:2]:
        clean_name = pattern_name.replace('_', ' ').title()
        lines.append(f"### {clean_name}\n\n")
        lines.append(f"I'm seeing {len(items)} projects in this space. ")
        lines.append("This tells me there's real demand here, not just hype.\n\n")
        
        for item in items[:3]:
            title = item.get('title', 'Unknown')
            url = item.get('url', '#')
            lines.append(f"- [{title}]({url})\n")
        lines.append("\n")
    
    return "".join(lines)


def generate_insights_section(inferences):
    """Generate section about key insights"""
    if not inferences:
        return ""
    
    lines = ["\n## 💡 What I'm Taking Away\n"]
    lines.append("Here's what I'm actually learning from all this:\n\n")
    
    for inf in inferences[:2]:
        pattern = inf.get('pattern', 'Unknown')
        observation = inf.get('observation', '')
        inference = inf.get('inference', '')
        confidence = inf.get('confidence', 'medium')
        
        clean_pattern = pattern.replace('_', ' ').title()
        lines.append(f"### {clean_pattern}\n\n")
        lines.append(f"**What I'm seeing**: {observation}\n\n")
        lines.append(f"**What it means**: {inference}\n\n")
        
        if confidence == "high":
            lines.append("I'm pretty confident about this one.\n\n")
        else:
            lines.append("Still watching this, but it's worth noting.\n\n")
    
    return "".join(lines)


def generate_personal_takeaway(aggregated, insights):
    """Generate personal reflection and action items"""
    lines = ["\n## 🎯 My Personal Takeaway\n"]
    
    takeaways = [
        "The Ollama ecosystem is moving fast, and I need to keep experimenting to stay current.",
        "What excites me most is how accessible this technology is becoming. Anyone can run these models now.",
        "I'm seeing a shift from 'can we do this?' to 'how do we do this well?' - that's maturity.",
        "The community is the real story here. Every day, someone ships something that makes me rethink what's possible.",
    ]
    
    lines.append(random.choice(takeaways) + "\n\n")
    
    lines.append("**What I'm going to try next**:\n\n")
    lines.append("1. Experiment with the latest Ollama Cloud models\n")
    lines.append("2. Build something small but useful with what I learned today\n")
    lines.append("3. Share my findings with the community\n\n")
    
    lines.append("That's it for today. Tomorrow, I'll be back tracking more discoveries.\n")
    
    return "".join(lines)


def generate_blog_post(aggregated, insights):
    """Generate the complete blog post"""
    today = get_today_date_str()
    
    # Separate data by source
    official = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page']]
    tools = [e for e in aggregated if e.get('source') in ['github', 'reddit']]
    patterns = insights.get('patterns', {})
    inferences = insights.get('inferences', [])
    
    # Build the post
    post = generate_opening(aggregated, insights) + "\n"
    post += generate_official_section(official)
    post += generate_community_section(tools)
    post += generate_patterns_section(patterns)
    post += generate_insights_section(inferences)
    post += generate_personal_takeaway(aggregated, insights)
    
    post += "\n---\n\n"
    post += "*This post was automatically generated from my daily Ollama ecosystem tracking. "
    post += f"Data sourced from [Ollama Pulse](https://grumpified-oggvct.github.io/ollama_pulse).*\n"
    
    return post


def save_blog_post(post_content):
    """Save the blog post with Jekyll front matter"""
    ensure_posts_dir()
    today = get_today_date_str()
    now = datetime.now()
    
    # Generate tags based on content
    tags = ["ollama", "AI", "daily-learning", "ecosystem-tracking"]
    
    # Jekyll front matter
    front_matter = f"""---
layout: post
title: "What I Learned Today: Ollama Ecosystem - {today}"
date: {now.strftime('%Y-%m-%d %H:%M:%S %z')}
author: GrumpiBot
tags: {tags}
repo_url: https://github.com/Grumpified-OGGVCT/ollama_pulse
---

"""
    
    # Save the post
    filename = f"{today}-ollama-daily-learning.md"
    filepath = POSTS_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter + post_content)
    
    print(f"✅ Blog post saved: {filepath}")
    return filepath


def main():
    print("🚀 Generating daily learning blog post...")
    
    # Load data from Ollama Pulse
    aggregated, insights = load_ollama_pulse_data()
    
    if not aggregated and not insights:
        print("⚠️  No Ollama Pulse data available for today")
        sys.exit(1)
    
    # Generate and save the post
    post_content = generate_blog_post(aggregated, insights)
    filepath = save_blog_post(post_content)
    
    print(f"✅ Daily learning blog post generated successfully!")
    print(f"📝 Post: {filepath}")


if __name__ == "__main__":
    main()

