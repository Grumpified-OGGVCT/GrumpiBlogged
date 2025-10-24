# GitHub Copilot Prompt for Ollama Pulse Workflow Fix

## 🎯 **Copy and paste this prompt to GitHub Copilot:**

---

**Fix the Ollama Pulse ingestion workflow to use the GH_PAT secret for git push operations**

**Repository**: `Grumpified-OGGVCT/ollama_pulse`  
**File**: `.github/workflows/ingest.yml`

**Problem**: 
The workflow fails at the "Commit and push data changes" step because the default `GITHUB_TOKEN` doesn't have permission to push commits to the repository.

**Solution**:
Update the workflow to use the `GH_PAT` secret (which has been added to repository secrets) instead of the default `GITHUB_TOKEN`.

**Required Changes**:

1. **Find the step** that commits and pushes data changes (should be near the end of the `ingest` job)

2. **Update the checkout action** at the beginning of the job to use the PAT:
   ```yaml
   - name: Checkout repository
     uses: actions/checkout@v4
     with:
       token: ${{ secrets.GH_PAT }}
   ```

3. **Ensure git config** uses the correct credentials:
   ```yaml
   - name: Commit and push data changes
     run: |
       git config user.name "GitHub Action"
       git config user.email "action@github.com"
       git add -A
       git commit -m "chore(data): automated ingestion $(date -u +'%Y-%m-%d %H:%M UTC')" || echo "No changes"
       git push
   ```

**Expected Result**:
- Workflow should successfully commit and push automated data updates
- No more authentication failures
- Data files updated daily

**Test**:
After making changes, trigger the workflow manually or wait for the next scheduled run to verify it works.

---

## 📋 **Alternative: Manual Fix Instructions**

If you prefer to fix it manually instead of using Copilot:

1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/blob/main/.github/workflows/ingest.yml

2. Click "Edit this file" (pencil icon)

3. Find the checkout step (near the top of the `ingest` job):
   ```yaml
   - name: Checkout repository
     uses: actions/checkout@v4
   ```

4. Change it to:
   ```yaml
   - name: Checkout repository
     uses: actions/checkout@v4
     with:
       token: ${{ secrets.GH_PAT }}
   ```

5. Scroll down and commit the change

6. The next workflow run should succeed!

---

## 🔍 **Why This Works**

**Default GITHUB_TOKEN**:
- Automatically provided by GitHub Actions
- Has limited permissions
- Cannot push to protected branches
- Cannot trigger other workflows

**GH_PAT (Personal Access Token)**:
- Has `repo` scope (full repository access)
- Can push commits
- Can trigger workflows
- Persists across workflow runs

**The Fix**:
By using `token: ${{ secrets.GH_PAT }}` in the checkout action, all subsequent git operations (including `git push`) will use the PAT instead of the default token, giving them the necessary permissions.

---

## ✅ **Verification Steps**

After applying the fix:

1. **Check workflow runs**: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions
2. **Look for green checkmarks** on "Ollama Pulse Ingestion" workflow
3. **Verify commits** are being pushed to the repository
4. **Check data files** are being updated (in `data/` directory)

---

## 🚨 **Common Mistakes to Avoid**

❌ **DON'T** hardcode the PAT in the workflow file  
✅ **DO** use `${{ secrets.GH_PAT }}`

❌ **DON'T** add the token to the git push command  
✅ **DO** add it to the checkout action

❌ **DON'T** forget to add the secret to repository settings first  
✅ **DO** verify the secret exists before updating the workflow

---

## 📊 **Expected Workflow Success**

After the fix, the workflow should:

```
✅ Step 1: Checkout repository (using GH_PAT)
✅ Step 2: Set up Python
✅ Step 3: Install dependencies
✅ Step 4: Run ingestion (parallel sources)
✅ Step 5: Aggregate data
✅ Step 6: Mine insights
✅ Step 7: Commit and push data changes ← THIS WILL NOW WORK!
```

---

## 🎊 **Success Criteria**

You'll know it's fixed when:
- ✅ Workflow runs complete without errors
- ✅ New commits appear in the repository from "GitHub Action"
- ✅ Data files are updated daily
- ✅ No more "permission denied" or "authentication failed" errors

---

**Ready to fix!** 🚀

Copy the prompt above and paste it into GitHub Copilot, or follow the manual fix instructions.

