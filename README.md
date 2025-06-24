# 🧠 Doc-Whisperer

> **Enhanced Multi-Model AI Document Analysis Platform with Modern 2025 UI/UX Design**

[![GitHub stars](https://img.shields.io/github/stars/swilliams9772/local-doc-whisperer?style=social)](https://github.com/swilliams9772/local-doc-whisperer/stargazers)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Doc-Whisperer is a cutting-edge document analysis platform that combines the power of AI language models (Claude & OpenAI) with a stunning modern web interface. Built with glassmorphism design principles and 2025 UI/UX trends, it offers an intuitive and beautiful way to interact with your documents.

## 🎨 Visual Showcase

### ✨ Modern Interface Design

<table>
<tr>
<td align="center">
<img src="assets/screenshots/dashboard-desktop.png" alt="Desktop Dashboard" width="400"/>
<br/><strong>Desktop Interface</strong>
<br/>Glassmorphism design with animated statistics
</td>
<td align="center">
<img src="assets/screenshots/dashboard-mobile.png" alt="Mobile Dashboard" width="200"/>
<br/><strong>Mobile Responsive</strong>
<br/>Perfect adaptation to all screen sizes
</td>
</tr>
</table>

### 🎬 Live Demonstrations

<table>
<tr>
<td align="center">
<img src="assets/gifs/document-ingestion-flow.gif" alt="Document Ingestion Demo" width="400"/>
<br/><strong>Document Ingestion Flow</strong>
<br/>Smooth upload process with beautiful feedback
</td>
<td align="center">
<img src="assets/gifs/qa-demo.gif" alt="Q&A Demo" width="400"/>
<br/><strong>AI-Powered Q&A</strong>
<br/>Interactive question answering with real-time responses
</td>
</tr>
</table>

<table>
<tr>
<td align="center">
<img src="assets/gifs/hover-effects.gif" alt="Hover Effects Demo" width="300"/>
<br/><strong>Micro-Interactions</strong>
<br/>Smooth hover effects and transitions
</td>
<td align="center">
<img src="assets/gifs/stats-animation.gif" alt="Statistics Animation" width="300"/>
<br/><strong>Animated Statistics</strong>
<br/>Live counting animations for engagement
</td>
<td align="center">
<img src="assets/gifs/responsive-demo.gif" alt="Responsive Demo" width="300"/>
<br/><strong>Responsive Design</strong>
<br/>Seamless layout adaptation
</td>
</tr>
</table>

> 📸 **Note**: Screenshots and GIFs are being captured to showcase the beautiful interface. See [VISUAL_ASSETS_GUIDE.md](VISUAL_ASSETS_GUIDE.md) for detailed capture instructions.

## ✨ Key Features

### 🎨 **Modern 2025 UI/UX Design**
- **Glassmorphism Effects**: Beautiful frosted glass cards with backdrop blur
- **Responsive Grid Layout**: Advanced CSS Grid with mobile-first design
- **Smooth Animations**: Micro-interactions and seamless transitions
- **Professional Typography**: Inter font family with perfect spacing
- **Animated Statistics**: Live counting animations for engagement
- **Modern Form Controls**: Glass-style inputs with floating labels

### 🤖 **AI-Powered Analysis**
- **Multi-Model Support**: Claude (Anthropic) and OpenAI GPT integration
- **Document Ingestion**: Automatic processing and vectorization
- **Intelligent Q&A**: Context-aware question answering
- **Multiple Templates**: Research, Educational, Business, and Creative analysis modes
- **Vector Database**: ChromaDB integration for efficient document retrieval

### 🛠 **Technical Excellence**
- **Python Backend**: Clean, maintainable HTTP server implementation
- **Real-time Updates**: Live statistics and document library updates
- **Error Handling**: Comprehensive error states with user-friendly feedback
- **Accessibility**: WCAG compliant with keyboard navigation support
- **Performance**: Optimized animations and efficient API calls

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- API keys for Claude or OpenAI

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/swilliams9772/local-doc-whisperer.git
   cd local-doc-whisperer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp env.example .env
   # Edit .env file with your API keys
   ```

5. **Run the application**
   ```bash
   python web_app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000` to experience the modern interface!

## 📱 Interface Preview

The new 2025 UI features:

- **Dashboard**: Live statistics with animated counters
- **Document Ingestion**: Modern file upload with progress indicators
- **AI Chat Interface**: Beautiful question/answer cards with metadata
- **Document Library**: Visual document management with icons
- **Responsive Design**: Perfect on desktop, tablet, and mobile

## 🎯 Usage Examples

### Web Interface
1. **Ingest Documents**: Upload your documents using the beautiful drag-and-drop interface
2. **Ask Questions**: Use the AI-powered Q&A system with real-time responses
3. **View Analytics**: Monitor your document library with live statistics
4. **Export Results**: Download analysis results in multiple formats

### CLI Interface
```bash
# Interactive mode
python main_minimal.py interactive

# Process single document
python main_enhanced.py process document.pdf --provider claude

# Bulk processing
python advanced_demo.py --batch-process docs/
```

## 🏗 Architecture

```
Doc-Whisperer/
├── 🎨 Frontend (Modern UI/UX)
│   ├── Glassmorphism Design
│   ├── Responsive Grid Layout
│   └── Smooth Animations
├── 🧠 AI Integration
│   ├── Claude (Anthropic)
│   ├── OpenAI GPT
│   └── Multi-Model Support
├── 📊 Vector Database
│   ├── ChromaDB Storage
│   ├── Efficient Retrieval
│   └── Semantic Search
└── 🛠 Backend Services
    ├── HTTP Server
    ├── Document Processing
    └── API Endpoints
```

## 🎨 Design System

The interface follows modern design principles:

- **Color Palette**: Custom CSS properties with glassmorphism effects
- **Typography**: Inter font family with proper hierarchy
- **Spacing**: Consistent 8px grid system
- **Components**: Reusable glass cards and modern buttons
- **Animations**: 60fps smooth transitions with cubic-bezier easing
- **Accessibility**: High contrast modes and keyboard navigation

## 🔧 Configuration

### API Providers
Configure your preferred AI models in `.env`:

```env
ANTHROPIC_API_KEY=your_claude_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Analysis Templates
Choose from multiple analysis modes:
- **Research**: Academic and scientific documents
- **Educational**: Learning materials and textbooks
- **Business**: Reports, proposals, and presentations
- **Creative**: Marketing content and creative writing

## 📸 Contributing Visual Assets

We welcome contributions of screenshots and demo GIFs! See our [Visual Assets Guide](VISUAL_ASSETS_GUIDE.md) for detailed instructions on capturing and optimizing visual content.

### Quick Capture Checklist:
- [ ] **Screenshots**: Dashboard, mobile view, forms, interactions
- [ ] **GIFs**: Loading animations, user flows, hover effects
- [ ] **Optimization**: Compress images and optimize GIF file sizes
- [ ] **Naming**: Follow the established naming convention

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI capabilities
- **OpenAI** for GPT integration
- **ChromaDB** for vector database functionality
- **Inter Font** for beautiful typography
- Modern UI/UX inspiration from leading design systems

## 📞 Support

- 📧 **Email**: [support@doc-whisperer.com](mailto:support@doc-whisperer.com)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/swilliams9772/local-doc-whisperer/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/swilliams9772/local-doc-whisperer/issues)

---

<p align="center">
  <strong>Built with ❤️ and modern web technologies</strong><br>
  <em>Bringing AI document analysis into 2025</em>
</p> 