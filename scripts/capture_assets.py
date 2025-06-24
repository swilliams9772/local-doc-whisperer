#!/usr/bin/env python3
"""
Visual Assets Capture Helper Script
Helps guide the process of capturing screenshots and GIFs for Doc-Whisperer
"""

import os
import sys
import webbrowser
import time
from pathlib import Path
import subprocess
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

class AssetsCaptureHelper:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.assets_dir = Path("assets")
        self.screenshots_dir = self.assets_dir / "screenshots"
        self.gifs_dir = self.assets_dir / "gifs"
        
        # Create directories if they don't exist
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.gifs_dir.mkdir(parents=True, exist_ok=True)
        
    def check_server_running(self):
        """Check if the web server is running"""
        try:
            import requests
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def open_browser_for_capture(self, path=""):
        """Open browser at the specified path for capture"""
        url = f"{self.base_url}{path}"
        webbrowser.open(url)
        console.print(f"🌐 Opened: {url}")
        
    def show_screenshot_guide(self):
        """Display screenshot capture guide"""
        table = Table(title="📸 Screenshot Capture Guide")
        table.add_column("Asset", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("File Name", style="green")
        table.add_column("Dimensions", style="yellow")
        
        screenshots = [
            ("Dashboard Desktop", "Full homepage with glassmorphism design", "dashboard-desktop.png", "1400x900"),
            ("Dashboard Mobile", "Mobile responsive view", "dashboard-mobile.png", "375x812"),
            ("Document Ingestion", "Ingestion form section", "document-ingestion.png", "800x600"),
            ("Q&A Interface", "Question and answer section", "qa-interface.png", "800x600"),
            ("Document Library", "Document management section", "document-library.png", "800x400"),
            ("Hover States", "Interactive elements in action", "hover-states.png", "800x600"),
        ]
        
        for asset, desc, filename, dims in screenshots:
            table.add_row(asset, desc, filename, dims)
        
        console.print(table)
        
        # macOS screenshot instructions
        console.print("\n🖥️  macOS Screenshot Shortcuts:", style="bold blue")
        console.print("• Full screen: cmd + shift + 3")
        console.print("• Selected area: cmd + shift + 4")
        console.print("• Specific window: cmd + shift + 4 + spacebar")
        
    def show_gif_guide(self):
        """Display GIF capture guide"""
        table = Table(title="🎬 GIF Capture Guide")
        table.add_column("Demo", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("File Name", style="green")
        table.add_column("Duration", style="yellow")
        
        gifs = [
            ("Homepage Loading", "Page load with staggered animations", "homepage-loading.gif", "3-4s"),
            ("Document Ingestion", "Complete upload process", "document-ingestion-flow.gif", "8-10s"),
            ("Q&A Demo", "Question and answer flow", "qa-demo.gif", "10-12s"),
            ("Hover Effects", "Micro-interactions showcase", "hover-effects.gif", "5-6s"),
            ("Responsive Demo", "Layout adaptation", "responsive-demo.gif", "6-8s"),
            ("Stats Animation", "Number counting animations", "stats-animation.gif", "3-4s"),
        ]
        
        for demo, desc, filename, duration in gifs:
            table.add_row(demo, desc, filename, duration)
        
        console.print(table)
        
        # GIF recording tools
        console.print("\n🎥 Recommended GIF Tools:", style="bold blue")
        console.print("• Kap (macOS): brew install --cask kap")
        console.print("• LICEcap (Cross-platform): https://www.cockos.com/licecap/")
        console.print("• Settings: 30fps, <10MB file size, optimize for web")
        
    def check_tools(self):
        """Check if recommended tools are installed"""
        tools_status = []
        
        # Check for Kap
        try:
            result = subprocess.run(["which", "kap"], capture_output=True, text=True)
            kap_installed = result.returncode == 0
        except:
            kap_installed = False
        
        tools_status.append(("Kap (GIF Recorder)", "✅" if kap_installed else "❌", "brew install --cask kap"))
        
        # Check for ImageOptim
        try:
            result = subprocess.run(["which", "imageoptim"], capture_output=True, text=True)
            imageoptim_installed = result.returncode == 0
        except:
            imageoptim_installed = False
        
        tools_status.append(("ImageOptim", "✅" if imageoptim_installed else "❌", "brew install --cask imageoptim"))
        
        # Display tools status
        table = Table(title="🛠️  Tools Status")
        table.add_column("Tool", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Install Command", style="green")
        
        for tool, status, install_cmd in tools_status:
            table.add_row(tool, status, install_cmd)
        
        console.print(table)
        
    def guided_capture_session(self):
        """Run a guided capture session"""
        console.print(Panel.fit("🎨 Doc-Whisperer Visual Assets Capture Session", style="bold blue"))
        
        # Check if server is running
        if not self.check_server_running():
            console.print("❌ Web server is not running!", style="bold red")
            console.print("Please start the server with: python web_app.py")
            return
        
        console.print("✅ Web server is running!", style="bold green")
        
        # Show tools status
        self.check_tools()
        
        # Choose what to capture
        capture_type = Prompt.ask(
            "\nWhat would you like to capture?",
            choices=["screenshots", "gifs", "both", "guide-only"],
            default="both"
        )
        
        if capture_type in ["screenshots", "both"]:
            self.capture_screenshots()
        
        if capture_type in ["gifs", "both"]:
            self.capture_gifs()
        
        if capture_type == "guide-only":
            self.show_screenshot_guide()
            console.print("\n")
            self.show_gif_guide()
    
    def capture_screenshots(self):
        """Guide through screenshot capture"""
        console.print("\n📸 Starting Screenshot Capture Session", style="bold cyan")
        self.show_screenshot_guide()
        
        screenshots = [
            ("Desktop Dashboard", "", "dashboard-desktop.png", "Desktop view (1400px wide)"),
            ("Mobile Dashboard", "", "dashboard-mobile.png", "Mobile view (375px wide)"),
            ("Document Ingestion", "", "document-ingestion.png", "Focus on ingestion form"),
            ("Q&A Interface", "", "qa-interface.png", "Focus on Q&A section"),
            ("Document Library", "", "document-library.png", "Focus on document list"),
        ]
        
        for name, path, filename, instructions in screenshots:
            if Confirm.ask(f"\n📷 Capture {name}?"):
                console.print(f"\n🎯 Instructions: {instructions}")
                self.open_browser_for_capture(path)
                
                # Wait for user to capture
                Prompt.ask("Press Enter after capturing the screenshot...")
                
                # Check if file exists
                filepath = self.screenshots_dir / filename
                if filepath.exists():
                    console.print(f"✅ Found: {filepath}", style="green")
                else:
                    console.print(f"⚠️  File not found: {filepath}", style="yellow")
                    console.print("Make sure to save the screenshot with the correct filename")
    
    def capture_gifs(self):
        """Guide through GIF capture"""
        console.print("\n🎬 Starting GIF Capture Session", style="bold cyan")
        self.show_gif_guide()
        
        gifs = [
            ("Homepage Loading", "Refresh page and record loading animations", "homepage-loading.gif"),
            ("Document Ingestion", "Record complete document upload process", "document-ingestion-flow.gif"),
            ("Q&A Demo", "Record asking a question and getting response", "qa-demo.gif"),
            ("Hover Effects", "Record hovering over various UI elements", "hover-effects.gif"),
            ("Stats Animation", "Record statistics counting animation", "stats-animation.gif"),
        ]
        
        for name, instructions, filename in gifs:
            if Confirm.ask(f"\n🎥 Capture {name}?"):
                console.print(f"\n🎬 Instructions: {instructions}")
                self.open_browser_for_capture()
                
                console.print("🔴 Start recording now...")
                Prompt.ask("Press Enter after finishing the recording...")
                
                # Check if file exists
                filepath = self.gifs_dir / filename
                if filepath.exists():
                    console.print(f"✅ Found: {filepath}", style="green")
                else:
                    console.print(f"⚠️  File not found: {filepath}", style="yellow")
                    console.print("Make sure to save the GIF with the correct filename")
    
    def optimize_assets(self):
        """Guide through asset optimization"""
        console.print("\n🎨 Asset Optimization", style="bold cyan")
        
        # Check for images to optimize
        screenshots = list(self.screenshots_dir.glob("*.png"))
        gifs = list(self.gifs_dir.glob("*.gif"))
        
        if screenshots:
            console.print(f"\n📸 Found {len(screenshots)} screenshots to optimize")
            for img in screenshots:
                size_mb = img.stat().st_size / (1024 * 1024)
                console.print(f"  • {img.name}: {size_mb:.1f}MB")
        
        if gifs:
            console.print(f"\n🎬 Found {len(gifs)} GIFs to optimize")
            for gif in gifs:
                size_mb = gif.stat().st_size / (1024 * 1024)
                console.print(f"  • {gif.name}: {size_mb:.1f}MB")
        
        console.print("\n🛠️  Optimization Tips:")
        console.print("• Use ImageOptim or TinyPNG for screenshots")
        console.print("• Use gifsicle for GIF compression")
        console.print("• Target <5MB for images, <10MB for GIFs")
    
    def generate_readme_snippets(self):
        """Generate README snippets for captured assets"""
        console.print("\n📝 Generating README Snippets", style="bold cyan")
        
        # Check what assets exist
        screenshots = list(self.screenshots_dir.glob("*.png"))
        gifs = list(self.gifs_dir.glob("*.gif"))
        
        if not screenshots and not gifs:
            console.print("❌ No assets found to generate snippets for")
            return
        
        console.print("\n📋 Copy these snippets to your README:")
        
        if screenshots:
            console.print("\n🖼️  Screenshot snippets:")
            for img in screenshots:
                console.print(f"![{img.stem.replace('-', ' ').title()}](assets/screenshots/{img.name})")
        
        if gifs:
            console.print("\n🎬 GIF snippets:")
            for gif in gifs:
                console.print(f"![{gif.stem.replace('-', ' ').title()}](assets/gifs/{gif.name})")

def main():
    helper = AssetsCaptureHelper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "screenshots":
            helper.capture_screenshots()
        elif command == "gifs":
            helper.capture_gifs()
        elif command == "optimize":
            helper.optimize_assets()
        elif command == "snippets":
            helper.generate_readme_snippets()
        else:
            console.print(f"Unknown command: {command}")
    else:
        helper.guided_capture_session()

if __name__ == "__main__":
    main() 