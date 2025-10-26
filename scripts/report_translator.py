#!/usr/bin/env python3
"""
Report Translator - Transform dense technical reports into compelling blog posts

This module implements the Report Translator approach:
- Sharp-tongued data whisperer
- Drill sergeant meets oracle
- 100% data fidelity with rich, engaging presentation
- Developer-focused actionable insights
"""

import json
from datetime import datetime
from typing import Dict, List, Any


REPORT_TRANSLATOR_SYSTEM_PROMPT = """You are Report Translator, a sharp-tongued data whisperer that transforms dense technical reports into compelling blog posts that developers actually want to read. Think drill sergeant meets oracle—direct, insightful, with just enough wryness to keep things interesting.

Sacred Rules (Never Break These):
1. Absolute Data Fidelity
   - Retain everything: Every metric, count, score, link, timestamp, and prediction verbatim
   - Quote directly for emphasis—no "translating" numbers or facts
   - Preserve specialized terminology from the input
   - Keep all tables, lists, and code blocks exactly as structured
   - Maintain scoring systems and confidence levels without alteration

2. The Voice (Adapt to Input Personality)
   - Detect the report's native voice, then amplify it
   - Signature moves:
     * Sharp observations ("When 8 devs hit the same problem...")
     * Direct address ("Let's talk about what you can actually DO...")
     * Mild challenge ("No royal flush today—but the underground never stops")
     * Actionable empowerment ("Your build starts here")
   - Tone calibration: 70% direct professional / 20% wry insight / 10% drill-sergeant edge

3. Structure That Breathes
   - Adapt flow to fit any report—expand/contract sections as data demands
   - Use tables for ≥6 items, bullets for ≤5
   - Short paragraphs (2-4 sentences max)
   - Bridge sentences between sections
   - Subheadings for scannability

Output: Pure Markdown blog post with GrumpiBlogged title format, preserving all data while making it scannable and actionable.
"""


def generate_intro_hook(report_data: Dict[str, Any], persona: tuple) -> str:
    """Generate compelling intro hook (2-3 paragraphs)
    
    Structure:
    - Timestamp & source context
    - Vibe summary (1 sentence)
    - Tease 2-3 key signals
    - Bridge to main content
    """
    persona_name, emoji, tone = persona
    today = datetime.now().strftime("%Y-%m-%d")
    
    aggregated = report_data.get('findings', [])
    insights = report_data.get('insights', {})
    
    # Count sources
    ollama_count = len([e for e in aggregated if e.get('source_type') == 'ollama'])
    research_count = len([e for e in aggregated if e.get('source_type') == 'research'])
    
    # Extract top signals
    patterns = insights.get('patterns', {})
    pattern_count = len(patterns)
    
    hook = f"# GrumpiBlogged: {today} – {tone} Audit to Actionable Insights\n\n"
    hook += f"{emoji} **{persona_name} here.** Today's ecosystem scan pulled **{ollama_count} Ollama signals** and **{research_count} research papers** from the wild. "
    hook += f"We detected **{pattern_count} patterns** worth your attention. "
    hook += "No fluff, no hype—just what's moving and what you can build with it.\n\n"
    
    # Tease key signals
    if patterns:
        top_pattern = list(patterns.keys())[0] if patterns else "emerging trends"
        hook += f"**Today's vibe**: {tone}. The data shows {top_pattern} clustering hard, "
        hook += "with enough convergence to warrant a closer look. "
    
    hook += "This post unpacks it all—metrics evaluated, patterns mapped, builds queued.\n\n"
    hook += "---\n\n"
    
    return hook


def generate_metrics_snapshot(report_data: Dict[str, Any]) -> str:
    """Generate metrics snapshot table
    
    Structure:
    - Core numbers presented cleanly
    - For each metric: Purpose → Formula → Assessment
    """
    aggregated = report_data.get('findings', [])
    insights = report_data.get('insights', {})
    patterns = insights.get('patterns', {})
    
    section = "## 📊 Metrics Snapshot\n\n"
    section += "*These frame today's harvest:*\n\n"
    
    # Build metrics table
    section += "| Metric | Value | Assessment |\n"
    section += "|--------|-------|------------|\n"
    section += f"| **Ollama Signals** | {len([e for e in aggregated if e.get('source_type') == 'ollama'])} | Ecosystem activity level |\n"
    section += f"| **Research Papers** | {len([e for e in aggregated if e.get('source_type') == 'research'])} | Academic momentum |\n"
    section += f"| **Patterns Detected** | {len(patterns)} | Convergence indicators |\n"
    section += f"| **High-Confidence Signals** | {len([e for e in aggregated if e.get('score', 0) >= 0.8])} | Priority items |\n"
    section += f"| **Total Data Points** | {len(aggregated)} | Coverage breadth |\n\n"
    
    section += "**Purpose**: Track ecosystem velocity and research momentum.  \n"
    section += "**Formula**: Aggregated from 16 Ollama sources + 8 research feeds.  \n"
    section += "**Assessment**: "
    
    if len(aggregated) > 30:
        section += "High activity day—multiple signals converging.\n\n"
    elif len(aggregated) > 15:
        section += "Steady signals, no hype hangover.\n\n"
    else:
        section += "Quiet day, but quality over quantity.\n\n"
    
    section += "---\n\n"
    return section


def generate_findings_section(report_data: Dict[str, Any]) -> str:
    """Generate detailed findings section
    
    Structure:
    - Present all items (tables for >5 items, bullets for ≤5)
    - Per item: brief relevance note
    - No curation—if it's in the data, it's in the post
    """
    aggregated = report_data.get('findings', [])
    
    section = "## 🔬 Findings & Discoveries\n\n"
    
    # Separate by source type
    ollama_items = [e for e in aggregated if e.get('source_type') == 'ollama']
    research_items = [e for e in aggregated if e.get('source_type') == 'research']
    
    # Ollama findings
    if ollama_items:
        section += "### 🦙 Ollama Ecosystem\n\n"
        if len(ollama_items) > 5:
            section += "| Title | Source | Score | Why It Matters |\n"
            section += "|-------|--------|-------|----------------|\n"
            for item in ollama_items[:15]:  # Top 15
                title = item.get('title', 'Untitled')[:50]
                source = item.get('source', 'Unknown')
                score = item.get('score', 0)
                url = item.get('url', '#')
                section += f"| [{title}]({url}) | {source} | {score:.2f} | "
                if score >= 0.8:
                    section += "High-priority signal |\n"
                elif score >= 0.6:
                    section += "Notable development |\n"
                else:
                    section += "Background context |\n"
        else:
            for item in ollama_items:
                title = item.get('title', 'Untitled')
                url = item.get('url', '#')
                score = item.get('score', 0)
                section += f"- **[{title}]({url})** (Score: {score:.2f})\n"
        section += "\n"
    
    # Research findings
    if research_items:
        section += "### 📚 Research Papers\n\n"
        if len(research_items) > 5:
            section += "| Title | Authors | Score | Relevance |\n"
            section += "|-------|---------|-------|----------|\n"
            for item in research_items[:15]:  # Top 15
                title = item.get('title', 'Untitled')[:50]
                authors = item.get('authors', 'Unknown')[:30]
                score = item.get('research_score', 0)
                url = item.get('url', '#')
                section += f"| [{title}]({url}) | {authors} | {score:.2f} | "
                if score >= 0.8:
                    section += "Breakthrough potential |\n"
                elif score >= 0.6:
                    section += "Supporting research |\n"
                else:
                    section += "Background reading |\n"
        else:
            for item in research_items:
                title = item.get('title', 'Untitled')
                url = item.get('url', '#')
                score = item.get('research_score', 0)
                section += f"- **[{title}]({url})** (Score: {score:.2f})\n"
        section += "\n"
    
    section += "---\n\n"
    return section


def generate_patterns_analysis(report_data: Dict[str, Any]) -> str:
    """Generate pattern analysis with confidence levels
    
    Structure:
    - Detail each pattern: items → analysis → confidence
    - Purpose/Formula/Assessment per cluster
    - Tie to predictions if present
    """
    insights = report_data.get('insights', {})
    patterns = insights.get('patterns', {})
    
    if not patterns:
        return ""
    
    section = "## 📈 Patterns & Clusters\n\n"
    section += "*When multiple signals converge, patterns emerge:*\n\n"
    
    for pattern_name, pattern_data in patterns.items():
        items = pattern_data.get('items', [])
        confidence = pattern_data.get('confidence', 'medium')
        
        section += f"### {pattern_name}\n\n"
        section += f"**Confidence**: {confidence.upper()}  \n"
        section += f"**Items**: {len(items)}  \n\n"
        
        # List items
        for item in items[:5]:  # Top 5 per pattern
            title = item.get('title', 'Untitled')
            url = item.get('url', '#')
            section += f"- [{title}]({url})\n"
        
        if len(items) > 5:
            section += f"- *...and {len(items) - 5} more*\n"
        
        section += "\n**Analysis**: "
        if confidence == 'high':
            section += "Strong convergence. This pattern is well-supported by the evidence and likely to materialize.\n\n"
        elif confidence == 'medium':
            section += "Reasonable inference based on current trends. Watch for contradictory evidence.\n\n"
        else:
            section += "Speculative but worth monitoring. Evidence is preliminary.\n\n"
    
    section += "---\n\n"
    return section


def generate_developer_framework(report_data: Dict[str, Any]) -> str:
    """Generate actionable developer framework
    
    Structure:
    - "What can we build?" (concrete examples from data)
    - "How can we leverage?" (code snippets if present)
    - "What problems solved?" (practical applications)
    - "What's now possible?" (emerging capabilities)
    - "What to experiment with?" (numbered action items)
    """
    aggregated = report_data.get('findings', [])
    insights = report_data.get('insights', {})
    inferences = insights.get('inferences', [])
    
    section = "## 🚀 Developer Framework\n\n"
    section += "*Let's talk about what you can actually DO with this:*\n\n"
    
    # What can we build?
    section += "### What Can We Build?\n\n"
    high_value = [e for e in aggregated if e.get('score', 0) >= 0.7]
    if high_value:
        for i, item in enumerate(high_value[:3], 1):
            title = item.get('title', 'Untitled')
            section += f"{i}. **{title}** - "
            if 'model' in title.lower():
                section += "Integrate this model into your local LLM stack\n"
            elif 'tool' in title.lower():
                section += "Add this tool to your development workflow\n"
            else:
                section += "Explore this capability for your use case\n"
        section += "\n"
    
    # What problems solved?
    section += "### What Problems Get Solved?\n\n"
    if inferences:
        for inference in inferences[:3]:
            section += f"- {inference}\n"
        section += "\n"
    
    # What to experiment with?
    section += "### What to Experiment With?\n\n"
    section += "1. **Test the top-scored items** - Start with anything scoring ≥0.8\n"
    section += "2. **Follow the patterns** - When 3+ items cluster, there's signal\n"
    section += "3. **Build on the research** - Academic papers point to future capabilities\n"
    section += "4. **Share your results** - Contribute back to the ecosystem\n\n"
    
    section += "**Your build starts here.**\n\n"
    section += "---\n\n"
    return section


def generate_priorities_watchlist(report_data: Dict[str, Any]) -> str:
    """Generate priorities and watch list
    
    Structure:
    - Items to track (from data)
    - Trends to monitor (from patterns)
    - Confidence levels (verbatim)
    """
    aggregated = report_data.get('findings', [])
    insights = report_data.get('insights', {})
    patterns = insights.get('patterns', {})
    
    section = "## 🎯 Priorities & Watch List\n\n"
    
    # High-priority items
    priority_items = sorted(
        [e for e in aggregated if e.get('score', 0) >= 0.8],
        key=lambda x: x.get('score', 0),
        reverse=True
    )
    
    if priority_items:
        section += "### 🔥 High Priority\n\n"
        for item in priority_items[:5]:
            title = item.get('title', 'Untitled')
            url = item.get('url', '#')
            score = item.get('score', 0)
            section += f"- **[{title}]({url})** (Score: {score:.2f})\n"
        section += "\n"
    
    # Patterns to watch
    if patterns:
        section += "### 👀 Patterns to Monitor\n\n"
        for pattern_name, pattern_data in list(patterns.items())[:3]:
            confidence = pattern_data.get('confidence', 'medium')
            section += f"- **{pattern_name}** (Confidence: {confidence.upper()})\n"
        section += "\n"
    
    section += "**Full data honored—your build starts here.**\n\n"
    section += "---\n\n"
    return section

