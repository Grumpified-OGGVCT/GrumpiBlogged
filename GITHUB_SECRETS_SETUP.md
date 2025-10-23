# 🔐 GitHub Secrets Setup for GrumpiBlogged

**Purpose**: Configure API keys for Phase 4 AI-Powered Editing in GitHub Actions

---

## 📋 **Required API Keys**

For GrumpiBlogged AI editing to work in GitHub Actions, you need to add these secrets:

### **Option 1: Single Key (Recommended - Simplest)**
```
OLLAMA_PROXY_API_KEY
```
**Value**: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`  
**Purpose**: Used for all AI editing (grammar, SEO, fact-checking)

### **Option 2: Separate Keys (Advanced - More Control)**
```
OLLAMA_PROXY_GRAMMAR_API_KEY    (for grammar checking)
OLLAMA_PROXY_FACT_CHECK_API_KEY (for fact-checking)
OLLAMA_PROXY_SEO_API_KEY        (for SEO optimization)
```

**Recommendation**: Use **Option 1** (single key) for simplicity. The code will use `OLLAMA_PROXY_API_KEY` for all operations.

---

## 🌍 **GitHub Secrets Scope**

### **Important: Secrets are Repository-Specific**

GitHub Secrets work at different levels:

1. **Repository Secrets** (Most Common)
   - Scope: Single repository only
   - Access: Only workflows in that repository
   - **This is what you need for GrumpiBlogged**

2. **Organization Secrets** (For Multiple Repos)
   - Scope: All repositories in the organization
   - Access: Can be shared across repos
   - Requires: Organization owner permissions
   - **Useful if you want to use the same key across multiple projects**

3. **Environment Secrets** (Advanced)
   - Scope: Specific deployment environments
   - Access: Only when deploying to that environment
   - Not needed for GrumpiBlogged

### **Answer to Your Question**:
❌ **No, you cannot apply one secret globally to cover both your account and organization**

You need to add secrets separately:
- Once for your **personal account repositories** (if any)
- Once for **Grumpified organization repositories**

---

## 🎯 **Where to Add Secrets**

### **For GrumpiBlogged Repository**:

**Repository**: `Grumpified-OGGVCT/GrumpiBlogged`

**URL**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions

**Steps**:
1. Go to repository settings
2. Click "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add the secret (see below)

---

### **For Organization-Wide Access** (Optional):

**Organization**: `Grumpified-OGGVCT`

**URL**: https://github.com/organizations/Grumpified-OGGVCT/settings/secrets/actions

**Steps**:
1. Go to organization settings
2. Click "Secrets and variables" → "Actions"
3. Click "New organization secret"
4. Add the secret
5. **Important**: Select which repositories can access it

**Benefits**:
- Share same key across multiple repos
- Easier to rotate keys (change once, applies everywhere)
- Centralized management

**Drawbacks**:
- Requires organization owner permissions
- More complex setup

---

## 🚀 **Quick Setup (Recommended)**

### **Step 1: Add to GrumpiBlogged Repository**

**Secret Name**: `OLLAMA_PROXY_API_KEY`  
**Secret Value**: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`

**Manual Method**:
1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. Click "New repository secret"
3. Name: `OLLAMA_PROXY_API_KEY`
4. Value: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`
5. Click "Add secret"

**Using GitHub CLI** (if installed):
```bash
gh secret set OLLAMA_PROXY_API_KEY \
  --repo Grumpified-OGGVCT/GrumpiBlogged \
  --body "op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109"
```

---

### **Step 2: Verify Secret is Added**

**Check via Web UI**:
1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. You should see `OLLAMA_PROXY_API_KEY` listed
3. Value will be hidden (shows as `***`)

**Check via GitHub CLI**:
```bash
gh secret list --repo Grumpified-OGGVCT/GrumpiBlogged
```

---

## 🔄 **Optional: Add to Organization**

If you want to use the same key across **all** Grumpified-OGGVCT repositories:

### **Step 1: Add Organization Secret**

**URL**: https://github.com/organizations/Grumpified-OGGVCT/settings/secrets/actions

**Steps**:
1. Go to organization settings
2. Click "Secrets and variables" → "Actions"
3. Click "New organization secret"
4. Name: `OLLAMA_PROXY_API_KEY`
5. Value: `op_2e0efc5f37c6c1b4_da2701b13246163ae6c8f4ece6d0e5f9082b9ac1849f7109`
6. **Repository access**: Select "Selected repositories"
7. Choose: `GrumpiBlogged` (and any other repos that need it)
8. Click "Add secret"

### **Step 2: Remove Repository Secret** (Optional)

If you added an organization secret, you can remove the repository-level secret to avoid duplication:

1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. Find `OLLAMA_PROXY_API_KEY`
3. Click "Remove"

**Note**: Organization secrets take precedence over repository secrets with the same name.

---

## 🧪 **Testing the Setup**

### **Method 1: Trigger a Workflow Manually**

1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/actions
2. Select "Ollama Pulse Post" or "Daily Learning Post" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"
6. Monitor the run - it should now use AI editing

### **Method 2: Wait for Scheduled Run**

- **Ollama Pulse**: Runs every 30 minutes
- **AI Research Daily**: Runs daily at 08:05 CT

Check the logs for:
```
🤖 Running AI-Powered Editing...
  ✅ SEO Score: 95/100
  ✅ Readability: Standard
  ✅ Clarity: 87/100
```

### **Method 3: Check Workflow Logs**

1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/actions
2. Click on the most recent workflow run
3. Expand the "Generate blog post" step
4. Look for AI editing output

**Success Indicators**:
- ✅ No "⚠️ AI editing skipped: No API key" messages
- ✅ SEO scores displayed
- ✅ Readability levels shown
- ✅ Clarity scores present

**Failure Indicators**:
- ❌ "⚠️ AI editing skipped" messages
- ❌ Missing SEO/readability data
- ❌ API authentication errors

---

## 🔒 **Security Best Practices**

### **Do's** ✅:
- ✅ Use GitHub Secrets (never commit keys to code)
- ✅ Rotate keys periodically (every 90 days)
- ✅ Use separate keys for different purposes (if needed)
- ✅ Monitor key usage in Ollama Proxy dashboard
- ✅ Revoke keys immediately if compromised

### **Don'ts** ❌:
- ❌ Never commit API keys to repository
- ❌ Never share keys in public issues/PRs
- ❌ Never log full API keys in workflow output
- ❌ Never use the same key for production and testing (if possible)

---

## 🔄 **Key Rotation**

If you need to rotate the API key:

### **Step 1: Create New Key**

1. Go to: http://127.0.0.1:8081/admin/users/1/keys/create
2. Login: `GrumpiFied` / `PlmQaz3#2@1!`
3. Create new key with name: `GrumpiBlogged-Production`
4. Copy the new key

### **Step 2: Update GitHub Secret**

1. Go to: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. Click on `OLLAMA_PROXY_API_KEY`
3. Click "Update secret"
4. Paste new key value
5. Click "Update secret"

### **Step 3: Revoke Old Key**

1. Go to: http://127.0.0.1:8081/admin/keys
2. Find old key: `op_2e0efc5f37c6c1b4_...`
3. Click "Revoke"
4. Confirm revocation

---

## 📊 **Monitoring Key Usage**

### **Ollama Proxy Dashboard**:

**URL**: http://127.0.0.1:8081/admin/keys

**What to Monitor**:
- Request count per key
- Last used timestamp
- Error rates
- Rate limit status

**Alerts to Set**:
- High error rate (>10%)
- Unusual request patterns
- Rate limit approaching

---

## 🆘 **Troubleshooting**

### **Problem: "AI editing skipped: No API key"**

**Solution**:
1. Verify secret is added: https://github.com/Grumpified-OGGVCT/GrumpiBlogged/settings/secrets/actions
2. Check secret name is exactly: `OLLAMA_PROXY_API_KEY` (case-sensitive)
3. Re-run workflow to test

### **Problem: "API authentication failed"**

**Solution**:
1. Verify key is valid in Ollama Proxy dashboard
2. Check key hasn't been revoked
3. Verify key has correct permissions
4. Try creating a new key

### **Problem: "Ollama Proxy not accessible"**

**Solution**:
- GitHub Actions runs in the cloud, cannot access `localhost:8081`
- **This is expected** - AI editing will be skipped
- **Workaround**: Deploy Ollama Proxy to a public URL (not recommended for security)
- **Alternative**: Run blog generation locally instead of GitHub Actions

**Important Note**: If your Ollama Proxy is only accessible at `localhost:8081`, GitHub Actions **cannot** reach it. You have two options:

1. **Accept graceful degradation**: AI editing will be skipped, posts will still generate
2. **Deploy Ollama Proxy publicly**: Use ngrok, Cloudflare Tunnel, or cloud hosting

---

## ✅ **Quick Checklist**

- [ ] Add `OLLAMA_PROXY_API_KEY` to repository secrets
- [ ] Verify secret appears in settings
- [ ] Trigger a test workflow run
- [ ] Check workflow logs for AI editing output
- [ ] Verify SEO metadata in generated posts
- [ ] Monitor first few automated runs
- [ ] (Optional) Add to organization secrets for reuse

---

**Next Steps**: After adding the secret, monitor the next automated blog run to verify AI editing is working!

