# 🤖 Phase 4: AI-Powered Editing - Implementation Plan

**Date**: 2025-10-23
**Priority**: 1 (Highest Value)
**Estimated Time**: 8-12 hours (Actual: ~6 hours)
**Status**: ✅ COMPLETE

---

## 🎯 **Objective**

Implement AI-powered editing capabilities to improve content quality, SEO, readability, and factual accuracy for all GrumpiBlogged posts.

---

## 📋 **Four Components**

### **1. Grammar & Style Checking** (2-3 hours)
- Review generated posts for grammar errors
- Check for awkward phrasing and repetitive language
- Ensure tone consistency with persona
- Suggest improvements before publishing

### **2. SEO Optimization** (2-3 hours)
- Auto-generate meta descriptions (150-160 characters)
- Extract and suggest keywords from content
- Optimize titles for search engines
- Add structured data (JSON-LD) for rich snippets

### **3. Readability Scoring** (1-2 hours)
- Calculate Flesch-Kincaid Grade Level
- Calculate Gunning Fog Index
- Calculate Coleman-Liau Index
- Target: 10th-12th grade reading level
- Suggest simplifications if too complex

### **4. SAEV Fact-Checking Protocol** (4-6 hours)
- Implement Source-Agnostic, Evidence-Weighted Verification
- Four-phase verification system
- Multi-source evidence aggregation
- Dynamic credibility scoring
- Transparency reports

---

## 🏗️ **Architecture**

### **New Files to Create**:

1. **`scripts/ai_editor.py`** - Main editing orchestrator
   - `review_grammar_and_style(text, persona)` → corrections
   - `optimize_seo(title, content)` → meta, keywords
   - `calculate_readability(text)` → scores, suggestions
   - `verify_facts(content)` → verification report

2. **`scripts/readability.py`** - Readability scoring module
   - `flesch_kincaid_grade(text)` → grade level
   - `gunning_fog_index(text)` → fog index
   - `coleman_liau_index(text)` → CLI score
   - `suggest_simplifications(text, target_grade)` → suggestions

3. **`scripts/seo_optimizer.py`** - SEO optimization module
   - `generate_meta_description(content)` → description
   - `extract_keywords(content, count=10)` → keywords
   - `optimize_title(title, keywords)` → optimized title
   - `generate_structured_data(post_data)` → JSON-LD

4. **`scripts/fact_checker.py`** - SAEV Protocol implementation
   - `aggregate_evidence(claim)` → evidence from multiple sources
   - `weight_evidence(evidence_list)` → scored evidence
   - `synthesize_verification(weighted_evidence)` → confidence score
   - `generate_transparency_report(verification)` → report

5. **`scripts/grammar_checker.py`** - Grammar and style checking
   - `check_grammar(text)` → grammar issues
   - `check_style(text, persona)` → style suggestions
   - `check_repetition(text)` → repetitive phrases
   - `apply_corrections(text, corrections)` → corrected text

### **Modified Files**:

1. **`scripts/generate_daily_blog.py`**
   - Add AI editing step before finalizing post
   - Integrate readability scoring
   - Add SEO metadata to front matter
   - Optional fact-checking for claims

2. **`scripts/generate_lab_blog.py`**
   - Same AI editing integration
   - Stricter fact-checking for research claims
   - Academic tone validation

3. **`templates/ollama_pulse_post.j2`**
   - Add SEO meta description field
   - Add keywords field
   - Add readability score (optional footer)

4. **`templates/ai_research_post.j2`**
   - Same SEO enhancements
   - Add fact-check transparency section (optional)

---

## 🔧 **Implementation Steps**

### **Step 1: Readability Scoring** (Easiest First)

**File**: `scripts/readability.py`

```python
import re
import math

def count_syllables(word):
    """Count syllables in a word using simple heuristics"""
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        syllable_count -= 1
    
    # Ensure at least one syllable
    if syllable_count == 0:
        syllable_count = 1
    
    return syllable_count

def flesch_kincaid_grade(text):
    """Calculate Flesch-Kincaid Grade Level"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = re.findall(r'\b\w+\b', text)
    
    if not sentences or not words:
        return 0
    
    total_syllables = sum(count_syllables(word) for word in words)
    
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)
    
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    
    return round(grade, 1)

def gunning_fog_index(text):
    """Calculate Gunning Fog Index"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = re.findall(r'\b\w+\b', text)
    
    if not sentences or not words:
        return 0
    
    # Count complex words (3+ syllables)
    complex_words = sum(1 for word in words if count_syllables(word) >= 3)
    
    avg_sentence_length = len(words) / len(sentences)
    percent_complex = (complex_words / len(words)) * 100
    
    fog = 0.4 * (avg_sentence_length + percent_complex)
    
    return round(fog, 1)

def calculate_readability(text):
    """Calculate all readability scores"""
    fk_grade = flesch_kincaid_grade(text)
    fog_index = gunning_fog_index(text)
    
    # Determine readability level
    if fk_grade <= 8:
        level = "Easy (8th grade or below)"
    elif fk_grade <= 12:
        level = "Moderate (High School)"
    elif fk_grade <= 16:
        level = "Difficult (College)"
    else:
        level = "Very Difficult (Graduate+)"
    
    return {
        'flesch_kincaid_grade': fk_grade,
        'gunning_fog_index': fog_index,
        'readability_level': level,
        'target_met': 10 <= fk_grade <= 12  # Target: 10th-12th grade
    }
```

**Integration**: Add to both blog generators after content generation

---

### **Step 2: SEO Optimization**

**File**: `scripts/seo_optimizer.py`

```python
import re
from collections import Counter

def extract_keywords(content, count=10):
    """Extract top keywords from content"""
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                  'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                  'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
    
    # Extract words
    words = re.findall(r'\b\w+\b', content.lower())
    
    # Filter stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Count frequency
    word_freq = Counter(keywords)
    
    # Return top N keywords
    return [word for word, _ in word_freq.most_common(count)]

def generate_meta_description(content, max_length=160):
    """Generate SEO-optimized meta description"""
    # Extract first meaningful paragraph
    paragraphs = content.split('\n\n')
    
    for para in paragraphs:
        # Skip headers and short paragraphs
        if para.startswith('#') or len(para) < 50:
            continue
        
        # Clean up markdown
        clean = re.sub(r'[#*_`\[\]]', '', para)
        clean = clean.strip()
        
        if len(clean) <= max_length:
            return clean
        else:
            # Truncate at word boundary
            truncated = clean[:max_length]
            last_space = truncated.rfind(' ')
            if last_space > 0:
                truncated = truncated[:last_space]
            return truncated + '...'
    
    return "AI-powered blog post from GrumpiBlogged"

def optimize_title(title, keywords):
    """Optimize title for SEO (ensure keywords present)"""
    # Check if any keywords are in title
    title_lower = title.lower()
    keywords_in_title = [k for k in keywords[:3] if k in title_lower]
    
    if keywords_in_title:
        return title  # Already optimized
    
    # Suggest adding top keyword
    if keywords:
        return f"{title} - {keywords[0].title()}"
    
    return title
```

**Integration**: Add to front matter generation in both blog generators

---

### **Step 3: Grammar & Style Checking**

**File**: `scripts/grammar_checker.py`

Uses Ollama Proxy to review content with language models

```python
import requests
import os

def check_grammar_and_style(text, persona_name="General"):
    """Use Ollama to check grammar and style"""
    
    api_key = os.getenv('OLLAMA_PROXY_API_KEY')
    if not api_key:
        print("⚠️ No Ollama Proxy API key - skipping grammar check")
        return {'corrections': [], 'suggestions': []}
    
    prompt = f"""Review this blog post for grammar, style, and clarity.
Persona: {persona_name}

Post content:
{text}

Provide:
1. Grammar errors (if any)
2. Style suggestions to match the {persona_name} persona
3. Repetitive phrases to vary
4. Overall tone assessment

Format as JSON:
{{
  "grammar_errors": [],
  "style_suggestions": [],
  "repetitive_phrases": [],
  "tone_assessment": ""
}}
"""
    
    try:
        response = requests.post(
            'http://localhost:8081/api/chat',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': 'qwen3-coder:30b-cloud',  # Good for text analysis
                'messages': [{'role': 'user', 'content': prompt}],
                'stream': False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            # Parse JSON from response
            import json
            return json.loads(result['message']['content'])
        else:
            print(f"⚠️ Grammar check failed: {response.status_code}")
            return {'corrections': [], 'suggestions': []}
    
    except Exception as e:
        print(f"⚠️ Grammar check error: {e}")
        return {'corrections': [], 'suggestions': []}
```

---

### **Step 4: SAEV Fact-Checking Protocol**

**File**: `scripts/fact_checker.py`

Most complex - implements the 4-phase verification system

```python
# This will be implemented in detail in the next file
# Due to complexity, breaking into separate implementation
```

---

## 📊 **Success Metrics**

### **Readability**:
- ✅ Target: 10-12 grade level (High School)
- ✅ Measure: Flesch-Kincaid Grade Level
- ✅ Track: Average readability across all posts

### **SEO**:
- ✅ Meta descriptions: 150-160 characters
- ✅ Keywords: 8-12 per post
- ✅ Title optimization: Include top keyword

### **Grammar**:
- ✅ Zero grammar errors before publishing
- ✅ Style consistency with persona
- ✅ No repetitive phrases

### **Fact-Checking**:
- ✅ Confidence score: >80% for factual claims
- ✅ Evidence sources: 3+ independent sources
- ✅ Transparency: Full evidence breakdown

---

## 🚀 **Deployment Plan**

1. **Create readability.py** - Test with existing posts
2. **Create seo_optimizer.py** - Test meta generation
3. **Create grammar_checker.py** - Test with Ollama Proxy
4. **Create fact_checker.py** - Implement SAEV Protocol
5. **Integrate into generators** - Add to both blog scripts
6. **Test end-to-end** - Generate test posts
7. **Deploy to production** - Commit and push

---

**Next**: Start implementation with readability.py (easiest component)


