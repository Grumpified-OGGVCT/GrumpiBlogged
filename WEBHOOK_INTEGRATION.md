# GrumpiBlogged - Webhook Integration Guide

This guide explains how to set up repository dispatch webhooks from the three source repositories to trigger automated blog post generation in GrumpiBlogged.

## Overview

GrumpiBlogged automatically transforms technical reports from three source repositories into humanized, engaging blog posts with distinct author personalities:

| Source Repository | Author Persona | Emoji | Characteristics | Post Time (CT) |
|-------------------|----------------|-------|-----------------|----------------|
| [ollama_pulse](https://github.com/Grumpified-OGGVCT/ollama_pulse) | **The Pulse** 🎯 | Dynamic (5 personas) | Enthusiastic, deeply-embedded guide to local AI | 08:00-08:30 |
| [AI_Research_Daily](https://github.com/AccidentalJedi/AI_Research_Daily) | **The Scholar** 📚 | Consistent | Rigorous, accessible academic voice | 08:00-08:30 |
| [idea_vault](https://github.com/Grumpified-OGGVCT/idea_vault) | **The Visionary** 💡 | Forward-thinking | Creative, practical dreamer bridging ideation and execution | 14:00-15:00 |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Source Repositories (Generate Raw Reports)                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ollama_pulse │  │AI_Research   │  │ idea_vault   │      │
│  │              │  │  _Daily      │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         │ (1) Generate    │ (1) Generate    │ (1) Generate │
│         │     Report      │     Report      │     Report   │
│         │                 │                 │              │
│         │ (2) Send        │ (2) Send        │ (2) Send     │
│         │  repository     │  repository     │  repository  │
│         │  _dispatch      │  _dispatch      │  _dispatch   │
│         │                 │                 │              │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│  GrumpiBlogged (Humanization & Publishing)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ollama-pulse │  │ daily-learning│  │ idea-vault   │      │
│  │  -post.yml   │  │  -post.yml   │  │  -post.yml   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         │ (3) Fetch       │ (3) Fetch       │ (3) Fetch    │
│         │     /docs       │     /docs       │     /docs    │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ generate_    │  │ generate_    │  │ generate_    │      │
│  │ daily_blog   │  │ lab_blog     │  │ idea_vault_  │      │
│  │   .py        │  │   .py        │  │  blog.py     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         │ (4) Humanize    │ (4) Humanize    │ (4) Humanize │
│         │  with persona   │  with persona   │  with persona│
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────────────────────────────────────────┐       │
│  │       AI Editor (SEO, Grammar, Readability)     │       │
│  └─────────────────────────────────────────────────┘       │
│         │                 │                 │              │
│         ▼                 ▼                 ▼              │
│  ┌─────────────────────────────────────────────────┐       │
│  │          docs/_posts/YYYY-MM-DD-*.md            │       │
│  └─────────────────────────────────────────────────┘       │
│         │                 │                 │              │
│         │ (5) Commit      │ (5) Commit      │ (5) Commit   │
│         │     and Push    │     and Push    │     and Push │
│         │                 │                 │              │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
    GitHub Pages (Jekyll) - Published Blog Posts
```

## Setting Up Webhooks

### Step 1: Create GitHub Personal Access Token (PAT)

**For source repository owners:**

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: `grumpiblogged-webhook`
4. Expiration: No expiration (or 1 year with renewal reminder)
5. Scopes required:
   - ✅ `repo` (all)
   - ✅ `workflow`
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again)

### Step 2: Configure Source Repository

**For each source repository (ollama_pulse, AI_Research_Daily, idea_vault):**

#### 2.1 Add GitHub Secret

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GRUMPIBLOGGED_DISPATCH_TOKEN`
4. Value: Paste the PAT from Step 1
5. Click "Add secret"

#### 2.2 Add Dispatch Step to Workflow

Add this step to the **end** of your existing workflow (after report generation):

**For ollama_pulse:**
```yaml
- name: Trigger GrumpiBlogged
  if: success()  # Only trigger if previous steps succeeded
  run: |
    curl -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.GRUMPIBLOGGED_DISPATCH_TOKEN }}" \
      https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
      -d '{"event_type":"ollama-pulse-update","client_payload":{"date":"'$(date -u '+%Y-%m-%d')'","repository":"ollama_pulse"}}'
```

**For AI_Research_Daily:**
```yaml
- name: Trigger GrumpiBlogged
  if: success()
  run: |
    curl -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.GRUMPIBLOGGED_DISPATCH_TOKEN }}" \
      https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
      -d '{"event_type":"ai-research-daily-update","client_payload":{"date":"'$(date -u '+%Y-%m-%d')'","repository":"AI_Research_Daily"}}'
```

**For idea_vault:**
```yaml
- name: Trigger GrumpiBlogged
  if: success()
  run: |
    curl -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.GRUMPIBLOGGED_DISPATCH_TOKEN }}" \
      https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
      -d '{"event_type":"idea-vault-update","client_payload":{"date":"'$(date -u '+%Y-%m-%d')'","repository":"idea_vault"}}'
```

### Step 3: Expected Data Structure

Each source repository should publish reports to the `/docs` folder with this structure:

**Directory Structure:**
```
source-repo/
└── docs/
    └── YYYY-MM-DD.json          # Daily report file
```

**JSON Format:**
```json
{
  "findings": [
    {
      "title": "...",
      "url": "...",
      "summary": "...",
      "highlights": [...],
      "source": "...",
      "timestamp": "..."
    }
  ],
  "insights": {
    "patterns": {...},
    "themes": [...]
  }
}
```

Alternative paths that are also checked:
- `data/YYYY-MM-DD.json`
- `data/aggregated/YYYY-MM-DD.json`
- `docs/reports/YYYY-MM-DD.json`

## Testing the Integration

### Manual Testing

1. **Test from source repository:**
   ```bash
   # Set your PAT
   export GITHUB_TOKEN="your-pat-here"
   
   # Trigger dispatch
   curl -X POST \
     -H "Accept: application/vnd.github+json" \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
     -d '{"event_type":"ollama-pulse-update","client_payload":{"date":"2025-01-15","repository":"ollama_pulse"}}'
   ```

2. **Monitor GrumpiBlogged:**
   - Go to GrumpiBlogged repository → Actions tab
   - Watch for workflow run to start
   - Check logs for any errors

3. **Verify output:**
   - Check `docs/_posts/` for new blog post
   - Verify formatting and persona voice
   - Check memory system was updated

### Automated Testing

GrumpiBlogged workflows can also be triggered manually:

1. Go to GrumpiBlogged → Actions
2. Select the workflow (e.g., "Ollama Pulse Blog Post")
3. Click "Run workflow"
4. Select branch and run

## Workflow Files

### GrumpiBlogged Workflows

| Workflow | Trigger Event | Generator Script | Author |
|----------|---------------|------------------|--------|
| `.github/workflows/ollama-pulse-post.yml` | `ollama-pulse-update` | `scripts/generate_daily_blog.py` | The Pulse 🎯 |
| `.github/workflows/daily-learning-post.yml` | `ai-research-daily-update` | `scripts/generate_lab_blog.py` | The Scholar 📚 |
| `.github/workflows/idea-vault-post.yml` | `idea-vault-update` | `scripts/generate_idea_vault_blog.py` | The Visionary 💡 |

### Scheduled Fallback

All workflows also run on schedule as a fallback:
- **ollama_pulse**: Every 30 minutes (detects new data automatically)
- **AI_Research_Daily**: 07:00-09:00 CT
- **idea_vault**: 14:00-16:00 CT

This ensures posts are generated even if the webhook fails.

## Author Personalities

### The Pulse (ollama_pulse) 🎯

**Dynamic 5-Persona System:**
- **Hype-Caster** 💡: Major model drops → energetic, forward-looking
- **The Mechanic** 🛠️: Bug fixes/updates → grounded, appreciative, practical
- **Curious Analyst** 🤔: Experimental → inquisitive, analytical
- **Trend-Spotter** 📈: Slow news → reflective, data-driven
- **Informed Enthusiast** 🎯: Balanced → insightful

### The Scholar (AI_Research_Daily) 📚

**Consistent Academic Voice:**
- Rigorous but accessible
- Contextual: Places research in broader context
- Measured: Avoids hype, focuses on evidence
- Pedagogical: Teaches readers how to think about research
- Humble: Acknowledges uncertainty and limitations

### The Visionary (idea_vault) 💡

**Forward-Thinking Innovation:**
- Creative: Combines ideas in novel ways
- Practical dreamer: Balances vision with reality
- Thought-provoking: Challenges assumptions
- Connective: Links disparate concepts
- Inspiring: Motivates readers to think bigger

## Troubleshooting

### Webhook Not Firing

1. **Check PAT permissions:**
   - Must have `repo` and `workflow` scopes
   - Must not be expired

2. **Check secret name:**
   - Must be exactly `GRUMPIBLOGGED_DISPATCH_TOKEN`

3. **Check event type:**
   - Must match exactly: `ollama-pulse-update`, `ai-research-daily-update`, or `idea-vault-update`

### Workflow Not Running

1. **Check workflow file:**
   - Must be in `.github/workflows/` directory
   - YAML syntax must be valid

2. **Check repository permissions:**
   - Actions must be enabled
   - Workflow must have `contents: write` permission

3. **Check data availability:**
   - Source repository must have data file for today
   - Data must be in expected location

### Post Not Publishing

1. **Check memory system:**
   - May be blocked as duplicate
   - Check `data/memory/` for history

2. **Check validation:**
   - Post quality checks may have failed
   - Check workflow logs for validation errors

3. **Check file format:**
   - Jekyll front matter must be valid
   - Content must not have syntax errors

## Monitoring

### GitHub Actions Dashboard

Monitor all workflows at:
- GrumpiBlogged → Actions tab
- Filter by workflow name
- Check run status and logs

### Post Output

Published posts appear at:
- **File**: `docs/_posts/YYYY-MM-DD-{source}.md`
- **Web**: `https://grumpified-oggvct.github.io/GrumpiBlogged/`

### Memory System

Track posting history:
- `data/memory/ollama-pulse.json`
- `data/memory/ai-research-daily.json`
- `data/memory/idea-vault.json`

## Best Practices

1. **Report Generation Timing:**
   - Generate reports early in the day
   - Allow 1-2 hours for GrumpiBlogged processing

2. **Data Quality:**
   - Ensure reports are complete before triggering webhook
   - Include all required fields (title, summary, highlights)

3. **Error Handling:**
   - Monitor workflow failures
   - Set up GitHub Actions notifications
   - Check logs regularly

4. **Testing:**
   - Test webhooks after any workflow changes
   - Use manual triggers for testing
   - Verify output before relying on automation

## Support

For issues or questions:
- **GrumpiBlogged Issues**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/issues
- **Documentation**: This file and workflow YAML comments
- **Author**: @Grumpified-OGGVCT

---

*Last Updated: 2025-01-15*
*Version: 1.0*
