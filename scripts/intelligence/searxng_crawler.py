#!/usr/bin/env python3
"""
SearXNG Crawler - Multi-Instance Social Media Intelligence Gathering

This isn't your basic search wrapper - this is a sophisticated
multi-instance crawler that:
1. Load balances across multiple SearXNG instances
2. Handles rate limiting and failures gracefully
3. Extracts structured data from unstructured results
4. Correlates results across platforms
5. Detects and handles instance failures in real-time

Author: GrumpiBlogged Intelligence Team
"""

import asyncio
import aiohttp
import random
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import hashlib
import re


@dataclass
class SearXNGInstance:
    """Represents a SearXNG instance with health tracking"""
    url: str
    health_score: float = 1.0  # 0.0 = dead, 1.0 = perfect
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    consecutive_failures: int = 0
    avg_response_time: float = 0.0
    total_requests: int = 0
    
    def update_health(self, success: bool, response_time: float):
        """Update health score based on request outcome"""
        self.total_requests += 1
        
        if success:
            self.last_success = datetime.now()
            self.consecutive_failures = 0
            self.health_score = min(1.0, self.health_score + 0.1)
        else:
            self.last_failure = datetime.now()
            self.consecutive_failures += 1
            self.health_score = max(0.0, self.health_score - 0.2)
        
        # Update average response time (exponential moving average)
        alpha = 0.3
        self.avg_response_time = (alpha * response_time + 
                                  (1 - alpha) * self.avg_response_time)
    
    @property
    def is_healthy(self) -> bool:
        """Check if instance is healthy enough to use"""
        return (self.health_score > 0.3 and 
                self.consecutive_failures < 3)


class SearXNGCrawler:
    """
    Advanced SearXNG crawler with multi-instance load balancing,
    intelligent retry logic, and platform-specific result parsing.
    """
    
    def __init__(self, instances: List[str]):
        self.instances = [SearXNGInstance(url=url) for url in instances]
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Platform detection patterns
        self.platform_patterns = {
            'twitter': [r'twitter\.com', r'x\.com'],
            'mastodon': [r'mastodon\.[a-z]+', r'[a-z]+\.social'],
            'reddit': [r'reddit\.com'],
            'youtube': [r'youtube\.com', r'youtu\.be'],
            'github': [r'github\.com'],
            'stackoverflow': [r'stackoverflow\.com'],
            'medium': [r'medium\.com'],
            'substack': [r'substack\.com'],
            'hackernews': [r'news\.ycombinator\.com'],
        }
        
        # Cache to avoid duplicate results
        self.result_cache: Set[str] = set()
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'GrumpiBlogged-Intelligence/2.0 (AI Research Aggregator)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _select_instance(self) -> Optional[SearXNGInstance]:
        """
        Select best instance using weighted random selection
        based on health scores.
        """
        healthy_instances = [i for i in self.instances if i.is_healthy]
        
        if not healthy_instances:
            # All instances unhealthy - try the least bad one
            return max(self.instances, key=lambda i: i.health_score)
        
        # Weighted random selection (healthier instances more likely)
        weights = [i.health_score for i in healthy_instances]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return random.choice(healthy_instances)
        
        normalized_weights = [w / total_weight for w in weights]
        return random.choices(healthy_instances, weights=normalized_weights)[0]
    
    async def search(
        self,
        query: str,
        categories: List[str] = None,
        time_range: str = "day",
        max_results: int = 50,
        engines: List[str] = None
    ) -> List[Dict]:
        """
        Search across SearXNG instances with intelligent load balancing.
        
        Args:
            query: Search query
            categories: List of categories (e.g., ['social media', 'news'])
            time_range: Time range filter ('day', 'week', 'month', 'year')
            max_results: Maximum results to return
            engines: Specific engines to use (e.g., ['twitter', 'reddit'])
        
        Returns:
            List of search results with platform detection and metadata
        """
        
        if categories is None:
            categories = ['social media', 'news', 'general']
        
        all_results = []
        attempts = 0
        max_attempts = len(self.instances) * 2  # Try each instance twice
        
        while len(all_results) < max_results and attempts < max_attempts:
            instance = self._select_instance()
            if not instance:
                break
            
            try:
                results = await self._search_instance(
                    instance=instance,
                    query=query,
                    categories=categories,
                    time_range=time_range,
                    engines=engines
                )
                
                # Filter out duplicates
                new_results = [
                    r for r in results 
                    if self._result_hash(r) not in self.result_cache
                ]
                
                # Add to cache
                for result in new_results:
                    self.result_cache.add(self._result_hash(result))
                
                all_results.extend(new_results)
                
            except Exception as e:
                print(f"   ⚠️  Instance {instance.url} failed: {e}")
            
            attempts += 1
        
        # Sort by relevance and recency
        all_results.sort(
            key=lambda r: (r.get('score', 0), r.get('publishedDate', '')),
            reverse=True
        )
        
        return all_results[:max_results]
    
    async def _search_instance(
        self,
        instance: SearXNGInstance,
        query: str,
        categories: List[str],
        time_range: str,
        engines: List[str] = None,
        retry_count: int = 0,
        max_retries: int = 3
    ) -> List[Dict]:
        """
        Execute search on a specific instance with retry logic and delays

        Implements:
        - Exponential backoff (1s, 2s, 4s delays)
        - Rate limiting protection (2s delay between requests)
        - Automatic retry on transient failures
        """

        start_time = datetime.now()

        # Add delay to avoid rate limiting (2 seconds between requests)
        await asyncio.sleep(2.0)

        try:
            # Build search parameters
            params = {
                'q': query,
                'format': 'json',
                'time_range': time_range,
                'categories': ','.join(categories)
            }

            if engines:
                params['engines'] = ','.join(engines)

            # Execute search with timeout
            async with self.session.get(
                f"{instance.url}/search",
                params=params,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                data = await response.json()

            # Parse results
            results = self._parse_results(data.get('results', []))

            # Update instance health
            response_time = (datetime.now() - start_time).total_seconds()
            instance.update_health(success=True, response_time=response_time)

            return results

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            # Update instance health
            response_time = (datetime.now() - start_time).total_seconds()
            instance.update_health(success=False, response_time=response_time)

            # Retry with exponential backoff
            if retry_count < max_retries:
                backoff_delay = 2 ** retry_count  # 1s, 2s, 4s
                print(f"   ⏳ Retrying {instance.url} in {backoff_delay}s (attempt {retry_count + 1}/{max_retries})")
                await asyncio.sleep(backoff_delay)

                return await self._search_instance(
                    instance=instance,
                    query=query,
                    categories=categories,
                    time_range=time_range,
                    engines=engines,
                    retry_count=retry_count + 1,
                    max_retries=max_retries
                )
            else:
                raise
    
    def _parse_results(self, raw_results: List[Dict]) -> List[Dict]:
        """
        Parse and enrich search results with platform detection,
        engagement metrics extraction, and metadata normalization.
        """
        
        parsed = []
        
        for result in raw_results:
            # Detect platform
            platform = self._detect_platform(result.get('url', ''))
            
            # Extract engagement metrics (if available in snippet)
            engagement = self._extract_engagement(result.get('content', ''))
            
            # Parse published date
            published = self._parse_date(result.get('publishedDate'))
            
            # Build enriched result
            enriched = {
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'content': result.get('content', ''),
                'platform': platform,
                'engine': result.get('engine', 'unknown'),
                'publishedDate': published,
                'engagement': engagement,
                'score': result.get('score', 0),
                'raw': result  # Keep original for debugging
            }
            
            parsed.append(enriched)
        
        return parsed
    
    def _detect_platform(self, url: str) -> str:
        """Detect platform from URL using regex patterns"""
        
        for platform, patterns in self.platform_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return platform
        
        return 'unknown'
    
    def _extract_engagement(self, content: str) -> Dict[str, int]:
        """
        Extract engagement metrics from content snippet.
        
        Looks for patterns like:
        - "123 likes"
        - "45 retweets"
        - "67 comments"
        - "890 upvotes"
        - "12K shares"
        """
        
        engagement = {}
        
        # Patterns for different metrics
        patterns = {
            'likes': r'(\d+(?:\.\d+)?[KMB]?)\s*(?:likes?|hearts?|favorites?)',
            'shares': r'(\d+(?:\.\d+)?[KMB]?)\s*(?:shares?|retweets?|reposts?)',
            'comments': r'(\d+(?:\.\d+)?[KMB]?)\s*(?:comments?|replies?)',
            'upvotes': r'(\d+(?:\.\d+)?[KMB]?)\s*(?:upvotes?|points?)',
            'views': r'(\d+(?:\.\d+)?[KMB]?)\s*(?:views?|watches?)',
        }
        
        for metric, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value_str = match.group(1)
                engagement[metric] = self._parse_number(value_str)
        
        return engagement
    
    def _parse_number(self, value_str: str) -> int:
        """Parse numbers like '1.2K', '3.5M', '100' into integers"""
        
        multipliers = {
            'K': 1_000,
            'M': 1_000_000,
            'B': 1_000_000_000
        }
        
        value_str = value_str.upper().strip()
        
        for suffix, multiplier in multipliers.items():
            if value_str.endswith(suffix):
                number = float(value_str[:-1])
                return int(number * multiplier)
        
        try:
            return int(float(value_str))
        except ValueError:
            return 0
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse various date formats into datetime"""
        
        if not date_str:
            return None
        
        # Try ISO format first
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pass
        
        # Try common formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _result_hash(self, result: Dict) -> str:
        """Generate hash for deduplication"""
        
        # Use URL as primary identifier
        url = result.get('url', '')
        if url:
            return hashlib.md5(url.encode()).hexdigest()
        
        # Fallback to title + content hash
        title = result.get('title', '')
        content = result.get('content', '')[:200]  # First 200 chars
        combined = f"{title}|{content}"
        
        return hashlib.md5(combined.encode()).hexdigest()
    
    async def search_social_media(
        self,
        query: str,
        platforms: List[str] = None,
        time_range: str = "day",
        max_results: int = 50
    ) -> Dict[str, List[Dict]]:
        """
        Search social media platforms specifically.
        
        Returns results grouped by platform.
        """
        
        if platforms is None:
            platforms = ['twitter', 'mastodon', 'reddit']
        
        # Search with social media category
        results = await self.search(
            query=query,
            categories=['social media'],
            time_range=time_range,
            max_results=max_results * 2  # Get more, filter later
        )
        
        # Group by platform
        by_platform = {platform: [] for platform in platforms}
        by_platform['other'] = []
        
        for result in results:
            platform = result['platform']
            if platform in by_platform:
                by_platform[platform].append(result)
            else:
                by_platform['other'].append(result)
        
        # Limit each platform to max_results
        for platform in by_platform:
            by_platform[platform] = by_platform[platform][:max_results]
        
        return by_platform
    
    def get_instance_health(self) -> List[Dict]:
        """Get health status of all instances"""
        
        return [
            {
                'url': instance.url,
                'health_score': instance.health_score,
                'is_healthy': instance.is_healthy,
                'consecutive_failures': instance.consecutive_failures,
                'avg_response_time': instance.avg_response_time,
                'total_requests': instance.total_requests,
                'last_success': instance.last_success.isoformat() if instance.last_success else None,
                'last_failure': instance.last_failure.isoformat() if instance.last_failure else None,
            }
            for instance in self.instances
        ]


# Example usage
async def main():
    """Test the SearXNG crawler"""
    
    instances = [
        "https://searx.be",
        "https://search.sapti.me",
        "https://searx.tiekoetter.com",
        "https://searx.work"
    ]
    
    async with SearXNGCrawler(instances) as crawler:
        print("🔍 Searching for AI/ML content across social media...")
        
        results = await crawler.search_social_media(
            query="local LLM OR Ollama OR AI models",
            platforms=['twitter', 'reddit', 'mastodon'],
            time_range="day",
            max_results=20
        )
        
        print(f"\n📊 Results by platform:")
        for platform, posts in results.items():
            if posts:
                print(f"\n{platform.upper()}: {len(posts)} posts")
                for post in posts[:3]:
                    print(f"  - {post['title'][:80]}...")
                    print(f"    Engagement: {post['engagement']}")
        
        print(f"\n🏥 Instance Health:")
        for health in crawler.get_instance_health():
            status = "✅" if health['is_healthy'] else "❌"
            print(f"  {status} {health['url']}: {health['health_score']:.2f}")


if __name__ == "__main__":
    asyncio.run(main())

