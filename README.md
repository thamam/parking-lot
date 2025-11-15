# Hebrew OCR to Markdown Converter

A powerful tool for converting Hebrew documents (PDFs and images) to Markdown format using Tesseract OCR and LLM-based text correction.

## Features

- **OCR Support**: Extract text from images and PDFs using Tesseract OCR
- **Hebrew Language**: Optimized for Hebrew text recognition
- **LLM Correction**: Uses local LLMs (via Ollama) to review and correct OCR errors
- **Markdown Output**: Converts documents to clean, formatted Markdown
- **Batch Processing**: Process multiple documents at once
- **CLI & Python API**: Use from command line or integrate into your Python code

## Prerequisites

### 1. System Requirements

- Python 3.8+
- Tesseract OCR
- Ollama (for LLM correction)

### 2. Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-heb
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 3. Install Ollama

Download and install from: https://ollama.ai

**Pull the recommended Hebrew model:**
```bash
ollama pull aya:8b
```

Alternative Hebrew-supporting models:
- `aya:latest` (larger, more accurate)
- `mistral:latest` (good multilingual support)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd parking-lot
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure (optional):**
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Command Line Interface

**Check system requirements:**
```bash
python main.py check
```

**Process a single document:**
```bash
# With LLM correction
python main.py process path/to/document.pdf -o output.md

# Without LLM correction (faster, less accurate)
python main.py process path/to/document.pdf -o output.md --no-llm

# With context (helps LLM understand the content)
python main.py process document.pdf -o output.md -c "ספר היסטורי מ-1970"
```

**Batch processing:**
```bash
# Process all PDFs in a directory
python main.py batch input_dir/ output_dir/ --pattern "*.pdf"

# Process all images
python main.py batch scans/ converted/ --pattern "*.png"
```

### Python API

```python
from src.hebrew_ocr import HebrewOCRPipeline

# Initialize the pipeline
pipeline = HebrewOCRPipeline(
    tesseract_lang="heb",
    dpi=300,
    llm_model="aya:8b",
    use_llm_correction=True
)

# Process a single document
result = pipeline.process_document(
    document_path="document.pdf",
    output_path="output.md",
    context="מסמך רשמי"  # Optional context
)

# Batch process
output_files = pipeline.batch_process(
    input_dir="scans/",
    output_dir="converted/",
    pattern="*.pdf"
)
```

## Configuration

Edit `.env` file to customize settings:

```env
# Tesseract Settings
TESSERACT_LANG=heb
DPI=300

# LLM Settings
LLM_MODEL=aya:8b
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2000
USE_LLM_CORRECTION=true

# Logging
LOG_LEVEL=INFO
```

## Project Structure

```
parking-lot/
├── src/hebrew_ocr/          # Main source code
│   ├── __init__.py
│   ├── ocr_engine.py        # Tesseract OCR wrapper
│   ├── llm_corrector.py     # LLM-based text correction
│   ├── pipeline.py          # Main processing pipeline
│   ├── config.py            # Configuration management
│   └── cli.py               # Command-line interface
├── examples/                # Usage examples
│   └── basic_usage.py
├── tests/                   # Test files (TODO)
├── docs/                    # Documentation
├── output/                  # Default output directory
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example configuration
└── README.md               # This file
```

## How It Works

1. **OCR Extraction**: Tesseract OCR extracts raw text from images/PDFs
2. **LLM Review**: The extracted text is sent to a local LLM (Aya:8b) for correction
3. **Markdown Formatting**: The corrected text is formatted as Markdown
4. **Output**: Clean, readable Markdown files

### LLM Correction

The LLM reviews OCR text and corrects common errors:
- Confused letters (ר/ד, ה/ח, ו/ז, ת/ן, etc.)
- Missing or extra spaces
- Punctuation errors
- Common word mistakes

## Tips for Best Results

1. **Higher DPI**: Use 300+ DPI for better OCR accuracy
2. **Clean Images**: Better scan quality = better results
3. **Provide Context**: Help the LLM understand the content type
4. **Choose the Right Model**: Larger models (aya:latest) are more accurate but slower

## Troubleshooting

**"Tesseract not found"**
- Ensure Tesseract is installed and in your PATH
- Run `tesseract --version` to verify

**"Hebrew language data not found"**
- Install Hebrew language pack: `sudo apt-get install tesseract-ocr-heb`

**"Ollama connection error"**
- Start Ollama: `ollama serve`
- Verify model is installed: `ollama list`

**Poor OCR quality**
- Increase DPI: `--dpi 600`
- Improve source image quality
- Try preprocessing the image (contrast, brightness, etc.)

## Contributing

This is a POC project. Contributions, suggestions, and feedback are welcome!

## License

MIT

## Acknowledgments

Based on the approach suggested by the community:
- Tesseract OCR for text extraction
- Aya:8b (Ollama) for Hebrew LLM review
- Inspired by real-world book scanning projects (1970-1980s printed books)
