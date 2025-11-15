"""Command-line interface for Hebrew OCR to Markdown converter."""

import logging
import click
from pathlib import Path
from .pipeline import HebrewOCRPipeline
from .config import Config


def setup_logging(level: str):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
@click.option('--model', default='aya:8b', help='LLM model name')
@click.option('--dpi', default=300, help='DPI for PDF conversion')
def process(input_path, output, context, no_llm, model, dpi):
    """Process a single document (image or PDF)."""
    click.echo(f"Processing: {input_path}")

    pipeline = HebrewOCRPipeline(
        tesseract_lang="heb",
        dpi=dpi,
        llm_model=model,
        use_llm_correction=not no_llm
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
@click.option('--model', default='aya:8b', help='LLM model name')
@click.option('--dpi', default=300, help='DPI for PDF conversion')
def batch(input_dir, output_dir, pattern, context, no_llm, model, dpi):
    """Process multiple documents in a directory."""
    click.echo(f"Batch processing: {input_dir}")

    pipeline = HebrewOCRPipeline(
        tesseract_lang="heb",
        dpi=dpi,
        llm_model=model,
        use_llm_correction=not no_llm
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
            click.echo(f"✓ Hebrew language data: Installed")
        else:
            click.echo(f"✗ Hebrew language data: Not installed")
            click.echo(f"  Available languages: {', '.join(langs)}")
    except Exception as e:
        click.echo(f"✗ Language check failed: {e}")

    # Check Ollama
    try:
        models = ollama.list()
        click.echo(f"✓ Ollama: Running")
        model_names = [m['name'] for m in models.get('models', [])]
        if model_names:
            click.echo(f"  Available models: {', '.join(model_names)}")
        else:
            click.echo(f"  No models installed")
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
