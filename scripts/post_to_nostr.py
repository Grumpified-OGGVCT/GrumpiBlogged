#!/usr/bin/env python3
"""
GrumpiBlogged - Nostr NIP-23 Publisher
Publishes blog posts to Nostr as long-form articles (kind 30023) with viral teaser notes (kind 1)
"""
import json
import time
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
import asyncio
import aiohttp
from typing import List, Dict, Optional

# Nostr event kinds
KIND_SHORT_NOTE = 1
KIND_LONG_FORM = 30023

# Load relay configuration
RELAY_CONFIG_PATH = Path("config/nostr_relays.json")


def load_relay_config() -> Dict:
    """Load Nostr relay configuration"""
    with open(RELAY_CONFIG_PATH, 'r') as f:
        return json.load(f)


def get_publishing_relays(config: Dict) -> List[str]:
    """Get list of relays to publish to (7 primary + 10 rotating secondary)"""
    relays = []
    
    # Always use all primary relays
    relays.extend(config['primary_relays']['relays'])
    
    # Add 10 relays from other categories (rotating)
    secondary_pools = [
        config['geographic_relays']['relays'],
        config['community_relays']['relays'],
        config['technical_relays']['relays'],
        config['storage_relays']['relays'],
        config['alternative_relays']['relays']
    ]
    
    # Flatten and take first 10
    all_secondary = []
    for pool in secondary_pools:
        all_secondary.extend(pool)
    
    relays.extend(all_secondary[:10])
    
    return relays


def generate_event_id(event: Dict) -> str:
    """Generate Nostr event ID (SHA256 hash of serialized event)"""
    # Serialize event per NIP-01
    serialized = json.dumps([
        0,  # Reserved for future use
        event['pubkey'],
        event['created_at'],
        event['kind'],
        event['tags'],
        event['content']
    ], separators=(',', ':'), ensure_ascii=False)
    
    return hashlib.sha256(serialized.encode()).hexdigest()


def sign_event(event: Dict, private_key: str) -> str:
    """Sign event with Schnorr signature (placeholder - use nostr library in production)"""
    # TODO: Implement proper Schnorr signing with secp256k1
    # For now, return placeholder - MUST use proper signing library
    # Recommended: python-nostr, nostr-sdk, or pynostr
    return "PLACEHOLDER_SIGNATURE_USE_PROPER_LIBRARY"


def create_long_form_event(
    content: str,
    title: str,
    summary: str,
    tags: List[str],
    pubkey: str,
    private_key: str,
    date_str: str,
    source: str = "ollama-pulse"
) -> Dict:
    """Create NIP-23 long-form content event (kind 30023)"""
    
    # Create unique identifier for this article
    article_id = f"grumpiblogged-{source}-{date_str}"
    
    # Build tags
    event_tags = [
        ["d", article_id],  # Unique identifier (makes it replaceable)
        ["title", title],
        ["published_at", str(int(time.time()))],
        ["summary", summary],
    ]
    
    # Add topic tags
    for tag in tags:
        event_tags.append(["t", tag])
    
    # Add source attribution
    if source == "ollama-pulse":
        event_tags.append(["r", "https://grumpified-oggvct.github.io/ollama_pulse"])
    elif source == "ai-research-daily":
        event_tags.append(["r", "https://grumpified-oggvct.github.io/AI_Research_Daily"])
    
    # Create event
    event = {
        "kind": KIND_LONG_FORM,
        "created_at": int(time.time()),
        "tags": event_tags,
        "content": content,
        "pubkey": pubkey
    }
    
    # Generate ID and sign
    event["id"] = generate_event_id(event)
    event["sig"] = sign_event(event, private_key)
    
    return event


def create_teaser_note(
    article_event: Dict,
    teaser_text: str,
    viral_hashtags: List[str],
    pubkey: str,
    private_key: str
) -> Dict:
    """Create viral teaser note (kind 1) linking to long-form article"""
    
    # Extract article info
    article_id = next(tag[1] for tag in article_event['tags'] if tag[0] == 'd')
    title = next(tag[1] for tag in article_event['tags'] if tag[0] == 'title')
    
    # Create naddr reference (NIP-19 format)
    # Format: nostr:naddr1<bech32-encoded-data>
    # For now, use simplified reference - proper implementation needs bech32 encoding
    naddr_ref = f"30023:{pubkey}:{article_id}"
    
    # Build teaser content with link
    content = f"{teaser_text}\n\n"
    content += f"📖 Read the full article: nostr:{naddr_ref}\n\n"
    content += " ".join([f"#{tag}" for tag in viral_hashtags])
    
    # Build tags
    event_tags = [
        ["a", naddr_ref],  # Reference to long-form article
    ]
    
    # Add viral hashtags as 't' tags
    for tag in viral_hashtags:
        event_tags.append(["t", tag])
    
    # Create event
    event = {
        "kind": KIND_SHORT_NOTE,
        "created_at": int(time.time()),
        "tags": event_tags,
        "content": content,
        "pubkey": pubkey
    }
    
    # Generate ID and sign
    event["id"] = generate_event_id(event)
    event["sig"] = sign_event(event, private_key)
    
    return event


async def publish_to_relay(relay_url: str, event: Dict, session: aiohttp.ClientSession) -> bool:
    """Publish event to a single relay"""
    try:
        # Convert to WebSocket URL if needed
        ws_url = relay_url.replace('http://', 'ws://').replace('https://', 'wss://')
        
        async with session.ws_connect(ws_url, timeout=aiohttp.ClientTimeout(total=10)) as ws:
            # Send EVENT message per NIP-01
            await ws.send_json(["EVENT", event])
            
            # Wait for OK response
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    response = json.loads(msg.data)
                    if response[0] == "OK":
                        return response[2]  # Success status
                    
        return False
    except Exception as e:
        print(f"❌ Failed to publish to {relay_url}: {e}")
        return False


async def broadcast_events(events: List[Dict], relays: List[str]) -> Dict[str, int]:
    """Broadcast events to all relays in parallel"""
    results = {
        "total_relays": len(relays),
        "successful": 0,
        "failed": 0,
        "relay_results": {}
    }
    
    async with aiohttp.ClientSession() as session:
        for event in events:
            event_kind = "article" if event['kind'] == KIND_LONG_FORM else "teaser"
            print(f"\n📡 Broadcasting {event_kind} to {len(relays)} relays...")
            
            tasks = [publish_to_relay(relay, event, session) for relay in relays]
            relay_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for relay, success in zip(relays, relay_results):
                if isinstance(success, Exception):
                    results["failed"] += 1
                    results["relay_results"][relay] = "error"
                elif success:
                    results["successful"] += 1
                    results["relay_results"][relay] = "success"
                    print(f"  ✅ {relay}")
                else:
                    results["failed"] += 1
                    results["relay_results"][relay] = "rejected"
                    print(f"  ❌ {relay}")
    
    return results


def generate_viral_teaser(title: str, source: str, persona: str) -> str:
    """Generate viral teaser text for short note"""
    teasers = {
        "ollama-pulse": [
            f"🔥 {title}\n\nThe Ollama ecosystem just got spicier. {persona} breaks it down.",
            f"⚡ Fresh from the Pulse: {title}\n\n{persona} spotted the patterns you need to see.",
            f"🎯 {title}\n\nYour daily dose of Ollama intelligence, served hot by {persona}."
        ],
        "ai-research-daily": [
            f"📚 {title}\n\nThe Scholar just dropped today's research intelligence. This one's worth your time.",
            f"🔬 {title}\n\nCutting-edge AI research, translated for humans. The Scholar delivers.",
            f"💡 {title}\n\nToday's breakthrough papers, decoded by The Scholar."
        ]
    }
    
    import random
    return random.choice(teasers.get(source, teasers["ollama-pulse"]))


def get_viral_hashtags(source: str, content: str) -> List[str]:
    """Generate viral hashtags based on content and current trends"""
    # Base hashtags
    base_tags = {
        "ollama-pulse": ["AI", "Ollama", "LocalLLM", "OpenSource", "MachineLearning"],
        "ai-research-daily": ["AI", "Research", "MachineLearning", "DeepLearning", "AIResearch"]
    }
    
    tags = base_tags.get(source, base_tags["ollama-pulse"])
    
    # Add trending topics (TODO: Make this dynamic based on actual trends)
    trending = ["AIAgents", "LLM", "GenAI"]
    tags.extend(trending[:2])
    
    return tags[:7]  # Limit to 7 hashtags for optimal visibility


def main():
    """Main publishing function"""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python post_to_nostr.py <markdown_file> <source> <pubkey> [private_key]")
        print("  source: 'ollama-pulse' or 'ai-research-daily'")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    source = sys.argv[2]
    pubkey = sys.argv[3]
    private_key = sys.argv[4] if len(sys.argv) > 4 else None
    
    if not private_key:
        print("⚠️  WARNING: No private key provided - using placeholder signatures")
        print("   Set NOSTR_PRIVATE_KEY environment variable or pass as argument")
        private_key = "PLACEHOLDER"
    
    # Load blog post
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata (TODO: Parse Jekyll front matter properly)
    title = f"GrumpiBlogged - {datetime.now().strftime('%Y-%m-%d')}"
    summary = "Daily AI ecosystem intelligence, translated for humans"
    date_str = datetime.now().strftime('%Y-%m-%d')
    persona = "The Pulse" if source == "ollama-pulse" else "The Scholar"
    
    # Generate viral content
    viral_hashtags = get_viral_hashtags(source, content)
    teaser_text = generate_viral_teaser(title, source, persona)
    
    # Create events
    print("📝 Creating Nostr events...")
    article_event = create_long_form_event(
        content=content,
        title=title,
        summary=summary,
        tags=viral_hashtags,
        pubkey=pubkey,
        private_key=private_key,
        date_str=date_str,
        source=source
    )
    
    teaser_event = create_teaser_note(
        article_event=article_event,
        teaser_text=teaser_text,
        viral_hashtags=viral_hashtags,
        pubkey=pubkey,
        private_key=private_key
    )
    
    # Load relay config and broadcast
    config = load_relay_config()
    relays = get_publishing_relays(config)
    
    print(f"\n🎯 Publishing to {len(relays)} relays...")
    print(f"   Article ID: {article_event['id'][:16]}...")
    print(f"   Teaser ID: {teaser_event['id'][:16]}...")
    
    # Broadcast both events
    results = asyncio.run(broadcast_events([article_event, teaser_event], relays))
    
    print(f"\n✅ Publishing complete!")
    print(f"   Successful: {results['successful']}/{results['total_relays'] * 2}")
    print(f"   Failed: {results['failed']}/{results['total_relays'] * 2}")


if __name__ == "__main__":
    main()

