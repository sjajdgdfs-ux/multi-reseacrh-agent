from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class ResearchPlan(BaseModel):
    topic: str
    questions: list[str]

class AgentState(BaseModel):
    topic: str
    plan: ResearchPlan | None = None
    search_results: dict[str, list[SearchResult]] = {}
    analysis: str = ""
    final_report: str = ""
    status: str = "started"
