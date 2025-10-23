#!/usr/bin/env python3
"""
GrumpiBlogged - Daily Learning Blog Post Generator
"The Pulse" - An enthusiastic, deeply-embedded guide to the fast-moving world of local AI

Persona: The Informed Enthusiast
- Knowledgeable: Explains why things matter, not just what happened
- Curious: Asks questions and speculates on future implications
- Tantalizingly verbose: Delivers high-value information with style and personality
- Dynamic: Adjusts tone daily based on the "vibe" of the news

Daily Personas:
- The Hype-Caster 💡: Major model drops → energetic, forward-looking
- The Mechanic 🛠️: Small updates/bug fixes → grounded, appreciative, practical
- The Curious Analyst 🤔: Weird/experimental models → inquisitive, analytical
- The Trend-Spotter 📈: Slow news day → reflective, data-driven, pattern-focused
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import random
from collections import defaultdict

# Paths
OLLAMA_PULSE_DATA = Path("../ollama_pulse_temp/data")
POSTS_DIR = Path("docs/_posts")
HISTORY_DIR = POSTS_DIR  # Previous posts for context


def ensure_posts_dir():
    """Create _posts directory if it doesn't exist"""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)


def get_today_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def load_ollama_pulse_data(date_override=None):
    """Load aggregated data and insights from Ollama Pulse

    Args:
        date_override: Optional date string (YYYY-MM-DD) for testing with historical data
    """
    target_date = date_override if date_override else get_today_date_str()
    agg_file = OLLAMA_PULSE_DATA / "aggregated" / f"{target_date}.json"
    insights_file = OLLAMA_PULSE_DATA / "insights" / f"{target_date}.json"

    aggregated = []
    if agg_file.exists():
        with open(agg_file, 'r', encoding='utf-8') as f:
            aggregated = json.load(f)
    else:
        print(f"⚠️  No aggregated data found at: {agg_file}")

    insights = {}
    if insights_file.exists():
        with open(insights_file, 'r', encoding='utf-8') as f:
            insights = json.load(f)
    else:
        print(f"⚠️  No insights data found at: {insights_file}")

    return aggregated, insights


def load_recent_history(days=7):
    """Load recent blog posts for context and continuity"""
    history = []
    today = datetime.now()

    for i in range(1, days + 1):
        past_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        post_file = POSTS_DIR / f"{past_date}-ollama-daily-learning.md"

        if post_file.exists():
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                history.append({
                    'date': past_date,
                    'content': content
                })

    return history


def detect_daily_vibe(aggregated, insights):
    """
    Detect the "vibe" of today's news to determine which persona to use
    Returns: ('persona_name', 'emoji', 'tone_description')
    """
    # Analyze the data
    has_major_models = any('model' in str(e.get('title', '')).lower() or
                          'release' in str(e.get('title', '')).lower()
                          for e in aggregated)

    has_cloud_models = any('cloud' in str(e).lower() for e in aggregated)

    bug_fix_keywords = ['fix', 'bug', 'patch', 'update', 'improve']
    mostly_fixes = sum(1 for e in aggregated
                      if any(kw in str(e.get('title', '')).lower()
                            for kw in bug_fix_keywords)) > len(aggregated) * 0.6

    has_weird_stuff = any(kw in str(e.get('title', '')).lower()
                         for e in aggregated
                         for kw in ['experimental', 'weird', 'unusual', 'strange', 'shakespeare', 'insult'])

    is_slow_day = len(aggregated) < 10

    # Determine persona
    if has_major_models or has_cloud_models:
        return ('hype_caster', '💡', 'energetic and forward-looking')
    elif mostly_fixes:
        return ('mechanic', '🛠️', 'grounded and appreciative')
    elif has_weird_stuff:
        return ('curious_analyst', '🤔', 'inquisitive and analytical')
    elif is_slow_day:
        return ('trend_spotter', '📈', 'reflective and data-driven')
    else:
        return ('informed_enthusiast', '🎯', 'balanced and insightful')


def generate_opening(aggregated, insights, persona, history):
    """Generate a dynamic opening based on persona and recent context"""
    persona_name, emoji, tone = persona
    count = len(aggregated)

    # Check if we mentioned something similar recently
    recent_topics = []
    if history:
        for h in history[:3]:
            if 'model' in h['content'].lower():
                recent_topics.append('models')
            if 'cloud' in h['content'].lower():
                recent_topics.append('cloud')

    openings = {
        'hype_caster': [
            f"{emoji} **Hold on.** I need to talk about what just dropped in the Ollama ecosystem today. We've got {count} new developments, and some of them are genuinely game-changing.",
            f"{emoji} Okay, so today's the kind of day that reminds me why I track this space obsessively. {count} updates came through, and at least a few of them are going to shift how we think about local AI.",
            f"{emoji} **Big news day.** The Ollama world just got {count} new pieces of the puzzle, and I'm seeing some serious potential here. Let me break down what matters.",
        ],
        'mechanic': [
            f"{emoji} No flashy headlines today—just {count} solid updates that make the whole Ollama experience better. And honestly? That's exactly what we need right now.",
            f"{emoji} Today's all about the nuts and bolts. {count} improvements, fixes, and refinements that might not grab headlines but absolutely matter if you're running Ollama daily.",
            f"{emoji} Sometimes the best days aren't about new models—they're about making what we have work better. Today brought {count} updates that do exactly that.",
        ],
        'curious_analyst': [
            f"{emoji} So... someone in the Ollama ecosystem just released something *interesting*. I found {count} updates today, and at least one of them made me stop and think 'wait, what?'",
            f"{emoji} Today's discoveries are a reminder that open-source AI is wonderfully weird. Out of {count} new things, there's definitely some experimental stuff worth unpacking.",
            f"{emoji} I love days like this. {count} updates, and buried in there is something so niche, so specific, that I can't help but dig into why it exists.",
        ],
        'trend_spotter': [
            f"{emoji} It's a quieter day in the Ollama world—only {count} updates—which means it's the perfect time to zoom out and look at the bigger picture.",
            f"{emoji} When the news slows down (just {count} items today), that's when the patterns become clearer. Let me connect some dots from this week.",
            f"{emoji} {count} updates today, which is lighter than usual. But that gives us space to talk about something I've been noticing over the past few days...",
        ],
        'informed_enthusiast': [
            f"{emoji} Another day tracking the Ollama ecosystem, another {count} discoveries. Some big, some small, all worth understanding.",
            f"{emoji} {count} new developments today in the Ollama world. Let me walk you through what's actually important and why it matters.",
            f"{emoji} I spent today sifting through {count} updates from across the Ollama ecosystem. Here's what caught my attention and what you should know.",
        ]
    }

    opening = random.choice(openings.get(persona_name, openings['informed_enthusiast']))

    # Add context from history if relevant
    if 'models' in recent_topics and persona_name == 'hype_caster':
        opening += f"\n\nAnd yes, I know—I've been talking about models a lot lately. But when the ecosystem is moving this fast, that's where the action is."

    return opening


def generate_official_section(official, persona):
    """Generate section about official updates with personality"""
    if not official:
        return ""

    persona_name, emoji, _ = persona

    intros = {
        'hype_caster': "## 📢 The Official Drop\n\nOkay, so here's what the Ollama core team actually shipped:\n\n",
        'mechanic': "## 📢 From the Core Team\n\nThe official updates are where you see the team's priorities. Here's what landed:\n\n",
        'curious_analyst': "## 📢 Official Updates Worth Examining\n\nLet's look at what the core team released and think about the implications:\n\n",
        'trend_spotter': "## 📢 Official Moves\n\nThe core team's updates tell us where they're placing their bets:\n\n",
        'informed_enthusiast': "## 📢 What the Ollama Team Shipped\n\nHere's what came from the official channels:\n\n"
    }

    lines = [intros.get(persona_name, intros['informed_enthusiast'])]

    for i, entry in enumerate(official[:3], 1):
        title = entry.get('title', 'Unknown')
        url = entry.get('url', '#')
        highlights = entry.get('highlights', [])

        # Add personality to each item
        if persona_name == 'hype_caster':
            lines.append(f"**{i}. [{title}]({url})**\n\n")
            if highlights:
                lines.append(f"   Key point: {highlights[0]}. This is the kind of update that opens up new possibilities.\n\n")
            else:
                lines.append(f"   This is significant because it shows the team is doubling down on core functionality.\n\n")

        elif persona_name == 'mechanic':
            lines.append(f"**{i}. [{title}]({url})**\n\n")
            lines.append(f"   Practical impact: This makes your daily Ollama workflow smoother. ")
            if highlights:
                lines.append(f"Specifically: {highlights[0]}\n\n")
            else:
                lines.append("Small change, big quality-of-life improvement.\n\n")

        else:
            lines.append(f"- **[{title}]({url})**")
            if highlights:
                lines.append(f" — {highlights[0]}")
            lines.append("\n")

    return "".join(lines)


def generate_project_commentary(entry, persona_name):
    """Generate unique, insightful commentary for a specific project"""
    summary = entry.get('summary', '')
    highlights = entry.get('highlights', [])

    # Extract star count from highlights
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

    # Analyze the summary for key features
    summary_lower = summary.lower()

    # Identify key characteristics
    is_privacy_focused = any(word in summary_lower for word in ['privacy', 'offline', 'local', 'on-device', 'private'])
    is_security_focused = any(word in summary_lower for word in ['security', 'scam', 'protection', 'safe'])
    is_performance_focused = any(word in summary_lower for word in ['fast', 'efficient', 'lightweight', 'optimized'])
    is_ui_tool = any(word in summary_lower for word in ['ui', 'interface', 'visual', 'dashboard', 'frontend'])
    is_integration = any(word in summary_lower for word in ['integration', 'connect', 'bridge', 'api'])
    is_framework = any(word in summary_lower for word in ['framework', 'library', 'toolkit', 'suite'])

    # Determine maturity level based on stars
    if stars == 0:
        maturity = "brand_new"
    elif stars < 10:
        maturity = "emerging"
    elif stars < 100:
        maturity = "growing"
    elif stars < 1000:
        maturity = "proven"
    else:
        maturity = "established"

    # Generate persona-specific commentary
    commentary_templates = {
        'hype_caster': {
            'brand_new': [
                f"Fresh off the press (0 stars) but the concept is exciting: {summary[:100]}... If this delivers, it could be a game-changer.",
                f"Just launched today with zero stars, but don't let that fool you—{summary[:100]}... Early adopters, this is your moment.",
                f"Brand new project tackling {summary[:80]}... The timing is perfect for this kind of innovation."
            ],
            'emerging': [
                f"Still early ({stars} stars) but gaining traction: {summary[:100]}... Watch this space.",
                f"Small but mighty ({stars} stars)—{summary[:100]}... This is the kind of project that could explode.",
                f"Just {stars} stars so far, but {summary[:100]}... The potential is massive."
            ],
            'proven': [
                f"{stars:,} stars and counting! {summary[:100]}... The community has spoken—this works.",
                f"Battle-tested with {stars:,} stars: {summary[:100]}... This is production-ready.",
                f"The {stars:,} stars tell the story: {summary[:100]}... Proven quality."
            ],
            'established': [
                f"{stars:,} stars don't lie—this is a cornerstone project. {summary[:100]}... Industry-grade quality.",
                f"With {stars:,} stars, this is basically essential infrastructure. {summary[:100]}... If you're not using this, you should be.",
                f"A heavyweight with {stars:,} stars: {summary[:100]}... This is what mature, reliable tooling looks like."
            ]
        },
        'mechanic': {
            'brand_new': [
                f"New tool (0 stars) that solves a real problem: {summary[:100]}... Practical and focused.",
                f"Just released, but the use case is clear: {summary[:100]}... This is the kind of utility we need.",
                f"Fresh project addressing {summary[:80]}... Simple, practical, useful."
            ],
            'proven': [
                f"{stars:,} stars means it's been tested in the field: {summary[:100]}... Reliable and production-ready.",
                f"Proven with {stars:,} stars: {summary[:100]}... This gets the job done.",
                f"{stars:,} developers can't be wrong: {summary[:100]}... Solid, dependable tool."
            ]
        },
        'curious_analyst': {
            'brand_new': [
                f"Interesting experiment (0 stars): {summary[:100]}... The approach is novel and worth studying.",
                f"New project exploring {summary[:80]}... The methodology here is fascinating.",
                f"Just launched with an intriguing premise: {summary[:100]}... Let's see how this evolves."
            ],
            'established': [
                f"With {stars:,} stars, this represents a mature approach: {summary[:100]}... The design patterns here are instructive.",
                f"{stars:,} stars indicate widespread adoption: {summary[:100]}... This is a case study in successful open source.",
                f"The {stars:,}-star rating reflects {summary[:80]}... There's a lot to learn from this project's trajectory."
            ]
        }
    }

    # Add special commentary for specific characteristics
    special_notes = []

    if is_privacy_focused:
        special_notes.append("Privacy-first design means your data never leaves your machine—critical for sensitive use cases.")

    if is_security_focused:
        special_notes.append("Built-in security features address real threats in the ecosystem.")

    if is_performance_focused:
        special_notes.append("Performance optimization is a first-class concern here, not an afterthought.")

    if language and language in ['Rust', 'Go', 'C++']:
        special_notes.append(f"{language} implementation suggests serious attention to performance and reliability.")

    if language == 'Lua' and 'vim' in summary_lower or 'neovim' in summary_lower:
        special_notes.append("The Vim/Neovim community is notoriously selective—this level of adoption signals genuine quality.")

    # Select appropriate template
    persona_templates = commentary_templates.get(persona_name, commentary_templates['hype_caster'])
    maturity_templates = persona_templates.get(maturity, persona_templates.get('brand_new', []))

    if not maturity_templates:
        # Fallback
        base_commentary = f"{summary[:120]}..."
    else:
        import random
        base_commentary = random.choice(maturity_templates)

    # Add special note if applicable
    if special_notes:
        base_commentary += " " + random.choice(special_notes)

    return base_commentary


def generate_community_section(tools, persona):
    """Generate section about community projects with deep analysis"""
    if not tools:
        return ""

    persona_name, emoji, _ = persona

    intros = {
        'hype_caster': "## 🚀 Community Innovation\n\nThis is where the real magic happens. The community is building stuff that's genuinely pushing boundaries:\n\n",
        'mechanic': "## 🛠️ What Developers Are Shipping\n\nThe community projects today are all about making Ollama more practical and usable:\n\n",
        'curious_analyst': "## 🔬 Community Experiments\n\nThe open-source community is trying some fascinating things. Let's examine what's happening:\n\n",
        'trend_spotter': "## 📊 Community Patterns\n\nLooking at what the community is building reveals some interesting trends:\n\n",
        'informed_enthusiast': "## 🛠️ What the Community is Building\n\nHere's what caught my eye from the community today:\n\n"
    }

    lines = [intros.get(persona_name, intros['informed_enthusiast'])]

    # Highlight top projects with analysis
    top_tools = tools[:5]

    for i, entry in enumerate(top_tools, 1):
        title = entry.get('title', 'Unknown')
        url = entry.get('url', '#')
        highlights = entry.get('highlights', [])
        source = entry.get('source', 'unknown')

        # Extract stars and language from highlights
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

        lines.append(f"**{i}. [{title}]({url})** (via {source})")

        # Add metadata if available
        if stars and language:
            lines.append(f" — {stars:,} ⭐ • {language}")
        lines.append("\n\n")

        # Generate unique commentary for this project
        commentary = generate_project_commentary(entry, persona_name)
        lines.append(f"   **Why this matters**: {commentary}\n\n")

    # Add closing insight
    closings = {
        'hype_caster': "\n**The takeaway**: The community is moving faster than ever. These aren't just experiments—they're production-ready tools.\n",
        'mechanic': "\n**Bottom line**: Every one of these projects makes Ollama more useful for real work. That's what matters.\n",
        'curious_analyst': "\n**What I'm thinking**: These projects reveal where developers see gaps. That's valuable market intelligence.\n",
        'trend_spotter': "\n**Pattern emerging**: The community is converging on specific use cases. Watch this space.\n",
        'informed_enthusiast': "\n**My take**: The community continues to amaze me with the creativity and quality of these projects.\n"
    }

    lines.append(closings.get(persona_name, closings['informed_enthusiast']))

    return "".join(lines)


def generate_patterns_section(patterns, persona, history):
    """Generate deep pattern analysis with historical context"""
    if not patterns:
        return ""

    persona_name, emoji, _ = persona

    # Check if we've mentioned these patterns before
    pattern_history = defaultdict(int)
    if history:
        for h in history[:7]:
            for pattern_name in patterns.keys():
                if pattern_name.replace('_', ' ') in h['content'].lower():
                    pattern_history[pattern_name] += 1

    intros = {
        'hype_caster': "## 🔥 Emerging Trends\n\nHere's where things get interesting—I'm seeing clear patterns that suggest where this is all heading:\n\n",
        'mechanic': "## 📊 What's Actually Being Built\n\nLooking at the data, here's what developers are focusing on:\n\n",
        'curious_analyst': "## 🔍 Pattern Analysis\n\nLet me dig into what these patterns tell us about the ecosystem:\n\n",
        'trend_spotter': "## 📈 The Bigger Picture\n\nThis is what I live for—connecting the dots across multiple data points:\n\n",
        'informed_enthusiast': "## 📈 Patterns Worth Watching\n\nWhen you track this daily, certain patterns become impossible to ignore:\n\n"
    }

    lines = [intros.get(persona_name, intros['informed_enthusiast'])]

    # Analyze top patterns
    sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)[:3]

    for pattern_name, items in sorted_patterns:
        clean_name = pattern_name.replace('_', ' ').title()
        count = len(items)
        times_mentioned = pattern_history.get(pattern_name, 0)

        lines.append(f"### {emoji} {clean_name}\n\n")

        # Add context based on history
        if times_mentioned > 3:
            lines.append(f"**Still growing**: I've been tracking this for {times_mentioned} days now, and it's accelerating. ")
        elif times_mentioned > 0:
            lines.append(f"**Gaining momentum**: Mentioned this {times_mentioned} days ago, and it's still expanding. ")
        else:
            lines.append(f"**New pattern**: This just emerged. ")

        lines.append(f"Today: **{count} projects** in this space.\n\n")

        # Add persona-specific analysis
        if persona_name == 'hype_caster':
            lines.append(f"**Why this is big**: This isn't a fad. When you see {count} independent projects converging on the same problem, that's a signal. The ecosystem is telling us this matters.\n\n")
        elif persona_name == 'mechanic':
            lines.append(f"**Practical impact**: {count} teams are solving this problem because users need it. That's validation.\n\n")
        elif persona_name == 'curious_analyst':
            lines.append(f"**What's interesting**: {count} different approaches to the same challenge. Let's see which architecture wins.\n\n")
        elif persona_name == 'trend_spotter':
            lines.append(f"**The trend**: {count} projects today, ")
            if times_mentioned > 0:
                lines.append(f"up from previous days. ")
            lines.append("This is becoming a category.\n\n")

        # Show examples
        lines.append("**Examples**:\n")
        for item in items[:3]:
            title = item.get('title', 'Unknown')
            url = item.get('url', '#')
            lines.append(f"- [{title}]({url})\n")
        lines.append("\n")

    return "".join(lines)


def generate_insights_section(inferences, persona):
    """Generate deep insights with speculation and analysis"""
    if not inferences:
        return ""

    persona_name, emoji, _ = persona

    intros = {
        'hype_caster': "## 💡 What This Means for the Future\n\nLet me connect the dots and tell you where I think this is heading:\n\n",
        'mechanic': "## 🎯 Practical Takeaways\n\nHere's what you should actually know from today's updates:\n\n",
        'curious_analyst': "## 🧠 Deeper Analysis\n\nLet's think through the implications of what we're seeing:\n\n",
        'trend_spotter': "## 📊 What the Data Tells Us\n\nZooming out, here's what the patterns reveal:\n\n",
        'informed_enthusiast': "## 💡 Key Insights\n\nHere's what I'm taking away from today:\n\n"
    }

    lines = [intros.get(persona_name, intros['informed_enthusiast'])]

    for i, inf in enumerate(inferences[:3], 1):
        pattern = inf.get('pattern', 'Unknown')
        observation = inf.get('observation', '')
        inference = inf.get('inference', '')
        confidence = inf.get('confidence', 'medium')

        clean_pattern = pattern.replace('_', ' ').title()

        lines.append(f"### {i}. {clean_pattern}\n\n")

        # Add persona-specific framing
        if persona_name == 'hype_caster':
            lines.append(f"**The signal**: {observation}\n\n")
            lines.append(f"**Why it matters**: {inference} This could reshape how we think about local AI.\n\n")
            if confidence == "high":
                lines.append("**Confidence level**: High. I'd bet on this.\n\n")
            else:
                lines.append("**Confidence level**: Medium. Worth watching closely.\n\n")

        elif persona_name == 'mechanic':
            lines.append(f"**What's happening**: {observation}\n\n")
            lines.append(f"**Practical impact**: {inference}\n\n")
            if confidence == "high":
                lines.append("This is solid. You can plan around it.\n\n")
            else:
                lines.append("Keep an eye on this, but don't commit yet.\n\n")

        elif persona_name == 'curious_analyst':
            lines.append(f"**Observation**: {observation}\n\n")
            lines.append(f"**Hypothesis**: {inference}\n\n")
            lines.append(f"**Questions to explore**: ")
            if confidence == "high":
                lines.append("How quickly will this become standard? Who benefits most?\n\n")
            else:
                lines.append("Is this sustainable? What are the edge cases?\n\n")

        elif persona_name == 'trend_spotter':
            lines.append(f"**Data point**: {observation}\n\n")
            lines.append(f"**Trend analysis**: {inference}\n\n")
            if confidence == "high":
                lines.append("**Prediction**: This becomes a major category within 3-6 months.\n\n")
            else:
                lines.append("**Prediction**: Too early to call, but the trajectory is interesting.\n\n")

        else:
            lines.append(f"**What I'm seeing**: {observation}\n\n")
            lines.append(f"**What it means**: {inference}\n\n")
            if confidence == "high":
                lines.append("I'm confident about this one.\n\n")
            else:
                lines.append("Still developing, but worth tracking.\n\n")

    return "".join(lines)


def generate_personal_takeaway(aggregated, insights, persona, history):
    """Generate authentic personal reflection with forward-looking action"""
    persona_name, emoji, _ = persona

    lines = ["\n---\n\n## 🎯 The Bottom Line\n\n"]

    # Persona-specific reflections
    reflections = {
        'hype_caster': [
            f"Today reminded me why I'm obsessed with this space. We're watching local AI go from 'interesting experiment' to 'production-ready infrastructure' in real-time. The {len(aggregated)} updates today aren't just incremental—they're foundational.",
            f"Look, I get excited easily. But {len(aggregated)} updates in one day, with at least a few that could change how we build AI applications? That's not hype. That's momentum.",
            f"The pace is accelerating. {len(aggregated)} developments today, and I can already see how they connect to what's coming next. This is the kind of day that makes me want to rebuild everything I'm working on.",
        ],
        'mechanic': [
            f"Here's what matters: {len(aggregated)} updates today, and every single one makes Ollama more reliable, more usable, or more powerful. That's not flashy, but it's exactly what we need.",
            f"I love days like this. No hype, no drama—just {len(aggregated)} solid improvements that make the tools we use every day work better. This is how great software gets built.",
            f"The real story isn't in the headlines. It's in these {len(aggregated)} updates that fix edge cases, improve performance, and make Ollama something you can actually depend on.",
        ],
        'curious_analyst': [
            f"Today's {len(aggregated)} updates raise more questions than they answer—and that's exactly what makes this interesting. We're seeing experimentation at scale.",
            f"What fascinates me about today's {len(aggregated)} discoveries is how they reveal the ecosystem's priorities. People are solving problems we didn't even know we had six months ago.",
            f"I spent today analyzing {len(aggregated)} updates, and the most interesting part isn't what they do—it's why they exist. The use cases are evolving faster than the technology.",
        ],
        'trend_spotter': [
            f"When I look at today's {len(aggregated)} updates alongside the past week's data, a clear picture emerges: the Ollama ecosystem is maturing. We're past the 'proof of concept' phase.",
            f"The {len(aggregated)} updates today fit into larger patterns I've been tracking. This isn't random innovation—it's convergence toward specific, valuable use cases.",
            f"Here's what the data tells me: {len(aggregated)} updates today, but they cluster around 2-3 core themes. That's not coincidence. That's the market speaking.",
        ],
        'informed_enthusiast': [
            f"Another day, another {len(aggregated)} reasons to be excited about local AI. The ecosystem continues to surprise me with its creativity and momentum.",
            f"Today's {len(aggregated)} updates remind me why I track this space obsessively. Every day brings something new, something useful, something that changes what's possible.",
            f"I've been following Ollama for a while now, and days like today—{len(aggregated)} solid updates—show how far we've come and how much further we're going.",
        ]
    }

    lines.append(random.choice(reflections.get(persona_name, reflections['informed_enthusiast'])))
    lines.append("\n\n")

    # Forward-looking action items (persona-specific)
    lines.append("### What I'm Doing Next\n\n")

    actions = {
        'hype_caster': [
            "1. **Test the new models immediately** — I need to see these capabilities firsthand\n",
            "2. **Prototype something ambitious** — The tools are ready; time to push boundaries\n",
            "3. **Share what I learn** — This is too good to keep to myself\n"
        ],
        'mechanic': [
            "1. **Update my local setup** — These improvements are worth integrating now\n",
            "2. **Document what works** — Someone else will hit the same issues I did\n",
            "3. **Contribute back** — Found a bug? File it. Have a fix? Submit it.\n"
        ],
        'curious_analyst': [
            "1. **Dig deeper into the weird stuff** — The experimental projects often reveal future trends\n",
            "2. **Test the edge cases** — Where do these new features break?\n",
            "3. **Write up my findings** — Analysis is only valuable if it's shared\n"
        ],
        'trend_spotter': [
            "1. **Map the connections** — How do today's updates fit into the bigger picture?\n",
            "2. **Predict what's next** — If these are the trends, what comes after?\n",
            "3. **Position accordingly** — Build for where the ecosystem is going, not where it is\n"
        ],
        'informed_enthusiast': [
            "1. **Experiment with today's discoveries** — Theory is great; practice is better\n",
            "2. **Connect with the community** — Someone's already solved the problem I'm thinking about\n",
            "3. **Keep tracking** — Tomorrow will bring more surprises\n"
        ]
    }

    for action in actions.get(persona_name, actions['informed_enthusiast']):
        lines.append(action)

    # Closing
    closings = {
        'hype_caster': "\n\n**See you tomorrow** — and trust me, you'll want to check back. This space moves fast.\n",
        'mechanic': "\n\n**Back tomorrow** with more updates, more fixes, and more reasons to love this ecosystem.\n",
        'curious_analyst': "\n\n**Tomorrow**: More data, more patterns, more questions. That's how we learn.\n",
        'trend_spotter': "\n\n**Tomorrow**: I'll be watching to see if today's patterns hold. Stay tuned.\n",
        'informed_enthusiast': "\n\n**Until tomorrow** — when I'll be back with more discoveries from the Ollama world.\n"
    }

    lines.append(closings.get(persona_name, closings['informed_enthusiast']))

    return "".join(lines)


def generate_headline(aggregated, insights, persona):
    """Generate a compelling, persona-specific headline"""
    persona_name, emoji, _ = persona
    today = get_today_date_str()

    # Analyze content for headline hooks
    has_major_models = any('model' in str(e.get('title', '')).lower() for e in aggregated)
    has_cloud = any('cloud' in str(e).lower() for e in aggregated)
    top_pattern = max(insights.get('patterns', {}).items(), key=lambda x: len(x[1]))[0] if insights.get('patterns') else None

    headlines = {
        'hype_caster': [
            f"Hold On—Today's Ollama Updates Are Genuinely Game-Changing",
            f"The Ollama Ecosystem Just Dropped {len(aggregated)} Updates, and Some Are Huge",
            f"Major Moves in Local AI: {len(aggregated)} Updates That Actually Matter",
        ],
        'mechanic': [
            f"No Flashy Models Today, Just {len(aggregated)} Updates That Make Ollama Better",
            f"The Nuts and Bolts: {len(aggregated)} Ollama Improvements You'll Actually Use",
            f"{len(aggregated)} Solid Updates That Make Your Ollama Workflow Smoother",
        ],
        'curious_analyst': [
            f"So, Someone Just Released Something Interesting in the Ollama World",
            f"{len(aggregated)} Updates Today, and At Least One Made Me Stop and Think",
            f"Let's Unpack Today's {len(aggregated)} Ollama Discoveries",
        ],
        'trend_spotter': [
            f"It's Quiet Today ({len(aggregated)} Updates), So Let's Talk About Patterns",
            f"Connecting the Dots: What {len(aggregated)} Updates Tell Us About Ollama's Future",
            f"The Bigger Picture: {len(aggregated)} Updates and What They Mean",
        ],
        'informed_enthusiast': [
            f"What I Learned Today: {len(aggregated)} Ollama Discoveries Worth Your Time",
            f"Daily Pulse: {len(aggregated)} Updates from the Ollama Ecosystem",
            f"Today in Local AI: {len(aggregated)} Ollama Updates Analyzed",
        ]
    }

    # Add specific hooks if available
    if has_major_models and persona_name == 'hype_caster':
        return f"{emoji} New Models Just Dropped in Ollama—Here's Why They Matter"
    elif top_pattern and persona_name == 'trend_spotter':
        clean_pattern = top_pattern.replace('_', ' ').title()
        return f"{emoji} Pattern Alert: {clean_pattern} Is Becoming a Category in Ollama"

    return f"{emoji} " + random.choice(headlines.get(persona_name, headlines['informed_enthusiast']))


def generate_seo_section(aggregated, insights, persona):
    """Generate SEO-optimized keywords and hashtags section"""
    persona_name, emoji, _ = persona

    # Core keywords that always apply
    keywords = ["Ollama", "LocalAI", "OpenSource", "MachineLearning", "ArtificialIntelligence"]
    hashtags = ["#Ollama", "#LocalAI", "#OpenSourceAI", "#MachineLearning", "#AI"]

    # Extract trending topics from patterns
    patterns = insights.get('patterns', {})
    if patterns:
        for pattern_name, items in patterns.items():
            # Add pattern as keyword and hashtag
            clean_pattern = pattern_name.replace('_', ' ').title().replace(' ', '')
            keywords.append(clean_pattern)
            hashtags.append(f"#{clean_pattern}")

    # Analyze aggregated data for technology keywords
    tech_keywords = set()
    for entry in aggregated[:10]:  # Top 10 items
        summary = entry.get('summary', '').lower()
        title = entry.get('title', '').lower()
        combined = summary + ' ' + title

        # Extract technology-specific keywords
        if 'voice' in combined or 'speech' in combined or 'audio' in combined:
            tech_keywords.add('VoiceAI')
            hashtags.append('#VoiceAI')
        if 'vision' in combined or 'image' in combined or 'visual' in combined:
            tech_keywords.add('ComputerVision')
            hashtags.append('#ComputerVision')
        if 'code' in combined or 'programming' in combined or 'developer' in combined:
            tech_keywords.add('CodeGeneration')
            hashtags.append('#AIcoding')
        if 'chat' in combined or 'conversation' in combined:
            tech_keywords.add('Chatbots')
            hashtags.append('#Chatbots')
        if 'rag' in combined or 'retrieval' in combined:
            tech_keywords.add('RAG')
            hashtags.append('#RAG')
        if 'agent' in combined or 'autonomous' in combined:
            tech_keywords.add('AIAgents')
            hashtags.append('#AIAgents')
        if 'embedding' in combined or 'vector' in combined:
            tech_keywords.add('Embeddings')
            hashtags.append('#VectorDB')
        if 'fine-tun' in combined or 'training' in combined:
            tech_keywords.add('FineTuning')
            hashtags.append('#FineTuning')
        if 'quantiz' in combined:
            tech_keywords.add('Quantization')
            hashtags.append('#Quantization')
        if 'privacy' in combined or 'secure' in combined or 'private' in combined:
            tech_keywords.add('PrivacyFirst')
            hashtags.append('#PrivacyFirst')
        if 'edge' in combined or 'iot' in combined or 'embedded' in combined:
            tech_keywords.add('EdgeAI')
            hashtags.append('#EdgeAI')
        if 'multimodal' in combined:
            tech_keywords.add('MultimodalAI')
            hashtags.append('#MultimodalAI')

    keywords.extend(sorted(tech_keywords))

    # Add persona-specific trending keywords
    if persona_name == 'hype_caster':
        keywords.extend(['Innovation', 'Breakthrough', 'GameChanger'])
        hashtags.extend(['#AIInnovation', '#TechBreakthrough', '#FutureOfAI'])
    elif persona_name == 'mechanic':
        keywords.extend(['Practical', 'Production', 'DevTools'])
        hashtags.extend(['#DevTools', '#ProductionReady', '#PracticalAI'])
    elif persona_name == 'curious_analyst':
        keywords.extend(['Research', 'Experimental', 'Analysis'])
        hashtags.extend(['#AIResearch', '#ExperimentalAI', '#DeepDive'])
    elif persona_name == 'trend_spotter':
        keywords.extend(['Trends', 'Patterns', 'DataDriven'])
        hashtags.extend(['#AITrends', '#TechPatterns', '#DataDriven'])

    # Add current year for freshness
    from datetime import datetime
    current_year = datetime.now().year
    keywords.append(f"AI{current_year}")
    hashtags.append(f"#AI{current_year}")

    # Add general trending AI hashtags
    trending_hashtags = [
        '#GenerativeAI', '#LLM', '#LargeLanguageModels',
        '#AITools', '#AIApplications', '#OpenSourceML',
        '#SelfHosted', '#PrivateAI', '#AIForDevelopers'
    ]
    hashtags.extend(trending_hashtags)

    # Remove duplicates while preserving order
    seen_keywords = set()
    unique_keywords = []
    for kw in keywords:
        if kw.lower() not in seen_keywords:
            seen_keywords.add(kw.lower())
            unique_keywords.append(kw)

    seen_hashtags = set()
    unique_hashtags = []
    for ht in hashtags:
        if ht.lower() not in seen_hashtags:
            seen_hashtags.add(ht.lower())
            unique_hashtags.append(ht)

    # Limit to reasonable numbers for SEO
    keywords = unique_keywords[:20]
    hashtags = unique_hashtags[:25]

    # Format the SEO section
    seo_section = "\n\n---\n\n"
    seo_section += "## 🔍 Keywords & Topics\n\n"
    seo_section += f"**Trending Topics**: {', '.join(keywords)}\n\n"
    seo_section += f"**Hashtags**: {' '.join(hashtags)}\n\n"
    seo_section += "*These keywords and hashtags help you discover related content and connect with the AI community. "
    seo_section += "Share this post using these tags to maximize visibility!*\n"

    return seo_section


def generate_blog_post(aggregated, insights, history):
    """Generate the complete blog post with personality and context"""
    today = get_today_date_str()

    # Detect daily vibe and persona
    persona = detect_daily_vibe(aggregated, insights)
    persona_name, emoji, tone = persona

    # Separate data by source
    official = [e for e in aggregated if e.get('source') in ['blog', 'cloud_page']]
    tools = [e for e in aggregated if e.get('source') in ['github', 'reddit']]
    patterns = insights.get('patterns', {})
    inferences = insights.get('inferences', [])

    # Build the post with personality
    post = generate_opening(aggregated, insights, persona, history) + "\n"
    post += generate_official_section(official, persona)
    post += generate_community_section(tools, persona)
    post += generate_patterns_section(patterns, persona, history)
    post += generate_insights_section(inferences, persona)
    post += generate_personal_takeaway(aggregated, insights, persona, history)

    # Add SEO-optimized keywords and hashtags section
    post += generate_seo_section(aggregated, insights, persona)

    post += "\n---\n\n"
    post += f"*Written by **The Pulse** {emoji} — your enthusiastic guide to the Ollama ecosystem. "
    post += f"Today's persona: **{persona_name.replace('_', ' ').title()}** ({tone}). "
    post += f"Data sourced from [Ollama Pulse](https://grumpified-oggvct.github.io/ollama_pulse).*\n"

    return post, persona


def save_blog_post(post_content, persona, aggregated, insights):
    """Save the blog post with dynamic Jekyll front matter"""
    ensure_posts_dir()
    today = get_today_date_str()
    now = datetime.now()

    persona_name, emoji, tone = persona

    # Generate dynamic headline
    headline = generate_headline(aggregated, insights, persona)

    # Generate tags based on content and persona
    tags = ["ollama", "AI", "daily-pulse", "local-ai"]

    # Add persona-specific tags
    if persona_name == 'hype_caster':
        tags.extend(["new-models", "innovation", "game-changer"])
    elif persona_name == 'mechanic':
        tags.extend(["updates", "improvements", "practical"])
    elif persona_name == 'curious_analyst':
        tags.extend(["analysis", "experimental", "deep-dive"])
    elif persona_name == 'trend_spotter':
        tags.extend(["trends", "patterns", "data-driven"])
    else:
        tags.extend(["insights", "ecosystem-tracking"])

    # Add pattern-based tags
    patterns = insights.get('patterns', {})
    if patterns:
        top_patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)[:2]
        for pattern_name, _ in top_patterns:
            tag = pattern_name.replace('_', '-').lower()
            if tag not in tags:
                tags.append(tag)

    # Jekyll front matter with dynamic headline
    front_matter = f"""---
layout: post
title: "{headline}"
date: {now.strftime('%Y-%m-%d %H:%M:%S %z')}
author: The Pulse {emoji}
tags: {tags}
persona: {persona_name}
tone: {tone}
repo_url: https://github.com/Grumpified-OGGVCT/ollama_pulse
---

"""

    # Save the post
    filename = f"{today}-ollama-daily-learning.md"
    filepath = POSTS_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter + post_content)

    print(f"✅ Blog post saved: {filepath}")
    print(f"📰 Headline: {headline}")
    print(f"🎭 Persona: {persona_name.replace('_', ' ').title()} ({tone})")
    print(f"🏷️  Tags: {', '.join(tags)}")
    return filepath


def main():
    print("🚀 Generating daily blog post with 'The Pulse' persona...")
    print("=" * 60)

    # Check for test mode (date override)
    test_date = None
    if len(sys.argv) > 1:
        test_date = sys.argv[1]
        print(f"🧪 TEST MODE: Using data from {test_date}")
        print()

    # Load data from Ollama Pulse
    aggregated, insights = load_ollama_pulse_data(date_override=test_date)

    if not aggregated and not insights:
        print("⚠️  No Ollama Pulse data available")
        sys.exit(1)

    print(f"📊 Loaded {len(aggregated)} aggregated items")
    print(f"🔍 Loaded {len(insights.get('patterns', {}))} patterns")
    print(f"💡 Loaded {len(insights.get('inferences', []))} inferences")
    print()

    # Load recent history for context
    history = load_recent_history(days=7)
    print(f"📚 Loaded {len(history)} days of history for context")
    print()

    # Generate and save the post
    post_content, persona = generate_blog_post(aggregated, insights, history)
    filepath = save_blog_post(post_content, persona, aggregated, insights)

    print()
    print("=" * 60)
    print(f"✅ Daily blog post generated successfully!")
    print(f"📝 Post: {filepath}")
    print(f"🎭 Today's vibe: {persona[0].replace('_', ' ').title()}")
    print(f"💬 Tone: {persona[2]}")
    print()
    print("The Pulse is live! 🎯")


if __name__ == "__main__":
    main()

