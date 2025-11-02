#!/usr/bin/env python3
"""
Personality & Humor System for GrumpiBlogged

Provides persona-specific jokes, anecdotes, and cultural references
that are tracked and rotated to avoid repetition.

All content is G-rated and professional.
"""

import random
from typing import List, Set


# ============================================================================
# OLLAMA PULSE PERSONAS
# ============================================================================

HYPE_CASTER_JOKES = [
    "llm-latté",  # "This model is smoother than my morning LLM-latté"
    "gpu-golf",  # "Playing GPU golf with these parameters"
    "neural-network-ninja",  # "These devs are neural network ninjas"
    "tensor-time",  # "It's tensor time, folks!"
    "gradient-descent-into-greatness",  # "Taking a gradient descent into greatness"
    "attention-is-all-you-need",  # "Attention is all you need... and maybe some coffee"
    "transformer-magic",  # "Pure transformer magic right here"
    "embedding-excellence",  # "Embedding excellence in every layer"
]

HYPE_CASTER_ANECDOTES = [
    "My 4-year-old asked if AI dreams of electric sheep. I said no, but it dreams of better benchmarks.",
    "Remember when we thought 7B was big? Those were simpler times.",
    "Plot twist: The real treasure was the tokens we processed along the way.",
    "Spoiler alert: This model is about to change everything. Again.",
]

MECHANIC_JOKES = [
    "byte-brew",  # "Fixing bugs with a fresh byte-brew"
    "patch-perfect",  # "This patch is patch-perfect"
    "debug-dance",  # "Doing the debug dance"
    "fix-it-friday",  # "Every day is fix-it Friday in AI land"
    "bug-squashing-season",  # "It's bug-squashing season"
    "maintenance-mode-activated",  # "Maintenance mode: activated"
]

MECHANIC_ANECDOTES = [
    "You know what's better than a new model? A model that actually works.",
    "Small updates, big impact. That's the mechanic's way.",
    "Sometimes the best innovation is just making things work reliably.",
    "Mic drop moment: When a bug fix makes everything 10x faster.",
]

CURIOUS_ANALYST_JOKES = [
    "experimental-espresso",  # "Fueled by experimental espresso"
    "hypothesis-hype",  # "Riding the hypothesis hype train"
    "research-rabbit-hole",  # "Down the research rabbit hole we go"
    "curiosity-coefficient",  # "My curiosity coefficient is off the charts"
    "what-if-wednesday",  # "It's what-if Wednesday every day"
]

CURIOUS_ANALYST_ANECDOTES = [
    "What if we're all just training data for a future AI? *adjusts tinfoil hat*",
    "The best questions don't have answers yet. That's what makes them interesting.",
    "Sometimes weird is wonderful. This is one of those times.",
    "I have more questions than answers, and I'm okay with that.",
]

TREND_SPOTTER_JOKES = [
    "pattern-recognition-pro",  # "Pattern recognition pro mode: engaged"
    "data-driven-detective",  # "Playing data-driven detective"
    "trend-tracking-tuesday",  # "Every day is trend-tracking Tuesday"
    "signal-vs-noise",  # "Separating signal from noise"
    "meta-analysis-mode",  # "Meta-analysis mode: activated"
]

TREND_SPOTTER_ANECDOTES = [
    "The data doesn't lie, but it does whisper sometimes.",
    "Slow news days are when the real patterns emerge.",
    "Zoom out far enough and everything is a trend.",
    "The best insights hide in plain sight.",
]

INFORMED_ENTHUSIAST_JOKES = [
    "balanced-breakfast",  # "Starting with a balanced breakfast of AI news"
    "context-is-king",  # "Context is king, and I'm the royal advisor"
    "nuance-ninja",  # "Nuance ninja reporting for duty"
    "informed-optimism",  # "Practicing informed optimism"
    "perspective-power",  # "Perspective is a superpower"
]

INFORMED_ENTHUSIAST_ANECDOTES = [
    "The truth is usually somewhere in the middle, but the middle is fascinating.",
    "Every story has multiple angles. I'm here for all of them.",
    "Balance isn't boring. It's brilliant.",
    "The best takes are well-informed and slightly optimistic.",
]


# ============================================================================
# AI RESEARCH DAILY (THE SCHOLAR)
# ============================================================================

SCHOLAR_JOKES = [
    "peer-review-pending",  # "Peer review pending, but the results look promising"
    "methodology-matters",  # "Methodology matters more than hype"
    "citation-needed",  # "[citation needed] but intriguing nonetheless"
    "reproducibility-rocks",  # "Reproducibility rocks"
    "null-hypothesis-hero",  # "Null hypothesis hero"
    "statistical-significance-squad",  # "Statistical significance squad"
]

SCHOLAR_ANECDOTES = [
    "As my advisor used to say: 'Extraordinary claims require extraordinary evidence.'",
    "The best research raises more questions than it answers.",
    "Science is a marathon, not a sprint. But sometimes we get exciting sprints.",
    "Replication is the sincerest form of scientific flattery.",
]

SCHOLAR_CULTURAL_REFS = [
    "standing-on-shoulders-of-giants",  # "Standing on the shoulders of giants"
    "paradigm-shift",  # "Potential paradigm shift alert"
    "occams-razor",  # "Occam's Razor suggests..."
    "correlation-causation",  # "Correlation ≠ causation, but..."
]


# ============================================================================
# IDEA VAULT (THE VISIONARY)
# ============================================================================

VISIONARY_JOKES = [
    "imagine-if",  # "Imagine if we could..."
    "what-if-wednesday",  # "Every day is what-if Wednesday"
    "future-forward",  # "Future-forward thinking engaged"
    "possibility-space",  # "Exploring the possibility space"
    "idea-lab",  # "Welcome to the idea lab"
    "innovation-engine",  # "Innovation engine running"
]

VISIONARY_ANECDOTES = [
    "The best ideas start with 'what if' and end with 'why not?'",
    "Today's wild idea is tomorrow's standard practice.",
    "Innovation happens when we connect dots that haven't been connected before.",
    "The future isn't something we predict—it's something we create.",
]

VISIONARY_CULTURAL_REFS = [
    "stand-on-shoulders",  # "Standing on the shoulders of those who dared to dream"
    "bridge-gap",  # "Bridging the gap between vision and reality"
    "compound-innovation",  # "The compound interest of innovation"
    "ideas-have-consequences",  # "Ideas have consequences—let's make them good ones"
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_persona_jokes(persona: str) -> List[str]:
    """Get jokes for a specific persona"""
    jokes_map = {
        'hype_caster': HYPE_CASTER_JOKES,
        'mechanic': MECHANIC_JOKES,
        'curious_analyst': CURIOUS_ANALYST_JOKES,
        'trend_spotter': TREND_SPOTTER_JOKES,
        'informed_enthusiast': INFORMED_ENTHUSIAST_JOKES,
        'scholar': SCHOLAR_JOKES,
        'visionary': VISIONARY_JOKES,
    }
    return jokes_map.get(persona, [])


def get_persona_anecdotes(persona: str) -> List[str]:
    """Get anecdotes for a specific persona"""
    anecdotes_map = {
        'hype_caster': HYPE_CASTER_ANECDOTES,
        'mechanic': MECHANIC_ANECDOTES,
        'curious_analyst': CURIOUS_ANALYST_ANECDOTES,
        'trend_spotter': TREND_SPOTTER_ANECDOTES,
        'informed_enthusiast': INFORMED_ENTHUSIAST_ANECDOTES,
        'scholar': SCHOLAR_ANECDOTES,
        'visionary': VISIONARY_ANECDOTES,
    }
    return anecdotes_map.get(persona, [])


def select_fresh_joke(persona: str, blacklist: Set[str]) -> str:
    """
    Select a joke that's not in the blacklist
    
    Args:
        persona: Persona name
        blacklist: Set of joke identifiers to avoid
        
    Returns:
        Joke identifier, or empty string if all are blacklisted
    """
    jokes = get_persona_jokes(persona)
    available = [j for j in jokes if j not in blacklist]
    
    if not available:
        return ""
    
    return random.choice(available)


def select_fresh_anecdote(persona: str, blacklist: Set[str]) -> str:
    """
    Select an anecdote that's not in the blacklist
    
    Args:
        persona: Persona name
        blacklist: Set of phrase identifiers to avoid
        
    Returns:
        Anecdote text, or empty string if all are blacklisted
    """
    anecdotes = get_persona_anecdotes(persona)
    
    # Create identifiers from first 3 words
    available = []
    for anecdote in anecdotes:
        identifier = '-'.join(anecdote.split()[:3]).lower()
        if identifier not in blacklist:
            available.append(anecdote)
    
    if not available:
        return ""
    
    return random.choice(available)


def inject_personality(text: str, persona: str, blacklist: Set[str], max_injections: int = 2) -> str:
    """
    Inject personality elements into text
    
    Args:
        text: Original text
        persona: Persona name
        blacklist: Set of phrases to avoid
        max_injections: Maximum number of personality elements to inject
        
    Returns:
        Text with personality injected
    """
    # For now, just return original text
    # This would be enhanced to actually inject jokes/anecdotes
    # in strategic locations within the text
    return text


def main():
    """Test personality system"""
    print("🎭 Testing Personality System\n")
    
    personas = ['hype_caster', 'mechanic', 'curious_analyst', 'trend_spotter', 'informed_enthusiast', 'scholar', 'visionary']
    
    for persona in personas:
        print(f"\n{'='*60}")
        print(f"Persona: {persona.replace('_', ' ').title()}")
        print(f"{'='*60}")
        
        jokes = get_persona_jokes(persona)
        print(f"\nJokes ({len(jokes)}):")
        for joke in jokes[:3]:
            print(f"  - {joke}")
        
        anecdotes = get_persona_anecdotes(persona)
        print(f"\nAnecdotes ({len(anecdotes)}):")
        for anecdote in anecdotes[:2]:
            print(f"  - {anecdote}")
    
    print("\n\n🎉 Personality system loaded successfully!")


if __name__ == "__main__":
    main()

