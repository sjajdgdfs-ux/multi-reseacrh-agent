from src.core.llm import generate
from src.core.schemas import ResearchPlan, SearchResult

SYSTEM = """You are a research analyst.
Your job is to synthesize search results into clear, structured insights.
Be objective, concise, and highlight the most important findings."""

def run(plan: ResearchPlan, search_results: dict[str, list[SearchResult]]) -> str:
    context = ""
    for question, results in search_results.items():
        context += f"\n\n### Question: {question}\n"
        for r in results:
            context += f"- {r.title}: {r.snippet}\n"
    prompt = f"""
Research topic: {plan.topic}

Here are the search results for each research question:
{context}

Analyze these results and provide:
1. Key findings (most important facts)
2. Main patterns or trends
3. Conflicting information (if any)
4. Gaps in the research

Be specific and cite sources when possible.
"""
    return generate(prompt, system=SYSTEM)
