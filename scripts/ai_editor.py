"""
AI Editor Orchestrator for GrumpiBlogged

Coordinates all AI-powered editing components:
1. Readability Scoring
2. SEO Optimization
3. Grammar & Style Checking
4. SAEV Fact-Checking Protocol

This is the main entry point for AI editing functionality.
"""

import json
from typing import Dict, Optional
from datetime import datetime

# Import all editing modules
from readability import calculate_readability
from seo_optimizer import optimize_post_seo
from grammar_checker import check_grammar_and_style, format_grammar_report
from fact_checker import SAEVFactChecker


class AIEditor:
    """
    Main AI Editor orchestrator
    
    Coordinates all editing components and provides unified interface
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Editor
        
        Args:
            api_key: Ollama Proxy API key (optional, uses environment if not provided)
        """
        self.api_key = api_key
        self.fact_checker = SAEVFactChecker(api_key=api_key)
    
    def edit_post(
        self,
        title: str,
        content: str,
        persona_name: str = "General",
        author: str = "GrumpiBot",
        url: str = "",
        image: str = "",
        enable_readability: bool = True,
        enable_seo: bool = True,
        enable_grammar: bool = True,
        enable_fact_check: bool = False,  # Disabled by default (time-consuming)
        fact_check_claims: Optional[list] = None
    ) -> Dict:
        """
        Complete AI editing of a blog post
        
        Args:
            title: Post title
            content: Post content
            persona_name: Persona for style matching
            author: Author name
            url: Post URL (optional)
            image: Featured image URL (optional)
            enable_readability: Run readability analysis
            enable_seo: Run SEO optimization
            enable_grammar: Run grammar checking
            enable_fact_check: Run fact-checking (slow, disabled by default)
            fact_check_claims: Specific claims to fact-check (optional)
        
        Returns:
            dict: Complete editing results
        """
        print("\n" + "=" * 70)
        print("🤖 AI EDITOR - PHASE 4: AI-POWERED EDITING")
        print("=" * 70)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'persona': persona_name,
            'readability': None,
            'seo': None,
            'grammar': None,
            'fact_checks': []
        }
        
        # 1. Readability Scoring
        if enable_readability:
            print("\n📊 Running Readability Analysis...")
            try:
                readability = calculate_readability(content)
                results['readability'] = readability
                
                print(f"  ✅ Average Grade Level: {readability['average_grade_level']:.1f}")
                print(f"  ✅ Readability: {readability['readability_level']}")
                print(f"  ✅ Target Met: {'Yes' if readability['target_met'] else 'No'}")
                
                if not readability['target_met']:
                    print(f"  💡 Recommendation: {readability['recommendation']}")
            
            except Exception as e:
                print(f"  ⚠️  Readability analysis failed: {e}")
                results['readability'] = {'error': str(e)}
        
        # 2. SEO Optimization
        if enable_seo:
            print("\n🔍 Running SEO Optimization...")
            try:
                seo = optimize_post_seo(title, content, author, url, image)
                results['seo'] = seo
                
                print(f"  ✅ Optimized Title: {seo['optimized_title']}")
                print(f"  ✅ Meta Description: {len(seo['meta_description'])} chars")
                print(f"  ✅ Keywords: {', '.join(seo['keywords'][:5])}...")
                print(f"  ✅ SEO Score: {seo['seo_score']}/100")
            
            except Exception as e:
                print(f"  ⚠️  SEO optimization failed: {e}")
                results['seo'] = {'error': str(e)}
        
        # 3. Grammar & Style Checking
        if enable_grammar:
            print("\n📝 Running Grammar & Style Check...")
            try:
                grammar = check_grammar_and_style(content, persona_name)
                results['grammar'] = grammar
                
                if grammar.get('skipped'):
                    print(f"  ⚠️  Skipped: {grammar.get('tone_assessment', 'No API key')}")
                else:
                    print(f"  ✅ Grammar Errors: {len(grammar.get('grammar_errors', []))}")
                    print(f"  ✅ Style Suggestions: {len(grammar.get('style_suggestions', []))}")
                    print(f"  ✅ Clarity Score: {grammar.get('clarity_score', 0)}/100")
            
            except Exception as e:
                print(f"  ⚠️  Grammar check failed: {e}")
                results['grammar'] = {'error': str(e)}
        
        # 4. SAEV Fact-Checking (optional, time-consuming)
        if enable_fact_check and fact_check_claims:
            print("\n🔍 Running SAEV Fact-Checking...")
            print(f"  Checking {len(fact_check_claims)} claims...")
            
            for i, claim in enumerate(fact_check_claims, 1):
                print(f"\n  Claim {i}/{len(fact_check_claims)}: {claim[:80]}...")
                try:
                    verification = self.fact_checker.verify_claim(claim, context=content[:500])
                    results['fact_checks'].append(verification.to_dict())
                    
                    print(f"    ✅ Verdict: {verification.verdict}")
                    print(f"    ✅ Confidence: {verification.confidence_score:.1f}%")
                
                except Exception as e:
                    print(f"    ⚠️  Fact-check failed: {e}")
                    results['fact_checks'].append({
                        'claim': claim,
                        'error': str(e)
                    })
        
        print("\n" + "=" * 70)
        print("✅ AI EDITING COMPLETE")
        print("=" * 70)
        
        return results
    
    def generate_editing_report(self, results: Dict) -> str:
        """
        Generate human-readable editing report
        
        Args:
            results: Results from edit_post()
        
        Returns:
            str: Formatted report
        """
        report = []
        report.append("=" * 70)
        report.append("📋 AI EDITING REPORT")
        report.append("=" * 70)
        report.append(f"\nPersona: {results.get('persona', 'Unknown')}")
        report.append(f"Timestamp: {results.get('timestamp', 'Unknown')}")
        
        # Readability
        if results.get('readability'):
            r = results['readability']
            if 'error' not in r:
                report.append(f"\n📊 READABILITY:")
                report.append(f"  Grade Level: {r.get('average_grade_level', 0):.1f}")
                report.append(f"  Level: {r.get('readability_level', 'Unknown')}")
                report.append(f"  Target Met: {'✅ Yes' if r.get('target_met') else '❌ No'}")
                if not r.get('target_met'):
                    report.append(f"  Recommendation: {r.get('recommendation', 'N/A')}")
        
        # SEO
        if results.get('seo'):
            s = results['seo']
            if 'error' not in s:
                report.append(f"\n🔍 SEO:")
                report.append(f"  Optimized Title: {s.get('optimized_title', 'N/A')}")
                report.append(f"  Meta Description: {s.get('meta_description', 'N/A')[:100]}...")
                report.append(f"  Keywords: {', '.join(s.get('keywords', [])[:8])}")
                report.append(f"  SEO Score: {s.get('seo_score', 0)}/100")
        
        # Grammar
        if results.get('grammar'):
            g = results['grammar']
            if 'error' not in g and not g.get('skipped'):
                report.append(f"\n📝 GRAMMAR & STYLE:")
                report.append(f"  Grammar Errors: {len(g.get('grammar_errors', []))}")
                report.append(f"  Style Suggestions: {len(g.get('style_suggestions', []))}")
                report.append(f"  Repetitive Phrases: {len(g.get('repetitive_phrases', []))}")
                report.append(f"  Clarity Score: {g.get('clarity_score', 0)}/100")
                report.append(f"  Tone: {g.get('tone_assessment', 'N/A')}")
        
        # Fact Checks
        if results.get('fact_checks'):
            report.append(f"\n🔍 FACT CHECKS ({len(results['fact_checks'])}):")
            for i, fc in enumerate(results['fact_checks'], 1):
                if 'error' not in fc:
                    report.append(f"\n  {i}. {fc.get('claim', 'Unknown')[:80]}...")
                    report.append(f"     Verdict: {fc.get('verdict', 'Unknown')}")
                    report.append(f"     Confidence: {fc.get('confidence_score', 0):.1f}%")
        
        report.append("\n" + "=" * 70)
        
        return '\n'.join(report)
    
    def save_results(self, results: Dict, output_file: str):
        """
        Save editing results to JSON file
        
        Args:
            results: Results from edit_post()
            output_file: Path to output JSON file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to: {output_file}")


# Convenience function for quick editing
def quick_edit(title: str, content: str, persona: str = "General") -> Dict:
    """
    Quick edit with default settings (no fact-checking)
    
    Args:
        title: Post title
        content: Post content
        persona: Persona name
    
    Returns:
        dict: Editing results
    """
    editor = AIEditor()
    return editor.edit_post(
        title=title,
        content=content,
        persona_name=persona,
        enable_readability=True,
        enable_seo=True,
        enable_grammar=True,
        enable_fact_check=False
    )


if __name__ == '__main__':
    # Test the AI editor
    sample_title = "New AI Models Released - Qwen3 and DeepSeek V3"
    sample_content = """
    # New AI Models Released
    
    Today we're exploring two groundbreaking AI models that just dropped: Qwen3-VL and DeepSeek V3.
    These models represent significant advances in vision-language understanding and reasoning capabilities.
    
    ## Qwen3-VL: Vision-Language Excellence
    
    Qwen3-VL brings state-of-the-art performance to multimodal tasks, combining visual understanding
    with natural language processing in unprecedented ways. The model excels at image captioning,
    visual question answering, and complex reasoning about visual content.
    
    ## DeepSeek V3: Reasoning Powerhouse
    
    DeepSeek V3 focuses on advanced reasoning and problem-solving, with impressive benchmarks
    across mathematical and logical reasoning tasks. It demonstrates strong performance on
    competitive programming challenges and complex analytical problems.
    """
    
    print("Testing AI Editor...")
    print("=" * 70)
    
    editor = AIEditor()
    results = editor.edit_post(
        title=sample_title,
        content=sample_content,
        persona_name="Tech Enthusiast",
        enable_readability=True,
        enable_seo=True,
        enable_grammar=False,  # Skip grammar (requires API key)
        enable_fact_check=False  # Skip fact-checking (time-consuming)
    )
    
    # Print report
    print("\n" + editor.generate_editing_report(results))

