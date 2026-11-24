from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5) -> list[dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r["title"],
                    "url":   r["href"],
                    "snippet": r["body"],
                })
    except Exception as e:
        print(f"[Search Error] {e}")
    return results
