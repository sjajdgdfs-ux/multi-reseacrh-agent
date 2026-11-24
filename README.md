# 🔬 Research Agent — Multi-Agent Deep Research System

A multi-agent AI system that takes any research topic and produces a complete, structured research report — powered by **Gemini** and real-time web search.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Gemini](https://img.shields.io/badge/LLM-Gemini%203.5%20Flash--Lite-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Multi-agent pipeline with 4 specialized agents
- Parallel web search (4x faster)
- Auto-retry on API failures
- Clean Streamlit web UI
- Download report as Markdown or Text
- Works on any topic in any language

## How It Works

Your Topic ↓ 🧠 Planner → breaks topic into 4 research questions ↓ 🔍 Searcher → searches the web in parallel ↓ 📊 Analyzer → synthesizes all results ↓ ✍️ Writer → writes the final report ↓ 📄 Download as Markdown or Text

## Project Structure

research-agent/ ├── app.py ← Streamlit UI ├── main.py ← Terminal version ├── requirements.txt └── src/ ├── agents/ │ ├── planner.py │ ├── searcher.py │ ├── analyzer.py │ └── writer.py ├── core/ │ ├── llm.py │ ├── schemas.py │ └── tools.py └── orchestrator.py

## Tech Stack

- Python 3.10+
- Google Gemini API (free tier)
- DuckDuckGo Search (no API key needed)
- Streamlit
- Pydantic
- Rich

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.\.venv\Scripts\Activate.ps1`
4. Install: `pip install -r requirements.txt`
5. Add API key to `.env`: `GEMINI_API_KEY=your_key_here`
6. Run: `python -m streamlit run app.py`

Get your free Gemini API key from: https://aistudio.google.com/apikey

## Note

This is a research prototype. Always verify important claims with original sources.
