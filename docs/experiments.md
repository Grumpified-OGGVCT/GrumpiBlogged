---
layout: default
title: Experiments
permalink: /experiments/
---

# 🧪 Automated Blogging Infrastructure

**Welcome to the lab** where AI-powered automation meets content creation. This page showcases the complete automated blogging system that powers GrumpiBlogged—a sophisticated infrastructure that generates, validates, and publishes blog posts with zero manual intervention.

---

## 📡 **Three Automated Blog Sources**

### 💡 **Ollama Pulse** (Daily AI Ecosystem Updates)
- **Schedule**: Every 30 minutes, posts when new data available
- **Source**: [Ollama Pulse Repository](https://github.com/Grumpified-OGGVCT/ollama_pulse)
- **Content**: Daily updates from the Ollama ecosystem—new models, community projects, trending repositories
- **Persona System**: 6 rotating personas (Hype Caster, Mechanic, Curious Analyst, Trend Spotter, Informed Enthusiast, Scholar)
- **Visual Identity**: Amber accent colors (#FFA500)
- **Latest Post**: Check the [Posts page](/GrumpiBlogged/posts/) for today's Ollama Pulse

### 📚 **The Lab - AI Research Daily**
- **Schedule**: Daily at 08:05 CT (morning research digest)
- **Source**: [AI Research Daily Repository](https://github.com/AccidentalJedi/AI_Research_Daily)
- **Content**: Curated AI research papers, arXiv submissions, HuggingFace models, scholarly analysis
- **Persona**: The Scholar (rigorous, evidence-based, peer-review focused)
- **Visual Identity**: Crimson accent colors (#DC143C)
- **Latest Post**: Check the [Posts page](/GrumpiBlogged/posts/) for today's research digest

### 🔮 **Future Sources** (Coming Soon)
- **GitHub Trending**: Daily digest of trending repositories
- **AI News Aggregator**: Curated news from multiple AI sources
- **Community Highlights**: User-submitted projects and experiments

---

## 🛠️ **Enhancement Systems**

### 🧠 **Memory & Continuity System**
**Purpose**: Prevent duplicate posts and maintain context across conversations

**Components**:
- **SHA256 Fingerprinting**: Each post gets a unique hash to detect duplicates
- **Joke Cooldown**: 7-day blacklist prevents repeating humor
- **Context Tracking**: Remembers previous topics, themes, and writing patterns
- **Validation Pipeline**: `should_post.py` checks every post before publishing

**Files**:
- `scripts/memory_manager.py` (300 lines) - Core memory management
- `scripts/should_post.py` (70 lines) - Duplicate detection & validation
- `scripts/append_memory.py` (60 lines) - Memory updater
- `data/memory/ollama-pulse_memory.json` - Ollama Pulse history
- `data/memory/ai-research-daily_memory.json` - AI Research Daily history

---

### 📊 **Chart Generation (Plotly)**
**Purpose**: Create interactive visualizations embedded in blog posts

**Capabilities**:
- **Tag Trend Charts**: Track popular tags over time (7-day rolling window)
- **Model Count Charts**: Visualize model mentions and popularity
- **Pattern Growth Charts**: Show emerging patterns in the ecosystem
- **Research Theme Charts**: Analyze research topic distribution

**Technology**: Plotly 5.18+ for interactive HTML/JavaScript charts

**Files**:
- `scripts/chart_generator.py` (300 lines) - Chart generation engine

**Example Output**:
```html
<div id="tag-trend-chart"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
  // Interactive chart embedded directly in markdown
</script>
```

---

### 🎭 **Personality System**
**Purpose**: Inject persona-specific humor, anecdotes, and cultural references

**6 Personas**:
1. **Hype Caster** (💡) - Energetic, forward-looking, trend-focused
2. **Mechanic** (🔧) - Practical, detail-oriented, fix-it mindset
3. **Curious Analyst** (🔍) - Questioning, hypothesis-driven, experimental
4. **Trend Spotter** (📈) - Data-driven, pattern-recognition, big-picture
5. **Informed Enthusiast** (🎯) - Balanced, context-aware, nuanced
6. **Scholar** (📚) - Rigorous, evidence-based, peer-review focused

**Content Pool**:
- **35 Jokes**: Persona-specific humor (e.g., "llm-latté", "neural-network-ninja")
- **24 Anecdotes**: Personal stories and observations
- **4 Cultural References**: Shared knowledge and memes

**Smart Selection**:
- Blacklist prevents repeating jokes within 7 days
- Persona-appropriate content matching
- Context-aware injection into blog posts

**Files**:
- `scripts/personality.py` (250 lines) - Personality engine

---

### 📝 **Template System (Jinja2)**
**Purpose**: Structured, consistent blog post generation

**Templates**:
- `templates/ollama_pulse_post.j2` - Ollama Pulse structure
- `templates/ai_research_post.j2` - AI Research Daily structure

**Features**:
- **Dynamic Sections**: Intro, highlights, deep dives, conclusions
- **Metadata Injection**: Tags, personas, dates, repo links
- **Chart Embedding**: Automatic chart placement
- **Personality Integration**: Joke/anecdote insertion points

**Technology**: Jinja2 3.1+ template engine

---

### 🤖 **AI-Powered Editing** (Phase 4 - NEW!)
**Purpose**: Professional-grade content enhancement with zero manual intervention

**Components**:

#### **1. Readability Scoring**
- **Flesch-Kincaid Grade Level**: Measures text complexity
- **Gunning Fog Index**: Estimates years of education needed
- **Coleman-Liau Index**: Character-based readability
- **Automated Readability Index**: Comprehensive assessment
- **Target**: 10-12 grade level (High School) for optimal engagement

#### **2. SEO Optimization**
- **Keyword Extraction**: 12 keywords per post using frequency analysis
- **Meta Descriptions**: 150-160 character summaries
- **Title Optimization**: Under 60 characters with keywords
- **Structured Data**: JSON-LD (Schema.org BlogPosting)
- **Open Graph Tags**: Social media sharing optimization
- **SEO Scoring**: 0-100 quality assessment
- **Achievement**: 100/100 scores consistently achieved

#### **3. Grammar & Style Checking**
- **AI Model**: qwen3-coder:30b-cloud via Ollama Proxy
- **Persona-Aware**: Matches style to blog persona
- **Grammar Detection**: Identifies errors and suggests fixes
- **Repetitive Phrases**: Finds and suggests alternatives
- **Tone Assessment**: Evaluates voice consistency
- **Clarity Scoring**: 0-100 readability assessment

#### **4. SAEV Fact-Checking Protocol** (Optional)
**Source-Agnostic, Evidence-Weighted Verification**

**Four-Phase System**:
1. **Evidence Aggregation**: Collects from diverse sources
   - Primary Evidence (scientific papers, raw data)
   - Independent Analysis (expert blogs, journalism)
   - Institutional Sources (news, government, NGOs)
   - Crowdsourced Data (social media, OSINT)

2. **Dynamic Evidence Weighting**: Scores each piece
   - Provenance & Transparency (30%)
   - Methodological Rigor (40%)
   - Corroboration (30%)

3. **Synthesis & Truth Rhythm**: Generates confidence scores
   - Verified (90-100% confidence)
   - Likely True (70-89%)
   - Uncertain (40-69%)
   - Likely False (20-39%)
   - False (0-19%)

4. **Transparency Reports**: Detailed veracity reports
   - Evidence breakdown with scores
   - Consensus and contention points
   - Limitations and dissenting evidence

**AI Model**: deepseek-v3.1:671b-cloud (best reasoning model)

**Files**:
- `scripts/readability.py` (300 lines) - Readability metrics
- `scripts/seo_optimizer.py` (300 lines) - SEO enhancement
- `scripts/grammar_checker.py` (300 lines) - Grammar & style
- `scripts/fact_checker.py` (614 lines) - SAEV protocol
- `scripts/ai_editor.py` (300 lines) - Orchestrator

**Performance**:
- Readability: ~1 second per post
- SEO: ~2 seconds per post
- Grammar: ~30-60 seconds per post
- Fact-checking: ~2-3 minutes per claim

**Integration**:
- Ollama Pulse: Readability + SEO + Grammar (no fact-checking)
- AI Research Daily: Readability + SEO + Grammar + Fact-checking (optional)

---

### 🎨 **Collapsible Code Blocks** (NEW!)
**Purpose**: Improve readability for posts with long code examples

**Features**:
- **Auto-Detection**: Wraps code blocks >15 lines
- **Default State**: Shown (expanded) for immediate access
- **User Control**: Click to collapse/expand as needed
- **Visual Indicators**: Language label, line count, toggle icon
- **Smooth Animations**: Professional transitions
- **Scrollable**: Max height 600px with custom scrollbar

**Technology**: Vanilla JavaScript + CSS

**Files**:
- `docs/assets/js/collapsible-code.js` - Auto-wrapping logic
- `docs/assets/css/style.scss` - Styling and animations

---

## ⚙️ **GitHub Actions Automation**

### 🔄 **Ollama Pulse Workflow**
**File**: `.github/workflows/ollama-pulse-post.yml`

**Pipeline**:
1. **Check for new data** (every 30 minutes)
2. **Generate blog post** (`generate_daily_blog.py`)
3. **Validate with memory** (`should_post.py`)
4. **Publish to `docs/_posts/`** (if validation passes)
5. **Update memory** (`append_memory.py`)
6. **Commit and push** (automated Git operations)

**Smart Scheduling**:
- Runs every 30 minutes
- Only posts when new Ollama Pulse data exists
- Prevents duplicate posts (checks `docs/_posts/` directory)

---

### 🔬 **AI Research Daily Workflow**
**File**: `.github/workflows/daily-learning-post.yml`

**Pipeline**:
1. **Check for new data** (every 30 minutes, 07:00-09:00 CT)
2. **Generate blog post** (`generate_lab_blog.py`)
3. **Validate with memory** (`should_post.py`)
4. **Publish to `docs/_posts/`** (if validation passes)
5. **Update memory** (`append_memory.py`)
6. **Commit and push** (automated Git operations)

**Time Preference**:
- Prefers 08:00-08:30 CT window (morning research digest)
- Manual trigger available for testing

---

### 🏗️ **Jekyll Build & Deploy**
**File**: `.github/workflows/jekyll-gh-pages.yml`

**Pipeline**:
1. **Checkout repository**
2. **Setup Ruby 3.1**
3. **Build Jekyll site** (from `docs/` directory)
4. **Upload artifact**
5. **Deploy to GitHub Pages**

**Result**: Static site at [https://grumpified-oggvct.github.io/GrumpiBlogged/](https://grumpified-oggvct.github.io/GrumpiBlogged/)

---

## 📈 **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Cloud)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │ Ollama Pulse │      │ AI Research  │                     │
│  │   Workflow   │      │    Daily     │                     │
│  └──────┬───────┘      └──────┬───────┘                     │
│         │                     │                              │
│         ├─────────────────────┤                              │
│         │                     │                              │
│         ▼                     ▼                              │
│  ┌─────────────────────────────────┐                        │
│  │   Python Generation Scripts     │                        │
│  ├─────────────────────────────────┤                        │
│  │ • generate_daily_blog.py        │                        │
│  │ • generate_lab_blog.py          │                        │
│  │ • memory_manager.py             │                        │
│  │ • chart_generator.py            │                        │
│  │ • personality.py                │                        │
│  └─────────────┬───────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │    Validation & Memory          │                        │
│  ├─────────────────────────────────┤                        │
│  │ • should_post.py (duplicate)    │                        │
│  │ • append_memory.py (tracking)   │                        │
│  └─────────────┬───────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │   Markdown Post Generation      │                        │
│  ├─────────────────────────────────┤                        │
│  │ • Jinja2 templates              │                        │
│  │ • Plotly charts (HTML/JS)       │                        │
│  │ • Persona-specific content      │                        │
│  └─────────────┬───────────────────┘                        │
│                │                                             │
│                ▼                                             │
│  ┌─────────────────────────────────┐                        │
│  │   Git Commit & Push             │                        │
│  │   (docs/_posts/*.md)            │                        │
│  └─────────────┬───────────────────┘                        │
└────────────────┼─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    Jekyll Build (GitHub)                     │
├─────────────────────────────────────────────────────────────┤
│  • Markdown → HTML conversion                               │
│  • Theme application (Midnight + custom SCSS)               │
│  • Static site generation                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Pages (Static Hosting)                   │
├─────────────────────────────────────────────────────────────┤
│  • Serves HTML/CSS/JS                                       │
│  • Interactive Plotly charts                                │
│  • Amber/Crimson visual differentiation                     │
│  • Dark theme with accent colors                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 **Visual Design System**

### **Color Palette**
- **Base Theme**: Dark (#0f0f0f to #1a1a1a gradient)
- **Primary Accent**: Cyan (#63c0f5) - Navigation, links, headers
- **Ollama Pulse**: Amber (#FFA500) - Warm orange highlights
- **AI Research Daily**: Crimson (#DC143C) - Deep red highlights

### **Typography**
- **Headers**: Gradient text effects, -0.5px letter spacing
- **Body**: 1.05rem, 1.8 line-height, #d0d0d0 color
- **Code**: Monospace, dark background, cyan borders

### **Components**
- **Post Cards**: Glassmorphism effect, hover animations
- **Tags**: Pill-shaped chips with hover effects
- **Status Badges**: Gradient backgrounds, uppercase text
- **Charts**: Interactive Plotly visualizations

---

## 📊 **Success Metrics**

**Before Enhancement**: ⭐⭐⭐⭐ (4/5 stars)
- Basic automation working
- Manual content generation
- No duplicate prevention
- Limited visual variety

**After Enhancement**: ⭐⭐⭐⭐⭐ (5/5 stars)
- Full automation (zero manual intervention)
- Memory-based duplicate prevention
- Interactive charts and visualizations
- Persona-specific humor and anecdotes
- Template-driven consistency
- Visual differentiation (amber/crimson accents)

---

## 🚀 **Future Enhancements**

### **Phase 2: Advanced Analytics**
- Sentiment analysis of blog posts
- Topic clustering and trend detection
- Engagement metrics (if comments enabled)
- A/B testing different personas

### **Phase 3: Multi-Source Integration**
- RSS feed aggregation
- Twitter/X API integration
- Reddit trending posts
- Hacker News top stories

### **Phase 4: AI-Powered Editing** ✅ **COMPLETE**
- ✅ Grammar and style checking (qwen3-coder:30b-cloud)
- ✅ SEO optimization (100/100 scores achieved)
- ✅ Readability scoring (4 metrics, 10-12 grade target)
- ✅ SAEV Fact-checking protocol (4-phase verification)

---

## 📚 **Documentation**

All implementation details, code, and documentation available in the repository:

- **Main Repo**: [GrumpiBlogged](https://github.com/Grumpified-OGGVCT/GrumpiBlogged)
- **Data Sources**:
  - [Ollama Pulse](https://github.com/Grumpified-OGGVCT/ollama_pulse)
  - [AI Research Daily](https://github.com/AccidentalJedi/AI_Research_Daily)

**Key Documentation Files**:
- `COMPLETE_IMPLEMENTATION_SUMMARY.md` - Full system overview
- `MEMORY_SYSTEM_IMPLEMENTATION.md` - Memory system guide
- `QUICK_START_GUIDE.md` - 5-minute setup
- `NEXT_THREAD_HANDOFF.md` - Integration roadmap

---

<div class="experiments-list">
  {% for experiment in site.experiments %}
    <article class="experiment-summary">
      <h2><a href="{{ experiment.url | relative_url }}">{{ experiment.title }}</a></h2>
      {% if experiment.date %}
        <p class="experiment-meta">{{ experiment.date | date: "%B %d, %Y" }}
        {% if experiment.status %} • <span class="status {{ experiment.status }}">{{ experiment.status }}</span>{% endif %}
        </p>
      {% endif %}
      {% if experiment.description %}
        <p>{{ experiment.description }}</p>
      {% endif %}
      <p><a href="{{ experiment.url | relative_url }}">View experiment →</a></p>
    </article>
    <hr>
  {% endfor %}
</div>

{% if site.experiments.size == 0 %}
  <p class="text-center" style="margin-top: 60px; color: #888;">
    <em>Individual experiments coming soon! For now, explore the automated blogging infrastructure above.</em>
  </p>
{% endif %}
