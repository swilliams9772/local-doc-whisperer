#!/usr/bin/env python3
"""
Test script for Local Doc-Whisperer
Validates core functionality without requiring API calls
"""

import os
import tempfile
from pathlib import Path
import sys

# Add current directory to path so we can import main
sys.path.insert(0, '.')

def test_text_extraction():
    """Test text extraction from different file formats."""
    print("🧪 Testing text extraction...")
    
    # Create a temporary markdown file
    test_content = """
# Test Document

This is a test document for the Doc-Whisperer system.

## Section 1
Some content here.

## Section 2
More content here.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        from main import DocWhisperer
        
        # Create DocWhisperer without API key (for text extraction only)
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'
        
        doc_whisperer = DocWhisperer()
        extracted_text = doc_whisperer.extract_text(temp_file)
        
        assert "Test Document" in extracted_text
        assert "Section 1" in extracted_text
        print("✅ Text extraction works correctly")
        
    except Exception as e:
        print(f"❌ Text extraction failed: {e}")
        return False
    finally:
        # Clean up
        os.unlink(temp_file)
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
    
    return True

def test_chunking():
    """Test text chunking functionality."""
    print("🧪 Testing text chunking...")
    
    # Create a long test document
    test_text = " ".join([f"This is sentence {i}." for i in range(1000)])
    
    try:
        from main import DocWhisperer
        
        # Mock API key for chunking test
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'
        
        doc_whisperer = DocWhisperer()
        chunks = doc_whisperer.chunk_text(test_text, "test_file.txt")
        
        assert len(chunks) > 1
        assert all('metadata' in chunk for chunk in chunks)
        assert all('source' in chunk['metadata'] for chunk in chunks)
        print(f"✅ Text chunking works correctly ({len(chunks)} chunks created)")
        
    except Exception as e:
        print(f"❌ Text chunking failed: {e}")
        return False
    finally:
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
    
    return True

def test_file_structure():
    """Test that required directories and files exist."""
    print("🧪 Testing file structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'env.example'
    ]
    
    required_dirs = [
        'docs_in',
        'summaries'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing required file: {file_path}")
            return False
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Missing required directory: {dir_path}")
            return False
    
    print("✅ File structure is correct")
    return True

def test_dependencies():
    """Test that all required dependencies can be imported."""
    print("🧪 Testing dependencies...")
    
    required_modules = [
        'anthropic',
        'chromadb',
        'pdfplumber',
        'typer',
        'rich',
        'dotenv'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are available")
    return True

def test_env_file():
    """Test environment file setup."""
    print("🧪 Testing environment configuration...")
    
    if not Path('env.example').exists():
        print("❌ env.example file not found")
        return False
    
    with open('env.example', 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY' not in content:
            print("❌ ANTHROPIC_API_KEY not found in env.example")
            return False
    
    print("✅ Environment configuration is correct")
    return True

def main():
    """Run all tests."""
    print("🧠 Local Doc-Whisperer Test Suite")
    print("=================================")
    print()
    
    tests = [
        test_file_structure,
        test_env_file,
        test_dependencies,
        test_text_extraction,
        test_chunking,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Doc-Whisperer is ready to use.")
        print()
        print("Next steps:")
        print("1. Copy env.example to .env")
        print("2. Add your Anthropic API key to .env")
        print("3. Run: python main.py ingest docs_in/sample_document.md")
        return True
    else:
        print("😞 Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 