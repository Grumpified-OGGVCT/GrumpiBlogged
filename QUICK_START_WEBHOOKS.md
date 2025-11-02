# Quick Start Guide for Source Repository Owners

This guide is for maintainers of **ollama_pulse**, **AI_Research_Daily**, and **idea_vault** repositories who want to integrate with GrumpiBlogged's automated blogging system.

## What You Need

1. **GitHub Personal Access Token (PAT)** with these scopes:
   - `repo` (full control)
   - `workflow`

2. **Report structure** in your `/docs` folder:
   ```
   your-repo/
   └── docs/
       └── YYYY-MM-DD.json  # Generated daily
   ```

3. **One webhook trigger** added to your workflow

## Setup Steps

### 1. Generate GitHub PAT (One-Time Setup)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `grumpiblogged-webhook`
4. Select scopes:
   - ✅ `repo`
   - ✅ `workflow`
5. Click "Generate token"
6. **Copy token immediately** (shown only once)

### 2. Add Secret to Your Repository

1. In your repository: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GRUMPIBLOGGED_DISPATCH_TOKEN`
4. Value: Paste the PAT from step 1
5. Click "Add secret"

### 3. Add Webhook Step to Your Workflow

Add this to the **end** of your workflow YAML file (after report generation):

#### For ollama_pulse:
```yaml
- name: Trigger GrumpiBlogged
  if: success()
  run: |
    curl -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${{ secrets.GRUMPIBLOGGED_DISPATCH_TOKEN }}" \
      https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
      -d '{"event_type":"ollama-pulse-update","client_payload":{"date":"'$(date -u '+%Y-%m-%d')'","repository":"ollama_pulse"}}'
```

#### For AI_Research_Daily:
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

#### For idea_vault:
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

### 4. Test the Integration

After adding the webhook step:

1. Push your workflow changes
2. Wait for your workflow to run (or trigger manually)
3. Check GrumpiBlogged → Actions tab
4. Look for your workflow to start automatically
5. After ~5 minutes, check https://grumpified-oggvct.github.io/GrumpiBlogged/

## Expected Data Format

Your daily report at `docs/YYYY-MM-DD.json` should follow this structure:

```json
{
  "findings": [
    {
      "title": "Example Finding",
      "url": "https://example.com",
      "summary": "Brief description...",
      "highlights": ["Key point 1", "Key point 2"],
      "source": "github",
      "timestamp": "2025-01-15T10:00:00Z"
    }
  ],
  "insights": {
    "patterns": {
      "trend_name": ["item1", "item2"]
    },
    "themes": ["Theme 1", "Theme 2"]
  }
}
```

**Alternative paths** (checked automatically):
- `data/YYYY-MM-DD.json`
- `data/aggregated/YYYY-MM-DD.json`
- `docs/reports/YYYY-MM-DD.json`

## What Happens Next

When your workflow triggers GrumpiBlogged:

1. **GrumpiBlogged receives webhook** → Workflow starts
2. **Checks out both repositories** → Your repo + GrumpiBlogged
3. **Fetches your report** → From `/docs` folder
4. **Generates humanized blog post** → With unique author persona
5. **Applies AI editing** → SEO, grammar, readability checks
6. **Publishes to Jekyll site** → Commits to `docs/_posts/`
7. **Updates memory system** → Prevents duplicates

## Author Personas

Your content will be transformed with a unique voice:

| Repository | Author | Voice |
|-----------|--------|-------|
| ollama_pulse | **The Pulse** 🎯 | Enthusiastic, dynamic (5 personas) |
| AI_Research_Daily | **The Scholar** 📚 | Rigorous, academic, pedagogical |
| idea_vault | **The Visionary** 💡 | Creative, forward-thinking, inspiring |

## Troubleshooting

### "Webhook not triggering"
- ✅ Secret name is exactly `GRUMPIBLOGGED_DISPATCH_TOKEN`
- ✅ PAT has `repo` and `workflow` scopes
- ✅ Webhook step has `if: success()` condition
- ✅ Event type matches your repository

### "Workflow runs but no post"
- ✅ Data file exists at `docs/YYYY-MM-DD.json`
- ✅ JSON structure is valid
- ✅ Not already posted today (check memory system)

### "Post quality issues"
- ✅ Include detailed summaries (not just titles)
- ✅ Provide highlights array
- ✅ Include source URLs

## Support

- **Full documentation**: [WEBHOOK_INTEGRATION.md](./WEBHOOK_INTEGRATION.md)
- **GrumpiBlogged issues**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/issues
- **Questions**: Open an issue or contact @Grumpified-OGGVCT

## Example Workflow Integration

Here's a complete example showing where to add the webhook:

```yaml
name: Generate Daily Report

on:
  schedule:
    - cron: '0 8 * * *'  # 8 AM daily
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate report
        run: |
          python scripts/generate_report.py
          
      - name: Commit report
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add docs/$(date -u '+%Y-%m-%d').json
          git commit -m "Daily report"
          git push
      
      # 👇 ADD THIS STEP HERE (at the end)
      - name: Trigger GrumpiBlogged
        if: success()
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github+json" \
            -H "Authorization: Bearer ${{ secrets.GRUMPIBLOGGED_DISPATCH_TOKEN }}" \
            https://api.github.com/repos/Grumpified-OGGVCT/GrumpiBlogged/dispatches \
            -d '{"event_type":"YOUR-EVENT-TYPE-HERE","client_payload":{"date":"'$(date -u '+%Y-%m-%d')'"}}'
```

**Remember to replace `YOUR-EVENT-TYPE-HERE` with:**
- `ollama-pulse-update` for ollama_pulse
- `ai-research-daily-update` for AI_Research_Daily  
- `idea-vault-update` for idea_vault

---

**That's it!** Your reports will now automatically become engaging blog posts. 🎉
