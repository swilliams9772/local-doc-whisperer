#!/usr/bin/env python3
"""
Advanced Doc-Whisperer Demo: Showcasing Enhanced Features
Demonstrates: Multi-model support, prompt templates, persistent storage, complex analysis
"""

import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import track

from main_enhanced import EnhancedDocWhisperer, ModelProvider, PromptTemplate

console = Console()

def display_banner():
    """Display the demo banner."""
    banner_text = """
# 🚀 Advanced Doc-Whisperer Demo

## Enhanced Features Showcase:
- 🤖 **Multi-Model Support**: Claude vs OpenAI comparison
- 📝 **Smart Prompt Templates**: Research, Educational, Business, Creative
- 💾 **Persistent Storage**: JSON-based document management
- 🔍 **Advanced Q&A**: Complex reasoning and analysis
- 🌐 **Web Interface**: Beautiful HTML dashboard
- 📊 **Analytics**: Document statistics and insights
    """
    
    console.print(Panel(
        Markdown(banner_text),
        title="🧠 Doc-Whisperer Advanced Demo",
        border_style="bold blue",
        padding=(1, 2)
    ))

def demonstrate_prompt_templates():
    """Demonstrate different prompt templates on the same document."""
    console.print("\n[bold blue]🎯 Prompt Template Demonstration[/bold blue]")
    
    doc_whisperer = EnhancedDocWhisperer()
    document_path = "docs_in/sample_document.md"
    
    templates = [
        (PromptTemplate.RESEARCH, "🔬 Research Analysis"),
        (PromptTemplate.EDUCATIONAL, "🎓 Educational Focus"),
        (PromptTemplate.BUSINESS, "💼 Business Perspective"),
        (PromptTemplate.CREATIVE, "🎨 Creative Interpretation")
    ]
    
    console.print("Analyzing the same document with different prompt templates...\n")
    
    for template, description in track(templates, description="Processing templates..."):
        console.print(f"\n[yellow]{description}[/yellow]")
        
        # Generate analysis with specific template
        text = doc_whisperer.extract_text(document_path)
        analysis = doc_whisperer.generate_analysis(text, document_path, ModelProvider.CLAUDE, template)
        
        # Display key concepts for this template
        concepts = analysis.get('key_concepts', [])
        if concepts:
            console.print(f"[dim]Key Concepts:[/dim] {', '.join(concepts[:3])}...")
        
        # Show part of summary
        summary = analysis.get('summary', '')
        console.print(f"[dim]Summary Preview:[/dim] {summary[:100]}...")
        
        time.sleep(1)  # Brief pause for effect

def demonstrate_complex_analysis():
    """Demonstrate Claude's advanced analysis capabilities."""
    console.print("\n[bold blue]🧠 Advanced Analysis Capabilities[/bold blue]")
    
    doc_whisperer = EnhancedDocWhisperer()
    
    # Complex questions that test different types of reasoning
    complex_questions = [
        ("Synthesis", "How do the benefits and challenges of AI in education create a complex ecosystem that requires careful balance?"),
        ("Prediction", "Based on current trends mentioned in the document, what educational paradigm shifts might we see in 5-10 years?"),
        ("Critical Analysis", "What are the potential unintended consequences of widespread AI adoption in education?"),
        ("Comparative", "How might AI's impact on education differ between developed and developing countries?"),
        ("Ethical Reasoning", "What ethical frameworks should guide AI implementation in educational settings?")
    ]
    
    for category, question in complex_questions:
        console.print(f"\n[yellow]📋 {category} Question:[/yellow]")
        console.print(f"[dim]{question}[/dim]")
        
        # Get Claude's response
        answer = doc_whisperer.query_documents(question, ModelProvider.CLAUDE)
        
        # Display shortened response
        preview = answer[:200] + "..." if len(answer) > 200 else answer
        console.print(Panel(
            preview,
            title=f"Claude's {category} Response",
            border_style="green",
            width=80
        ))
        
        time.sleep(2)  # Pause between questions

def demonstrate_persistence():
    """Demonstrate persistent storage capabilities."""
    console.print("\n[bold blue]💾 Persistent Storage Demo[/bold blue]")
    
    doc_whisperer = EnhancedDocWhisperer()
    
    # Show storage statistics
    stats = {
        "total_documents": len(doc_whisperer.documents),
        "total_characters": sum(doc["file_size"] for doc in doc_whisperer.documents.values()),
        "storage_file_size": Path("doc_whisperer_data.json").stat().st_size if Path("doc_whisperer_data.json").exists() else 0
    }
    
    table = Table(title="📊 Storage Statistics")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Documents", str(stats["total_documents"]))
    table.add_row("Total Characters", f"{stats['total_characters']:,}")
    table.add_row("Storage File Size", f"{stats['storage_file_size']:,} bytes")
    
    console.print(table)
    
    # Show document list
    if doc_whisperer.documents:
        console.print("\n[green]📚 Documents in Knowledge Base:[/green]")
        for i, (path, info) in enumerate(doc_whisperer.documents.items(), 1):
            console.print(f"  {i}. {path} ({info['file_size']:,} chars)")

def demonstrate_file_outputs():
    """Show the different files created by the system."""
    console.print("\n[bold blue]📁 Generated Files Overview[/bold blue]")
    
    # Check summaries directory
    summaries_dir = Path("summaries")
    if summaries_dir.exists():
        summaries = list(summaries_dir.glob("*.md"))
        console.print(f"[green]📄 Summary Files Generated:[/green] {len(summaries)}")
        for summary in summaries[:3]:  # Show first 3
            console.print(f"  • {summary.name}")
    
    # Check comparisons directory
    comparisons_dir = Path("comparisons")
    if comparisons_dir.exists():
        comparisons = list(comparisons_dir.glob("*.md"))
        console.print(f"[yellow]⚖️  Comparison Files:[/yellow] {len(comparisons)}")
        for comparison in comparisons[:2]:  # Show first 2
            console.print(f"  • {comparison.name}")
    
    # Check storage file
    storage_file = Path("doc_whisperer_data.json")
    if storage_file.exists():
        console.print(f"[blue]💾 Persistent Storage:[/blue] {storage_file.name} ({storage_file.stat().st_size:,} bytes)")

def show_feature_comparison():
    """Show comparison between minimal and enhanced versions."""
    console.print("\n[bold blue]🔄 Feature Comparison[/bold blue]")
    
    comparison_table = Table(title="📋 Minimal vs Enhanced Features")
    comparison_table.add_column("Feature", style="cyan", no_wrap=True)
    comparison_table.add_column("Minimal Version", style="yellow")
    comparison_table.add_column("Enhanced Version", style="green")
    
    features = [
        ("AI Providers", "Claude only", "Claude + OpenAI"),
        ("Prompt Templates", "Fixed prompts", "4 customizable templates"),
        ("Storage", "In-memory only", "Persistent JSON storage"),
        ("Web Interface", "CLI only", "Beautiful web dashboard"),
        ("Analysis Depth", "Basic summaries", "Advanced reasoning"),
        ("Model Comparison", "Not available", "Side-by-side comparison"),
        ("File Formats", "Text/Markdown", "Extensible architecture"),
        ("Output Options", "Single format", "Multiple formats")
    ]
    
    for feature, minimal, enhanced in features:
        comparison_table.add_row(feature, minimal, enhanced)
    
    console.print(comparison_table)

def show_next_steps():
    """Show potential next steps and improvements."""
    console.print("\n[bold blue]🚀 Potential Enhancements[/bold blue]")
    
    next_steps = """
## 🔮 Future Enhancements

### Technical Improvements
- **Vector Database**: ChromaDB/FAISS for semantic search
- **PDF Support**: Advanced PDF parsing with images/tables
- **Batch Processing**: Parallel document processing
- **API Server**: RESTful API for integration

### AI Capabilities
- **Model Comparison**: A/B testing framework
- **Custom Fine-tuning**: Domain-specific models
- **Multi-modal**: Image and video analysis
- **Real-time**: Streaming analysis

### User Experience
- **Streamlit Dashboard**: Professional web interface
- **Mobile App**: Cross-platform mobile access
- **Collaboration**: Multi-user knowledge bases
- **Visualization**: Interactive data exploration

### Enterprise Features
- **Authentication**: User management and access control
- **Audit Logs**: Comprehensive activity tracking
- **Integration**: Slack, Teams, email notifications
- **Scaling**: Distributed processing architecture
    """
    
    console.print(Panel(
        Markdown(next_steps),
        title="🎯 Roadmap",
        border_style="magenta"
    ))

def main():
    """Run the complete advanced demo."""
    console.clear()
    display_banner()
    
    # Wait for user to read
    console.input("\n[dim]Press Enter to start the demonstration...[/dim]")
    
    # Run all demonstrations
    demonstrate_prompt_templates()
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    demonstrate_complex_analysis()
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    demonstrate_persistence()
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    demonstrate_file_outputs()
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    show_feature_comparison()
    console.input("\n[dim]Press Enter to see future enhancements...[/dim]")
    
    show_next_steps()
    
    # Final summary
    console.print("\n" + "="*80)
    console.print(Panel(
        "[bold green]🎉 Demo Complete![/bold green]\n\n"
        "You've seen the enhanced Doc-Whisperer with:\n"
        "✅ Multi-model AI support\n"
        "✅ Advanced prompt engineering\n"
        "✅ Persistent storage\n"
        "✅ Complex reasoning capabilities\n"
        "✅ Beautiful web interface\n"
        "✅ Professional documentation\n\n"
        "[dim]The web interface is still running at http://localhost:8000[/dim]",
        title="🧠 Enhanced Doc-Whisperer",
        border_style="bold green"
    ))

if __name__ == "__main__":
    main() 