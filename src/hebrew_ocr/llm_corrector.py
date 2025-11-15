"""LLM-based text correction for Hebrew OCR output."""

import logging
from typing import Optional
import ollama

logger = logging.getLogger(__name__)


class LLMCorrector:
    """Uses LLM to review and correct OCR text output."""

    def __init__(
        self,
        model: str = "aya:8b",
        temperature: float = 0.3,
        max_tokens: int = 2000
    ):
        """Initialize LLM Corrector.

        Args:
            model: Ollama model name (default: "aya:8b" - good for Hebrew)
            temperature: Sampling temperature (lower = more deterministic)
            max_tokens: Maximum tokens in response
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info(f"LLM Corrector initialized with model: {model}")

    def correct_text(self, ocr_text: str, context: Optional[str] = None) -> str:
        """Correct OCR text using LLM.

        Args:
            ocr_text: Raw text from OCR
            context: Optional context about the document

        Returns:
            Corrected text
        """
        if not ocr_text.strip():
            logger.warning("Empty OCR text provided")
            return ocr_text

        prompt = self._build_correction_prompt(ocr_text, context)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )

            corrected_text = response['message']['content']
            logger.info(f"Text corrected: {len(ocr_text)} -> {len(corrected_text)} chars")
            return corrected_text

        except Exception as e:
            logger.error(f"Error during LLM correction: {e}")
            logger.warning("Returning original OCR text due to error")
            return ocr_text

    def _build_correction_prompt(self, ocr_text: str, context: Optional[str] = None) -> str:
        """Build the correction prompt for the LLM.

        Args:
            ocr_text: Raw OCR text
            context: Optional context

        Returns:
            Formatted prompt
        """
        prompt = """אתה עוזר מומחה לתיקון טקסט שעבר OCR. המשימה שלך היא לתקן טעויות OCR בטקסט העברי הבא.

שים לב במיוחד ל:
- אותיות דומות שנבלבלות בקלות (ר/ד, ה/ח, ו/ז, ת/ן וכו')
- רווחים חסרים או מיותרים
- סימני פיסוק
- שגיאות במילים נפוצות

חשוב: תחזיר רק את הטקסט המתוקן, ללא הסברים או הערות נוספות.
"""

        if context:
            prompt += f"\n\nהקשר על המסמך: {context}\n"

        prompt += f"\n\nטקסט OCR לתיקון:\n{ocr_text}\n\nטקסט מתוקן:"

        return prompt

    def check_model_available(self) -> bool:
        """Check if the configured model is available in Ollama.

        Returns:
            True if model is available, False otherwise
        """
        try:
            models = ollama.list()
            available_models = [m['name'] for m in models.get('models', [])]
            is_available = self.model in available_models

            if not is_available:
                logger.warning(
                    f"Model {self.model} not found. "
                    f"Available models: {', '.join(available_models)}"
                )

            return is_available
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
