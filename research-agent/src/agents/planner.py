from src.core.llm import generate
from src.core.schemas import ResearchPlan
import json
import re

SYSTEM = """You are a research planner.
Your job is to break down a research topic into 4 focused search questions.
Always respond with valid JSON only."""

def run(topic: str) -> ResearchPlan:
    prompt = f"""
Research topic: {topic}

Create exactly 4 search questions that together will give a full picture of this topic.
Each question should cover a different angle.

Respond ONLY with this JSON (no extra text):
{{
  "questions": [
    "question 1",
    "question 2",
    "question 3",
    "question 4"
  ]
}}
"""
    response = generate(prompt, system=SYSTEM)
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if not match:
        raise ValueError(f"Planner returned invalid JSON:\n{response}")
    data = json.loads(match.group())
    return ResearchPlan(topic=topic, questions=data["questions"])
