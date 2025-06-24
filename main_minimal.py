#!/usr/bin/env python3
"""
Local Doc-Whisperer (Minimal Version): A CLI tool to digest text documents and create summaries using Claude.
This version uses in-memory storage instead of ChromaDB to avoid dependency issues.
"""

import os
import json
import textwrap
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

class SimpleDocWhisperer:
    def __init__(self):
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            console.print("[red]Error: ANTHROPIC_API_KEY not found in environment.[/red]")
            console.print("Please copy env.example to .env and add your API key.")
            raise typer.Exit(1)
        
        self.anthropic = Anthropic(api_key=api_key)
        self.model = os.getenv("DEFAULT_MODEL", "claude-3-sonnet-20240229")
        
        # Simple in-memory storage for documents
        self.documents = {}  # file_path -> content
        self.summaries = {}  # file_path -> summary data
        
        # Ensure output directory exists
        Path("summaries").mkdir(exist_ok=True)

    def extract_text(self, file_path: str) -> str:
        """Extract text from text files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def generate_summary_and_quiz(self, text: str, file_path: str) -> Dict[str, Any]:
        """Use Claude to generate summary and quiz questions."""
        
        # Truncate text if too long (keeping within token limits)
        max_chars = 70000  # Rough approximation for token limit
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[Content truncated...]"
        
        system_prompt = """You are a research analyst. Given a document, create:

1. A concise 150-word summary that captures the main points
2. Three quiz questions with answers for self-study
3. For each answer, include the section where the information can be found

Return your response as valid JSON with this structure:
{
  "summary": "150-word summary here",
  "quiz": [
    {
      "question": "Question 1",
      "answer": "Answer with citation",
      "source_location": "Section or paragraph reference"
    },
    {
      "question": "Question 2", 
      "answer": "Answer with citation",
      "source_location": "Section or paragraph reference"
    },
    {
      "question": "Question 3",
      "answer": "Answer with citation", 
      "source_location": "Section or paragraph reference"
    }
  ]
}"""

        user_content = f"Document to analyze:\n\n{text}"
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task(description="Asking Claude for summary and quiz...", total=None)
                
                message = self.anthropic.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_content}]
                )
            
            # Parse the JSON response
            response_text = message.content[0].text
            
            # Try to extract JSON from the response
            try:
                # Look for JSON block
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    # Fallback: treat as plain text and structure manually
                    return {
                        "summary": response_text[:500] + "..." if len(response_text) > 500 else response_text,
                        "quiz": [
                            {
                                "question": "What are the main topics covered?",
                                "answer": "See the generated summary above",
                                "source_location": "Throughout document"
                            }
                        ]
                    }
            except json.JSONDecodeError:
                console.print("[yellow]Warning: Could not parse JSON response, using fallback format[/yellow]")
                return {
                    "summary": response_text,
                    "quiz": []
                }
                
        except Exception as e:
            console.print(f"[red]Error generating summary: {e}[/red]")
            return {
                "summary": f"Error generating summary for {file_path}",
                "quiz": []
            }

    def ingest_document(self, file_path: str) -> bool:
        """Process a single document: extract and summarize."""
        console.print(f"\n[bold blue]Processing: {file_path}[/bold blue]")
        
        # Extract text
        text = self.extract_text(file_path)
        if not text.strip():
            console.print(f"[red]No text extracted from {file_path}[/red]")
            return False
        
        console.print(f"Extracted {len(text)} characters")
        
        # Store document in memory
        self.documents[file_path] = text
        
        # Generate summary and quiz
        analysis = self.generate_summary_and_quiz(text, file_path)
        self.summaries[file_path] = analysis
        
        # Save summary to markdown file
        file_stem = Path(file_path).stem
        summary_path = Path("summaries") / f"{file_stem}.md"
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"# Analysis of {file_stem}\n\n")
                f.write(f"**Source:** `{file_path}`\n")
                f.write(f"**Processed:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("## Summary\n\n")
                f.write(analysis["summary"])
                f.write("\n\n")
                
                if analysis.get("quiz"):
                    f.write("## Quiz Questions\n\n")
                    for i, qa in enumerate(analysis["quiz"], 1):
                        f.write(f"### Question {i}\n")
                        f.write(f"**Q:** {qa['question']}\n\n")
                        f.write(f"**A:** {qa['answer']}\n\n")
                        f.write(f"**Source:** {qa['source_location']}\n\n")
            
            console.print(f"[green]✓ Summary saved to {summary_path}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving summary: {e}[/red]")
            return False
        
        return True

    def query_documents(self, question: str) -> str:
        """Answer questions based on ingested documents."""
        console.print(f"\n[bold blue]Searching for: {question}[/bold blue]")
        
        if not self.documents:
            return "No documents have been ingested yet. Use 'ingest' command first."
        
        # Simple search: combine all document content
        all_text = "\n\n---DOCUMENT SEPARATOR---\n\n".join(
            f"From {path}:\n{content}" 
            for path, content in self.documents.items()
        )
        
        # Truncate if too long
        max_chars = 50000
        if len(all_text) > max_chars:
            all_text = all_text[:max_chars] + "\n\n[Content truncated...]"
        
        system_prompt = """You are a helpful research assistant. Use the provided document excerpts to answer the user's question. 

Important guidelines:
- Base your answer on the provided context
- If you can identify specific sources, mention them
- If the context doesn't contain enough information, say so
- Be concise but thorough"""

        user_content = f"""Context from documents:

{all_text}

Question: {question}"""

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task(description="Getting answer from Claude...", total=None)
                
                message = self.anthropic.messages.create(
                    model=self.model,
                    max_tokens=800,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_content}]
                )
            
            return message.content[0].text
            
        except Exception as e:
            return f"Error querying documents: {e}"

    def list_documents(self) -> List[str]:
        """List all ingested documents."""
        return list(self.documents.keys())


# CLI Application
app = typer.Typer(help="Local Doc-Whisperer (Minimal): Process text documents with Claude AI")

@app.command()
def ingest(
    path: str = typer.Argument(..., help="Path to document or directory to process"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Process directories recursively")
):
    """Ingest one or more text documents into the knowledge base."""
    doc_whisperer = SimpleDocWhisperer()
    
    path_obj = Path(path)
    
    if path_obj.is_file():
        # Process single file
        success = doc_whisperer.ingest_document(str(path_obj))
        if success:
            console.print(f"\n[bold green]✓ Successfully processed {path}[/bold green]")
        else:
            console.print(f"\n[bold red]✗ Failed to process {path}[/bold red]")
    
    elif path_obj.is_dir():
        # Process directory
        pattern = "**/*" if recursive else "*"
        extensions = [".txt", ".md", ".markdown"]
        
        files_to_process = []
        for ext in extensions:
            files_to_process.extend(path_obj.glob(f"{pattern}{ext}"))
        
        if not files_to_process:
            console.print(f"[yellow]No supported files found in {path}[/yellow]")
            return
        
        console.print(f"Found {len(files_to_process)} files to process")
        
        successful = 0
        for file_path in files_to_process:
            if doc_whisperer.ingest_document(str(file_path)):
                successful += 1
        
        console.print(f"\n[bold green]✓ Successfully processed {successful}/{len(files_to_process)} files[/bold green]")
    
    else:
        console.print(f"[red]Error: {path} is not a valid file or directory[/red]")

@app.command()
def ask(question: str = typer.Argument(..., help="Question to ask about your documents")):
    """Ask a question about your ingested documents."""
    doc_whisperer = SimpleDocWhisperer()
    
    answer = doc_whisperer.query_documents(question)
    
    # Display the answer in a nice panel
    console.print()
    console.print(Panel(
        Markdown(answer),
        title=f"Answer: {question[:50]}{'...' if len(question) > 50 else ''}",
        border_style="blue"
    ))

@app.command()
def list_docs():
    """List all documents in the knowledge base."""
    doc_whisperer = SimpleDocWhisperer()
    
    documents = doc_whisperer.list_documents()
    
    if documents:
        console.print("\n[bold blue]Documents in knowledge base:[/bold blue]")
        for i, doc in enumerate(documents, 1):
            console.print(f"{i:2d}. {doc}")
    else:
        console.print("[yellow]No documents found in knowledge base.[/yellow]")
        console.print("Use 'python main_minimal.py ingest <path>' to add documents.")

@app.command()
def interactive():
    """Start an interactive Q&A session."""
    doc_whisperer = SimpleDocWhisperer()
    
    console.print(Panel(
        "[bold blue]Interactive Doc-Whisperer Session[/bold blue]\n"
        "Ask questions about your documents. Type 'quit' or 'exit' to end.\n"
        "Type 'list' to see available documents.",
        title="Welcome",
        border_style="green"
    ))
    
    while True:
        try:
            question = typer.prompt("\n❓ Your question")
            
            if question.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif question.lower() == 'list':
                documents = doc_whisperer.list_documents()
                if documents:
                    console.print("\n[bold blue]Available documents:[/bold blue]")
                    for doc in documents:
                        console.print(f"  • {doc}")
                else:
                    console.print("[yellow]No documents in knowledge base.[/yellow]")
                continue
            
            answer = doc_whisperer.query_documents(question)
            
            console.print()
            console.print(Panel(
                Markdown(answer),
                title="Answer",
                border_style="blue"
            ))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except EOFError:
            console.print("\n[yellow]Goodbye![/yellow]")
            break

if __name__ == "__main__":
    app() 