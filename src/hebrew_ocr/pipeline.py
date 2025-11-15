"""Main pipeline for Hebrew OCR to Markdown conversion."""

import logging
from pathlib import Path
from typing import Union, List, Optional
from tqdm import tqdm

from .ocr_engine import OCREngine
from .llm_corrector import LLMCorrector

logger = logging.getLogger(__name__)


class HebrewOCRPipeline:
    """Complete pipeline for converting Hebrew documents to Markdown."""

    def __init__(
        self,
        tesseract_lang: str = "heb",
        dpi: int = 300,
        llm_model: str = "aya:8b",
        use_llm_correction: bool = True
    ):
        """Initialize the OCR pipeline.

        Args:
            tesseract_lang: Language for Tesseract OCR
            dpi: DPI for PDF conversion
            llm_model: Model name for LLM correction
            use_llm_correction: Whether to use LLM for text correction
        """
        self.ocr_engine = OCREngine(tesseract_lang=tesseract_lang, dpi=dpi)
        self.use_llm_correction = use_llm_correction

        if use_llm_correction:
            self.llm_corrector = LLMCorrector(model=llm_model)
        else:
            self.llm_corrector = None

        logger.info(f"Pipeline initialized (LLM correction: {use_llm_correction})")

    def process_document(
        self,
        document_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        context: Optional[str] = None
    ) -> str:
        """Process a document and convert to Markdown.

        Args:
            document_path: Path to input document
            output_path: Optional path to save Markdown output
            context: Optional context about the document for LLM

        Returns:
            Markdown-formatted text
        """
        logger.info(f"Processing document: {document_path}")

        # Step 1: OCR
        ocr_result = self.ocr_engine.process_document(document_path)

        # Handle both single string (image) and list of strings (PDF)
        if isinstance(ocr_result, list):
            pages = ocr_result
        else:
            pages = [ocr_result]

        # Step 2: LLM Correction (if enabled)
        corrected_pages = []
        for i, page_text in enumerate(tqdm(pages, desc="Processing pages"), 1):
            if self.use_llm_correction and self.llm_corrector:
                corrected_text = self.llm_corrector.correct_text(page_text, context)
            else:
                corrected_text = page_text

            corrected_pages.append(corrected_text)

        # Step 3: Convert to Markdown
        markdown_output = self._format_as_markdown(corrected_pages)

        # Step 4: Save if output path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(markdown_output, encoding='utf-8')
            logger.info(f"Saved output to: {output_path}")

        return markdown_output

    def _format_as_markdown(self, pages: List[str]) -> str:
        """Format extracted text as Markdown.

        Args:
            pages: List of page texts

        Returns:
            Markdown-formatted document
        """
        markdown_parts = []

        for i, page_text in enumerate(pages, 1):
            if len(pages) > 1:
                # Add page separators for multi-page documents
                markdown_parts.append(f"## עמוד {i}\n")

            # Clean up the text
            cleaned_text = page_text.strip()

            # Add the text
            markdown_parts.append(cleaned_text)

            if i < len(pages):
                markdown_parts.append("\n\n---\n")  # Page separator

        return "\n".join(markdown_parts)

    def batch_process(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        pattern: str = "*",
        context: Optional[str] = None
    ) -> List[Path]:
        """Process multiple documents in a directory.

        Args:
            input_dir: Directory containing input documents
            output_dir: Directory for output Markdown files
            pattern: File pattern to match (default: all files)
            context: Optional context for all documents

        Returns:
            List of output file paths
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all matching files
        files = list(input_path.glob(pattern))
        logger.info(f"Found {len(files)} files to process")

        output_files = []
        for input_file in tqdm(files, desc="Processing documents"):
            try:
                # Generate output filename
                output_file = output_path / f"{input_file.stem}.md"

                # Process document
                self.process_document(
                    input_file,
                    output_file,
                    context=context
                )

                output_files.append(output_file)
            except Exception as e:
                logger.error(f"Error processing {input_file}: {e}")

        logger.info(f"Processed {len(output_files)} documents successfully")
        return output_files
