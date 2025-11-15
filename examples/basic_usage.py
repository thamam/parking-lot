"""Basic usage example for Hebrew OCR to Markdown converter."""

from hebrew_ocr import HebrewOCRPipeline


def main():
    """Run basic OCR example."""
    # Initialize the pipeline
    pipeline = HebrewOCRPipeline(
        tesseract_lang="heb",
        dpi=300,
        llm_model="aya:8b",
        use_llm_correction=True  # Set to False to skip LLM correction
    )

    # Example 1: Process a single image
    print("Example 1: Processing a single image")
    try:
        result = pipeline.process_document(
            document_path="path/to/your/hebrew_document.png",
            output_path="output/result.md",
            context="מסמך היסטורי מתקופת המנדט"  # Optional context
        )
        print("✓ Processed successfully")
        print(f"Preview:\n{result[:200]}...\n")
    except FileNotFoundError:
        print("! Please provide a valid document path")

    # Example 2: Process a PDF
    print("Example 2: Processing a PDF")
    try:
        result = pipeline.process_document(
            document_path="path/to/your/hebrew_book.pdf",
            output_path="output/book.md"
        )
        print("✓ PDF processed successfully\n")
    except FileNotFoundError:
        print("! Please provide a valid PDF path")

    # Example 3: Batch processing
    print("Example 3: Batch processing multiple documents")
    try:
        output_files = pipeline.batch_process(
            input_dir="path/to/input/directory",
            output_dir="output/batch",
            pattern="*.png",  # Process all PNG files
            context="ספרים היסטוריים"
        )
        print(f"✓ Processed {len(output_files)} documents")
    except FileNotFoundError:
        print("! Please provide a valid input directory")


if __name__ == "__main__":
    main()
