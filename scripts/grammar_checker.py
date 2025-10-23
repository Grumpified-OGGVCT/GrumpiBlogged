"""
Grammar and Style Checking Module for GrumpiBlogged

Uses Ollama Proxy with cloud models to review blog posts for:
- Grammar errors
- Style consistency with persona
- Repetitive phrases
- Tone assessment
- Clarity improvements
"""

import requests
import json
import os
from typing import Dict, List, Optional


def check_grammar_and_style(text: str, persona_name: str = "General", model: str = "qwen3-coder:30b-cloud") -> Dict:
    """
    Use Ollama Proxy to check grammar and style
    
    Args:
        text: Blog post content to review
        persona_name: Persona name for style matching (e.g., "Hype Caster", "The Scholar")
        model: Ollama model to use (default: qwen3-coder:30b-cloud for text analysis)
    
    Returns:
        dict: Grammar and style analysis
            - grammar_errors: List of grammar issues
            - style_suggestions: List of style improvements
            - repetitive_phrases: List of phrases to vary
            - tone_assessment: Overall tone evaluation
            - clarity_score: 0-100 score
    """
    
    # Get API key from environment
    api_key = os.getenv('OLLAMA_PROXY_GRAMMAR_API_KEY') or os.getenv('OLLAMA_PROXY_API_KEY')
    
    if not api_key:
        print("⚠️  No Ollama Proxy API key found - skipping grammar check")
        print("   Set OLLAMA_PROXY_GRAMMAR_API_KEY or OLLAMA_PROXY_API_KEY environment variable")
        return {
            'grammar_errors': [],
            'style_suggestions': [],
            'repetitive_phrases': [],
            'tone_assessment': 'Unable to assess - no API key',
            'clarity_score': 0,
            'skipped': True
        }
    
    # Prepare prompt
    prompt = f"""You are an expert editor reviewing a blog post for grammar, style, and clarity.

**Persona**: {persona_name}
**Task**: Review this blog post and provide detailed feedback.

**Blog Post Content**:
{text[:4000]}  

**Instructions**:
1. Identify any grammar errors (spelling, punctuation, syntax)
2. Suggest style improvements to match the {persona_name} persona
3. Find repetitive phrases that should be varied
4. Assess the overall tone and clarity
5. Rate clarity on a scale of 0-100

**Output Format** (JSON only, no other text):
{{
  "grammar_errors": [
    {{"issue": "description", "location": "approximate location", "suggestion": "how to fix"}}
  ],
  "style_suggestions": [
    {{"issue": "description", "suggestion": "improvement"}}
  ],
  "repetitive_phrases": [
    {{"phrase": "repeated phrase", "count": number, "suggestion": "alternatives"}}
  ],
  "tone_assessment": "brief assessment of tone and persona match",
  "clarity_score": 85
}}

Respond with ONLY the JSON object, no additional text."""

    try:
        # Call Ollama Proxy
        response = requests.post(
            'http://localhost:8081/api/chat',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'stream': False,
                'temperature': 0.3  # Lower temperature for more consistent analysis
            },
            timeout=120  # 2 minutes for analysis
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('message', {}).get('content', '{}')
            
            # Extract JSON from response (handle markdown code blocks)
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            try:
                analysis = json.loads(content)
                analysis['skipped'] = False
                return analysis
            except json.JSONDecodeError as e:
                print(f"⚠️  Failed to parse grammar check response: {e}")
                print(f"   Response: {content[:200]}...")
                return {
                    'grammar_errors': [],
                    'style_suggestions': [],
                    'repetitive_phrases': [],
                    'tone_assessment': 'Parse error - unable to analyze',
                    'clarity_score': 0,
                    'skipped': True,
                    'error': str(e)
                }
        
        else:
            print(f"⚠️  Grammar check API error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return {
                'grammar_errors': [],
                'style_suggestions': [],
                'repetitive_phrases': [],
                'tone_assessment': f'API error {response.status_code}',
                'clarity_score': 0,
                'skipped': True,
                'error': f'HTTP {response.status_code}'
            }
    
    except requests.exceptions.Timeout:
        print("⚠️  Grammar check timed out (120s)")
        return {
            'grammar_errors': [],
            'style_suggestions': [],
            'repetitive_phrases': [],
            'tone_assessment': 'Timeout - unable to complete analysis',
            'clarity_score': 0,
            'skipped': True,
            'error': 'Timeout'
        }
    
    except Exception as e:
        print(f"⚠️  Grammar check error: {e}")
        return {
            'grammar_errors': [],
            'style_suggestions': [],
            'repetitive_phrases': [],
            'tone_assessment': f'Error: {str(e)}',
            'clarity_score': 0,
            'skipped': True,
            'error': str(e)
        }


def apply_grammar_corrections(text: str, corrections: List[Dict]) -> str:
    """
    Apply grammar corrections to text (optional - for auto-fix)
    
    Args:
        text: Original text
        corrections: List of corrections from check_grammar_and_style
    
    Returns:
        str: Corrected text
    
    Note: This is a simple implementation. For production, consider more sophisticated
    text replacement strategies to avoid breaking markdown formatting.
    """
    corrected = text
    
    for correction in corrections:
        if 'location' in correction and 'suggestion' in correction:
            # Simple replacement (can be improved)
            location = correction['location']
            suggestion = correction['suggestion']
            
            # Try to find and replace the issue
            # This is a basic implementation - production would need more sophisticated matching
            if location in corrected:
                corrected = corrected.replace(location, suggestion, 1)
    
    return corrected


def format_grammar_report(analysis: Dict) -> str:
    """
    Format grammar analysis into a readable report
    
    Args:
        analysis: Analysis results from check_grammar_and_style
    
    Returns:
        str: Formatted report
    """
    if analysis.get('skipped'):
        return "⚠️  Grammar check skipped (no API key or error)\n"
    
    report = []
    report.append("📝 Grammar & Style Analysis")
    report.append("=" * 50)
    
    # Grammar errors
    if analysis.get('grammar_errors'):
        report.append(f"\n❌ Grammar Errors ({len(analysis['grammar_errors'])}):")
        for i, error in enumerate(analysis['grammar_errors'], 1):
            report.append(f"  {i}. {error.get('issue', 'Unknown issue')}")
            if 'location' in error:
                report.append(f"     Location: {error['location']}")
            if 'suggestion' in error:
                report.append(f"     Fix: {error['suggestion']}")
    else:
        report.append("\n✅ No grammar errors found")
    
    # Style suggestions
    if analysis.get('style_suggestions'):
        report.append(f"\n💡 Style Suggestions ({len(analysis['style_suggestions'])}):")
        for i, suggestion in enumerate(analysis['style_suggestions'], 1):
            report.append(f"  {i}. {suggestion.get('issue', 'Unknown issue')}")
            if 'suggestion' in suggestion:
                report.append(f"     Suggestion: {suggestion['suggestion']}")
    else:
        report.append("\n✅ Style looks good")
    
    # Repetitive phrases
    if analysis.get('repetitive_phrases'):
        report.append(f"\n🔁 Repetitive Phrases ({len(analysis['repetitive_phrases'])}):")
        for i, phrase in enumerate(analysis['repetitive_phrases'], 1):
            report.append(f"  {i}. \"{phrase.get('phrase', 'Unknown')}\" (used {phrase.get('count', 0)}x)")
            if 'suggestion' in phrase:
                report.append(f"     Alternatives: {phrase['suggestion']}")
    else:
        report.append("\n✅ No repetitive phrases detected")
    
    # Tone assessment
    report.append(f"\n🎭 Tone Assessment:")
    report.append(f"  {analysis.get('tone_assessment', 'No assessment available')}")
    
    # Clarity score
    clarity = analysis.get('clarity_score', 0)
    report.append(f"\n📊 Clarity Score: {clarity}/100")
    if clarity >= 80:
        report.append("  ✅ Excellent clarity")
    elif clarity >= 60:
        report.append("  ⚠️  Good, but could be clearer")
    else:
        report.append("  ❌ Needs improvement")
    
    return '\n'.join(report)


if __name__ == '__main__':
    # Test with sample text
    sample_text = """
    # New AI Models Released
    
    Today we're exploring two groundbreaking AI models. These models are really amazing.
    The models represent significant advances. The models are very impressive.
    
    ## Qwen3-VL
    
    Qwen3-VL brings state-of-the-art performance to multimodal tasks. It's performance
    is really good and the model is very powerful.
    """
    
    print("Testing grammar checker...")
    print("=" * 60)
    
    # Check if API key is available
    if not os.getenv('OLLAMA_PROXY_API_KEY'):
        print("⚠️  Set OLLAMA_PROXY_API_KEY environment variable to test")
        print("   Example: export OLLAMA_PROXY_API_KEY='your-key-here'")
    else:
        results = check_grammar_and_style(sample_text, persona_name="Tech Enthusiast")
        print(format_grammar_report(results))

