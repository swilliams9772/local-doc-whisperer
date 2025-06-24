#!/usr/bin/env python3
"""
Enhanced Local Doc-Whisperer: Multi-model support with Claude and OpenAI
Features: Custom prompts, persistent storage, model comparison
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from enum import Enum

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from dotenv import load_dotenv
from anthropic import Anthropic
import openai

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

class ModelProvider(str, Enum):
    CLAUDE = "claude"
    OPENAI = "openai"

class PromptTemplate(str, Enum):
    RESEARCH = "research"
    EDUCATIONAL = "educational"
    BUSINESS = "business"
    CREATIVE = "creative"

class EnhancedDocWhisperer:
    def __init__(self):
        # Initialize API clients
        self._init_api_clients()
        
        # Configuration
        self.default_model = os.getenv("DEFAULT_MODEL", "claude-3-sonnet-20240229")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Persistent storage
        self.storage_file = Path("doc_whisperer_data.json")
        self.documents = {}
        self.summaries = {}
        self.load_data()
        
        # Ensure output directory exists
        Path("summaries").mkdir(exist_ok=True)
        Path("comparisons").mkdir(exist_ok=True)

    def _init_api_clients(self):
        """Initialize API clients for both providers."""
        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic = Anthropic(api_key=anthropic_key)
        else:
            self.anthropic = None
            
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
        else:
            self.openai_client = None

    def get_prompt_template(self, template: PromptTemplate) -> Dict[str, str]:
        """Get different prompt templates for various use cases."""
        templates = {
            PromptTemplate.RESEARCH: {
                "system": """You are a research analyst specializing in academic and scientific content.""",
                "summary_focus": "research methodology, key findings, and implications",
                "question_style": "analytical and research-focused"
            },
            PromptTemplate.EDUCATIONAL: {
                "system": """You are an educational content specialist.""",
                "summary_focus": "core concepts and learning objectives",
                "question_style": "educational and concept-testing"
            },
            PromptTemplate.BUSINESS: {
                "system": """You are a business analyst reviewing strategic documents.""",
                "summary_focus": "strategic insights and business implications",
                "question_style": "strategic and implementation-focused"
            },
            PromptTemplate.CREATIVE: {
                "system": """You are a creative content analyst.""",
                "summary_focus": "themes and creative elements",
                "question_style": "interpretive and thematic"
            }
        }
        return templates[template]

    def generate_analysis(self, text: str, file_path: str, provider: ModelProvider, 
                         template: PromptTemplate = PromptTemplate.RESEARCH) -> Dict[str, Any]:
        """Generate analysis using specified AI provider and prompt template."""
        
        # Truncate text if too long
        max_chars = 70000
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[Content truncated...]"
        
        prompt_template = self.get_prompt_template(template)
        
        system_prompt = f"""{prompt_template['system']}

Create a JSON response with this structure:
{{
  "summary": "150-word summary",
  "quiz": [
    {{"question": "Question 1", "answer": "Answer 1", "source_location": "Reference"}},
    {{"question": "Question 2", "answer": "Answer 2", "source_location": "Reference"}},
    {{"question": "Question 3", "answer": "Answer 3", "source_location": "Reference"}}
  ],
  "key_concepts": ["concept1", "concept2", "concept3"]
}}"""

        user_content = f"Document to analyze:\n\n{text}"
        
        try:
            if provider == ModelProvider.CLAUDE:
                return self._generate_with_claude(system_prompt, user_content, file_path)
            elif provider == ModelProvider.OPENAI:
                return self._generate_with_openai(system_prompt, user_content, file_path)
        except Exception as e:
            console.print(f"[red]Error generating analysis with {provider.value}: {e}[/red]")
            return self._fallback_analysis(file_path, str(e))

    def _generate_with_claude(self, system_prompt: str, user_content: str, file_path: str) -> Dict[str, Any]:
        """Generate analysis using Claude."""
        if not self.anthropic:
            raise Exception("Anthropic API key not configured")
            
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            progress.add_task(description="Asking Claude for analysis...", total=None)
            
            message = self.anthropic.messages.create(
                model=self.default_model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_content}]
            )
        
        return self._parse_json_response(message.content[0].text, "claude")

    def _generate_with_openai(self, system_prompt: str, user_content: str, file_path: str) -> Dict[str, Any]:
        """Generate analysis using OpenAI."""
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
            
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            progress.add_task(description="Asking OpenAI for analysis...", total=None)
            
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
        
        return self._parse_json_response(response.choices[0].message.content, "openai")

    def _parse_json_response(self, response_text: str, provider: str) -> Dict[str, Any]:
        """Parse JSON response from AI models."""
        try:
            # Look for JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)
                parsed["provider"] = provider
                parsed["timestamp"] = datetime.now().isoformat()
                return parsed
        except json.JSONDecodeError:
            pass
        
        # Fallback for non-JSON responses
        return {
            "summary": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "quiz": [],
            "provider": provider,
            "timestamp": datetime.now().isoformat(),
            "key_concepts": []
        }

    def _fallback_analysis(self, file_path: str, error: str) -> Dict[str, Any]:
        """Fallback analysis when API calls fail."""
        return {
            "summary": f"Error generating analysis for {file_path}: {error}",
            "quiz": [],
            "provider": "fallback",
            "timestamp": datetime.now().isoformat(),
            "key_concepts": []
        }

    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def ingest_document(self, file_path: str, provider: ModelProvider = ModelProvider.CLAUDE, 
                       template: PromptTemplate = PromptTemplate.RESEARCH) -> bool:
        """Process a document with specified provider and template."""
        console.print(f"\n[bold blue]Processing: {file_path}[/bold blue]")
        console.print(f"[dim]Provider: {provider.value} | Template: {template.value}[/dim]")
        
        # Extract text
        text = self.extract_text(file_path)
        if not text.strip():
            console.print(f"[red]No text extracted from {file_path}[/red]")
            return False
        
        console.print(f"Extracted {len(text)} characters")
        
        # Store document
        self.documents[file_path] = {
            "content": text,
            "ingested_at": datetime.now().isoformat(),
            "file_size": len(text)
        }
        
        # Generate analysis
        analysis = self.generate_analysis(text, file_path, provider, template)
        self.summaries[file_path] = analysis
        
        # Save to file
        self.save_summary_to_file(file_path, analysis)
        self.save_data()
        
        return True

    def save_summary_to_file(self, file_path: str, analysis: Dict[str, Any]):
        """Save analysis to markdown file."""
        file_stem = Path(file_path).stem
        provider = analysis.get('provider', 'unknown')
        
        summary_path = Path("summaries") / f"{file_stem}_{provider}_enhanced.md"
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(f"# Analysis of {file_stem}\n\n")
                f.write(f"**Source:** `{file_path}`\n")
                f.write(f"**Provider:** {provider.upper()}\n")
                f.write(f"**Processed:** {analysis.get('timestamp', 'unknown')}\n\n")
                
                # Key concepts
                if analysis.get("key_concepts"):
                    f.write("## Key Concepts\n\n")
                    for concept in analysis["key_concepts"]:
                        f.write(f"- {concept}\n")
                    f.write("\n")
                
                # Summary
                f.write("## Summary\n\n")
                f.write(analysis["summary"])
                f.write("\n\n")
                
                # Quiz
                if analysis.get("quiz"):
                    f.write("## Quiz Questions\n\n")
                    for i, qa in enumerate(analysis["quiz"], 1):
                        f.write(f"### Question {i}\n")
                        f.write(f"**Q:** {qa['question']}\n\n")
                        f.write(f"**A:** {qa['answer']}\n\n")
                        if qa.get('source_location'):
                            f.write(f"**Source:** {qa['source_location']}\n\n")
            
            console.print(f"[green]✓ Analysis saved to {summary_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error saving analysis: {e}[/red]")

    def compare_models(self, file_path: str, template: PromptTemplate = PromptTemplate.RESEARCH) -> Dict[str, Any]:
        """Compare Claude and OpenAI responses for the same document."""
        if file_path not in self.documents:
            return {"error": "Document not found. Please ingest it first."}
        
        text = self.documents[file_path]["content"]
        console.print(f"\n[bold blue]Comparing models for: {file_path}[/bold blue]")
        
        results = {}
        
        # Get Claude analysis
        if self.anthropic:
            console.print("[yellow]Getting Claude analysis...[/yellow]")
            results["claude"] = self.generate_analysis(text, file_path, ModelProvider.CLAUDE, template)
        
        # Get OpenAI analysis
        if self.openai_client:
            console.print("[yellow]Getting OpenAI analysis...[/yellow]")
            results["openai"] = self.generate_analysis(text, file_path, ModelProvider.OPENAI, template)
        
        # Save comparison
        if len(results) > 1:
            self.save_comparison(file_path, results, template)
        
        return results

    def save_comparison(self, file_path: str, results: Dict[str, Any], template: PromptTemplate):
        """Save model comparison to file."""
        file_stem = Path(file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        comparison_path = Path("comparisons") / f"{file_stem}_comparison_{template.value}_{timestamp}.md"
        
        try:
            with open(comparison_path, 'w', encoding='utf-8') as f:
                f.write(f"# Model Comparison: {file_stem}\n\n")
                f.write(f"**Source:** `{file_path}`\n")
                f.write(f"**Template:** {template.value.title()}\n")
                f.write(f"**Compared:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for provider, analysis in results.items():
                    f.write(f"## {provider.upper()} Analysis\n\n")
                    
                    # Summary
                    f.write("### Summary\n\n")
                    f.write(analysis.get("summary", "No summary available"))
                    f.write("\n\n")
                    
                    # Key concepts
                    if analysis.get("key_concepts"):
                        f.write("### Key Concepts\n\n")
                        for concept in analysis["key_concepts"]:
                            f.write(f"- {concept}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")
            
            console.print(f"[green]✓ Comparison saved to {comparison_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error saving comparison: {e}[/red]")

    def query_documents(self, question: str, provider: ModelProvider = ModelProvider.CLAUDE) -> str:
        """Query documents using specified AI provider."""
        if not self.documents:
            return "No documents have been ingested yet. Use 'ingest' command first."
        
        # Combine all document content
        all_text = "\n\n---DOCUMENT SEPARATOR---\n\n".join(
            f"From {path}:\n{doc['content']}" 
            for path, doc in self.documents.items()
        )
        
        # Truncate if too long
        max_chars = 50000
        if len(all_text) > max_chars:
            all_text = all_text[:max_chars] + "\n\n[Content truncated...]"
        
        system_prompt = """You are a helpful research assistant. Answer questions based on the provided context."""
        user_content = f"Context:\n{all_text}\n\nQuestion: {question}"

        try:
            if provider == ModelProvider.CLAUDE and self.anthropic:
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
                    progress.add_task(description="Getting answer from Claude...", total=None)
                    message = self.anthropic.messages.create(
                        model=self.default_model,
                        max_tokens=1000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_content}]
                    )
                return message.content[0].text
                
            elif provider == ModelProvider.OPENAI and self.openai_client:
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
                    progress.add_task(description="Getting answer from OpenAI...", total=None)
                    response = self.openai_client.chat.completions.create(
                        model=self.openai_model,
                        max_tokens=1000,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ]
                    )
                return response.choices[0].message.content
            else:
                return f"Provider {provider.value} not available."
                
        except Exception as e:
            return f"Error: {e}"

    def save_data(self):
        """Save documents and summaries to persistent storage."""
        data = {
            "documents": self.documents,
            "summaries": self.summaries,
            "last_updated": datetime.now().isoformat()
        }
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving data: {e}[/red]")

    def load_data(self):
        """Load documents and summaries from persistent storage."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get("documents", {})
                    self.summaries = data.get("summaries", {})
                console.print(f"[green]✓ Loaded {len(self.documents)} documents from storage[/green]")
            except Exception as e:
                console.print(f"[red]Error loading data: {e}[/red]")
                self.documents = {}
                self.summaries = {}


# CLI Application
app = typer.Typer(help="Enhanced Local Doc-Whisperer: Multi-model AI document analysis")

@app.command()
def ingest(
    path: str = typer.Argument(..., help="Path to document to process"),
    provider: ModelProvider = typer.Option(ModelProvider.CLAUDE, help="AI provider to use"),
    template: PromptTemplate = typer.Option(PromptTemplate.RESEARCH, help="Prompt template to use")
):
    """Ingest documents with specified AI provider and prompt template."""
    doc_whisperer = EnhancedDocWhisperer()
    success = doc_whisperer.ingest_document(path, provider, template)
    if success:
        console.print(f"\n[bold green]✓ Successfully processed {path}[/bold green]")
    else:
        console.print(f"\n[bold red]✗ Failed to process {path}[/bold red]")

@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask about your documents"),
    provider: ModelProvider = typer.Option(ModelProvider.CLAUDE, help="AI provider to use")
):
    """Ask a question using specified AI provider."""
    doc_whisperer = EnhancedDocWhisperer()
    answer = doc_whisperer.query_documents(question, provider)
    
    console.print()
    console.print(Panel(
        Markdown(answer),
        title=f"Answer ({provider.value.upper()})",
        border_style="blue"
    ))

@app.command()
def compare(
    file_path: str = typer.Argument(..., help="Path to document to compare"),
    template: PromptTemplate = typer.Option(PromptTemplate.RESEARCH, help="Prompt template to use")
):
    """Compare Claude and OpenAI responses for a document."""
    doc_whisperer = EnhancedDocWhisperer()
    results = doc_whisperer.compare_models(file_path, template)
    
    if "error" in results:
        console.print(f"[red]Error: {results['error']}[/red]")
        return
    
    # Display comparison
    console.print()
    for provider, analysis in results.items():
        console.print(Panel(
            f"**Summary:** {analysis.get('summary', 'No summary')[:200]}...\n\n"
            f"**Key Concepts:** {', '.join(analysis.get('key_concepts', [])[:3])}",
            title=f"{provider.upper()} Analysis",
            border_style="green" if provider == "claude" else "yellow"
        ))

@app.command()
def list_docs():
    """List all documents in the knowledge base."""
    doc_whisperer = EnhancedDocWhisperer()
    documents = list(doc_whisperer.documents.keys())
    
    if documents:
        console.print("\n[bold blue]Documents in knowledge base:[/bold blue]")
        for i, doc in enumerate(documents, 1):
            doc_info = doc_whisperer.documents[doc]
            console.print(f"{i:2d}. {doc} ({doc_info['file_size']:,} chars)")
    else:
        console.print("[yellow]No documents found in knowledge base.[/yellow]")

if __name__ == "__main__":
    app() 