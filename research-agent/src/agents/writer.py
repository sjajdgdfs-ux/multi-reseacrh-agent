from src.core.llm import generate
from src.core.schemas import ResearchPlan

SYSTEM = """You are a professional research writer working for a top consulting firm.
Your reports are known for being:
- Clear and well-structured
- Evidence-based with specific facts and numbers
- Actionable with concrete insights
- Written in professional markdown format"""

def run(plan: ResearchPlan, analysis: str) -> str:
    prompt = f"""
Research topic: {plan.topic}

Analysis from our research team:
{analysis}

Write a comprehensive research report with these sections:

# {plan.topic}

## Executive Summary
(3-4 sentences: what this is, why it matters, key takeaway)

## Key Findings
(5-7 bullet points, each with a specific fact or number if available)

## Detailed Analysis

### [Main Subtopic 1]
(2-3 paragraphs)

### [Main Subtopic 2]
(2-3 paragraphs)

### [Main Subtopic 3]
(2-3 paragraphs)

## Implications and Recommendations
(What should someone do with this information?)

## Conclusion
(2-3 sentences wrapping up)

## Sources Consulted
(List the sources used in the research)

Rules:
- Use specific numbers and facts wherever possible
- Keep paragraphs short and readable
- Make every sentence add value
"""
    return generate(prompt, system=SYSTEM)
