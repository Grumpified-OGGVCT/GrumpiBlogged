"""
SAEV Fact-Checking Protocol for GrumpiBlogged

Source-Agnostic, Evidence-Weighted Verification Protocol

Four-Phase Verification System:
1. Evidence Aggregation - Collect from diverse sources
2. Dynamic Evidence Weighting - Score based on provenance, rigor, corroboration
3. Synthesis & Truth Rhythm - Generate confidence scores
4. Transparency & User Empowerment - Detailed veracity reports

This implements a sophisticated fact-checking system that:
- Casts a wide net across diverse source categories
- Weights evidence based on transparent scoring
- Learns from its own performance over time
- Provides full transparency in verification reports
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class EvidenceSource:
    """Represents a single piece of evidence"""
    claim: str
    source_type: str  # 'primary', 'independent', 'institutional', 'crowdsourced'
    source_name: str
    content: str
    url: Optional[str] = None
    date: Optional[str] = None
    
    # Scoring components
    provenance_score: float = 0.0  # 0-100: transparency, funding disclosure, conflicts
    rigor_score: float = 0.0       # 0-100: methodology, reproducibility, logic
    corroboration_score: float = 0.0  # 0-100: independent confirmation
    
    # Calculated
    total_weight: float = 0.0
    
    def calculate_weight(self):
        """Calculate total evidence weight from component scores"""
        self.total_weight = (
            self.provenance_score * 0.3 +
            self.rigor_score * 0.4 +
            self.corroboration_score * 0.3
        )
        return self.total_weight


@dataclass
class VerificationResult:
    """Complete verification result for a claim"""
    claim: str
    confidence_score: float  # 0-100
    verdict: str  # 'verified', 'likely_true', 'uncertain', 'likely_false', 'false'
    evidence_count: int
    evidence_sources: List[EvidenceSource]
    consensus_points: List[str]
    contention_points: List[str]
    limitations: List[str]
    timestamp: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'claim': self.claim,
            'confidence_score': self.confidence_score,
            'verdict': self.verdict,
            'evidence_count': self.evidence_count,
            'evidence_sources': [asdict(e) for e in self.evidence_sources],
            'consensus_points': self.consensus_points,
            'contention_points': self.contention_points,
            'limitations': self.limitations,
            'timestamp': self.timestamp
        }


class SAEVFactChecker:
    """
    Source-Agnostic, Evidence-Weighted Verification Protocol
    
    Implements the four-phase verification system with learning capabilities
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize fact checker
        
        Args:
            api_key: Ollama Proxy API key (or use environment variable)
        """
        self.api_key = api_key or os.getenv('OLLAMA_PROXY_FACT_CHECK_API_KEY') or os.getenv('OLLAMA_PROXY_API_KEY')
        self.model = "deepseek-v3.1:671b-cloud"  # Best reasoning model for fact-checking
        self.verification_history = []
    
    def verify_claim(self, claim: str, context: str = "") -> VerificationResult:
        """
        Complete SAEV verification of a claim
        
        Args:
            claim: The claim to verify
            context: Additional context about the claim
        
        Returns:
            VerificationResult: Complete verification with evidence and scoring
        """
        print(f"\n🔍 SAEV Fact-Checking: {claim[:100]}...")
        
        # Phase 1: Evidence Aggregation
        evidence_sources = self._aggregate_evidence(claim, context)
        
        if not evidence_sources:
            return VerificationResult(
                claim=claim,
                confidence_score=0.0,
                verdict='insufficient_evidence',
                evidence_count=0,
                evidence_sources=[],
                consensus_points=[],
                contention_points=['No evidence could be gathered'],
                limitations=['Unable to verify - no sources available'],
                timestamp=datetime.now().isoformat()
            )
        
        # Phase 2: Dynamic Evidence Weighting
        weighted_evidence = self._weight_evidence(evidence_sources)
        
        # Phase 3: Synthesis & Truth Rhythm
        verification = self._synthesize_verification(claim, weighted_evidence)
        
        # Phase 4: Transparency (handled by caller via generate_transparency_report)
        
        # Store in history for learning
        self.verification_history.append(verification)
        
        return verification
    
    def _aggregate_evidence(self, claim: str, context: str) -> List[EvidenceSource]:
        """
        Phase 1: Evidence Aggregation
        
        Cast wide net across diverse source categories:
        - Primary Evidence (scientific papers, raw data, official docs)
        - Independent Analysis (expert blogs, independent journalists)
        - Institutional Sources (major news, government, NGOs)
        - Crowdsourced Data (social media trends, OSINT)
        
        Args:
            claim: Claim to verify
            context: Additional context
        
        Returns:
            List[EvidenceSource]: Evidence from diverse sources
        """
        if not self.api_key:
            print("⚠️  No API key - skipping evidence aggregation")
            return []
        
        # Use AI to search for and evaluate evidence
        prompt = f"""You are a fact-checking researcher gathering evidence for a claim.

**Claim to Verify**: {claim}

**Context**: {context if context else "No additional context provided"}

**Task**: Search your knowledge base and identify evidence from diverse source categories:

1. **Primary Evidence**: Scientific papers, research data, official documents
2. **Independent Analysis**: Expert analysis, investigative journalism
3. **Institutional Sources**: Mainstream news, government statements, NGO reports
4. **Crowdsourced Data**: Community observations, open-source intelligence

For each piece of evidence, provide:
- Source type (primary/independent/institutional/crowdsourced)
- Source name
- Evidence content (what it says about the claim)
- Assessment of source quality

**Output Format** (JSON only):
{{
  "evidence": [
    {{
      "source_type": "primary",
      "source_name": "Nature Journal",
      "content": "Study shows...",
      "quality_assessment": "High quality - peer reviewed, reproducible methods"
    }}
  ]
}}

Provide 3-5 diverse evidence sources if available. Respond with ONLY the JSON object."""

        try:
            response = requests.post(
                'http://localhost:8081/api/chat',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'stream': False,
                    'temperature': 0.4
                },
                timeout=180  # 3 minutes for evidence gathering
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '{}')
                
                # Extract JSON
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                data = json.loads(content)
                evidence_list = data.get('evidence', [])
                
                # Convert to EvidenceSource objects
                sources = []
                for ev in evidence_list:
                    source = EvidenceSource(
                        claim=claim,
                        source_type=ev.get('source_type', 'unknown'),
                        source_name=ev.get('source_name', 'Unknown'),
                        content=ev.get('content', ''),
                        url=ev.get('url'),
                        date=ev.get('date')
                    )
                    sources.append(source)
                
                print(f"  ✅ Gathered {len(sources)} evidence sources")
                return sources
            
            else:
                print(f"  ⚠️  Evidence aggregation failed: HTTP {response.status_code}")
                return []
        
        except Exception as e:
            print(f"  ⚠️  Evidence aggregation error: {e}")
            return []
    
    def _weight_evidence(self, evidence_sources: List[EvidenceSource]) -> List[EvidenceSource]:
        """
        Phase 2: Dynamic Evidence Weighting
        
        Score each piece of evidence on:
        - Provenance & Transparency (30%): Methods, funding, conflicts disclosed
        - Methodological Rigor (40%): Controlled studies, reproducibility, logic
        - Corroboration (30%): Independent confirmation from other sources
        
        Args:
            evidence_sources: Raw evidence to score
        
        Returns:
            List[EvidenceSource]: Evidence with calculated weights
        """
        if not self.api_key or not evidence_sources:
            return evidence_sources
        
        print(f"  📊 Weighting {len(evidence_sources)} evidence sources...")
        
        for source in evidence_sources:
            # Use AI to score each dimension
            prompt = f"""You are an evidence quality assessor. Score this evidence on three dimensions:

**Evidence**:
- Source Type: {source.source_type}
- Source Name: {source.source_name}
- Content: {source.content}

**Scoring Dimensions** (0-100 each):

1. **Provenance & Transparency Score** (0-100):
   - Are methods disclosed?
   - Is funding transparent?
   - Are conflicts of interest noted?
   - Is data verifiable?

2. **Methodological Rigor Score** (0-100):
   - Based on controlled studies/experiments?
   - Reproducible methods?
   - Logical reasoning with clear premises?
   - Avoids fallacies and emotional appeals?

3. **Corroboration Score** (0-100):
   - Supported by independent sources?
   - Confirmed across different source categories?
   - Consensus among experts?

**Output Format** (JSON only):
{{
  "provenance_score": 85,
  "rigor_score": 90,
  "corroboration_score": 75,
  "reasoning": "brief explanation"
}}

Respond with ONLY the JSON object."""

            try:
                response = requests.post(
                    'http://localhost:8081/api/chat',
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': self.model,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'stream': False,
                        'temperature': 0.2  # Low temp for consistent scoring
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get('message', {}).get('content', '{}')
                    
                    # Extract JSON
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0].strip()
                    
                    scores = json.loads(content)
                    
                    source.provenance_score = scores.get('provenance_score', 50)
                    source.rigor_score = scores.get('rigor_score', 50)
                    source.corroboration_score = scores.get('corroboration_score', 50)
                    source.calculate_weight()
                    
                    print(f"    - {source.source_name}: Weight={source.total_weight:.1f}")
                
                else:
                    # Default moderate scores if API fails
                    source.provenance_score = 50
                    source.rigor_score = 50
                    source.corroboration_score = 50
                    source.calculate_weight()
            
            except Exception as e:
                print(f"    ⚠️  Scoring error for {source.source_name}: {e}")
                source.provenance_score = 50
                source.rigor_score = 50
                source.corroboration_score = 50
                source.calculate_weight()

        return evidence_sources

    def _synthesize_verification(self, claim: str, weighted_evidence: List[EvidenceSource]) -> VerificationResult:
        """
        Phase 3: Synthesis & Truth Rhythm Adjustment

        Synthesize weighted evidence into coherent assessment with:
        - Confidence score
        - Verdict (verified/likely_true/uncertain/likely_false/false)
        - Consensus points
        - Contention points
        - Limitations

        Args:
            claim: Original claim
            weighted_evidence: Evidence with calculated weights

        Returns:
            VerificationResult: Complete verification
        """
        if not weighted_evidence:
            return VerificationResult(
                claim=claim,
                confidence_score=0.0,
                verdict='insufficient_evidence',
                evidence_count=0,
                evidence_sources=[],
                consensus_points=[],
                contention_points=['No evidence available'],
                limitations=['Cannot verify without evidence'],
                timestamp=datetime.now().isoformat()
            )

        print(f"  🔬 Synthesizing verification from {len(weighted_evidence)} sources...")

        # Calculate overall confidence based on weighted evidence
        total_weight = sum(e.total_weight for e in weighted_evidence)
        avg_weight = total_weight / len(weighted_evidence) if weighted_evidence else 0

        # Use AI to synthesize final assessment
        evidence_summary = "\n".join([
            f"- {e.source_name} ({e.source_type}): {e.content[:200]}... [Weight: {e.total_weight:.1f}]"
            for e in weighted_evidence
        ])

        prompt = f"""You are a fact-checking synthesizer. Analyze this weighted evidence and provide a final verdict.

**Claim**: {claim}

**Weighted Evidence**:
{evidence_summary}

**Average Evidence Weight**: {avg_weight:.1f}/100

**Task**: Synthesize this evidence into a final assessment.

**Output Format** (JSON only):
{{
  "confidence_score": 85,
  "verdict": "verified",
  "consensus_points": ["Point 1", "Point 2"],
  "contention_points": ["Disagreement 1"],
  "limitations": ["Limitation 1"],
  "reasoning": "brief explanation"
}}

**Verdict Options**:
- "verified" (90-100% confidence, strong evidence)
- "likely_true" (70-89% confidence, good evidence)
- "uncertain" (40-69% confidence, conflicting evidence)
- "likely_false" (20-39% confidence, evidence suggests false)
- "false" (0-19% confidence, strong evidence against)

Respond with ONLY the JSON object."""

        try:
            response = requests.post(
                'http://localhost:8081/api/chat',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'stream': False,
                    'temperature': 0.3
                },
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '{}')

                # Extract JSON
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                synthesis = json.loads(content)

                verification = VerificationResult(
                    claim=claim,
                    confidence_score=synthesis.get('confidence_score', avg_weight),
                    verdict=synthesis.get('verdict', 'uncertain'),
                    evidence_count=len(weighted_evidence),
                    evidence_sources=weighted_evidence,
                    consensus_points=synthesis.get('consensus_points', []),
                    contention_points=synthesis.get('contention_points', []),
                    limitations=synthesis.get('limitations', []),
                    timestamp=datetime.now().isoformat()
                )

                print(f"  ✅ Verdict: {verification.verdict} (confidence: {verification.confidence_score:.1f}%)")
                return verification

            else:
                # Fallback to simple averaging
                return self._simple_synthesis(claim, weighted_evidence, avg_weight)

        except Exception as e:
            print(f"  ⚠️  Synthesis error: {e}")
            return self._simple_synthesis(claim, weighted_evidence, avg_weight)

    def _simple_synthesis(self, claim: str, evidence: List[EvidenceSource], avg_weight: float) -> VerificationResult:
        """Fallback synthesis when AI synthesis fails"""
        if avg_weight >= 80:
            verdict = 'verified'
        elif avg_weight >= 60:
            verdict = 'likely_true'
        elif avg_weight >= 40:
            verdict = 'uncertain'
        elif avg_weight >= 20:
            verdict = 'likely_false'
        else:
            verdict = 'false'

        return VerificationResult(
            claim=claim,
            confidence_score=avg_weight,
            verdict=verdict,
            evidence_count=len(evidence),
            evidence_sources=evidence,
            consensus_points=['Multiple sources consulted'],
            contention_points=['Automated synthesis - manual review recommended'],
            limitations=['AI synthesis unavailable - using simple averaging'],
            timestamp=datetime.now().isoformat()
        )

    def generate_transparency_report(self, verification: VerificationResult) -> str:
        """
        Phase 4: Transparency & User Empowerment

        Generate detailed veracity report showing:
        - Final confidence level
        - Evidence breakdown with scores
        - Reasoning explanation
        - Limitations and dissenting evidence

        Args:
            verification: Verification result

        Returns:
            str: Formatted transparency report
        """
        report = []
        report.append("=" * 70)
        report.append("🔍 SAEV FACT-CHECK TRANSPARENCY REPORT")
        report.append("=" * 70)

        # Claim and verdict
        report.append(f"\n📋 CLAIM:")
        report.append(f"  {verification.claim}")

        report.append(f"\n⚖️  VERDICT: {verification.verdict.upper().replace('_', ' ')}")
        report.append(f"  Confidence Score: {verification.confidence_score:.1f}/100")

        # Confidence bar
        bar_length = int(verification.confidence_score / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        report.append(f"  [{bar}] {verification.confidence_score:.0f}%")

        # Evidence breakdown
        report.append(f"\n📊 EVIDENCE ANALYSIS ({verification.evidence_count} sources):")
        for i, evidence in enumerate(verification.evidence_sources, 1):
            report.append(f"\n  {i}. {evidence.source_name} ({evidence.source_type})")
            report.append(f"     Content: {evidence.content[:150]}...")
            report.append(f"     Scores:")
            report.append(f"       - Provenance & Transparency: {evidence.provenance_score:.1f}/100")
            report.append(f"       - Methodological Rigor: {evidence.rigor_score:.1f}/100")
            report.append(f"       - Corroboration: {evidence.corroboration_score:.1f}/100")
            report.append(f"     Total Weight: {evidence.total_weight:.1f}/100")

        # Consensus points
        if verification.consensus_points:
            report.append(f"\n✅ CONSENSUS POINTS:")
            for point in verification.consensus_points:
                report.append(f"  • {point}")

        # Contention points
        if verification.contention_points:
            report.append(f"\n⚠️  CONTENTION POINTS:")
            for point in verification.contention_points:
                report.append(f"  • {point}")

        # Limitations
        if verification.limitations:
            report.append(f"\n⚠️  LIMITATIONS:")
            for limitation in verification.limitations:
                report.append(f"  • {limitation}")

        # Timestamp
        report.append(f"\n🕐 Verified: {verification.timestamp}")

        report.append("\n" + "=" * 70)

        return '\n'.join(report)


# Convenience function for quick fact-checking
def quick_fact_check(claim: str, context: str = "") -> Dict:
    """
    Quick fact-check a single claim

    Args:
        claim: Claim to verify
        context: Additional context

    Returns:
        dict: Verification result as dictionary
    """
    checker = SAEVFactChecker()
    result = checker.verify_claim(claim, context)
    return result.to_dict()


if __name__ == '__main__':
    # Test the fact checker
    print("Testing SAEV Fact-Checking Protocol...")
    print("=" * 70)

    # Check if API key is available
    if not os.getenv('OLLAMA_PROXY_API_KEY'):
        print("⚠️  Set OLLAMA_PROXY_API_KEY environment variable to test")
        print("   Example: export OLLAMA_PROXY_API_KEY='your-key-here'")
    else:
        # Test claim
        test_claim = "Qwen3-VL is a state-of-the-art vision-language model released in 2024"

        checker = SAEVFactChecker()
        result = checker.verify_claim(test_claim)

        # Print transparency report
        print(checker.generate_transparency_report(result))

