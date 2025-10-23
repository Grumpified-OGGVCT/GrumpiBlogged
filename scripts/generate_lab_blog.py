#!/usr/bin/env python3
"""
GrumpiBlogged - AI Research Daily Blog Post Generator
"The Lab" - Where cutting-edge AI research meets practical understanding

Persona: The Scholar 📚
- Rigorous but accessible: Maintains scientific accuracy while explaining clearly
- Contextual: Places new research in context of what came before
- Measured: Avoids hype, focuses on evidence and methodology
- Curious: Asks probing questions about implications and limitations
- Pedagogical: Teaches readers how to think about research
- Humble: Acknowledges uncertainty and limitations
- Connective: Draws links between disparate research areas

Voice Characteristics:
- Consistent academic voice (unlike The Pulse's 5 dynamic personas)
- Moderate, thoughtful energy
- "We observe", "This suggests", "Consider the implications"
- Careful hypotheses with caveats
- Academic but accessible language
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random
from collections import defaultdict
import requests
import base64

# Paths
AI_RESEARCH_DAILY_REPO = "https://api.github.com/repos/AccidentalJedi/AI_Research_Daily"
POSTS_DIR = Path("docs/_posts")
DATA_DIR = Path("data/lab")  # Local cache of Lab data


def ensure_directories():
    """Create necessary directories if they don't exist"""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def fetch_lab_data_from_github(date_override=None):
    """Fetch aggregated data from AI Research Daily GitHub repository
    
    Args:
        date_override: Optional date string (YYYY-MM-DD) for testing with historical data
    """
    target_date = date_override if date_override else get_today_date_str()
    
    # Try to fetch from GitHub
    agg_url = f"{AI_RESEARCH_DAILY_REPO}/contents/data/aggregated/{target_date}.json"
    insights_url = f"{AI_RESEARCH_DAILY_REPO}/contents/data/insights/{target_date}.json"
    
    aggregated = []
    insights = {}
    
    try:
        # Fetch aggregated data
        print(f"📡 Fetching aggregated data for {target_date}...")
        response = requests.get(agg_url, timeout=10)
        if response.status_code == 200:
            content = response.json()
            # Decode base64 content
            decoded = base64.b64decode(content['content']).decode('utf-8')
            aggregated = json.loads(decoded)
            print(f"✅ Loaded {len(aggregated)} items from GitHub")
            
            # Cache locally
            cache_file = DATA_DIR / f"{target_date}.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(aggregated, f, indent=2)
        else:
            print(f"⚠️  GitHub fetch failed (status {response.status_code}), trying local cache...")
            # Try local cache
            cache_file = DATA_DIR / f"{target_date}.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    aggregated = json.load(f)
                print(f"✅ Loaded {len(aggregated)} items from local cache")
    
    except Exception as e:
        print(f"❌ Error fetching from GitHub: {e}")
        # Try local cache as fallback
        cache_file = DATA_DIR / f"{target_date}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                aggregated = json.load(f)
            print(f"✅ Loaded {len(aggregated)} items from local cache")
    
    try:
        # Fetch insights data
        print(f"📡 Fetching insights data for {target_date}...")
        response = requests.get(insights_url, timeout=10)
        if response.status_code == 200:
            content = response.json()
            decoded = base64.b64decode(content['content']).decode('utf-8')
            insights = json.loads(decoded)
            print(f"✅ Loaded insights from GitHub")
    except Exception as e:
        print(f"⚠️  No insights data available: {e}")
    
    return aggregated, insights


def load_recent_history(days=7):
    """Load recent Lab blog posts for context and continuity"""
    history = []
    today = datetime.now()
    
    for i in range(1, days + 1):
        past_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        post_file = POSTS_DIR / f"{past_date}-ai-research-daily.md"
        
        if post_file.exists():
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                history.append({
                    'date': past_date,
                    'content': content
                })
    
    return history


def analyze_research_focus(aggregated):
    """
    Analyze the research focus for today's content
    Returns: dict with research themes and characteristics
    """
    themes = {
        'breakthrough': 0,
        'incremental': 0,
        'controversial': 0,
        'replication': 0,
        'survey': 0,
        'architecture': 0,
        'benchmark': 0,
        'application': 0
    }
    
    # Analyze titles and summaries
    for entry in aggregated:
        title = entry.get('title', '').lower()
        summary = entry.get('summary', '').lower()
        combined = title + ' ' + summary
        
        # Detect research types
        if any(word in combined for word in ['novel', 'new', 'breakthrough', 'first', 'unprecedented']):
            themes['breakthrough'] += 1
        
        if any(word in combined for word in ['improve', 'enhance', 'better', 'faster', 'efficient']):
            themes['incremental'] += 1
        
        if any(word in combined for word in ['challenge', 'question', 'debate', 'controversial']):
            themes['controversial'] += 1
        
        if any(word in combined for word in ['replicate', 'reproduce', 'verify', 'validation']):
            themes['replication'] += 1
        
        if any(word in combined for word in ['survey', 'review', 'overview', 'comprehensive']):
            themes['survey'] += 1
        
        if any(word in combined for word in ['architecture', 'model', 'network', 'transformer', 'attention']):
            themes['architecture'] += 1
        
        if any(word in combined for word in ['benchmark', 'sota', 'state-of-the-art', 'performance']):
            themes['benchmark'] += 1
        
        if any(word in combined for word in ['application', 'practical', 'deployment', 'production']):
            themes['application'] += 1
    
    return themes


def generate_scholar_opening(aggregated, themes):
    """Generate The Scholar's opening based on research themes"""
    total_items = len(aggregated)
    
    # Determine dominant theme
    dominant_theme = max(themes.items(), key=lambda x: x[1])[0] if themes else 'general'
    
    openings = {
        'breakthrough': [
            f"📚 Today's research landscape brings something genuinely significant: {total_items} developments that challenge our fundamental assumptions. Let's unpack why this matters.",
            f"📚 The research community delivered {total_items} noteworthy contributions today, several of which represent genuine advances in the field. Let's examine the evidence.",
        ],
        'incremental': [
            f"📚 Progress in AI research is often incremental, and today's {total_items} papers exemplify this steady advancement. The pattern is telling.",
            f"📚 Today we observe {total_items} contributions that, while individually modest, collectively advance our understanding. This is how science progresses.",
        ],
        'controversial': [
            f"📚 Bold claims landed in the research community today: {total_items} papers that require scrutiny. Let's examine the evidence carefully.",
            f"📚 Today's {total_items} papers include some provocative claims. The methodology deserves our attention.",
        ],
        'survey': [
            f"📚 Sometimes the most valuable research isn't a new breakthrough—it's a comprehensive look at what we've learned. Today's {total_items} contributions include exactly that kind of synthesis.",
            f"📚 Today we have {total_items} papers that help us step back and see the bigger picture. This meta-analysis is illuminating.",
        ],
        'architecture': [
            f"📚 The architecture frontier is active today: {total_items} papers exploring how we structure intelligence. The implications are worth considering.",
            f"📚 Today's {total_items} contributions focus on fundamental questions of model design. Let's examine what they reveal.",
        ],
        'benchmark': [
            f"📚 Performance metrics tell a story: today's {total_items} papers push boundaries on established benchmarks. But we must read beyond the numbers.",
            f"📚 Today we have {total_items} papers claiming improvements. Let's examine what these benchmarks actually measure.",
        ],
        'general': [
            f"📚 Today's research intelligence: {total_items} developments across the AI landscape. Let's identify what matters most.",
            f"📚 The research community produced {total_items} noteworthy papers today. Let's examine the signal through the noise.",
        ]
    }
    
    return random.choice(openings.get(dominant_theme, openings['general']))


def generate_research_commentary(entry):
    """Generate unique, rigorous commentary for a research paper/project
    
    This is The Scholar's voice: measured, contextual, pedagogical
    """
    title = entry.get('title', 'Unknown')
    summary = entry.get('summary', '')
    highlights = entry.get('highlights', [])
    
    # Extract metadata
    stars = 0
    language = ''
    for h in highlights:
        if 'stars:' in h.lower():
            try:
                stars = int(h.split(':')[1].strip())
            except:
                pass
        if 'language:' in h.lower():
            language = h.split(':')[1].strip()
    
    # Analyze the research/project
    summary_lower = summary.lower()
    
    # Identify research characteristics
    is_theoretical = any(word in summary_lower for word in ['theory', 'theoretical', 'mathematical', 'proof', 'theorem'])
    is_empirical = any(word in summary_lower for word in ['experiment', 'empirical', 'benchmark', 'evaluation', 'test'])
    is_novel_architecture = any(word in summary_lower for word in ['novel', 'new architecture', 'transformer', 'attention', 'mechanism'])
    is_application = any(word in summary_lower for word in ['application', 'practical', 'deployment', 'production', 'real-world'])
    is_survey = any(word in summary_lower for word in ['survey', 'review', 'comprehensive', 'overview'])
    is_replication = any(word in summary_lower for word in ['replicate', 'reproduce', 'verify', 'validation'])
    
    # Generate commentary based on characteristics
    commentaries = []
    
    if is_theoretical:
        commentaries.append(f"This work contributes to our theoretical understanding of {summary[:80]}... The mathematical foundations deserve careful examination.")
    
    if is_empirical:
        commentaries.append(f"The empirical results are noteworthy: {summary[:80]}... However, we should examine the experimental design before drawing conclusions.")
    
    if is_novel_architecture:
        commentaries.append(f"A novel architectural approach: {summary[:80]}... If this holds up under scrutiny, it could influence how we design future systems.")
    
    if is_application:
        commentaries.append(f"This bridges research and practice: {summary[:80]}... The path from paper to production is worth monitoring.")
    
    if is_survey:
        commentaries.append(f"A valuable synthesis: {summary[:80]}... Survey papers like this help us see patterns we might otherwise miss.")
    
    if is_replication:
        commentaries.append(f"Science advances through replication: {summary[:80]}... Independent verification is how we build confidence in results.")
    
    # Add maturity/adoption context based on stars
    if stars > 1000:
        commentaries.append(f"With {stars:,} stars, this has achieved significant community adoption—a signal of practical value beyond academic interest.")
    elif stars > 100:
        commentaries.append(f"Growing adoption ({stars:,} stars) suggests the community finds this useful. Worth tracking.")
    elif stars > 0:
        commentaries.append(f"Early stage ({stars} stars) but the concept merits attention.")
    
    # Select and combine commentaries
    if commentaries:
        return ' '.join(commentaries[:2])  # Use up to 2 commentary elements
    else:
        # Fallback: generic scholarly commentary
        return f"This work addresses {summary[:100]}... The approach and methodology warrant further examination."


def generate_research_section(aggregated):
    """Generate section about research papers and projects with deep analysis"""
    if not aggregated:
        return ""
    
    lines = []
    lines.append("## 🔬 Today's Research Intelligence\n\n")
    lines.append("*Curated from the daily firehose of AI research, filtered for significance and impact.*\n\n")
    
    # Take top 5-7 most significant items
    top_items = aggregated[:7]
    
    for i, entry in enumerate(top_items, 1):
        title = entry.get('title', 'Unknown')
        url = entry.get('url', '#')
        source = entry.get('source', 'unknown')
        summary = entry.get('summary', '')
        highlights = entry.get('highlights', [])
        
        # Extract stars and language
        stars = ''
        language = ''
        for h in highlights:
            if 'stars:' in h.lower():
                try:
                    star_count = int(h.split(':')[1].strip())
                    stars = f"{star_count:,} ⭐"
                except:
                    pass
            if 'language:' in h.lower():
                language = h.split(':')[1].strip()
        
        lines.append(f"**{i}. [{title}]({url})** (via {source})")
        
        # Add metadata if available
        if stars and language:
            lines.append(f" — {stars} • {language}")
        elif stars:
            lines.append(f" — {stars}")
        lines.append("\n\n")
        
        # Generate unique scholarly commentary
        commentary = generate_research_commentary(entry)
        lines.append(f"   **Analysis**: {commentary}\n\n")
    
    return ''.join(lines)


def generate_implications_section(aggregated, themes):
    """Generate section on broader implications and future directions"""
    lines = []
    lines.append("## 🔮 Implications and Future Directions\n\n")

    # Analyze dominant themes
    dominant_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]

    if dominant_themes[0][1] > 0:
        theme_name = dominant_themes[0][0]

        implications = {
            'breakthrough': "The breakthrough work we're seeing today suggests we're at an inflection point. These aren't incremental improvements—they're fundamental rethinks of how we approach the problem. If these results hold up under independent replication, we can expect rapid adoption within 6-12 months.",
            'incremental': "While no single paper represents a breakthrough, the collective progress is significant. This is how science advances: steady, methodical improvement. The cumulative effect of these incremental gains often exceeds the impact of headline-grabbing breakthroughs.",
            'architecture': "The architectural innovations we're observing today will shape the next generation of models. Pay attention to which approaches gain traction in the coming months—early adoption by major labs is often a leading indicator of long-term viability.",
            'benchmark': "Benchmark improvements tell us where the field is heading, but we must read them critically. What matters isn't just the numbers—it's whether the improvements generalize beyond the specific test set. Look for papers that include ablation studies and failure analysis.",
            'application': "The gap between research and production is narrowing. Today's papers show increasing focus on practical deployment, which suggests the field is maturing. This is good news for practitioners looking to leverage cutting-edge research.",
            'survey': "Survey papers like these are invaluable for understanding the current state of the field. They help us identify gaps, spot emerging trends, and avoid reinventing the wheel. This is required reading for anyone planning research in these areas.",
        }

        lines.append(implications.get(theme_name, "Today's research contributions advance our understanding across multiple fronts. The diversity of approaches suggests a healthy, vibrant field exploring many promising directions."))
        lines.append("\n\n")

    lines.append("**What to watch**: ")
    watch_items = [
        "Independent replication attempts",
        "Adoption by major research labs",
        "Real-world deployment case studies",
        "Follow-up work addressing limitations",
        "Benchmark performance on diverse tasks"
    ]
    lines.append(", ".join(watch_items[:3]))
    lines.append(".\n\n")

    return ''.join(lines)


def generate_lab_seo_section(aggregated, themes):
    """Generate SEO-optimized keywords and hashtags for research content"""
    # Core research keywords
    keywords = ["AIResearch", "MachineLearning", "DeepLearning", "AcademicAI", "ResearchPapers"]
    hashtags = ["#AIResearch", "#MachineLearning", "#DeepLearning", "#AcademicAI", "#MLPapers"]

    # Add theme-based keywords
    for theme, count in themes.items():
        if count > 0:
            theme_keywords = {
                'breakthrough': (['Breakthrough', 'Innovation', 'NovelAI'], ['#AIBreakthrough', '#Innovation']),
                'architecture': (['NeuralArchitecture', 'Transformers', 'ModelDesign'], ['#NeuralNets', '#Transformers']),
                'benchmark': (['Benchmarks', 'SOTA', 'Performance'], ['#SOTA', '#AIBenchmarks']),
                'application': (['AIApplications', 'Production', 'Deployment'], ['#ProductionAI', '#MLOps']),
                'survey': (['ResearchReview', 'Survey', 'MetaAnalysis'], ['#ResearchReview', '#AITrends']),
                'replication': (['Reproducibility', 'Replication', 'Verification'], ['#ReproducibleAI']),
            }

            if theme in theme_keywords:
                kw, ht = theme_keywords[theme]
                keywords.extend(kw)
                hashtags.extend(ht)

    # Analyze aggregated data for specific technologies
    tech_keywords = set()
    for entry in aggregated[:10]:
        summary = entry.get('summary', '').lower()
        title = entry.get('title', '').lower()
        combined = summary + ' ' + title

        # Extract technology-specific keywords
        if 'llm' in combined or 'language model' in combined:
            tech_keywords.add('LLM')
            hashtags.append('#LLM')
        if 'vision' in combined or 'image' in combined or 'visual' in combined:
            tech_keywords.add('ComputerVision')
            hashtags.append('#ComputerVision')
        if 'multimodal' in combined:
            tech_keywords.add('Multimodal')
            hashtags.append('#MultimodalAI')
        if 'rag' in combined or 'retrieval' in combined:
            tech_keywords.add('RAG')
            hashtags.append('#RAG')
        if 'agent' in combined:
            tech_keywords.add('AIAgents')
            hashtags.append('#AIAgents')
        if 'reasoning' in combined:
            tech_keywords.add('AIReasoning')
            hashtags.append('#Reasoning')
        if 'embedding' in combined:
            tech_keywords.add('Embeddings')
            hashtags.append('#Embeddings')

    keywords.extend(list(tech_keywords))

    # Add current year
    current_year = datetime.now().year
    keywords.append(f"AI{current_year}")
    hashtags.append(f"#AI{current_year}")

    # Add general trending research hashtags
    trending_hashtags = [
        '#ArXiv', '#HuggingFace', '#PapersWithCode',
        '#AIResearchDaily', '#MLResearch', '#NeurIPS',
        '#ICML', '#ICLR', '#CVPR', '#ACL'
    ]
    hashtags.extend(trending_hashtags)

    # Deduplicate while preserving order
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

    # Limit to reasonable numbers
    unique_keywords = unique_keywords[:20]
    unique_hashtags = unique_hashtags[:25]

    # Format the SEO section
    seo_section = "\n\n---\n\n"
    seo_section += "## 🔍 Keywords & Topics\n\n"
    seo_section += f"**Research Topics**: {', '.join(unique_keywords)}\n\n"
    seo_section += f"**Hashtags**: {' '.join(unique_hashtags)}\n\n"
    seo_section += "*These keywords and hashtags help you discover related research and connect with the AI research community. Share this post using these tags to maximize visibility!*\n"

    return seo_section


def generate_blog_post(aggregated, themes):
    """Generate the complete blog post with The Scholar's voice"""
    if not aggregated:
        return None

    # Generate opening
    opening = generate_scholar_opening(aggregated, themes)

    # Build the post
    post = f"{opening}\n\n"
    post += f"**Today's Intelligence**: {len(aggregated)} research developments analyzed\n\n"
    post += "---\n\n"

    # Research section
    post += generate_research_section(aggregated)

    # Implications section
    post += generate_implications_section(aggregated, themes)

    # SEO section
    post += generate_lab_seo_section(aggregated, themes)

    post += "\n---\n\n"
    post += f"*Written by **The Scholar** 📚 — your rigorous guide to AI research breakthroughs. "
    post += f"Data sourced from [AI Research Daily](https://accidentaljedi.github.io/AI_Research_Daily/).*\n"

    return post


def save_blog_post(content, date_str):
    """Save the blog post as a Jekyll markdown file"""
    filename = f"{date_str}-ai-research-daily.md"
    filepath = POSTS_DIR / filename

    # Create Jekyll front matter
    front_matter = f"""---
layout: post
title: "The Lab - AI Research Daily ({date_str})"
date: {date_str} 08:05:00 -0600
categories: [ai-research, daily-intelligence]
tags: [research, papers, arxiv, huggingface, machine-learning]
author: The Scholar
---

"""

    full_content = front_matter + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ Blog post saved: {filepath}")
    return filepath


def main():
    """Main execution function"""
    print("🔬 The Lab - AI Research Daily Blog Generator")
    print("=" * 60)

    # Check for date override argument
    date_override = sys.argv[1] if len(sys.argv) > 1 else None
    if date_override:
        print(f"📅 Using date override: {date_override}")

    # Ensure directories exist
    ensure_directories()

    # Fetch data from AI Research Daily
    aggregated, insights = fetch_lab_data_from_github(date_override)

    if not aggregated:
        print("❌ No data available. Cannot generate blog post.")
        return 1

    print(f"📊 Loaded {len(aggregated)} research items")

    # Analyze research themes
    themes = analyze_research_focus(aggregated)
    print(f"🎯 Research themes: {dict(themes)}")

    # Generate blog post
    print("✍️  Generating blog post...")
    blog_content = generate_blog_post(aggregated, themes)

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

