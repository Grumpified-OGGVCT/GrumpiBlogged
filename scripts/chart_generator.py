#!/usr/bin/env python3
"""
Chart Generator for GrumpiBlogged

Creates interactive Plotly charts for blog posts:
- Tag trends over time
- Model count visualization
- Pattern growth charts
- Research theme distribution

Charts are embedded as HTML in markdown posts.
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import json
from typing import Dict, List, Tuple


def create_tag_trend_chart(tag_history: Dict[str, List[Tuple[str, int]]], days: int = 7) -> str:
    """
    Create a line chart showing tag trends over time
    
    Args:
        tag_history: Dict mapping tag names to list of (date, count) tuples
        days: Number of days to show
        
    Returns:
        HTML string for embedding in markdown
    """
    fig = go.Figure()
    
    # Add a line for each tag
    for tag, history in tag_history.items():
        if not history:
            continue
            
        dates = [h[0] for h in history[-days:]]
        counts = [h[1] for h in history[-days:]]
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
            name=tag,
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Tag Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Mentions",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='tag-trends')


def create_model_count_chart(model_counts: Dict[str, int]) -> str:
    """
    Create a bar chart showing model mentions
    
    Args:
        model_counts: Dict mapping model names to mention counts
        
    Returns:
        HTML string for embedding in markdown
    """
    # Sort by count descending
    sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    models = [m[0] for m in sorted_models]
    counts = [m[1] for m in sorted_models]
    
    fig = go.Figure(data=[
        go.Bar(
            x=models,
            y=counts,
            marker_color='rgb(55, 83, 109)',
            text=counts,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Top Models This Week",
        xaxis_title="Model",
        yaxis_title="Mentions",
        template='plotly_white',
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='model-counts')


def create_pattern_growth_chart(pattern_history: Dict[str, List[Tuple[str, int]]]) -> str:
    """
    Create an area chart showing pattern growth over time
    
    Args:
        pattern_history: Dict mapping pattern names to list of (date, count) tuples
        
    Returns:
        HTML string for embedding in markdown
    """
    fig = go.Figure()
    
    # Add an area for each pattern
    for pattern, history in pattern_history.items():
        if not history:
            continue
            
        dates = [h[0] for h in history]
        counts = [h[1] for h in history]
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=counts,
            mode='lines',
            name=pattern,
            stackgroup='one',
            fillcolor='rgba(0,0,0,0.1)'
        ))
    
    fig.update_layout(
        title="Pattern Growth Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Mentions",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        showlegend=True
    ))
    
    return fig.to_html(include_plotlyjs='cdn', div_id='pattern-growth')


def create_research_theme_chart(themes: Dict[str, int]) -> str:
    """
    Create a pie chart showing research theme distribution
    
    Args:
        themes: Dict mapping theme names to counts
        
    Returns:
        HTML string for embedding in markdown
    """
    labels = list(themes.keys())
    values = list(themes.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=px.colors.qualitative.Set3
    )])
    
    fig.update_layout(
        title="Research Themes Distribution",
        template='plotly_white',
        height=400
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='research-themes')


def extract_tag_history_from_posts(posts_dir: Path, days: int = 7) -> Dict[str, List[Tuple[str, int]]]:
    """
    Extract tag history from recent blog posts
    
    Args:
        posts_dir: Path to _posts directory
        days: Number of days to look back
        
    Returns:
        Dict mapping tag names to list of (date, count) tuples
    """
    tag_history = defaultdict(list)
    today = datetime.now()
    
    for i in range(days):
        past_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        
        # Check both post types
        for post_pattern in [f"{past_date}-ollama-*.md", f"{past_date}-ai-research-*.md"]:
            for post_file in posts_dir.glob(post_pattern):
                try:
                    content = post_file.read_text(encoding='utf-8')
                    
                    # Extract tags from front matter
                    if '---' in content:
                        front_matter = content.split('---')[1]
                        if 'tags:' in front_matter:
                            tags_line = [line for line in front_matter.split('\n') if 'tags:' in line][0]
                            tags = tags_line.split('[')[1].split(']')[0].split(',')
                            tags = [t.strip().strip('"').strip("'") for t in tags]
                            
                            # Count tags
                            tag_counts = Counter(tags)
                            for tag, count in tag_counts.items():
                                tag_history[tag].append((past_date, count))
                except Exception as e:
                    print(f"⚠️  Error processing {post_file}: {e}")
                    continue
    
    return dict(tag_history)


def extract_model_counts_from_posts(posts_dir: Path, days: int = 7) -> Dict[str, int]:
    """
    Extract model mention counts from recent blog posts
    
    Args:
        posts_dir: Path to _posts directory
        days: Number of days to look back
        
    Returns:
        Dict mapping model names to total mention counts
    """
    model_counts = Counter()
    today = datetime.now()
    
    # Common model patterns
    model_keywords = [
        'llama', 'mistral', 'qwen', 'deepseek', 'gemma', 'phi',
        'codellama', 'mixtral', 'vicuna', 'orca', 'falcon',
        'gpt', 'claude', 'palm', 'bard'
    ]
    
    for i in range(days):
        past_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        
        for post_pattern in [f"{past_date}-ollama-*.md"]:
            for post_file in posts_dir.glob(post_pattern):
                try:
                    content = post_file.read_text(encoding='utf-8').lower()
                    
                    for model in model_keywords:
                        count = content.count(model)
                        if count > 0:
                            model_counts[model.title()] += count
                except Exception as e:
                    print(f"⚠️  Error processing {post_file}: {e}")
                    continue
    
    return dict(model_counts)


def main():
    """Test chart generation"""
    import sys
    
    posts_dir = Path("docs/_posts")
    
    if not posts_dir.exists():
        print(f"❌ Posts directory not found: {posts_dir}")
        sys.exit(1)
    
    print("📊 Generating test charts...")
    
    # Test tag trends
    tag_history = extract_tag_history_from_posts(posts_dir)
    if tag_history:
        html = create_tag_trend_chart(tag_history)
        Path("test_tag_trends.html").write_text(html)
        print(f"✅ Tag trends chart: test_tag_trends.html")
    
    # Test model counts
    model_counts = extract_model_counts_from_posts(posts_dir)
    if model_counts:
        html = create_model_count_chart(model_counts)
        Path("test_model_counts.html").write_text(html)
        print(f"✅ Model counts chart: test_model_counts.html")
    
    print("\n🎉 Chart generation complete!")


if __name__ == "__main__":
    main()

