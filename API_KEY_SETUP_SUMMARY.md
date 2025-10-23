# 🔐 API Key Setup - Quick Summary

**Your Question**: Can one API key be applied globally to cover both account and organization?

**Answer**: ❌ **No, GitHub Secrets are repository-specific or organization-specific, not global across both.**

---

## 🎯 **What You Need to Do**

### **For GrumpiBlogged (Simplest - Recommended)**

**Add ONE secret to the GrumpiBlogged repository**:

**Secret Name**: `OLLAMA_PROXY_API_KEY`  
**Secret Value**: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`  
**Where**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions

---

## 🌍 **GitHub Secrets Scope Explained**

### **Three Levels of Secrets**:

1. **Repository Secrets** (What you need for GrumpiBlogged)
   - Scope: Single repository only
   - Example: `Grumpified-OGGVCT/GrumpiBlogged`
   - Access: Only workflows in that specific repo
   - **This is the standard approach**

2. **Organization Secrets** (For multiple repos)
   - Scope: All repos in the organization
   - Example: All repos under `Grumpified-OGGVCT`
   - Access: Can be shared across repos
   - Requires: Organization owner permissions
   - **Useful if you have multiple projects using the same key**

3. **Personal Account** (Your personal repos)
   - Scope: Repos under your personal account (`AccidentalJedi`)
   - Access: Only your personal repos
   - Separate from organization repos

### **Key Point**: 
You **cannot** create one secret that works for both:
- Your personal account repos (`AccidentalJedi/*`)
- AND organization repos (`Grumpified-OGGVCT/*`)

You must add secrets separately to each scope.

---

## 📋 **Your Current Situation**

### **GrumpiBlogged Repository**:
- Owner: `Grumpified-OGGVCT` (organization)
- Repo: `GrumpiBlogged`
- Needs: `OLLAMA_PROXY_API_KEY` secret

### **Your Options**:

#### **Option 1: Repository Secret (Recommended - Simplest)**
✅ Add secret to `Grumpified-OGGVCT/GrumpiBlogged` only  
✅ Works immediately  
✅ No organization permissions needed  
❌ Only works for this one repo  

#### **Option 2: Organization Secret (If you have multiple projects)**
✅ Add secret to `Grumpified-OGGVCT` organization  
✅ Can be shared across all organization repos  
✅ Easier to rotate (change once, applies everywhere)  
❌ Requires organization owner permissions  
❌ More complex setup  

---

## 🚀 **Quick Setup (3 Methods)**

### **Method 1: Web UI (Easiest)**

1. **Go to**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions

2. **Click**: "New repository secret"

3. **Enter**:
   - Name: `OLLAMA_PROXY_API_KEY`
   - Value: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`

4. **Click**: "Add secret"

5. **Done!** ✅

---

### **Method 2: GitHub CLI (If installed)**

```bash
gh secret set OLLAMA_PROXY_API_KEY \
  --repo Grumpified-OGGVCT/GrumpiBlogged \
  --body "op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109"
```

---

### **Method 3: Python Script (Automated)**

```bash
cd grumpiblogged_work
pip install PyNaCl requests
python scripts/add_github_secret.py
```

**Note**: You'll need a GitHub Personal Access Token with `repo` scope.  
Create one at: https://github.com/settings/tokens/new

---

## ⚠️ **Important Limitation**

### **Ollama Proxy Accessibility**

Your Ollama Proxy runs at: `http://127.0.0.1:8081`

**Problem**: GitHub Actions runs in the cloud and **cannot** access `localhost:8081`

**Impact**:
- ✅ Secret will be added successfully
- ❌ GitHub Actions workflows **cannot** reach your local Ollama Proxy
- ⚠️  AI editing will be **gracefully skipped** in automated runs
- ✅ Posts will still generate (without AI editing)

### **Solutions**:

#### **Option A: Accept Graceful Degradation (Recommended)**
- AI editing works when running scripts locally
- GitHub Actions workflows skip AI editing
- Posts still generate successfully
- No security risks

#### **Option B: Deploy Ollama Proxy Publicly (Advanced)**
- Use ngrok, Cloudflare Tunnel, or cloud hosting
- Make Ollama Proxy accessible via public URL
- Update scripts to use public URL instead of localhost
- **Security risk**: Exposes your Ollama Proxy to the internet

#### **Option C: Run Blog Generation Locally (Alternative)**
- Don't use GitHub Actions for blog generation
- Run `generate_daily_blog.py` and `generate_lab_blog.py` locally
- Commit and push generated posts manually
- AI editing works perfectly (local access to Ollama Proxy)

---

## 🧪 **Testing After Setup**

### **Step 1: Verify Secret is Added**

**Web UI**:
1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. You should see `OLLAMA_PROXY_API_KEY` listed
3. Value will be hidden (shows as `***`)

**GitHub CLI**:
```bash
gh secret list --repo Grumpified-OGGVCT/GrumpiBlogged
```

---

### **Step 2: Trigger Test Workflow**

1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/actions
2. Select "Ollama Pulse Post" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

---

### **Step 3: Check Workflow Logs**

1. Click on the running workflow
2. Expand "Generate blog post" step
3. Look for:

**If Ollama Proxy is accessible** (unlikely from GitHub Actions):
```
🤖 Running AI-Powered Editing...
  ✅ SEO Score: 95/100
  ✅ Readability: Standard
  ✅ Clarity: 87/100
```

**If Ollama Proxy is NOT accessible** (expected):
```
⚠️  AI editing skipped: Cannot connect to Ollama Proxy
📝 Continuing with post generation...
```

Both are **valid outcomes** - the second is expected given your setup.

---

## 📊 **Recommendation**

### **For Your Setup**:

1. ✅ **Add the secret** (for completeness and future use)
2. ✅ **Accept that GitHub Actions can't use AI editing** (localhost limitation)
3. ✅ **Run blog generation locally** if you want AI editing
4. ✅ **Or deploy Ollama Proxy publicly** if you want automated AI editing

### **Immediate Action**:

**Add the secret using Method 1 (Web UI)**:
1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. Click "New repository secret"
3. Name: `OLLAMA_PROXY_API_KEY`
4. Value: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`
5. Click "Add secret"

**Done!** ✅

---

## 🔄 **For Organization-Wide Access** (Optional)

If you want to use the same key across **all** Grumpified-OGGVCT repos:

1. Go to: https://github.com/organizations/Grumpified-OGGVCT/settings/secrets/actions
2. Click "New organization secret"
3. Name: `OLLAMA_PROXY_API_KEY`
4. Value: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`
5. Repository access: Select "Selected repositories"
6. Choose: `GrumpiBlogged` (and any others)
7. Click "Add secret"

**Note**: This requires organization owner permissions.

---

## ✅ **Quick Checklist**

- [ ] Add `OLLAMA_PROXY_API_KEY` to GrumpiBlogged repository
- [ ] Verify secret appears in settings
- [ ] Understand that GitHub Actions can't reach localhost:8081
- [ ] Accept graceful degradation (AI editing skipped in automated runs)
- [ ] (Optional) Deploy Ollama Proxy publicly for automated AI editing
- [ ] (Optional) Add to organization secrets for reuse across repos

---

**Bottom Line**: Add the secret for completeness, but understand that GitHub Actions workflows won't be able to use AI editing unless you deploy Ollama Proxy to a public URL.

