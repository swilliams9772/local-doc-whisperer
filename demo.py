#!/usr/bin/env python3
"""
Demo script for Local Doc-Whisperer
Shows the complete workflow: ingest → ask questions
"""

from main_minimal import SimpleDocWhisperer
from rich.console import Console

console = Console()

def main():
    console.print("[bold green]🧠 Local Doc-Whisperer Demo[/bold green]")
    console.print("=" * 40)
    
    # Create the whisperer instance
    doc_whisperer = SimpleDocWhisperer()
    
    # Ingest the sample document
    console.print("\n[bold blue]Step 1: Ingesting sample document...[/bold blue]")
    success = doc_whisperer.ingest_document("docs_in/sample_document.md")
    
    if not success:
        console.print("[red]Failed to ingest document![/red]")
        return
    
    # List documents
    console.print("\n[bold blue]Step 2: Documents in knowledge base:[/bold blue]")
    docs = doc_whisperer.list_documents()
    for i, doc in enumerate(docs, 1):
        console.print(f"  {i}. {doc}")
    
    # Ask some questions
    questions = [
        "What are the main benefits of AI in education?",
        "What challenges does AI face in education?",
        "What are some examples of current AI applications in education?"
    ]
    
    console.print("\n[bold blue]Step 3: Asking questions...[/bold blue]")
    
    for i, question in enumerate(questions, 1):
        console.print(f"\n[yellow]Question {i}: {question}[/yellow]")
        answer = doc_whisperer.query_documents(question)
        console.print(f"[green]Answer:[/green] {answer[:200]}..." if len(answer) > 200 else f"[green]Answer:[/green] {answer}")
        console.print("-" * 50)
    
    console.print("\n[bold green]✅ Demo completed successfully![/bold green]")
    console.print("\nNow you can:")
    console.print("• Check summaries/ folder for generated summaries")
    console.print("• Use 'python3 main_minimal.py interactive' for chat mode")
    console.print("• Add your own .txt or .md files to docs_in/ and ingest them")

if __name__ == "__main__":
    main() 