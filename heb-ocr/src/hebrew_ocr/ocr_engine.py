"""OCR Engine for Hebrew text extraction using Tesseract."""

import logging
from pathlib import Path
from typing import List, Union, Optional
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

# Supported image file extensions
SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif'}


class OCREngine:
    """Handles OCR processing for Hebrew documents."""

    def __init__(self, tesseract_lang: str = "heb", dpi: int = 300):
        """Initialize OCR Engine.

        Args:
            tesseract_lang: Language code for Tesseract (default: "heb" for Hebrew)
            dpi: DPI for PDF to image conversion (default: 300)
        """
        self.tesseract_lang = tesseract_lang
        self.dpi = dpi
        logger.info(f"OCR Engine initialized with language: {tesseract_lang}, DPI: {dpi}")

    def process_image(self, image_path: Union[str, Path]) -> str:
        """Extract text from an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text from the image
        """
        try:
            with Image.open(image_path) as image:
                text = pytesseract.image_to_string(
                    image,
                    lang=self.tesseract_lang,
                    config='--psm 3'  # Fully automatic page segmentation
                )
                logger.info(f"Extracted {len(text)} characters from {image_path}")
                return text
        except FileNotFoundError:
            logger.exception(f"Image file not found: {image_path}")
            raise
        except (IOError, OSError):
            logger.exception(f"Error reading image file: {image_path}")
            raise
        except pytesseract.TesseractError:
            logger.exception(f"Tesseract error processing image: {image_path}")
            raise
        except Exception:
            logger.exception(f"Unexpected error processing image: {image_path}")
            raise

    def process_pdf(self, pdf_path: Union[str, Path]) -> List[str]:
        """Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of extracted text, one per page
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=self.dpi)
            logger.info(f"Converted PDF to {len(images)} images")

            texts = []
            for i, image in enumerate(images, 1):
                text = pytesseract.image_to_string(
                    image,
                    lang=self.tesseract_lang,
                    config='--psm 3'
                )
                texts.append(text)
                logger.info(f"Processed page {i}/{len(images)}")

            return texts
        except FileNotFoundError:
            logger.exception(f"PDF file not found: {pdf_path}")
            raise
        except (IOError, OSError):
            logger.exception(f"Error reading PDF file: {pdf_path}")
            raise
        except pytesseract.TesseractError:
            logger.exception(f"Tesseract error processing PDF: {pdf_path}")
            raise
        except Exception:
            logger.exception(f"Unexpected error processing PDF: {pdf_path}")
            raise

    def process_document(self, document_path: Union[str, Path]) -> Union[str, List[str]]:
        """Process a document (image or PDF).

        Args:
            document_path: Path to the document

        Returns:
            Extracted text (string for images, list of strings for PDFs)
        """
        path = Path(document_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")

        suffix = path.suffix.lower()
        if suffix == '.pdf':
            return self.process_pdf(path)
        elif suffix in SUPPORTED_IMAGE_EXTENSIONS:
            return self.process_image(path)
        else:
            supported_formats = ', '.join(sorted(SUPPORTED_IMAGE_EXTENSIONS | {'.pdf'}))
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: {supported_formats}"
            )
