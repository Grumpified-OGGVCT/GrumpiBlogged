#!/usr/bin/env python3
"""
Intelligence Synthesis Engine - Turning Raw Data into Compelling Narratives

This is where the magic happens. We take raw intelligence from multiple
sources and synthesize it into:
1. Coherent narratives that tell a story
2. Actionable insights with predictions
3. Cross-platform correlation analysis
4. Trend detection and future forecasting
5. Influence mapping and community dynamics

This isn't just "summarization" - this is SYNTHESIS.
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from collections import defaultdict, Counter


@dataclass
class IntelligenceReport:
    """Complete intelligence report ready for blog post generation"""
    
    # Executive summary
    headline: str
    summary: str
    confidence_score: float  # 0-1
    
    # Core intelligence
    emerging_trends: List[Dict]
    cross_platform_stories: List[Dict]
    top_influencers: List[Dict]
    topic_clusters: Dict[str, List]
    
    # Predictions
    predictions: List[Dict]
    
    # Metadata
    total_signals: int
    platforms_analyzed: List[str]
    time_range: str
    generated_at: datetime


class OllamaCloudClient:
    """
    Enhanced Ollama Cloud API Client with ALL Turbo capabilities:
    - Thinking (advanced reasoning)
    - Vision (image analysis)
    - Web Search (fallback when scraping fails)
    - Tool Calling (orchestrate external APIs)
    - Embeddings (semantic clustering)
    - Structured Outputs (clean JSON responses)
    """

    def __init__(self, api_key: str, base_url: str = "https://api.ollama.ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        thinking: bool = False,
        web_search: bool = False,
        structured_output: Optional[Dict] = None,
        images: Optional[List[str]] = None,
        tools: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate text using Ollama Cloud with ALL capabilities

        Args:
            model: Model name (e.g., 'deepseek-v3.1:671b-cloud')
            prompt: Text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            thinking: Enable advanced reasoning mode
            web_search: Enable web search capability
            structured_output: JSON schema for structured response
            images: List of image URLs or base64 data for vision
            tools: List of tool definitions for tool calling
        """

        url = f"{self.base_url}/api/chat"

        # Build message content
        message_content = prompt
        if images:
            # Vision mode: include images
            message_content = {
                'text': prompt,
                'images': images
            }

        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': message_content}],
            'stream': False,
            'options': {
                'num_predict': max_tokens,
                'temperature': temperature
            }
        }

        # Enable thinking mode
        if thinking:
            payload['options']['thinking'] = True

        # Enable web search
        if web_search:
            payload['web_search'] = True

        # Enable structured outputs
        if structured_output:
            payload['format'] = structured_output

        # Enable tool calling
        if tools:
            payload['tools'] = tools

        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data['message']['content']

    async def web_search(
        self,
        model: str,
        query: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Perform web search using Ollama Turbo (fallback when scraping fails)

        Args:
            model: Model to use for search synthesis
            query: Search query
            max_tokens: Max response length
            temperature: Sampling temperature

        Returns:
            Synthesized search results
        """
        return await self.generate(
            model=model,
            prompt=query,
            max_tokens=max_tokens,
            temperature=temperature,
            web_search=True
        )

    async def analyze_image(
        self,
        model: str,
        image_url: str,
        prompt: str,
        max_tokens: int = 1000
    ) -> str:
        """
        Analyze image using vision capability

        Args:
            model: Vision-capable model (e.g., 'qwen3-vl:235b-cloud')
            image_url: URL or base64 data of image
            prompt: Analysis prompt
            max_tokens: Max response length

        Returns:
            Image analysis
        """
        return await self.generate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            images=[image_url]
        )

    async def structured_generate(
        self,
        model: str,
        prompt: str,
        schema: Dict,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict:
        """
        Generate structured JSON output matching schema

        Args:
            model: Model to use
            prompt: Generation prompt
            schema: JSON schema for output
            max_tokens: Max tokens
            temperature: Sampling temperature

        Returns:
            Parsed JSON matching schema
        """
        import json
        response = await self.generate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            structured_output=schema
        )
        return json.loads(response)

    async def embed_batch(self, model: str, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""

        embeddings = []

        for text in texts:
            url = f"{self.base_url}/api/embeddings"
            payload = {'model': model, 'prompt': text}

            async with self.session.post(url, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                embeddings.append(data['embedding'])

        return embeddings


class SynthesisEngine:
    """
    Advanced synthesis engine that transforms raw intelligence
    into compelling, actionable narratives.

    Enhanced with ALL Ollama Turbo capabilities:
    - Thinking mode for deep analysis
    - Vision for image/chart analysis
    - Web search as fallback
    - Structured outputs for clean data
    - Tool calling for orchestration
    """

    def __init__(self, ollama_api_key: str):
        self.ollama = OllamaCloudClient(ollama_api_key)

        # Model selection for different tasks - using Ollama Cloud models
        self.models = {
            'reasoning': 'deepseek-v3.1:671b-cloud',  # Best for analysis (thinking mode)
            'creative': 'qwen3-coder:30b-cloud',      # Best for writing
            'vision': 'qwen3-vl:235b-cloud',          # Best for image analysis
            'embedding': 'nomic-embed-text'            # Best for embeddings
        }
    
    async def synthesize(self, intelligence_data: Dict) -> IntelligenceReport:
        """
        Main synthesis pipeline: Transform raw intelligence into report.
        
        Pipeline:
        1. Analyze emerging trends
        2. Detect cross-platform stories
        3. Identify key influencers
        4. Generate predictions
        5. Create narrative synthesis
        """
        
        print("✨ Phase 1: Analyzing emerging trends...")
        emerging_trends = await self._analyze_trends(intelligence_data)
        
        print("✨ Phase 2: Detecting cross-platform stories...")
        cross_platform = await self._detect_cross_platform(intelligence_data)
        
        print("✨ Phase 3: Identifying key influencers...")
        influencers = await self._identify_influencers(intelligence_data)
        
        print("✨ Phase 4: Generating predictions...")
        predictions = await self._generate_predictions(emerging_trends)
        
        print("✨ Phase 5: Creating narrative synthesis...")
        headline, summary = await self._create_narrative(
            trends=emerging_trends,
            cross_platform=cross_platform,
            influencers=influencers,
            predictions=predictions
        )
        
        # Compute confidence score
        confidence = self._compute_confidence(intelligence_data)
        
        return IntelligenceReport(
            headline=headline,
            summary=summary,
            confidence_score=confidence,
            emerging_trends=emerging_trends,
            cross_platform_stories=cross_platform,
            top_influencers=influencers,
            topic_clusters=intelligence_data.get('topic_clusters', {}),
            predictions=predictions,
            total_signals=intelligence_data.get('total_signals', 0),
            platforms_analyzed=self._get_platforms(intelligence_data),
            time_range="Last 24 hours",
            generated_at=datetime.now()
        )
    
    async def _analyze_trends(self, data: Dict) -> List[Dict]:
        """
        Analyze emerging trends using velocity, acceleration,
        and cross-platform correlation.
        """
        
        trends = data.get('emerging_trends', [])
        
        # Enrich each trend with AI analysis
        enriched_trends = []
        
        for trend in trends[:5]:  # Top 5 trends
            # Generate insight using reasoning model
            prompt = f"""Analyze this emerging AI/ML trend:

Topic: {trend['topic']}
Velocity: {trend['velocity']:.2f} signals/hour
Platforms: {trend['platforms']}
Sample signals:
{self._format_signals(trend['signals'][:3])}

Provide:
1. What's driving this trend?
2. Why is it significant?
3. What are the implications?

Be concise and insightful (3-4 sentences)."""
            
            async with self.ollama as client:
                insight = await client.generate(
                    model=self.models['reasoning'],
                    prompt=prompt,
                    max_tokens=300
                )
            
            enriched_trends.append({
                **trend,
                'insight': insight.strip(),
                'significance': self._compute_significance(trend)
            })
        
        return enriched_trends
    
    async def _detect_cross_platform(self, data: Dict) -> List[Dict]:
        """
        Detect stories that appeared on multiple platforms.
        This indicates high-impact news.
        """
        
        cross_platform = data.get('cross_platform_stories', [])
        
        # Enrich with synthesis
        enriched = []
        
        for story in cross_platform[:10]:  # Top 10
            # Generate synthesis
            prompt = f"""Synthesize this cross-platform AI/ML story:

Title: {story['title']}
Platforms: {', '.join(story['platforms'])}
Total Engagement: {story['total_engagement']}

What's the core story? Why did it spread across platforms?
(2-3 sentences)"""
            
            async with self.ollama as client:
                synthesis = await client.generate(
                    model=self.models['creative'],
                    prompt=prompt,
                    max_tokens=200
                )
            
            enriched.append({
                **story,
                'synthesis': synthesis.strip()
            })
        
        return enriched
    
    async def _identify_influencers(self, data: Dict) -> List[Dict]:
        """Identify and profile key influencers"""
        
        influencers = data.get('top_influencers', [])
        
        # Add context about why they're influential
        for influencer in influencers[:10]:
            # Determine influence type
            if influencer['signals'] > 10:
                influence_type = "Prolific Creator"
            elif influencer['total_engagement'] > 1000:
                influence_type = "High Engagement"
            else:
                influence_type = "Rising Voice"
            
            influencer['influence_type'] = influence_type
        
        return influencers
    
    async def _generate_predictions(self, trends: List[Dict]) -> List[Dict]:
        """
        Generate predictions about where trends are heading.
        
        This uses the reasoning model to extrapolate future developments.
        """
        
        predictions = []
        
        for trend in trends[:3]:  # Top 3 trends
            prompt = f"""Based on this AI/ML trend, predict what happens next:

Topic: {trend['topic']}
Current State: {trend['insight']}
Velocity: {trend['velocity']:.2f} signals/hour
Acceleration: {trend.get('acceleration', 0):.2f}

Predict:
1. What happens in the next 7 days?
2. What are the key milestones to watch for?
3. What's the potential impact?

Be specific and actionable (4-5 sentences)."""
            
            async with self.ollama as client:
                prediction = await client.generate(
                    model=self.models['reasoning'],
                    prompt=prediction,
                    max_tokens=400
                )
            
            predictions.append({
                'topic': trend['topic'],
                'prediction': prediction.strip(),
                'confidence': trend.get('score', 0) / 10.0,
                'timeframe': '7 days'
            })
        
        return predictions
    
    async def _create_narrative(
        self,
        trends: List[Dict],
        cross_platform: List[Dict],
        influencers: List[Dict],
        predictions: List[Dict]
    ) -> tuple[str, str]:
        """
        Create compelling headline and summary that ties everything together.
        
        This is the final synthesis - turning data into story.
        """
        
        # Build context for narrative generation
        context = f"""Create a compelling blog post headline and summary for today's AI/ML intelligence report.

EMERGING TRENDS:
{self._format_trends(trends)}

CROSS-PLATFORM STORIES:
{self._format_cross_platform(cross_platform)}

KEY PREDICTIONS:
{self._format_predictions(predictions)}

Generate:
1. A compelling headline (10-15 words, exciting but accurate)
2. An executive summary (3-4 sentences that capture the essence)

Format:
HEADLINE: [your headline]
SUMMARY: [your summary]"""
        
        async with self.ollama as client:
            response = await client.generate(
                model=self.models['creative'],
                prompt=context,
                max_tokens=300,
                temperature=0.8  # More creative
            )
        
        # Parse response
        lines = response.strip().split('\n')
        headline = ""
        summary = ""
        
        for line in lines:
            if line.startswith('HEADLINE:'):
                headline = line.replace('HEADLINE:', '').strip()
            elif line.startswith('SUMMARY:'):
                summary = line.replace('SUMMARY:', '').strip()
        
        # Fallback if parsing fails
        if not headline:
            headline = "AI/ML Intelligence Report: " + trends[0]['topic'] if trends else "Daily AI/ML Update"
        if not summary:
            summary = "Today's intelligence report covering emerging trends, cross-platform stories, and predictions."
        
        return headline, summary
    
    def _compute_confidence(self, data: Dict) -> float:
        """
        Compute confidence score based on:
        - Number of signals
        - Platform diversity
        - Source quality
        """
        
        total_signals = data.get('total_signals', 0)
        platforms = len(self._get_platforms(data))
        
        # Normalize to 0-1
        signal_score = min(total_signals / 100, 1.0)
        platform_score = min(platforms / 5, 1.0)
        
        confidence = (signal_score * 0.6 + platform_score * 0.4)
        
        return confidence
    
    def _get_platforms(self, data: Dict) -> List[str]:
        """Extract unique platforms from data"""
        
        platforms = set()
        
        for signal in data.get('signals', []):
            platforms.add(signal.get('source', 'unknown'))
        
        return list(platforms)
    
    def _compute_significance(self, trend: Dict) -> str:
        """Compute significance level"""
        
        score = trend.get('score', 0)
        
        if score > 20:
            return "Critical"
        elif score > 10:
            return "High"
        elif score > 5:
            return "Medium"
        else:
            return "Low"
    
    def _format_signals(self, signals: List) -> str:
        """Format signals for prompt"""
        return "\n".join(f"- {s.title}" for s in signals)
    
    def _format_trends(self, trends: List[Dict]) -> str:
        """Format trends for prompt"""
        return "\n".join(
            f"- {t['topic']}: {t['insight'][:100]}..."
            for t in trends[:3]
        )
    
    def _format_cross_platform(self, stories: List[Dict]) -> str:
        """Format cross-platform stories for prompt"""
        return "\n".join(
            f"- {s['title'][:80]}... ({len(s['platforms'])} platforms)"
            for s in stories[:3]
        )
    
    def _format_predictions(self, predictions: List[Dict]) -> str:
        """Format predictions for prompt"""
        return "\n".join(
            f"- {p['topic']}: {p['prediction'][:100]}..."
            for p in predictions[:2]
        )

