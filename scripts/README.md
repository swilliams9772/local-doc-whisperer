# 🛠 Scripts Directory

This directory contains helper scripts for the Doc-Whisperer project.

## 📸 capture_assets.py

An interactive Python script to help capture screenshots and demo GIFs for showcasing the modern UI/UX design.

### Features:
- **Guided Capture**: Step-by-step instructions for screenshots and GIFs
- **Tool Checking**: Verifies if recommended capture tools are installed
- **Browser Automation**: Opens the correct URLs for capture
- **Asset Organization**: Automatically organizes files in the correct directories
- **Optimization Tips**: Provides guidance on compressing and optimizing assets
- **README Integration**: Generates markdown snippets for the README

### Usage:

```bash
# Run interactive guided session
python scripts/capture_assets.py

# Capture only screenshots
python scripts/capture_assets.py screenshots

# Capture only GIFs
python scripts/capture_assets.py gifs

# Check asset optimization
python scripts/capture_assets.py optimize

# Generate README snippets
python scripts/capture_assets.py snippets
```

### Prerequisites:
- Web server running (`python web_app.py`)
- `rich` library installed (`pip install rich requests`)
- Recommended tools:
  - **Kap**: `brew install --cask kap` (for GIFs)
  - **ImageOptim**: `brew install --cask imageoptim` (for optimization)

### Output Structure:
```
assets/
├── screenshots/
│   ├── dashboard-desktop.png
│   ├── dashboard-mobile.png
│   ├── document-ingestion.png
│   ├── qa-interface.png
│   ├── document-library.png
│   └── hover-states.png
└── gifs/
    ├── homepage-loading.gif
    ├── document-ingestion-flow.gif
    ├── qa-demo.gif
    ├── hover-effects.gif
    ├── responsive-demo.gif
    └── stats-animation.gif
```

### Tips:
- Start the web server before running the script
- Ensure you have documents ingested for better screenshots
- Use consistent browser zoom (100%) for all captures
- Keep GIF file sizes under 10MB for GitHub compatibility 