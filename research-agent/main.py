from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from src.orchestrator import run

console = Console()

def save_report(topic: str, report: str):
    filename = topic.replace(" ", "_").lower()[:30] + "_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    return filename

def main():
    console.print(Panel(
        "[bold green]🔬 Research Agent[/bold green]\nMulti-Agent Deep Research System",
        expand=False
    ))
    topic = input("\n📝 Enter research topic: ").strip()
    if not topic:
        console.print("[red]❌ Please enter a topic[/red]")
        return
    console.print(f"\n[bold]Starting research on:[/bold] {topic}\n")
    state = run(topic)
    console.print("\n")
    console.print(Panel("📄 [bold green]FINAL REPORT[/bold green]"))
    console.print(Markdown(state.final_report))
    filename = save_report(topic, state.final_report)
    console.print(f"\n[green]💾 Report saved to:[/green] {filename}")

if __name__ == "__main__":
    main()
