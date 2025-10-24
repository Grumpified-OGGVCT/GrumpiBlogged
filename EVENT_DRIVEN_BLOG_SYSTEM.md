# 🎯 Event-Driven Blog Posting System

**Date**: 2025-10-23  
**Status**: ACTIVE  
**Type**: Smart, data-driven automation

---

## 🌟 **Overview**

GrumpiBlogged now uses an **event-driven system** that detects new data and posts automatically, instead of relying on rigid time gates!

### **Key Features**

✅ **Data-Driven**: Posts when new data is available, not on a fixed schedule  
✅ **Idempotent**: Won't double-post if data already processed  
✅ **Time-Aware**: AI Research Daily prefers morning window (0800-0830 CT)  
✅ **Manual Override**: Manual triggers always work, regardless of time  
✅ **No Time Gates**: Ollama Pulse posts whenever data is ready

---

## 📊 **Two Blog Workflows**

### **1. Ollama Pulse Blog Post** 🔄

**File**: `.github/workflows/ollama-pulse-post.yml`  
**Data Source**: `Grumpified-OGGVCT/ollama_pulse`  
**Schedule**: Every 30 minutes  
**Time Preference**: NONE - posts immediately when data is ready

**How It Works**:
1. Checks every 30 minutes for new data
2. Looks for `ollama_pulse/data/aggregated/YYYY-MM-DD.json`
3. Checks if already posted today (`docs/_posts/YYYY-MM-DD-ollama-pulse.md`)
4. If new data + no post = **POST IMMEDIATELY**
5. Generates post using `scripts/generate_daily_blog.py`

**Post Filename**: `YYYY-MM-DD-ollama-pulse.md`  
**Commit Message**: `feat(pulse): Ollama Pulse - YYYY-MM-DD`

---

### **2. AI Research Daily Blog Post** 📚

**File**: `.github/workflows/daily-learning-post.yml`  
**Data Source**: `AccidentalJedi/AI_Research_Daily`  
**Schedule**: Every 30 minutes during 0700-0900 CT  
**Time Preference**: 0800-0830 CT (soft preference)

**How It Works**:
1. Checks every 30 minutes during morning hours (0700-0900 CT)
2. Looks for `ai_research_daily/data/aggregated/YYYY-MM-DD.json`
3. Checks if already posted today (`docs/_posts/YYYY-MM-DD-ai-research-daily.md`)
4. **If manual trigger**: POST IMMEDIATELY (ignore time)
5. **If scheduled run**: 
   - If 0800-0830 CT: POST IMMEDIATELY
   - If outside window: WAIT for next check
6. Generates post using `scripts/generate_lab_blog.py`

**Post Filename**: `YYYY-MM-DD-ai-research-daily.md`  
**Commit Message**: `feat(lab): AI Research Daily - YYYY-MM-DD`

---

## 🔍 **Smart Detection Logic**

### **Data Detection**

Both workflows check for the existence of today's data file:

```bash
TODAY=$(date -u '+%Y-%m-%d')

# Ollama Pulse
if [ ! -f "ollama_pulse/data/aggregated/${TODAY}.json" ]; then
  echo "No data - skipping"
  exit 0
fi

# AI Research Daily
if [ ! -f "ai_research_daily/data/aggregated/${TODAY}.json" ]; then
  echo "No data - skipping"
  exit 0
fi
```

### **Duplicate Prevention**

Both workflows check if we've already posted today:

```bash
# Ollama Pulse
if [ -f "grumpiblogged/docs/_posts/${TODAY}-ollama-pulse.md" ]; then
  echo "Already posted - skipping"
  exit 0
fi

# AI Research Daily
if [ -f "grumpiblogged/docs/_posts/${TODAY}-ai-research-daily.md" ]; then
  echo "Already posted - skipping"
  exit 0
fi
```

### **Time Preference (AI Research Daily Only)**

```bash
HOUR=$(date +%H)

# Manual trigger = always post
if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
  echo "Manual trigger - posting immediately"
  exit 0
fi

# Scheduled run = prefer 0800-0830 CT
if [ "$HOUR" -ge "8" ] && [ "$HOUR" -le "8" ]; then
  echo "In preferred time window - posting"
else
  echo "Outside preferred time window - waiting"
  exit 0
fi
```

---

## ⏰ **Schedule Breakdown**

### **Ollama Pulse**

```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes, 24/7
```

**Checks**: 48 times per day  
**Posts**: Once per day (when data is ready)

### **AI Research Daily**

```yaml
schedule:
  # 0700-0900 CDT (UTC-5)
  - cron: '0,30 12-14 * * *'
  # 0700-0900 CST (UTC-6)
  - cron: '0,30 13-15 * * *'
```

**Checks**: 6 times per morning (0700, 0730, 0800, 0830, 0900)  
**Posts**: Once per day (preferably 0800-0830 CT)

---

## 🎯 **Typical Daily Flow**

### **Morning Sequence**

**0700 CT**: AI Research Daily workflow checks
- No data yet → Skip

**0730 CT**: AI Research Daily workflow checks
- Data available! But not in preferred window (0800-0830) → Wait

**0800 CT**: AI Research Daily workflow checks
- Data available! In preferred window! → **POST** 📚

**0805 CT**: Ollama Pulse workflow checks
- Data available! No post yet! → **POST** 🔄

**0830 CT**: Both workflows check
- Already posted today → Skip

**Throughout the day**: Workflows continue checking
- Already posted → Skip every time

---

## 🚀 **Manual Triggers**

### **Trigger Ollama Pulse Post**

```bash
gh workflow run ollama-pulse-post.yml --repo Grumpified-OGGVCT/GrumpiBlogged
```

**Result**: Posts immediately if data is available, regardless of time

### **Trigger AI Research Daily Post**

```bash
gh workflow run daily-learning-post.yml --repo Grumpified-OGGVCT/GrumpiBlogged
```

**Result**: Posts immediately if data is available, **ignores time preference**

---

## 📈 **Advantages Over Time Gates**

### **Old System (Time Gates)**

❌ Rigid schedule (must be exactly 16:05 CT)  
❌ Fails if data isn't ready at that exact time  
❌ Can't test outside of scheduled time  
❌ Requires manual intervention if missed  
❌ No awareness of data availability

### **New System (Event-Driven)**

✅ Flexible - posts when data is ready  
✅ Resilient - keeps checking until data appears  
✅ Testable - manual triggers work anytime  
✅ Self-healing - automatically catches up  
✅ Data-aware - knows when to post

---

## 🔧 **Configuration**

### **Adjust Check Frequency**

**Ollama Pulse** (currently every 30 minutes):
```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes
  # OR
  - cron: '0 * * * *'     # Every hour
  # OR
  - cron: '*/15 * * * *'  # Every 15 minutes
```

**AI Research Daily** (currently 0700-0900 CT):
```yaml
schedule:
  # Check every 15 minutes during morning
  - cron: '*/15 12-14 * * *'  # 0700-0900 CDT
  - cron: '*/15 13-15 * * *'  # 0700-0900 CST
```

### **Adjust Time Preference**

Change the preferred posting window for AI Research Daily:

```bash
# Current: 0800-0830 CT
if [ "$HOUR" -ge "8" ] && [ "$HOUR" -le "8" ]; then

# Example: 0700-0900 CT
if [ "$HOUR" -ge "7" ] && [ "$HOUR" -le "9" ]; then

# Example: Any time
# (Just remove the time check entirely)
```

---

## 📊 **Monitoring**

### **Check Workflow Runs**

```bash
# Ollama Pulse posts
gh run list --workflow=ollama-pulse-post.yml --repo Grumpified-OGGVCT/GrumpiBlogged

# AI Research Daily posts
gh run list --workflow=daily-learning-post.yml --repo Grumpified-OGGVCT/GrumpiBlogged
```

### **Check Recent Posts**

```bash
# List recent blog posts
ls -lt grumpiblogged_work/docs/_posts/ | head -10

# Check today's posts
TODAY=$(date '+%Y-%m-%d')
ls grumpiblogged_work/docs/_posts/${TODAY}-*.md
```

---

## 🎊 **Benefits**

1. **Automatic**: No manual intervention needed
2. **Reliable**: Won't miss posts if data is delayed
3. **Efficient**: Only posts when new data is available
4. **Flexible**: Easy to test and debug
5. **Smart**: Respects time preferences but doesn't block

---

## 📝 **Files Modified**

1. `.github/workflows/daily-learning-post.yml` - AI Research Daily (event-driven)
2. `.github/workflows/ollama-pulse-post.yml` - Ollama Pulse (NEW, event-driven)

---

## 🔗 **Related Documentation**

- `PIPELINE_TEST_RESULTS.md` - Test results and fixes
- `FIXES_APPLIED_SUMMARY.md` - Summary of all fixes
- `QUICK_FIX_GUIDE.md` - Quick reference

---

**System Status**: ✅ ACTIVE  
**Last Updated**: 2025-10-23  
**Next Review**: After first week of automated posts

