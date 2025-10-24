# 🚀 Quick Start Guide - Enhanced Blog System

**Get up and running in 5 minutes!**

---

## 📋 **Prerequisites**

- Python 3.11+
- Git
- GitHub account with GrumpiBlogged repository access

---

## ⚡ **Quick Setup** (5 minutes)

### **Step 1: Install Dependencies** (1 minute)

```bash
cd grumpiblogged_work
pip install -r requirements.txt
```

**What this installs**:
- `plotly` - Chart generation
- `Jinja2` - Template engine
- `requests` - API calls
- `python-dateutil` - Date handling

---

### **Step 2: Test Memory System** (1 minute)

```bash
# Test Ollama Pulse memory
python scripts/memory_manager.py ollama-pulse

# Test AI Research Daily memory
python scripts/memory_manager.py ai-research-daily
```

**Expected output**:
```
📊 Memory Status for ollama-pulse
Total posts in memory: 0
Last run: Never

**Recent Post History:**
No prior context available.
```

---

### **Step 3: Test Chart Generation** (1 minute)

```bash
python scripts/chart_generator.py
```

**Expected output**:
```
📊 Generating test charts...
✅ Tag trends chart: test_tag_trends.html
✅ Model counts chart: test_model_counts.html

🎉 Chart generation complete!
```

Open the HTML files in your browser to see the charts!

---

### **Step 4: Test Personality System** (1 minute)

```bash
python scripts/personality.py
```

**Expected output**:
```
🎭 Testing Personality System

============================================================
Persona: Hype Caster
============================================================

Jokes (8):
  - llm-latté
  - gpu-golf
  - neural-network-ninja

Anecdotes (4):
  - My 4-year-old asked if AI dreams of electric sheep...
  - Remember when we thought 7B was big?

[... more personas ...]

🎉 Personality system loaded successfully!
```

---

### **Step 5: Test Post Validation** (1 minute)

```bash
# Create a test post
echo "---
layout: post
title: Test Post
---

## Test Content

This is a test post with enough content to pass validation.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
" > test_post.md

# Test validation
python scripts/should_post.py test_post.md ollama-pulse
```

**Expected output**:
```
✅ SHOULD POST: Content is unique and ready to post

📊 Memory Context:
**Recent Post History:**
No prior context available.
```

---

## 🎯 **Usage Examples**

### **Generate a Blog Post with Memory**

```bash
# Ollama Pulse
python scripts/generate_daily_blog.py

# AI Research Daily
python scripts/generate_lab_blog.py
```

**What happens**:
1. ✅ Loads memory (past posts, joke blacklist)
2. ✅ Displays context summary
3. ✅ Generates post with awareness of history
4. ✅ Saves post to `docs/_posts/`

---

### **Check if Post Should Be Published**

```bash
python scripts/should_post.py draft.md ollama-pulse
```

**Exit codes**:
- `0` = Should post (unique, valid)
- `1` = Should NOT post (duplicate or invalid)

---

### **Update Memory After Publishing**

```bash
python scripts/append_memory.py ollama-pulse 2025-10-23 test-post docs/_posts/2025-10-23-ollama-pulse.md
```

**What happens**:
1. ✅ Extracts tone words from post
2. ✅ Extracts jokes/phrases from post
3. ✅ Generates SHA256 fingerprint
4. ✅ Saves to memory JSON
5. ✅ Keeps last 30 posts

---

### **Generate Charts from Historical Data**

```python
from chart_generator import *
from pathlib import Path

# Extract data
posts_dir = Path("docs/_posts")
tag_history = extract_tag_history_from_posts(posts_dir, days=7)
model_counts = extract_model_counts_from_posts(posts_dir, days=7)

# Generate charts
tag_chart_html = create_tag_trend_chart(tag_history)
model_chart_html = create_model_count_chart(model_counts)

# Save or embed in post
Path("tag_trends.html").write_text(tag_chart_html)
```

---

### **Use Personality System**

```python
from personality import *

# Get jokes for a persona
jokes = get_persona_jokes('hype_caster')
print(jokes)  # ['llm-latté', 'gpu-golf', ...]

# Select a fresh joke (not in blacklist)
blacklist = {'llm-latté', 'gpu-golf'}
fresh_joke = select_fresh_joke('hype_caster', blacklist)
print(fresh_joke)  # 'neural-network-ninja'

# Get anecdotes
anecdotes = get_persona_anecdotes('scholar')
print(anecdotes[0])  # "As my advisor used to say..."
```

---

## 🔄 **Complete Workflow**

### **Manual Post Generation**

```bash
# 1. Generate post
python scripts/generate_daily_blog.py > draft.md

# 2. Validate post
if python scripts/should_post.py draft.md ollama-pulse; then
    # 3. Publish post
    TODAY=$(date +%Y-%m-%d)
    cp draft.md docs/_posts/${TODAY}-ollama-pulse.md
    
    # 4. Update memory
    python scripts/append_memory.py ollama-pulse ${TODAY} ollama-pulse-${TODAY} docs/_posts/${TODAY}-ollama-pulse.md
    
    # 5. Commit
    git add docs/_posts/ data/memory/
    git commit -m "feat(pulse): Ollama Pulse - ${TODAY}"
    git push
else
    echo "⛔ Post blocked (duplicate or quality issue)"
fi
```

---

## 🐛 **Troubleshooting**

### **Problem: "Module not found: memory_manager"**

**Solution**:
```bash
# Make sure you're in the grumpiblogged_work directory
cd grumpiblogged_work

# Run from scripts directory
cd scripts
python memory_manager.py ollama-pulse
```

---

### **Problem: "No module named 'plotly'"**

**Solution**:
```bash
pip install plotly
```

---

### **Problem: "Memory file not found"**

**Solution**:
```bash
# Initialize memory files
mkdir -p data/memory

cat > data/memory/ollama-pulse_memory.json << 'EOF'
{
  "workflow": "ollama-pulse",
  "last_run": null,
  "post_history": []
}
EOF

cat > data/memory/ai-research-daily_memory.json << 'EOF'
{
  "workflow": "ai-research-daily",
  "last_run": null,
  "post_history": []
}
EOF
```

---

### **Problem: "Duplicate content detected"**

**Solution**:
This is working as intended! The memory system is preventing duplicate posts.

To override (for testing):
```bash
# Clear memory
echo '{"workflow": "ollama-pulse", "last_run": null, "post_history": []}' > data/memory/ollama-pulse_memory.json
```

---

## 📚 **Documentation**

- **Memory System**: `MEMORY_SYSTEM_IMPLEMENTATION.md`
- **Complete Plan**: `COMPLETE_ENHANCEMENT_PLAN.md`
- **Implementation Summary**: `COMPLETE_IMPLEMENTATION_SUMMARY.md`
- **Feature Comparison**: `BLOG_GENERATOR_COMPARISON.md`

---

## 🎯 **Next Steps**

1. ✅ Install dependencies
2. ✅ Test all systems
3. ⏳ Integrate charts into generators
4. ⏳ Integrate personality into generators
5. ⏳ Integrate templates into generators
6. ⏳ Run end-to-end test
7. ⏳ Commit and push

---

## 🎊 **You're Ready!**

All systems are implemented and tested. Time to integrate and deploy! 🚀

**Questions?** Check the documentation files or run the test scripts.

**Happy blogging!** 📝

