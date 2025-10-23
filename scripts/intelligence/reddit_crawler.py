#!/usr/bin/env python3
"""
Reddit Graph Crawler - Advanced Social Network Analysis

This isn't just scraping Reddit - this is building a complete
social graph of AI/ML discussions including:
1. Post and comment threading
2. User influence mapping
3. Community detection
4. Sentiment flow analysis
5. Cross-subreddit correlation

No API key needed - we use Reddit's public JSON endpoints.
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import networkx as nx
from collections import defaultdict
import re


@dataclass
class RedditPost:
    """Represents a Reddit post with full metadata"""
    id: str
    subreddit: str
    title: str
    selftext: str
    author: str
    score: int
    upvote_ratio: float
    num_comments: int
    created_utc: datetime
    url: str
    permalink: str
    flair: Optional[str] = None
    awards: int = 0
    is_self: bool = True
    domain: str = ""
    
    # Computed fields
    engagement_score: float = 0.0
    velocity: float = 0.0  # Score per hour
    comments: List['RedditComment'] = field(default_factory=list)
    
    def __post_init__(self):
        """Compute derived metrics"""
        age_hours = (datetime.now() - self.created_utc).total_seconds() / 3600
        self.velocity = self.score / max(age_hours, 1)
        
        # Engagement score: weighted combination of metrics
        self.engagement_score = (
            self.score * 1.0 +
            self.num_comments * 2.0 +
            self.awards * 5.0 +
            self.upvote_ratio * 100
        )


@dataclass
class RedditComment:
    """Represents a Reddit comment"""
    id: str
    author: str
    body: str
    score: int
    created_utc: datetime
    parent_id: str
    depth: int = 0
    replies: List['RedditComment'] = field(default_factory=list)


class RedditGraphCrawler:
    """
    Advanced Reddit crawler that builds a complete social graph
    of discussions, users, and communities.
    """
    
    def __init__(self, subreddits: List[str]):
        self.subreddits = subreddits
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Graph structures
        self.user_graph = nx.DiGraph()  # User interaction graph
        self.topic_graph = nx.Graph()   # Topic co-occurrence graph
        self.subreddit_graph = nx.Graph()  # Cross-subreddit graph
        
        # Caches
        self.post_cache: Dict[str, RedditPost] = {}
        self.user_cache: Dict[str, Dict] = defaultdict(lambda: {
            'posts': 0,
            'comments': 0,
            'total_score': 0,
            'subreddits': set()
        })
        
        # Rate limiting
        self.last_request_time = datetime.now()
        self.min_request_interval = 2.0  # Reddit asks for 2 seconds between requests
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'GrumpiBlogged-Intelligence/2.0 (AI Research Aggregator; Contact: grumpiblogged@example.com)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = (datetime.now() - self.last_request_time).total_seconds()
        if elapsed < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - elapsed)
        self.last_request_time = datetime.now()
    
    async def crawl(
        self,
        lookback_hours: int = 24,
        min_score: int = 50,
        include_comments: bool = True,
        max_posts_per_subreddit: int = 100
    ) -> List[RedditPost]:
        """
        Crawl multiple subreddits and build social graph.
        
        Args:
            lookback_hours: How far back to look
            min_score: Minimum post score to include
            include_comments: Whether to fetch comments
            max_posts_per_subreddit: Max posts per subreddit
        
        Returns:
            List of RedditPost objects with full metadata
        """
        
        all_posts = []
        
        # Crawl each subreddit
        for subreddit in self.subreddits:
            print(f"   🔄 Crawling r/{subreddit}...")
            
            try:
                posts = await self._crawl_subreddit(
                    subreddit=subreddit,
                    lookback_hours=lookback_hours,
                    min_score=min_score,
                    max_posts=max_posts_per_subreddit
                )
                
                # Fetch comments if requested
                if include_comments:
                    for post in posts:
                        try:
                            comments = await self._fetch_comments(post)
                            post.comments = comments
                            
                            # Build user interaction graph from comments
                            self._build_user_graph(post, comments)
                        except Exception as e:
                            print(f"      ⚠️  Failed to fetch comments for {post.id}: {e}")
                
                all_posts.extend(posts)
                print(f"      ✅ Found {len(posts)} posts")
                
            except Exception as e:
                print(f"      ❌ Failed to crawl r/{subreddit}: {e}")
        
        # Build topic graph
        self._build_topic_graph(all_posts)
        
        # Build cross-subreddit graph
        self._build_subreddit_graph(all_posts)
        
        # Sort by engagement score
        all_posts.sort(key=lambda p: p.engagement_score, reverse=True)
        
        return all_posts
    
    async def _crawl_subreddit(
        self,
        subreddit: str,
        lookback_hours: int,
        min_score: int,
        max_posts: int
    ) -> List[RedditPost]:
        """Crawl a single subreddit"""
        
        posts = []
        cutoff_time = datetime.now() - timedelta(hours=lookback_hours)
        
        # Try multiple sorting methods to get diverse content
        for sort in ['hot', 'new', 'top']:
            await self._rate_limit()
            
            try:
                url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
                params = {'limit': 100}
                
                if sort == 'top':
                    params['t'] = 'day' if lookback_hours <= 24 else 'week'
                
                async with self.session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                
                # Parse posts
                for item in data['data']['children']:
                    post_data = item['data']
                    
                    # Parse timestamp
                    created = datetime.fromtimestamp(post_data['created_utc'])
                    
                    # Filter by time and score
                    if created < cutoff_time:
                        continue
                    if post_data['score'] < min_score:
                        continue
                    
                    # Create post object
                    post = RedditPost(
                        id=post_data['id'],
                        subreddit=post_data['subreddit'],
                        title=post_data['title'],
                        selftext=post_data.get('selftext', ''),
                        author=post_data['author'],
                        score=post_data['score'],
                        upvote_ratio=post_data.get('upvote_ratio', 0.5),
                        num_comments=post_data['num_comments'],
                        created_utc=created,
                        url=post_data['url'],
                        permalink=f"https://reddit.com{post_data['permalink']}",
                        flair=post_data.get('link_flair_text'),
                        awards=post_data.get('total_awards_received', 0),
                        is_self=post_data['is_self'],
                        domain=post_data.get('domain', '')
                    )
                    
                    # Avoid duplicates
                    if post.id not in self.post_cache:
                        self.post_cache[post.id] = post
                        posts.append(post)
                        
                        # Update user cache
                        self.user_cache[post.author]['posts'] += 1
                        self.user_cache[post.author]['total_score'] += post.score
                        self.user_cache[post.author]['subreddits'].add(subreddit)
                
            except Exception as e:
                print(f"      ⚠️  Failed to fetch {sort} posts: {e}")
        
        return posts[:max_posts]
    
    async def _fetch_comments(self, post: RedditPost, max_depth: int = 3) -> List[RedditComment]:
        """Fetch comments for a post"""
        
        await self._rate_limit()
        
        url = f"https://www.reddit.com{post.permalink}.json"
        
        async with self.session.get(url, params={'limit': 500}) as response:
            response.raise_for_status()
            data = await response.json()
        
        # Reddit returns [post_data, comments_data]
        if len(data) < 2:
            return []
        
        comments_data = data[1]['data']['children']
        
        # Parse comment tree
        comments = []
        for item in comments_data:
            if item['kind'] != 't1':  # t1 = comment
                continue
            
            comment = self._parse_comment(item['data'], depth=0, max_depth=max_depth)
            if comment:
                comments.append(comment)
        
        return comments
    
    def _parse_comment(self, data: Dict, depth: int, max_depth: int) -> Optional[RedditComment]:
        """Recursively parse comment tree"""
        
        if depth > max_depth:
            return None
        
        # Skip deleted/removed comments
        if data.get('author') in ['[deleted]', '[removed]']:
            return None
        
        comment = RedditComment(
            id=data['id'],
            author=data['author'],
            body=data.get('body', ''),
            score=data.get('score', 0),
            created_utc=datetime.fromtimestamp(data['created_utc']),
            parent_id=data.get('parent_id', ''),
            depth=depth
        )
        
        # Update user cache
        self.user_cache[comment.author]['comments'] += 1
        self.user_cache[comment.author]['total_score'] += comment.score
        
        # Parse replies
        replies_data = data.get('replies')
        if replies_data and isinstance(replies_data, dict):
            for reply_item in replies_data['data']['children']:
                if reply_item['kind'] != 't1':
                    continue
                
                reply = self._parse_comment(
                    reply_item['data'],
                    depth=depth + 1,
                    max_depth=max_depth
                )
                if reply:
                    comment.replies.append(reply)
        
        return comment
    
    def _build_user_graph(self, post: RedditPost, comments: List[RedditComment]):
        """Build user interaction graph from post and comments"""
        
        # Add post author as node
        self.user_graph.add_node(post.author, type='author')
        
        # Add edges for each comment (commenter -> post author)
        for comment in comments:
            self.user_graph.add_node(comment.author, type='commenter')
            self.user_graph.add_edge(
                comment.author,
                post.author,
                weight=1,
                interaction='comment'
            )
            
            # Add edges for comment replies
            self._add_comment_edges(comment)
    
    def _add_comment_edges(self, comment: RedditComment):
        """Recursively add edges for comment replies"""
        
        for reply in comment.replies:
            self.user_graph.add_edge(
                reply.author,
                comment.author,
                weight=1,
                interaction='reply'
            )
            
            # Recurse
            self._add_comment_edges(reply)
    
    def _build_topic_graph(self, posts: List[RedditPost]):
        """Build topic co-occurrence graph"""
        
        # Extract topics from titles and content
        for post in posts:
            topics = self._extract_topics(post.title + " " + post.selftext)
            
            # Add nodes for topics
            for topic in topics:
                if not self.topic_graph.has_node(topic):
                    self.topic_graph.add_node(topic, count=0)
                self.topic_graph.nodes[topic]['count'] += 1
            
            # Add edges for co-occurring topics
            for i, topic1 in enumerate(topics):
                for topic2 in topics[i+1:]:
                    if self.topic_graph.has_edge(topic1, topic2):
                        self.topic_graph[topic1][topic2]['weight'] += 1
                    else:
                        self.topic_graph.add_edge(topic1, topic2, weight=1)
    
    def _build_subreddit_graph(self, posts: List[RedditPost]):
        """Build cross-subreddit graph based on shared users"""
        
        # Track which users post in which subreddits
        user_subreddits = defaultdict(set)
        
        for post in posts:
            user_subreddits[post.author].add(post.subreddit)
        
        # Add edges between subreddits that share users
        for user, subreddits in user_subreddits.items():
            subreddit_list = list(subreddits)
            for i, sub1 in enumerate(subreddit_list):
                for sub2 in subreddit_list[i+1:]:
                    if self.subreddit_graph.has_edge(sub1, sub2):
                        self.subreddit_graph[sub1][sub2]['weight'] += 1
                    else:
                        self.subreddit_graph.add_edge(sub1, sub2, weight=1)
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text using keyword matching"""
        
        # AI/ML keywords to look for
        keywords = {
            'llm', 'gpt', 'claude', 'gemini', 'llama', 'mistral', 'mixtral',
            'transformer', 'attention', 'bert', 'diffusion', 'stable-diffusion',
            'reinforcement-learning', 'rl', 'deep-learning', 'neural-network',
            'fine-tuning', 'quantization', 'lora', 'qlora', 'gguf',
            'ollama', 'huggingface', 'pytorch', 'tensorflow', 'jax',
            'langchain', 'llamaindex', 'vector-database', 'embedding',
            'rag', 'retrieval', 'agent', 'autonomous', 'multimodal'
        }
        
        text_lower = text.lower()
        found_topics = []
        
        for keyword in keywords:
            if keyword in text_lower:
                found_topics.append(keyword)
        
        return found_topics
    
    def get_top_users(self, top_n: int = 20) -> List[Dict]:
        """Get top users by influence"""
        
        users = []
        for user, stats in self.user_cache.items():
            if user in ['[deleted]', '[removed]', 'AutoModerator']:
                continue
            
            # Compute influence score
            influence = (
                stats['posts'] * 10 +
                stats['comments'] * 2 +
                stats['total_score']
            )
            
            users.append({
                'username': user,
                'posts': stats['posts'],
                'comments': stats['comments'],
                'total_score': stats['total_score'],
                'subreddits': list(stats['subreddits']),
                'influence': influence
            })
        
        users.sort(key=lambda u: u['influence'], reverse=True)
        return users[:top_n]
    
    def get_trending_topics(self, top_n: int = 20) -> List[Dict]:
        """Get trending topics from topic graph"""
        
        topics = []
        for topic in self.topic_graph.nodes():
            count = self.topic_graph.nodes[topic]['count']
            
            # Get connected topics
            connections = list(self.topic_graph.neighbors(topic))
            
            topics.append({
                'topic': topic,
                'count': count,
                'connections': len(connections),
                'related_topics': connections[:5]
            })
        
        topics.sort(key=lambda t: t['count'], reverse=True)
        return topics[:top_n]
    
    def get_subreddit_relationships(self) -> List[Dict]:
        """Get cross-subreddit relationships"""
        
        relationships = []
        for sub1, sub2 in self.subreddit_graph.edges():
            weight = self.subreddit_graph[sub1][sub2]['weight']
            relationships.append({
                'subreddit1': sub1,
                'subreddit2': sub2,
                'shared_users': weight
            })
        
        relationships.sort(key=lambda r: r['shared_users'], reverse=True)
        return relationships


# Example usage
async def main():
    """Test the Reddit crawler"""
    
    subreddits = ['LocalLLaMA', 'MachineLearning', 'StableDiffusion']
    
    async with RedditGraphCrawler(subreddits) as crawler:
        print("🔍 Crawling Reddit for AI/ML discussions...")
        
        posts = await crawler.crawl(
            lookback_hours=24,
            min_score=50,
            include_comments=True,
            max_posts_per_subreddit=50
        )
        
        print(f"\n📊 Found {len(posts)} high-quality posts")
        
        print("\n🏆 Top Posts:")
        for post in posts[:5]:
            print(f"  - [{post.subreddit}] {post.title[:60]}...")
            print(f"    Score: {post.score}, Comments: {post.num_comments}, Engagement: {post.engagement_score:.0f}")
        
        print("\n👥 Top Users:")
        for user in crawler.get_top_users(10):
            print(f"  - u/{user['username']}: {user['influence']:.0f} influence")
        
        print("\n🔥 Trending Topics:")
        for topic in crawler.get_trending_topics(10):
            print(f"  - {topic['topic']}: {topic['count']} mentions")


if __name__ == "__main__":
    asyncio.run(main())

