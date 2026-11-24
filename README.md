# 🔬 Research Agent — Multi-Agent Deep Research System

A multi-agent AI system that takes any research topic and produces a complete, structured research report — powered by **Gemini** and real-time web search.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Gemini](https://img.shields.io/badge/LLM-Gemini%203.5%20Flash--Lite-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **4 specialized agents** working in a sequential pipeline
- **Parallel web search** (4x faster than sequential)
- **Automatic retry** with exponential backoff on LLM failures
- **Live agent status** in the UI (waiting → running → done)
- **Structured reports** with executive summary, key findings, analysis, and recommendations
- **Multilingual** — responds in the language of the topic (English, Arabic, etc.)
- **Download** reports as Markdown or plain text
- **100% free** — Gemini free tier + DuckDuckGo (no API key needed for search)

---

## 🏗️ Architecture
