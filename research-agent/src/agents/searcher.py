import concurrent.futures
from src.core.tools import web_search
from src.core.schemas import ResearchPlan, SearchResult

def search_one(question: str) -> tuple[str, list[SearchResult]]:
    try:
        raw = web_search(question, max_results=4)
        results = [
            SearchResult(title=r["title"], url=r["url"], snippet=r["snippet"])
            for r in raw
        ]
    except Exception as e:
        print(f"[Search Error] '{question}': {e}")
        results = []
    return question, results

def run(plan: ResearchPlan) -> dict[str, list[SearchResult]]:
    all_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(search_one, question): question
            for question in plan.questions
        }
        for future in concurrent.futures.as_completed(futures):
            question, results = future.result()
            all_results[question] = results
    return all_results
