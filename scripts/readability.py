"""
Readability Scoring Module for GrumpiBlogged

Calculates readability metrics for blog posts:
- Flesch-Kincaid Grade Level
- Gunning Fog Index
- Coleman-Liau Index
- Automated Readability Index (ARI)

Target: 10th-12th grade reading level for optimal engagement
"""

import re
import math


def count_syllables(word):
    """
    Count syllables in a word using simple heuristics
    
    Args:
        word: String word to analyze
    
    Returns:
        int: Number of syllables
    """
    word = word.lower().strip()
    
    # Handle empty or very short words
    if len(word) <= 2:
        return 1
    
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    # Adjust for 'le' ending
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    
    # Ensure at least one syllable
    if syllable_count == 0:
        syllable_count = 1
    
    return syllable_count


def clean_text_for_analysis(text):
    """
    Clean markdown and special characters from text for analysis
    
    Args:
        text: Raw markdown text
    
    Returns:
        str: Cleaned text
    """
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove markdown headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove markdown formatting
    text = re.sub(r'[*_~`]', '', text)
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove emojis and special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?;:\-\']', ' ', text)
    
    return text


def flesch_kincaid_grade(text):
    """
    Calculate Flesch-Kincaid Grade Level
    
    Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
    
    Args:
        text: Text to analyze
    
    Returns:
        float: Grade level (e.g., 10.5 = 10th-11th grade)
    """
    clean = clean_text_for_analysis(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', clean)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    # Extract words
    words = re.findall(r'\b\w+\b', clean)
    words = [w for w in words if len(w) > 0]
    
    if not sentences or not words:
        return 0.0
    
    # Count syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Calculate averages
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)
    
    # Flesch-Kincaid formula
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    
    return round(grade, 1)


def gunning_fog_index(text):
    """
    Calculate Gunning Fog Index
    
    Formula: 0.4 * ((words/sentences) + 100 * (complex_words/words))
    Complex words = 3+ syllables
    
    Args:
        text: Text to analyze
    
    Returns:
        float: Fog index (years of education needed)
    """
    clean = clean_text_for_analysis(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', clean)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    # Extract words
    words = re.findall(r'\b\w+\b', clean)
    words = [w for w in words if len(w) > 0]
    
    if not sentences or not words:
        return 0.0
    
    # Count complex words (3+ syllables, excluding proper nouns and compound words)
    complex_words = 0
    for word in words:
        syllables = count_syllables(word)
        # Exclude proper nouns (capitalized) and common suffixes
        if syllables >= 3 and not word[0].isupper():
            # Exclude common suffixes that add syllables
            if not (word.endswith('es') or word.endswith('ed') or word.endswith('ing')):
                complex_words += 1
    
    # Calculate metrics
    avg_sentence_length = len(words) / len(sentences)
    percent_complex = (complex_words / len(words)) * 100
    
    # Gunning Fog formula
    fog = 0.4 * (avg_sentence_length + percent_complex)
    
    return round(fog, 1)


def coleman_liau_index(text):
    """
    Calculate Coleman-Liau Index
    
    Formula: 0.0588 * L - 0.296 * S - 15.8
    L = average letters per 100 words
    S = average sentences per 100 words
    
    Args:
        text: Text to analyze
    
    Returns:
        float: Grade level
    """
    clean = clean_text_for_analysis(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', clean)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    # Extract words
    words = re.findall(r'\b\w+\b', clean)
    words = [w for w in words if len(w) > 0]
    
    if not sentences or not words:
        return 0.0
    
    # Count letters
    total_letters = sum(len(word) for word in words)
    
    # Calculate per 100 words
    L = (total_letters / len(words)) * 100
    S = (len(sentences) / len(words)) * 100
    
    # Coleman-Liau formula
    cli = 0.0588 * L - 0.296 * S - 15.8
    
    return round(cli, 1)


def automated_readability_index(text):
    """
    Calculate Automated Readability Index (ARI)
    
    Formula: 4.71 * (characters/words) + 0.5 * (words/sentences) - 21.43
    
    Args:
        text: Text to analyze
    
    Returns:
        float: Grade level
    """
    clean = clean_text_for_analysis(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', clean)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    # Extract words
    words = re.findall(r'\b\w+\b', clean)
    words = [w for w in words if len(w) > 0]
    
    if not sentences or not words:
        return 0.0
    
    # Count characters
    total_chars = sum(len(word) for word in words)
    
    # Calculate metrics
    chars_per_word = total_chars / len(words)
    words_per_sentence = len(words) / len(sentences)
    
    # ARI formula
    ari = 4.71 * chars_per_word + 0.5 * words_per_sentence - 21.43
    
    return round(ari, 1)


def calculate_readability(text):
    """
    Calculate all readability scores and provide assessment
    
    Args:
        text: Text to analyze
    
    Returns:
        dict: Readability metrics and assessment
    """
    fk_grade = flesch_kincaid_grade(text)
    fog_index = gunning_fog_index(text)
    cli = coleman_liau_index(text)
    ari = automated_readability_index(text)
    
    # Average grade level
    avg_grade = (fk_grade + fog_index + cli + ari) / 4
    
    # Determine readability level
    if avg_grade <= 8:
        level = "Easy"
        description = "8th grade or below - Very accessible"
    elif avg_grade <= 10:
        level = "Moderate"
        description = "9th-10th grade - Accessible to most readers"
    elif avg_grade <= 12:
        level = "Standard"
        description = "11th-12th grade - High school level"
    elif avg_grade <= 16:
        level = "Difficult"
        description = "College level - Requires focused reading"
    else:
        level = "Very Difficult"
        description = "Graduate+ level - Academic/technical audience"
    
    # Check if target met (10-12 grade level)
    target_met = 10 <= avg_grade <= 12
    
    return {
        'flesch_kincaid_grade': fk_grade,
        'gunning_fog_index': fog_index,
        'coleman_liau_index': cli,
        'automated_readability_index': ari,
        'average_grade_level': round(avg_grade, 1),
        'readability_level': level,
        'description': description,
        'target_met': target_met,
        'recommendation': 'Perfect!' if target_met else (
            'Consider simplifying - too complex' if avg_grade > 12 else
            'Consider adding more depth - too simple'
        )
    }


if __name__ == '__main__':
    # Test with sample text
    sample = """
    # Test Blog Post
    
    Today we're exploring the fascinating world of artificial intelligence and machine learning.
    These technologies are transforming how we interact with computers and process information.
    
    Machine learning algorithms can identify patterns in data that humans might miss.
    This capability has applications in healthcare, finance, and many other fields.
    
    ## Deep Dive
    
    The transformer architecture revolutionized natural language processing in 2017.
    It uses self-attention mechanisms to process sequential data more effectively than previous approaches.
    """
    
    results = calculate_readability(sample)
    
    print("📊 Readability Analysis:")
    print(f"  Flesch-Kincaid Grade: {results['flesch_kincaid_grade']}")
    print(f"  Gunning Fog Index: {results['gunning_fog_index']}")
    print(f"  Coleman-Liau Index: {results['coleman_liau_index']}")
    print(f"  Automated Readability Index: {results['automated_readability_index']}")
    print(f"\n  Average Grade Level: {results['average_grade_level']}")
    print(f"  Readability: {results['readability_level']}")
    print(f"  Description: {results['description']}")
    print(f"  Target Met: {'✅ Yes' if results['target_met'] else '❌ No'}")
    print(f"  Recommendation: {results['recommendation']}")

