# 🧠 Local Doc-Whisperer

A tiny Python CLI that digests any PDF, text file, or Markdown note you drop into a folder, asks Claude 4 for a concise summary plus three flash-card questions, and stores both the embeddings and the AI output in a lightweight ChromaDB vector database so you can later ask follow-up questions offline.

![Demo](https://img.shields.io/badge/Status-Ready%20to%20Use-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Why This Project?

### Perfect First Project for AI Development

- **Single-script simplicity**: Everything runs from one `main.py`; the only external service is the Anthropic HTTPS endpoint
- **Long-context proof-point**: Claude's 200k-token window means you can feed entire research papers in one go
- **Local privacy & speed**: Storing vectors in ChromaDB keeps all embeddings on disk; only raw text goes to Claude
- **Future-proof with MCP**: Can be upgraded to a full Model Context Protocol endpoint later

## 🏗️ Architecture

```
┌───────────────┐        ┌───────────────┐        ┌───────────────────────┐
│  Drop Zone    │──TXT──▶│ Chunker &     │──JSON─▶│ Claude 4 API (stream) │
│  /docs_in     │        │ Embed/Store   │◀─EMB──│  (summary + quiz)      │
└───────────────┘        └───────────────┘        └───────────────┬───────┘
                                          │ markdown output       │
                                          ▼                       ▼
                               local_chroma.db            summaries/*.md
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- [Anthropic API key](https://docs.anthropic.com/en/docs/get-started) (get one from the Anthropic Console)

### 2. Installation

```bash
# Clone or download this project
git clone <your-repo-url>
cd local-doc-whisperer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Usage

#### Ingest Documents

```bash
# Process a single document
python main.py ingest docs_in/my_paper.pdf

# Process all documents in a directory
python main.py ingest docs_in/

# Process recursively through subdirectories
python main.py ingest docs_in/ --recursive
```

#### Ask Questions

```bash
# Ask a specific question
python main.py ask "What are the three key findings?"

# Start interactive session
python main.py interactive

# List ingested documents
python main.py list-docs
```

## 📁 File Structure

```
local-doc-whisperer/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
├── docs_in/            # Drop documents here for processing
├── summaries/          # Generated summaries and quizzes (Markdown)
├── chroma_db/          # Vector database (auto-created)
└── README.md           # This file
```

## 🎯 Features

### Document Processing
- **PDF extraction**: Uses `pdfplumber` for accurate text extraction
- **Multiple formats**: Supports PDF, TXT, MD, and Markdown files
- **Smart chunking**: Splits large documents into 3.5k-token chunks with overlap
- **Metadata tracking**: Preserves source information and page numbers

### AI-Powered Analysis
- **Intelligent summaries**: 150-word concise summaries using Claude
- **Quiz generation**: Three Q&A flashcards for self-study
- **Citation tracking**: Source locations for each answer
- **JSON structured output**: Consistent, parseable responses

### Vector Search
- **Local storage**: ChromaDB for fast, offline vector search
- **Semantic search**: Find relevant chunks using natural language queries
- **Privacy-first**: No data leaves your machine except API calls to Claude
- **Persistent database**: Data survives between sessions

### User Experience
- **Beautiful CLI**: Rich terminal output with colors and progress bars
- **Interactive mode**: Conversational Q&A sessions
- **Batch processing**: Handle multiple documents at once
- **Error handling**: Graceful fallbacks and informative error messages

## 🔧 Command Reference

### Ingest Command
```bash
python main.py ingest [PATH] [OPTIONS]

Arguments:
  PATH    Path to document or directory to process

Options:
  -r, --recursive    Process directories recursively
  --help            Show help message
```

### Ask Command
```bash
python main.py ask "Your question here"

# Examples:
python main.py ask "What are the main conclusions?"
python main.py ask "How does this relate to previous research?"
python main.py ask "What methodology was used?"
```

### Interactive Mode
```bash
python main.py interactive

# Special commands in interactive mode:
# - Type 'list' to see available documents
# - Type 'quit', 'exit', or 'q' to end session
# - Ctrl+C to exit
```

### List Documents
```bash
python main.py list-docs
```

## ⚙️ Configuration

Edit your `.env` file to customize behavior:

```bash
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=your_key_here

# Optional: Model selection (default: claude-3-sonnet-20240229)
DEFAULT_MODEL=claude-3-opus-20240229

# Optional: Vector database location (default: ./chroma_db)
CHROMA_PERSIST_DIR=./chroma_db

# Optional: Text chunking settings
CHUNK_SIZE=3500
CHUNK_OVERLAP=100
```

## 🔍 Example Workflow

1. **Add documents to process:**
   ```bash
   # Copy your PDFs/text files to docs_in/
   cp ~/Downloads/research_paper.pdf docs_in/
   cp ~/Notes/*.md docs_in/
   ```

2. **Ingest them:**
   ```bash
   python main.py ingest docs_in/
   ```
   
   This will:
   - Extract text from each document
   - Create vector embeddings
   - Generate summaries with flashcard questions
   - Save everything locally

3. **Ask questions:**
   ```bash
   python main.py ask "What is the main hypothesis?"
   
   # Or start interactive mode
   python main.py interactive
   ```

4. **Review summaries:**
   Check the `summaries/` folder for generated Markdown files with summaries and quiz questions.

## 🚀 Extension Ideas

Once you have the basic version working, consider these enhancements:

| Extension | Skills You'll Learn | Implementation Notes |
|-----------|-------------------|---------------------|
| **Tool-calling** | JSON schema & argument parsing | Auto-open PDFs when Claude suggests "see appendix" |
| **MCP wrapper** | HTTP routing, protocol compliance | Let other apps subscribe to your vector store |
| **GUI dashboard** | Web frameworks | Streamlit app showing summaries & similarity scores |
| **Auto-scheduler** | File watching, cron jobs | Re-index changed files nightly |
| **Obsidian sync** | File system APIs | Export to personal knowledge graphs |
| **Multi-model support** | API abstraction | Compare Claude vs GPT-4 vs local models |

## 🐛 Troubleshooting

### Token Limits
- Even with 200k context, PDFs >150k tokens may need chunk summarization first
- Switch from Opus to Sonnet for bulk ingestion to save costs

### Rate Limits
- Free tier has lower rate limits - add delays between requests if needed
- Consider upgrading to paid tier for heavy usage

### Performance
- ChromaDB runs fine on CPU for <100k embeddings
- For larger datasets, consider GPU acceleration or FAISS alternative

### Common Issues

**"No API key found"**
```bash
# Make sure you've copied env.example to .env and added your key
cp env.example .env
# Edit .env with your actual API key
```

**"No text extracted from PDF"**
- Some PDFs are image-based and need OCR
- Try using a different PDF or converting to text first

**"Vector database errors"**
- Delete `chroma_db/` folder and restart to reset database
- Check file permissions in the project directory

## 🤝 Contributing

This is a learning project! Feel free to:
- Add support for more file formats
- Improve the summarization prompts
- Add new CLI commands
- Create a web interface
- Add tests and documentation

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Anthropic](https://docs.anthropic.com/en/docs/get-started) for the Claude API
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [Typer](https://typer.tiangolo.com/) for the CLI framework

---

**Happy hacking!** 🚀 In just a couple hundred lines of code, you'll have hands-on experience with the Anthropic SDK, long-context reasoning, and a privacy-respecting local knowledge base that you can grow at your own pace. 