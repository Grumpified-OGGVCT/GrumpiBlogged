#!/usr/bin/env python3
"""
Hacker News Graph Crawler - Elite Tech Discussion Intelligence

This crawler doesn't just fetch HN stories - it builds a complete
discussion graph including:
1. Story ranking and velocity analysis
2. Comment thread analysis and sentiment
3. User influence mapping (karma, posting patterns)
4. Topic clustering and trend detection
5. Cross-reference detection (same story on multiple platforms)

Uses HN Algolia API for search + Firebase API for real-time data.
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import networkx as nx


@dataclass
class HNStory:
    """Represents a Hacker News story with full metadata"""
    id: int
    title: str
    url: Optional[str]
    text: Optional[str]  # For Ask HN, Show HN
    author: str
    points: int
    num_comments: int
    created_at: datetime
    story_type: str  # 'story', 'ask_hn', 'show_hn', 'job'
    
    # Computed fields
    velocity: float = 0.0  # Points per hour
    comment_ratio: float = 0.0  # Comments per point
    engagement_score: float = 0.0
    rank: int = 0
    
    # Related data
    comments: List['HNComment'] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Compute derived metrics"""
        age_hours = (datetime.now() - self.created_at).total_seconds() / 3600
        self.velocity = self.points / max(age_hours, 1)
        self.comment_ratio = self.num_comments / max(self.points, 1)
        
        # Engagement score: weighted combination
        self.engagement_score = (
            self.points * 1.0 +
            self.num_comments * 3.0 +
            self.velocity * 10.0
        )
    
    @property
    def hn_url(self) -> str:
        """Get HN discussion URL"""
        return f"https://news.ycombinator.com/item?id={self.id}"


@dataclass
class HNComment:
    """Represents a Hacker News comment"""
    id: int
    author: str
    text: str
    created_at: datetime
    parent_id: int
    depth: int = 0
    replies: List['HNComment'] = field(default_factory=list)


class HackerNewsGraphCrawler:
    """
    Advanced Hacker News crawler using both Algolia API (search)
    and Firebase API (real-time data).
    """
    
    ALGOLIA_API = "https://hn.algolia.com/api/v1"
    FIREBASE_API = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Graph structures
        self.user_graph = nx.DiGraph()  # User interaction graph
        self.topic_graph = nx.Graph()   # Topic co-occurrence
        
        # Caches
        self.story_cache: Dict[int, HNStory] = {}
        self.user_cache: Dict[str, Dict] = defaultdict(lambda: {
            'stories': 0,
            'comments': 0,
            'total_points': 0,
            'topics': set()
        })
        
        # AI/ML keywords for filtering
        self.ai_keywords = {
            'ai', 'ml', 'llm', 'gpt', 'claude', 'gemini', 'openai', 'anthropic',
            'machine learning', 'deep learning', 'neural network', 'transformer',
            'diffusion', 'stable diffusion', 'midjourney', 'dall-e',
            'langchain', 'llamaindex', 'vector database', 'embedding',
            'fine-tuning', 'rlhf', 'reinforcement learning',
            'ollama', 'huggingface', 'pytorch', 'tensorflow',
            'rag', 'retrieval', 'agent', 'autonomous', 'agi'
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'GrumpiBlogged-Intelligence/2.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def crawl(
        self,
        lookback_hours: int = 24,
        min_points: int = 50,
        include_comments: bool = True,
        max_stories: int = 100
    ) -> List[HNStory]:
        """
        Crawl Hacker News for AI/ML stories.
        
        Args:
            lookback_hours: How far back to look
            min_points: Minimum story points
            include_comments: Whether to fetch comments
            max_stories: Maximum stories to return
        
        Returns:
            List of HNStory objects
        """
        
        print("   🔄 Searching Hacker News for AI/ML stories...")
        
        # Search using Algolia API
        stories = await self._search_stories(
            lookback_hours=lookback_hours,
            min_points=min_points,
            max_results=max_stories * 2  # Get more, filter later
        )
        
        print(f"      ✅ Found {len(stories)} stories")
        
        # Fetch comments if requested
        if include_comments:
            print("   🔄 Fetching comments...")
            for story in stories[:max_stories]:  # Limit to avoid rate limits
                try:
                    comments = await self._fetch_comments(story.id)
                    story.comments = comments
                    
                    # Build user graph
                    self._build_user_graph(story, comments)
                except Exception as e:
                    print(f"      ⚠️  Failed to fetch comments for {story.id}: {e}")
        
        # Build topic graph
        self._build_topic_graph(stories)
        
        # Sort by engagement score
        stories.sort(key=lambda s: s.engagement_score, reverse=True)
        
        return stories[:max_stories]
    
    async def _search_stories(
        self,
        lookback_hours: int,
        min_points: int,
        max_results: int
    ) -> List[HNStory]:
        """Search for AI/ML stories using Algolia API"""
        
        # Build search query
        query_parts = []
        for keyword in list(self.ai_keywords)[:10]:  # Use top 10 keywords
            query_parts.append(keyword)
        
        query = " OR ".join(query_parts)
        
        # Calculate timestamp filter
        cutoff_timestamp = int((datetime.now() - timedelta(hours=lookback_hours)).timestamp())
        
        # Search parameters
        params = {
            'query': query,
            'tags': 'story',  # Only stories, not comments
            'numericFilters': f'points>{min_points},created_at_i>{cutoff_timestamp}',
            'hitsPerPage': max_results
        }
        
        url = f"{self.ALGOLIA_API}/search"
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            data = await response.json()
        
        # Parse stories
        stories = []
        for hit in data.get('hits', []):
            story = self._parse_story(hit)
            if story:
                stories.append(story)
                self.story_cache[story.id] = story
                
                # Update user cache
                self.user_cache[story.author]['stories'] += 1
                self.user_cache[story.author]['total_points'] += story.points
        
        return stories
    
    def _parse_story(self, hit: Dict) -> Optional[HNStory]:
        """Parse Algolia search hit into HNStory"""
        
        try:
            # Determine story type
            story_type = 'story'
            title = hit.get('title', '')
            
            if title.lower().startswith('ask hn'):
                story_type = 'ask_hn'
            elif title.lower().startswith('show hn'):
                story_type = 'show_hn'
            elif 'job' in hit.get('_tags', []):
                story_type = 'job'
            
            # Extract tags
            tags = []
            for keyword in self.ai_keywords:
                if keyword in title.lower() or keyword in hit.get('story_text', '').lower():
                    tags.append(keyword)
            
            story = HNStory(
                id=hit['objectID'],
                title=title,
                url=hit.get('url'),
                text=hit.get('story_text'),
                author=hit.get('author', 'unknown'),
                points=hit.get('points', 0),
                num_comments=hit.get('num_comments', 0),
                created_at=datetime.fromtimestamp(hit.get('created_at_i', 0)),
                story_type=story_type,
                tags=tags
            )
            
            return story
        
        except Exception as e:
            print(f"      ⚠️  Failed to parse story: {e}")
            return None
    
    async def _fetch_comments(self, story_id: int, max_depth: int = 3) -> List[HNComment]:
        """Fetch comments for a story using Firebase API"""
        
        # Get story item (includes comment IDs)
        url = f"{self.FIREBASE_API}/item/{story_id}.json"
        
        async with self.session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
        
        if not data or 'kids' not in data:
            return []
        
        # Fetch top-level comments
        comment_ids = data['kids']
        comments = []
        
        for comment_id in comment_ids[:50]:  # Limit to 50 top-level comments
            comment = await self._fetch_comment(comment_id, depth=0, max_depth=max_depth)
            if comment:
                comments.append(comment)
        
        return comments
    
    async def _fetch_comment(self, comment_id: int, depth: int, max_depth: int) -> Optional[HNComment]:
        """Recursively fetch comment and its replies"""
        
        if depth > max_depth:
            return None
        
        url = f"{self.FIREBASE_API}/item/{comment_id}.json"
        
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
            
            if not data or data.get('deleted') or data.get('dead'):
                return None
            
            comment = HNComment(
                id=comment_id,
                author=data.get('by', 'unknown'),
                text=data.get('text', ''),
                created_at=datetime.fromtimestamp(data.get('time', 0)),
                parent_id=data.get('parent', 0),
                depth=depth
            )
            
            # Update user cache
            self.user_cache[comment.author]['comments'] += 1
            
            # Fetch replies
            if 'kids' in data:
                for kid_id in data['kids'][:10]:  # Limit replies
                    reply = await self._fetch_comment(kid_id, depth + 1, max_depth)
                    if reply:
                        comment.replies.append(reply)
            
            return comment
        
        except Exception:
            return None
    
    def _build_user_graph(self, story: HNStory, comments: List[HNComment]):
        """Build user interaction graph"""
        
        # Add story author
        self.user_graph.add_node(story.author, type='author')
        
        # Add edges for comments
        for comment in comments:
            self.user_graph.add_node(comment.author, type='commenter')
            self.user_graph.add_edge(
                comment.author,
                story.author,
                weight=1,
                interaction='comment'
            )
            
            # Add reply edges
            self._add_comment_edges(comment)
    
    def _add_comment_edges(self, comment: HNComment):
        """Recursively add edges for comment replies"""
        
        for reply in comment.replies:
            self.user_graph.add_edge(
                reply.author,
                comment.author,
                weight=1,
                interaction='reply'
            )
            self._add_comment_edges(reply)
    
    def _build_topic_graph(self, stories: List[HNStory]):
        """Build topic co-occurrence graph"""
        
        for story in stories:
            # Add nodes for tags
            for tag in story.tags:
                if not self.topic_graph.has_node(tag):
                    self.topic_graph.add_node(tag, count=0)
                self.topic_graph.nodes[tag]['count'] += 1
            
            # Add edges for co-occurring tags
            for i, tag1 in enumerate(story.tags):
                for tag2 in story.tags[i+1:]:
                    if self.topic_graph.has_edge(tag1, tag2):
                        self.topic_graph[tag1][tag2]['weight'] += 1
                    else:
                        self.topic_graph.add_edge(tag1, tag2, weight=1)
    
    def get_top_users(self, top_n: int = 20) -> List[Dict]:
        """Get top users by influence"""
        
        users = []
        for user, stats in self.user_cache.items():
            if user == 'unknown':
                continue
            
            influence = (
                stats['stories'] * 20 +
                stats['comments'] * 2 +
                stats['total_points']
            )
            
            users.append({
                'username': user,
                'stories': stats['stories'],
                'comments': stats['comments'],
                'total_points': stats['total_points'],
                'influence': influence
            })
        
        users.sort(key=lambda u: u['influence'], reverse=True)
        return users[:top_n]
    
    def get_trending_topics(self, top_n: int = 20) -> List[Dict]:
        """Get trending topics"""
        
        topics = []
        for topic in self.topic_graph.nodes():
            count = self.topic_graph.nodes[topic]['count']
            connections = list(self.topic_graph.neighbors(topic))
            
            topics.append({
                'topic': topic,
                'count': count,
                'connections': len(connections),
                'related_topics': connections[:5]
            })
        
        topics.sort(key=lambda t: t['count'], reverse=True)
        return topics[:top_n]


# Example usage
async def main():
    """Test the HN crawler"""
    
    async with HackerNewsGraphCrawler() as crawler:
        print("🔍 Crawling Hacker News for AI/ML stories...")
        
        stories = await crawler.crawl(
            lookback_hours=24,
            min_points=50,
            include_comments=True,
            max_stories=50
        )
        
        print(f"\n📊 Found {len(stories)} stories")
        
        print("\n🏆 Top Stories:")
        for story in stories[:5]:
            print(f"  - {story.title[:60]}...")
            print(f"    Points: {story.points}, Comments: {story.num_comments}, Velocity: {story.velocity:.1f}")
            print(f"    {story.hn_url}")
        
        print("\n👥 Top Users:")
        for user in crawler.get_top_users(10):
            print(f"  - {user['username']}: {user['influence']:.0f} influence")
        
        print("\n🔥 Trending Topics:")
        for topic in crawler.get_trending_topics(10):
            print(f"  - {topic['topic']}: {topic['count']} mentions")


if __name__ == "__main__":
    asyncio.run(main())

