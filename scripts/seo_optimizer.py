"""
SEO Optimization Module for GrumpiBlogged

Provides SEO enhancements for blog posts:
- Meta description generation (150-160 characters)
- Keyword extraction and optimization
- Title optimization
- Structured data (JSON-LD) generation
- Open Graph tags
"""

import re
from collections import Counter
from datetime import datetime


# Common stop words to exclude from keyword extraction
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
    'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just'
}


def clean_text_for_seo(text):
    """
    Clean markdown and special characters from text for SEO analysis
    
    Args:
        text: Raw markdown text
    
    Returns:
        str: Cleaned text
    """
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove markdown headers but keep the text
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove markdown formatting
    text = re.sub(r'[*_~]', '', text)
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    return text


def extract_keywords(content, count=12, min_length=4):
    """
    Extract top keywords from content using frequency analysis
    
    Args:
        content: Text content to analyze
        count: Number of keywords to return (default: 12)
        min_length: Minimum word length to consider (default: 4)
    
    Returns:
        list: Top keywords sorted by frequency
    """
    clean = clean_text_for_seo(content)
    
    # Extract words
    words = re.findall(r'\b\w+\b', clean.lower())
    
    # Filter stop words, short words, and numbers
    keywords = [
        w for w in words 
        if w not in STOP_WORDS 
        and len(w) >= min_length
        and not w.isdigit()
    ]
    
    # Count frequency
    word_freq = Counter(keywords)
    
    # Return top N keywords
    return [word for word, _ in word_freq.most_common(count)]


def generate_meta_description(content, title="", max_length=160):
    """
    Generate SEO-optimized meta description
    
    Aims for 150-160 characters for optimal display in search results
    
    Args:
        content: Post content
        title: Post title (optional, for context)
        max_length: Maximum description length (default: 160)
    
    Returns:
        str: Meta description
    """
    clean = clean_text_for_seo(content)
    
    # Split into paragraphs
    paragraphs = clean.split('\n\n')
    
    # Find first meaningful paragraph (skip headers, short text)
    for para in paragraphs:
        para = para.strip()
        
        # Skip if too short or looks like a header
        if len(para) < 50 or para.isupper():
            continue
        
        # Clean up extra whitespace
        para = ' '.join(para.split())
        
        # If paragraph fits, use it
        if len(para) <= max_length:
            return para
        
        # Otherwise, truncate at word boundary
        truncated = para[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # Only truncate if we're close to the end
            truncated = truncated[:last_space]
        
        return truncated.rstrip('.,;:') + '...'
    
    # Fallback: use title or generic description
    if title:
        return f"{title} - AI-powered insights from GrumpiBlogged"
    
    return "Explore AI-powered coding adventures and research insights from GrumpiBlogged"


def optimize_title(title, keywords, max_length=60):
    """
    Optimize title for SEO
    
    Ensures title includes relevant keywords and is under 60 characters
    
    Args:
        title: Original title
        keywords: List of keywords
        max_length: Maximum title length (default: 60)
    
    Returns:
        str: Optimized title
    """
    # Check if title is already good
    if len(title) <= max_length:
        title_lower = title.lower()
        keywords_in_title = [k for k in keywords[:3] if k in title_lower]
        
        if keywords_in_title:
            return title  # Already optimized
    
    # If title is too long, truncate
    if len(title) > max_length:
        truncated = title[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:
            title = truncated[:last_space]
        else:
            title = truncated
    
    # If no keywords in title, suggest adding top keyword
    title_lower = title.lower()
    if keywords and not any(k in title_lower for k in keywords[:3]):
        top_keyword = keywords[0].title()
        
        # Try to add keyword without exceeding length
        suggested = f"{title} - {top_keyword}"
        if len(suggested) <= max_length:
            return suggested
    
    return title


def generate_structured_data(post_data):
    """
    Generate JSON-LD structured data for rich snippets
    
    Args:
        post_data: Dictionary with post information
            - title: Post title
            - description: Meta description
            - author: Author name
            - date: Publication date (YYYY-MM-DD)
            - url: Post URL
            - image: Featured image URL (optional)
            - keywords: List of keywords
    
    Returns:
        dict: JSON-LD structured data
    """
    structured_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post_data.get('title', ''),
        "description": post_data.get('description', ''),
        "author": {
            "@type": "Person",
            "name": post_data.get('author', 'GrumpiBot')
        },
        "datePublished": post_data.get('date', datetime.now().strftime('%Y-%m-%d')),
        "publisher": {
            "@type": "Organization",
            "name": "GrumpiBlogged",
            "logo": {
                "@type": "ImageObject",
                "url": "https://grumpified-oggvct.github.io/GrumpiBlogged/assets/logo.png"
            }
        }
    }
    
    # Add URL if provided
    if 'url' in post_data:
        structured_data['url'] = post_data['url']
        structured_data['mainEntityOfPage'] = {
            "@type": "WebPage",
            "@id": post_data['url']
        }
    
    # Add image if provided
    if 'image' in post_data:
        structured_data['image'] = post_data['image']
    
    # Add keywords if provided
    if 'keywords' in post_data and post_data['keywords']:
        structured_data['keywords'] = ', '.join(post_data['keywords'])
    
    return structured_data


def generate_open_graph_tags(post_data):
    """
    Generate Open Graph meta tags for social media sharing
    
    Args:
        post_data: Dictionary with post information
            - title: Post title
            - description: Meta description
            - url: Post URL
            - image: Featured image URL (optional)
            - type: Content type (default: 'article')
    
    Returns:
        dict: Open Graph tags
    """
    og_tags = {
        'og:title': post_data.get('title', ''),
        'og:description': post_data.get('description', ''),
        'og:type': post_data.get('type', 'article'),
        'og:site_name': 'GrumpiBlogged'
    }
    
    # Add URL if provided
    if 'url' in post_data:
        og_tags['og:url'] = post_data['url']
    
    # Add image if provided
    if 'image' in post_data:
        og_tags['og:image'] = post_data['image']
    
    # Twitter Card tags
    og_tags['twitter:card'] = 'summary_large_image'
    og_tags['twitter:title'] = post_data.get('title', '')
    og_tags['twitter:description'] = post_data.get('description', '')
    
    if 'image' in post_data:
        og_tags['twitter:image'] = post_data['image']
    
    return og_tags


def optimize_post_seo(title, content, author="GrumpiBot", url="", image=""):
    """
    Complete SEO optimization for a blog post
    
    Args:
        title: Post title
        content: Post content
        author: Author name (default: "GrumpiBot")
        url: Post URL (optional)
        image: Featured image URL (optional)
    
    Returns:
        dict: Complete SEO package
    """
    # Extract keywords
    keywords = extract_keywords(content, count=12)
    
    # Generate meta description
    meta_description = generate_meta_description(content, title)
    
    # Optimize title
    optimized_title = optimize_title(title, keywords)
    
    # Prepare post data
    post_data = {
        'title': optimized_title,
        'description': meta_description,
        'author': author,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'keywords': keywords
    }
    
    if url:
        post_data['url'] = url
    if image:
        post_data['image'] = image
    
    # Generate structured data
    structured_data = generate_structured_data(post_data)
    
    # Generate Open Graph tags
    og_tags = generate_open_graph_tags(post_data)
    
    return {
        'optimized_title': optimized_title,
        'meta_description': meta_description,
        'keywords': keywords,
        'structured_data': structured_data,
        'open_graph_tags': og_tags,
        'seo_score': calculate_seo_score(optimized_title, meta_description, keywords)
    }


def calculate_seo_score(title, description, keywords):
    """
    Calculate SEO quality score (0-100)
    
    Args:
        title: Post title
        description: Meta description
        keywords: List of keywords
    
    Returns:
        int: SEO score (0-100)
    """
    score = 0
    
    # Title checks (30 points)
    if 30 <= len(title) <= 60:
        score += 15
    if any(k in title.lower() for k in keywords[:3]):
        score += 15
    
    # Description checks (30 points)
    if 150 <= len(description) <= 160:
        score += 15
    if any(k in description.lower() for k in keywords[:5]):
        score += 15
    
    # Keywords checks (40 points)
    if len(keywords) >= 8:
        score += 20
    if len(keywords) >= 12:
        score += 10
    
    # Bonus for keyword diversity
    unique_keywords = len(set(keywords))
    if unique_keywords >= 10:
        score += 10
    
    return min(score, 100)


if __name__ == '__main__':
    # Test with sample content
    sample_title = "New AI Models Released - Qwen3 and DeepSeek V3"
    sample_content = """
    # New AI Models Released
    
    Today we're exploring two groundbreaking AI models that just dropped: Qwen3-VL and DeepSeek V3.
    These models represent significant advances in vision-language understanding and reasoning capabilities.
    
    ## Qwen3-VL: Vision-Language Excellence
    
    Qwen3-VL brings state-of-the-art performance to multimodal tasks, combining visual understanding
    with natural language processing in unprecedented ways.
    
    ## DeepSeek V3: Reasoning Powerhouse
    
    DeepSeek V3 focuses on advanced reasoning and problem-solving, with impressive benchmarks
    across mathematical and logical reasoning tasks.
    """
    
    results = optimize_post_seo(sample_title, sample_content)
    
    print("🔍 SEO Optimization Results:")
    print(f"\n  Original Title: {sample_title}")
    print(f"  Optimized Title: {results['optimized_title']}")
    print(f"\n  Meta Description ({len(results['meta_description'])} chars):")
    print(f"  {results['meta_description']}")
    print(f"\n  Keywords: {', '.join(results['keywords'][:8])}")
    print(f"\n  SEO Score: {results['seo_score']}/100")

