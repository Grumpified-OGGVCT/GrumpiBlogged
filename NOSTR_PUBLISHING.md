# 📡 GrumpiBlogged Nostr Publishing System

## Overview

GrumpiBlogged publishes blog posts to Nostr using **NIP-23 (Long-form Content)** with viral teaser notes for maximum visibility.

### What Gets Published

For each blog post, we publish **TWO events**:

1. **NIP-23 Long-form Article** (kind 30023)
   - Full blog post in Markdown
   - Includes title, summary, tags
   - Replaceable event (can be updated)

2. **NIP-1 Teaser Note** (kind 1)
   - Short viral hook (2-3 sentences)
   - Link to full article (naddr format)
   - Viral hashtags for discovery

### Publishing Strategy

- **48 Free Relays** organized by category
- **17 Relays per publish**: 7 primary + 10 rotating secondary
- **Parallel broadcasting** for speed
- **Success tracking** per relay

---

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `nostr-sdk>=0.32.0` - Rust-based Nostr SDK with proper Schnorr signing
- `aiohttp>=3.9.0` - Async HTTP for parallel relay broadcasting

### 2. Generate Nostr Keys

You need a Nostr keypair (public + private keys):

**Option A: Use existing Nostr client**
- Export keys from Damus, Amethyst, Snort, etc.

**Option B: Generate new keys**
```python
from nostr_sdk import Keys

keys = Keys.generate()
print(f"Public key (hex): {keys.public_key().to_hex()}")
print(f"Private key (hex): {keys.secret_key().to_hex()}")
print(f"Public key (npub): {keys.public_key().to_bech32()}")
print(f"Private key (nsec): {keys.secret_key().to_bech32()}")
```

### 3. Configure Environment

Set your private key as an environment variable:

```bash
# Linux/Mac
export NOSTR_PRIVATE_KEY="your_hex_private_key_here"

# Windows PowerShell
$env:NOSTR_PRIVATE_KEY="your_hex_private_key_here"
```

**⚠️ SECURITY WARNING**: Never commit your private key to Git!

---

## 📝 Usage

### Manual Publishing

```bash
python scripts/post_to_nostr.py \
  docs/_posts/2025-10-26-ollama-daily-learning.md \
  ollama-pulse \
  your_public_key_hex \
  your_private_key_hex
```

**Parameters**:
- `markdown_file`: Path to blog post
- `source`: `ollama-pulse` or `ai-research-daily`
- `pubkey`: Your Nostr public key (hex format)
- `private_key`: Your Nostr private key (hex format) - optional if set in env

### Automated Publishing (GitHub Actions)

Add to workflow after blog post generation:

```yaml
- name: Publish to Nostr
  env:
    NOSTR_PRIVATE_KEY: ${{ secrets.NOSTR_PRIVATE_KEY }}
  run: |
    python scripts/post_to_nostr.py \
      docs/_posts/${TODAY}-ollama-daily-learning.md \
      ollama-pulse \
      ${{ secrets.NOSTR_PUBLIC_KEY }}
```

**Required Secrets**:
- `NOSTR_PUBLIC_KEY` - Your public key (hex)
- `NOSTR_PRIVATE_KEY` - Your private key (hex)

---

## 🎯 How It Works

### 1. Long-form Article (NIP-23)

```json
{
  "kind": 30023,
  "content": "# Full blog post in Markdown...",
  "tags": [
    ["d", "grumpiblogged-ollama-pulse-2025-10-26"],
    ["title", "Ollama Pulse - 2025-10-26"],
    ["published_at", "1730000000"],
    ["summary", "Daily Ollama ecosystem intelligence"],
    ["t", "AI"],
    ["t", "Ollama"],
    ["t", "LocalLLM"],
    ["r", "https://grumpified-oggvct.github.io/ollama_pulse"]
  ]
}
```

### 2. Teaser Note (NIP-1)

```json
{
  "kind": 1,
  "content": "🔥 Ollama Pulse - 2025-10-26\n\nThe Ollama ecosystem just got spicier. The Pulse breaks it down.\n\n📖 Read the full article: nostr:naddr1...\n\n#AI #Ollama #LocalLLM #OpenSource",
  "tags": [
    ["a", "30023:pubkey:grumpiblogged-ollama-pulse-2025-10-26"],
    ["t", "AI"],
    ["t", "Ollama"],
    ["t", "LocalLLM"]
  ]
}
```

### 3. Viral Hashtag Strategy

**Base Tags** (always included):
- Ollama Pulse: `#AI #Ollama #LocalLLM #OpenSource #MachineLearning`
- AI Research Daily: `#AI #Research #MachineLearning #DeepLearning #AIResearch`

**Trending Tags** (rotated based on current trends):
- `#AIAgents` - Hot topic in 2025
- `#LLM` - Evergreen
- `#GenAI` - Broad appeal

**Limit**: 7 hashtags total for optimal visibility

---

## 🌐 Relay Configuration

### Relay Categories

**Primary Relays** (7) - Always used:
- relay.damus.io
- nos.lol
- nostr.wine
- relay.snort.social
- relay.primal.net
- nostr.mom
- relay.nostr.band

**Secondary Relays** (10 rotating):
- Geographic (4 relays)
- Community (9 relays)
- Technical (8 relays)
- Storage (3 relays)
- Alternative (13 relays)

**Total**: 17 relays per publish

### Relay Selection Logic

1. Publish to all 7 primary relays
2. Select 10 relays from secondary pools
3. Rotate secondary selection for broad distribution
4. Track success rate per relay
5. Adjust selection based on performance

---

## 🔍 NIPs Used

### Core NIPs

- **NIP-01**: Basic event structure, signing, timestamps
- **NIP-23**: Long-form content (kind 30023)
- **NIP-19**: Bech32 identifiers (naddr for articles)
- **NIP-21**: nostr: URI scheme for clickable links

### Discovery NIPs

- **NIP-12**: Extra message fields ('t' tags for hashtags)
- **NIP-27**: Internal references ('a' tags for article links)

### Optional NIPs

- **NIP-25**: Reactions (for engagement tracking)
- **NIP-57**: Lightning Zaps (for monetization)

---

## 📊 Success Metrics

### Per-Publish Report

```
📡 Broadcasting article to 17 relays...
  ✅ wss://relay.damus.io
  ✅ wss://nos.lol
  ✅ wss://nostr.wine
  ❌ wss://relay.snort.social (timeout)
  ...

✅ Publishing complete!
   Successful: 32/34 (94%)
   Failed: 2/34 (6%)
```

### Tracking

- Total relays attempted
- Successful publishes
- Failed publishes
- Relay-specific success rates

---

## 🚀 Future Enhancements

### Phase 1 (Current)
- ✅ NIP-23 long-form publishing
- ✅ NIP-1 teaser notes
- ✅ Viral hashtag generation
- ✅ 48 relay broadcasting

### Phase 2 (Planned)
- [ ] Proper bech32 encoding for naddr
- [ ] Dynamic trending hashtag detection
- [ ] Relay performance monitoring
- [ ] Automatic relay rotation based on success rates

### Phase 3 (Future)
- [ ] NIP-25 reaction tracking
- [ ] NIP-57 Lightning Zap integration
- [ ] Analytics dashboard
- [ ] A/B testing for teaser text

---

## 🔒 Security Best Practices

1. **Never commit private keys** - Use environment variables or secrets
2. **Use separate keys** - Don't reuse personal Nostr keys
3. **Rotate keys periodically** - Generate new keypairs every 6-12 months
4. **Monitor relay responses** - Watch for suspicious activity
5. **Validate event signatures** - Ensure proper signing before broadcast

---

## 📚 Resources

- [NIP-23 Specification](https://github.com/nostr-protocol/nips/blob/master/23.md)
- [NIP-01 Specification](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [Nostr SDK Documentation](https://rust-nostr.org/)
- [Relay List](https://nostr.watch/)

---

**Built with passion by the GrumpiBlogged team** 🚀

