import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.core.schemas import AgentState
from src.agents import planner, searcher, analyzer, writer

console = Console()

def run(topic: str) -> AgentState:
    state = AgentState(topic=topic)
    total_start = time.time()

    console.print(Panel("🧠 [bold cyan]Planner Agent[/bold cyan] — Breaking down the topic..."))
    t = time.time()
    state.plan = planner.run(topic)
    console.print(f"[green]✅ Plan ready[/green] ({time.time()-t:.1f}s)")
    for i, q in enumerate(state.plan.questions, 1):
        console.print(f"   {i}. {q}")

    console.print(Panel("🔍 [bold cyan]Searcher Agent[/bold cyan] — Parallel web search..."))
    t = time.time()
    state.search_results = searcher.run(state.plan)
    total_results = sum(len(v) for v in state.search_results.values())
    console.print(f"[green]✅ Found {total_results} results across {len(state.plan.questions)} questions[/green] ({time.time()-t:.1f}s)")

    console.print(Panel("📊 [bold cyan]Analyzer Agent[/bold cyan] — Synthesizing findings..."))
    t = time.time()
    state.analysis = analyzer.run(state.plan, state.search_results)
    console.print(f"[green]✅ Analysis complete[/green] ({time.time()-t:.1f}s)")

    console.print(Panel("✍️  [bold cyan]Writer Agent[/bold cyan] — Writing final report..."))
    t = time.time()
    state.final_report = writer.run(state.plan, state.analysis)
    console.print(f"[green]✅ Report ready[/green] ({time.time()-t:.1f}s)")

    table = Table(title="Pipeline Summary")
    table.add_column("Agent", style="cyan")
    table.add_column("Status", style="green")
    table.add_row("🧠 Planner",  "✅ Done")
    table.add_row("🔍 Searcher", f"✅ {total_results} results (parallel)")
    table.add_row("📊 Analyzer", "✅ Done")
    table.add_row("✍️  Writer",   "✅ Done")
    table.add_row("⏱️  Total Time", f"{time.time()-total_start:.1f}s")
    console.print(table)

    state.status = "completed"
    return state
