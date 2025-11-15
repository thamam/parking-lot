"""Command-line interface for Hebrew OCR to Markdown converter."""

import logging
import click
from pathlib import Path
from typing import Optional
from .pipeline import HebrewOCRPipeline
from .config import Config


def setup_logging(level: str):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_pipeline(
    tesseract_lang: Optional[str] = None,
    dpi: Optional[int] = None,
    model: Optional[str] = None,
    use_llm: Optional[bool] = None
) -> HebrewOCRPipeline:
    """Create a pipeline with config defaults and CLI overrides.

    Args:
        tesseract_lang: Tesseract language (overrides config)
        dpi: DPI for PDF conversion (overrides config)
        model: LLM model name (overrides config)
        use_llm: Whether to use LLM correction (overrides config)

    Returns:
        Configured pipeline instance
    """
    config = Config()

    return HebrewOCRPipeline(
        tesseract_lang=tesseract_lang or config.TESSERACT_LANG,
        dpi=dpi or config.DPI,
        llm_model=model or config.LLM_MODEL,
        use_llm_correction=use_llm if use_llm is not None else config.USE_LLM_CORRECTION
    )


@click.group()
@click.option('--log-level', default='INFO', help='Logging level')
def cli(log_level):
    """Hebrew OCR to Markdown Converter.

    Convert Hebrew documents (images and PDFs) to Markdown format
    using Tesseract OCR and LLM-based text correction.
    """
    setup_logging(log_level)


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output Markdown file path')
@click.option('--context', '-c', help='Context about the document')
@click.option('--no-llm', is_flag=True, help='Disable LLM correction')
@click.option('--model', default=None, help='LLM model name (overrides config)')
@click.option('--dpi', default=None, type=int, help='DPI for PDF conversion (overrides config)')
@click.option('--lang', default=None, help='Tesseract language (overrides config)')
def process(input_path, output, context, no_llm, model, dpi, lang):
    """Process a single document (image or PDF)."""
    click.echo(f"Processing: {input_path}")

    # Determine use_llm based on flag
    use_llm = False if no_llm else None

    pipeline = create_pipeline(
        tesseract_lang=lang,
        dpi=dpi,
        model=model,
        use_llm=use_llm
    )

    try:
        result = pipeline.process_document(
            document_path=input_path,
            output_path=output,
            context=context
        )

        if output:
            click.echo(f"✓ Saved to: {output}")
        else:
            click.echo("\n--- Result ---")
            click.echo(result)

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_dir', type=click.Path())
@click.option('--pattern', default='*', help='File pattern to match')
@click.option('--context', '-c', help='Context about the documents')
@click.option('--no-llm', is_flag=True, help='Disable LLM correction')
@click.option('--model', default=None, help='LLM model name (overrides config)')
@click.option('--dpi', default=None, type=int, help='DPI for PDF conversion (overrides config)')
@click.option('--lang', default=None, help='Tesseract language (overrides config)')
def batch(input_dir, output_dir, pattern, context, no_llm, model, dpi, lang):
    """Process multiple documents in a directory."""
    click.echo(f"Batch processing: {input_dir}")

    # Determine use_llm based on flag
    use_llm = False if no_llm else None

    pipeline = create_pipeline(
        tesseract_lang=lang,
        dpi=dpi,
        model=model,
        use_llm=use_llm
    )

    try:
        output_files = pipeline.batch_process(
            input_dir=input_dir,
            output_dir=output_dir,
            pattern=pattern,
            context=context
        )

        click.echo(f"✓ Processed {len(output_files)} documents")
        click.echo(f"✓ Output saved to: {output_dir}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def check():
    """Check system requirements and configuration."""
    import pytesseract
    import ollama

    click.echo("Checking system requirements...\n")

    # Check Tesseract
    try:
        version = pytesseract.get_tesseract_version()
        click.echo(f"✓ Tesseract: {version}")
    except Exception as e:
        click.echo(f"✗ Tesseract: Not found or error ({e})")

    # Check Hebrew language data
    try:
        langs = pytesseract.get_languages()
        if 'heb' in langs:
            click.echo("✓ Hebrew language data: Installed")
        else:
            click.echo("✗ Hebrew language data: Not installed")
            click.echo(f"  Available languages: {', '.join(langs)}")
    except Exception as e:
        click.echo(f"✗ Language check failed: {e}")

    # Check Ollama
    try:
        models = ollama.list()
        click.echo("✓ Ollama: Running")
        model_names = [m['name'] for m in models.get('models', [])]
        if model_names:
            click.echo(f"  Available models: {', '.join(model_names)}")
        else:
            click.echo("  No models installed")
    except Exception as e:
        click.echo(f"✗ Ollama: Not running or error ({e})")

    click.echo("\nConfiguration:")
    config = Config()
    click.echo(f"  LLM Model: {config.LLM_MODEL}")
    click.echo(f"  Tesseract Lang: {config.TESSERACT_LANG}")
    click.echo(f"  DPI: {config.DPI}")
    click.echo(f"  Use LLM Correction: {config.USE_LLM_CORRECTION}")


if __name__ == '__main__':
    cli()
