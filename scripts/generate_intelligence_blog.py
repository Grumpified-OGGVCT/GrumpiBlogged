#!/usr/bin/env python3
"""
Intelligence Blog Generator - The Complete Pipeline

This is the MASTER SCRIPT that runs the entire intelligence
gathering, synthesis, and blog generation pipeline.

Pipeline:
1. Crawl all sources (SearXNG, Reddit, HN, RSS, etc.)
2. Deduplicate and normalize signals
3. Compute embeddings and cluster topics
4. Build influence and topic graphs
5. Detect emerging trends
6. Generate predictions
7. Synthesize into compelling narrative
8. Create interactive visualizations
9. Generate blog post with AI editing
10. Commit and push to GitHub

This is the culmination of everything we've built.
"""

import asyncio
import os
import sys
from datetime import datetime
import pytz
from pathlib import Path

# Add intelligence module to path
sys.path.insert(0, str(Path(__file__).parent / 'intelligence'))

from searxng_crawler import SearXNGCrawler
from reddit_crawler import RedditGraphCrawler
from hackernews_crawler import HackerNewsGraphCrawler
from synthesis_engine import SynthesisEngine, IntelligenceReport
from visualization import IntelligenceVisualizer


class IntelligenceBlogGenerator:
    """
    Master orchestrator for the complete intelligence blog pipeline.
    """
    
    def __init__(self, ollama_api_key: str):
        self.ollama_api_key = ollama_api_key
        
        # Initialize components
        self.searxng_instances = [
            "https://searx.be",
            "https://search.sapti.me",
            "https://searx.tiekoetter.com",
            "https://searx.work"
        ]
        
        self.ai_subreddits = [
            "LocalLLaMA",
            "MachineLearning",
            "StableDiffusion",
            "OpenAI",
            "ArtificialIntelligence",
            "learnmachinelearning"
        ]
    
    async def run_full_pipeline(self) -> IntelligenceReport:
        """
        Execute the complete intelligence pipeline.
        
        Returns:
            IntelligenceReport ready for blog post generation
        """
        
        print("🚀 INTELLIGENCE PIPELINE STARTING")
        print("=" * 80)
        
        # Phase 1: Parallel crawling
        print("\n📡 PHASE 1: DISTRIBUTED CRAWLING")
        print("-" * 80)
        
        intelligence_data = await self._crawl_all_sources()
        
        # Phase 2: Synthesis
        print("\n✨ PHASE 2: INTELLIGENCE SYNTHESIS")
        print("-" * 80)
        
        report = await self._synthesize_intelligence(intelligence_data)
        
        # Phase 3: Visualization
        print("\n📊 PHASE 3: VISUALIZATION GENERATION")
        print("-" * 80)
        
        visualizations = await self._create_visualizations(intelligence_data)
        
        # Phase 4: Blog post generation
        print("\n📝 PHASE 4: BLOG POST GENERATION")
        print("-" * 80)
        
        blog_post = await self._generate_blog_post(report, visualizations)
        
        print("\n" + "=" * 80)
        print("✅ PIPELINE COMPLETE!")
        print(f"   Blog post: {blog_post}")
        
        return report
    
    async def _crawl_all_sources(self) -> dict:
        """
        Phase 1: Crawl all intelligence sources in parallel

        Enhanced with Ollama Turbo web search fallback:
        - If manual crawling fails or returns < 10 signals
        - Use Ollama web search to gather intelligence
        - Ensures we always have data to analyze
        """

        # Create crawlers
        searxng = SearXNGCrawler(self.searxng_instances)
        reddit = RedditGraphCrawler(self.ai_subreddits)
        hackernews = HackerNewsGraphCrawler()

        # Parallel crawling
        print("🕷️  Launching parallel crawlers...")

        results = await asyncio.gather(
            self._crawl_searxng(searxng),
            self._crawl_reddit(reddit),
            self._crawl_hackernews(hackernews),
            return_exceptions=True
        )

        # Combine results
        all_signals = []
        graphs = {
            'user_graph': None,
            'topic_graph': None
        }

        for result in results:
            if isinstance(result, Exception):
                print(f"   ⚠️  Crawler failed: {result}")
                continue

            all_signals.extend(result.get('signals', []))

            # Merge graphs (simplified - in production, use proper graph merging)
            if result.get('user_graph'):
                graphs['user_graph'] = result['user_graph']
            if result.get('topic_graph'):
                graphs['topic_graph'] = result['topic_graph']

        print(f"\n✅ Crawling complete: {len(all_signals)} total signals")

        # FALLBACK: Use Ollama web search if we got too few signals
        if len(all_signals) < 10:
            print(f"\n⚠️  Only {len(all_signals)} signals - using Ollama web search fallback...")
            fallback_signals = await self._web_search_fallback()
            all_signals.extend(fallback_signals)
            print(f"   ✅ Added {len(fallback_signals)} signals from web search")

        return {
            'signals': all_signals,
            'total_signals': len(all_signals),
            **graphs
        }
    
    async def _crawl_searxng(self, crawler: SearXNGCrawler) -> dict:
        """Crawl SearXNG for social media signals"""
        
        print("   🔍 SearXNG: Searching social media...")
        
        async with crawler:
            results = await crawler.search_social_media(
                query="AI OR machine learning OR LLM OR local models",
                platforms=['twitter', 'reddit', 'mastodon'],
                time_range="day",
                max_results=100
            )
        
        # Convert to signals
        signals = []
        for platform, posts in results.items():
            for post in posts:
                signals.append({
                    'source': platform,
                    'title': post['title'],
                    'url': post['url'],
                    'content': post['content'],
                    'engagement': post['engagement'],
                    'timestamp': post.get('publishedDate', datetime.now())
                })
        
        print(f"      ✅ Found {len(signals)} social media signals")
        
        return {'signals': signals}
    
    async def _crawl_reddit(self, crawler: RedditGraphCrawler) -> dict:
        """Crawl Reddit for discussions"""
        
        print("   🤖 Reddit: Crawling AI/ML subreddits...")
        
        async with crawler:
            posts = await crawler.crawl(
                lookback_hours=24,
                min_score=50,
                include_comments=True,
                max_posts_per_subreddit=50
            )
        
        # Convert to signals
        signals = []
        for post in posts:
            signals.append({
                'source': 'reddit',
                'title': post.title,
                'url': post.permalink,
                'content': post.selftext,
                'engagement': {
                    'upvotes': post.score,
                    'comments': post.num_comments
                },
                'timestamp': post.created_utc
            })
        
        print(f"      ✅ Found {len(signals)} Reddit posts")
        
        return {
            'signals': signals,
            'user_graph': crawler.user_graph,
            'topic_graph': crawler.topic_graph
        }
    
    async def _crawl_hackernews(self, crawler: HackerNewsGraphCrawler) -> dict:
        """Crawl Hacker News for tech discussions"""
        
        print("   📰 Hacker News: Searching AI/ML stories...")
        
        async with crawler:
            stories = await crawler.crawl(
                lookback_hours=24,
                min_points=50,
                include_comments=True,
                max_stories=50
            )
        
        # Convert to signals
        signals = []
        for story in stories:
            signals.append({
                'source': 'hackernews',
                'title': story.title,
                'url': story.hn_url,
                'content': story.text or '',
                'engagement': {
                    'points': story.points,
                    'comments': story.num_comments
                },
                'timestamp': story.created_at
            })
        
        print(f"      ✅ Found {len(signals)} HN stories")
        
        return {
            'signals': signals,
            'user_graph': crawler.user_graph,
            'topic_graph': crawler.topic_graph
        }
    
    async def _web_search_fallback(self) -> List[dict]:
        """
        Fallback: Use Ollama Turbo web search when manual crawling fails

        Queries:
        - Latest AI/ML developments
        - New LLM releases
        - AI research breakthroughs
        - Local AI tools and models
        """
        from synthesis_engine import OllamaCloudClient

        signals = []

        async with OllamaCloudClient(self.ollama_api_key) as client:
            queries = [
                "Latest AI and machine learning developments today",
                "New LLM releases and local AI models",
                "AI research breakthroughs and papers",
                "Open source AI tools and frameworks"
            ]

            for query in queries:
                try:
                    print(f"   🔍 Web search: {query}")
                    result = await client.web_search(
                        model='deepseek-v3.1:671b-cloud',
                        query=query,
                        max_tokens=1000
                    )

                    # Parse web search results into signals
                    signals.append({
                        'source': 'ollama_web_search',
                        'title': query,
                        'content': result,
                        'url': 'https://ollama.ai',
                        'engagement': {'score': 1.0},
                        'timestamp': datetime.now().isoformat()
                    })

                except Exception as e:
                    print(f"      ⚠️  Web search failed: {e}")

        return signals

    async def _synthesize_intelligence(self, data: dict) -> IntelligenceReport:
        """Phase 2: Synthesize raw intelligence into insights"""

        print("🧠 Synthesizing intelligence...")

        engine = SynthesisEngine(self.ollama_api_key)
        report = await engine.synthesize(data)

        print(f"   ✅ Generated intelligence report")
        print(f"      Headline: {report.headline}")
        print(f"      Confidence: {report.confidence_score:.2%}")

        return report
    
    async def _create_visualizations(self, data: dict) -> dict:
        """Phase 3: Create interactive visualizations"""

        print("📊 Creating visualizations...")

        visualizer = IntelligenceVisualizer(dark_mode=True)

        # Save to docs/assets/visualizations for Jekyll
        output_dir = Path("docs/assets/visualizations")
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_files = visualizer.save_all_visualizations(data, str(output_dir))
        
        print(f"   ✅ Created {len(saved_files)} visualizations")
        for viz_type, path in saved_files.items():
            print(f"      - {viz_type}: {path}")
        
        return saved_files
    
    async def _generate_blog_post(self, report: IntelligenceReport, visualizations: dict) -> str:
        """Phase 4: Generate final blog post"""

        print("📝 Generating blog post...")

        # Build blog post content
        content = self._build_blog_content(report, visualizations)

        # Save to docs/_posts for Jekyll
        timestamp = datetime.now().strftime("%Y-%m-%d")
        posts_dir = Path("docs/_posts")
        posts_dir.mkdir(parents=True, exist_ok=True)
        filename = posts_dir / f"{timestamp}-intelligence-report.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✅ Blog post saved: {filename}")

        return str(filename)
    
    def _build_blog_content(self, report: IntelligenceReport, visualizations: dict) -> str:
        """Build complete blog post content"""
        
        # Jekyll front matter
        front_matter = f"""---
layout: post
title: "{report.headline}"
date: {datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d %H:%M:%S %z')}
author: The Intelligence Network
tags: [ai, ml, intelligence, trends, analysis]
description: "{report.summary[:160]}"
---

"""
        
        # Executive summary
        summary_section = f"""# 🧠 Intelligence Report

{report.summary}

**Confidence Score**: {report.confidence_score:.0%}  
**Platforms Analyzed**: {', '.join(report.platforms_analyzed)}  
**Total Signals**: {report.total_signals:,}  
**Time Range**: {report.time_range}

---

"""
        
        # Emerging trends
        trends_section = "## 🔥 Emerging Trends\n\n"
        for trend in report.emerging_trends[:5]:
            trends_section += f"""### {trend['topic']}

**Significance**: {trend['significance']}  
**Velocity**: {trend['velocity']:.2f} signals/hour  
**Platforms**: {trend['platforms']}

{trend['insight']}

---

"""
        
        # Cross-platform stories
        cross_platform_section = "## 🌐 Cross-Platform Stories\n\n"
        for story in report.cross_platform_stories[:5]:
            cross_platform_section += f"""### {story['title']}

**Platforms**: {', '.join(story['platforms'])}  
**Total Engagement**: {story['total_engagement']:,}

{story['synthesis']}

[Read more]({story['signals'][0].url if story['signals'] else '#'})

---

"""
        
        # Predictions
        predictions_section = "## 🔮 Predictions\n\n"
        for pred in report.predictions:
            predictions_section += f"""### {pred['topic']}

**Confidence**: {pred['confidence']:.0%}  
**Timeframe**: {pred['timeframe']}

{pred['prediction']}

---

"""
        
        # Visualizations
        viz_section = "## 📊 Interactive Visualizations\n\n"
        for viz_type, path in visualizations.items():
            viz_section += f"- [{viz_type.replace('_', ' ').title()}]({path})\n"
        
        # Combine all sections
        return (
            front_matter +
            summary_section +
            trends_section +
            cross_platform_section +
            predictions_section +
            viz_section
        )


async def main():
    """Main entry point"""

    # Get API key from environment (Ollama Cloud API for GitHub Actions)
    api_key = os.getenv('OLLAMA_CLOUD_API_KEY')

    if not api_key:
        print("❌ Error: OLLAMA_CLOUD_API_KEY environment variable not set")
        print("   Set it with: export OLLAMA_CLOUD_API_KEY='your-key-here'")
        return 1
    
    # Run pipeline
    generator = IntelligenceBlogGenerator(api_key)
    
    try:
        report = await generator.run_full_pipeline()
        print("\n🎉 SUCCESS! Intelligence blog generated.")
        return 0
    
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

