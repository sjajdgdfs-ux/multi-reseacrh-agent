import streamlit as st
import time
import sys
import os

# Add project root to path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.agents import planner, searcher, analyzer, writer
from src.core.schemas import AgentState

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 900px; margin: 0 auto; }

    .agent-box {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 6px 0;
        font-size: 15px;
    }
    .agent-waiting  { background: #f0f0f0; color: #888; }
    .agent-running  { background: #fff8e1; color: #f57c00; }
    .agent-done     { background: #e8f5e9; color: #2e7d32; }
    .agent-error    { background: #ffebee; color: #c62828; }

    .report-box {
        background: #fafafa;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 24px;
        margin-top: 16px;
    }

    .stat-card {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────
def agent_box(label: str, status: str, detail: str = "") -> str:
    icons = {
        "waiting": "⏳",
        "running": "🔄",
        "done":    "✅",
        "error":   "❌"
    }
    icon = icons.get(status, "⏳")
    detail_html = f"<br><small>{detail}</small>" if detail else ""
    return f"""
    <div class="agent-box agent-{status}">
        {icon} <b>{label}</b>{detail_html}
    </div>
    """


def run_pipeline(topic: str):
    state = AgentState(topic=topic)
    total_start = time.time()

    # ── Layout ────────────────────────────────────────
    st.markdown("### 🤖 Agents Status")
    col1, col2 = st.columns(2)

    with col1:
        planner_slot  = st.empty()
        searcher_slot = st.empty()
    with col2:
        analyzer_slot = st.empty()
        writer_slot   = st.empty()

    stats_slot  = st.empty()
    report_slot = st.empty()

    # ── Initial State (all waiting) ───────────────────
    planner_slot .markdown(agent_box("🧠 Planner",  "waiting"), unsafe_allow_html=True)
    searcher_slot.markdown(agent_box("🔍 Searcher", "waiting"), unsafe_allow_html=True)
    analyzer_slot.markdown(agent_box("📊 Analyzer", "waiting"), unsafe_allow_html=True)
    writer_slot  .markdown(agent_box("✍️ Writer",   "waiting"), unsafe_allow_html=True)

    # ── Step 1: Planner ───────────────────────────────
    planner_slot.markdown(agent_box("🧠 Planner", "running", "Breaking down topic..."), unsafe_allow_html=True)
    t = time.time()
    try:
        state.plan = planner.run(topic)
        planner_time = time.time() - t
        questions_preview = " | ".join([f"Q{i+1}" for i in range(len(state.plan.questions))])
        planner_slot.markdown(
            agent_box("🧠 Planner", "done", f"{len(state.plan.questions)} questions in {planner_time:.1f}s"),
            unsafe_allow_html=True
        )

        # Show questions in expander
        with st.expander("📋 Research Questions", expanded=False):
            for i, q in enumerate(state.plan.questions, 1):
                st.markdown(f"**{i}.** {q}")

    except Exception as e:
        planner_slot.markdown(agent_box("🧠 Planner", "error", str(e)), unsafe_allow_html=True)
        st.error(f"Planner failed: {e}")
        return None

    # ── Step 2: Searcher ──────────────────────────────
    searcher_slot.markdown(agent_box("🔍 Searcher", "running", "Parallel web search..."), unsafe_allow_html=True)
    t = time.time()
    try:
        state.search_results = searcher.run(state.plan)
        searcher_time = time.time() - t
        total_results = sum(len(v) for v in state.search_results.values())
        searcher_slot.markdown(
            agent_box("🔍 Searcher", "done", f"{total_results} results in {searcher_time:.1f}s (parallel)"),
            unsafe_allow_html=True
        )

        # Show search results in expander
        with st.expander("🔍 Search Results", expanded=False):
            for question, results in state.search_results.items():
                st.markdown(f"**Q:** {question}")
                for r in results:
                    st.markdown(f"- [{r.title}]({r.url})")
                st.divider()

    except Exception as e:
        searcher_slot.markdown(agent_box("🔍 Searcher", "error", str(e)), unsafe_allow_html=True)
        st.error(f"Searcher failed: {e}")
        return None

    # ── Step 3: Analyzer ──────────────────────────────
    analyzer_slot.markdown(agent_box("📊 Analyzer", "running", "Synthesizing findings..."), unsafe_allow_html=True)
    t = time.time()
    try:
        state.analysis = analyzer.run(state.plan, state.search_results)
        analyzer_time = time.time() - t
        analyzer_slot.markdown(
            agent_box("📊 Analyzer", "done", f"Analysis ready in {analyzer_time:.1f}s"),
            unsafe_allow_html=True
        )

        with st.expander("📊 Raw Analysis", expanded=False):
            st.markdown(state.analysis)

    except Exception as e:
        analyzer_slot.markdown(agent_box("📊 Analyzer", "error", str(e)), unsafe_allow_html=True)
        st.error(f"Analyzer failed: {e}")
        return None

    # ── Step 4: Writer ────────────────────────────────
    writer_slot.markdown(agent_box("✍️ Writer", "running", "Writing final report..."), unsafe_allow_html=True)
    t = time.time()
    try:
        state.final_report = writer.run(state.plan, state.analysis)
        writer_time = time.time() - t
        writer_slot.markdown(
            agent_box("✍️ Writer", "done", f"Report ready in {writer_time:.1f}s"),
            unsafe_allow_html=True
        )
    except Exception as e:
        writer_slot.markdown(agent_box("✍️ Writer", "error", str(e)), unsafe_allow_html=True)
        st.error(f"Writer failed: {e}")
        return None

    # ── Stats ─────────────────────────────────────────
    total_time = time.time() - total_start
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧠 Planner",  f"{planner_time:.1f}s")
    c2.metric("🔍 Searcher", f"{searcher_time:.1f}s")
    c3.metric("📊 Analyzer", f"{analyzer_time:.1f}s")
    c4.metric("⏱️ Total",    f"{total_time:.1f}s")

    state.status = "completed"
    return state


# ── Main UI ───────────────────────────────────────────
def main():
    # Header
    st.markdown("# 🔬 Research Agent")
    st.markdown("**Multi-Agent Deep Research System** — Powered by Gemini + DuckDuckGo")
    st.divider()

    # Input
    col1, col2 = st.columns([4, 1])
    with col1:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. The future of AI Agents in 2026",
            label_visibility="collapsed"
        )
    with col2:
        start = st.button("🚀 Start Research", use_container_width=True)

    # Examples
    st.markdown("**Examples:**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        if st.button("🤖 AI Agents 2026", use_container_width=True):
            topic = "AI Agents in 2026"
            start = True
    with ex_col2:
        if st.button("🌍 Climate Change", use_container_width=True):
            topic = "Climate change impact on Egypt"
            start = True
    with ex_col3:
        if st.button("💰 Freelance AI", use_container_width=True):
            topic = "Freelancing as an AI Engineer in 2026"
            start = True

    st.divider()

    # Run pipeline
    if start and topic:
        state = run_pipeline(topic)

        if state and state.final_report:
            st.divider()
            st.markdown("## 📄 Final Report")

            # Display report
            st.markdown(
                f'<div class="report-box">{state.final_report}</div>',
                unsafe_allow_html=True
            )

            # Download buttons
            st.divider()
            dl_col1, dl_col2 = st.columns(2)

            with dl_col1:
                st.download_button(
                    label="⬇️ Download as Markdown",
                    data=state.final_report,
                    file_name=f"{topic[:30].replace(' ', '_')}_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with dl_col2:
                st.download_button(
                    label="⬇️ Download as Text",
                    data=state.final_report,
                    file_name=f"{topic[:30].replace(' ', '_')}_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    elif start and not topic:
        st.warning("⚠️ Please enter a research topic first.")


if __name__ == "__main__":
    main()

