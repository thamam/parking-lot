"""
CLI interface for AI Duo Validator orchestrator.
"""

import sys
import click
from pathlib import Path
from colorama import Fore, Style
from .orchestrator import AIOrchestrator
from .parser import ParserError


# Global orchestrator instance
current_orchestrator = None


@click.group()
def cli():
    """AI Duo Validator - Orchestrate validation between two AI agents."""
    pass


@cli.command()
def start():
    """Start a new orchestration session."""
    global current_orchestrator

    current_orchestrator = AIOrchestrator()
    session_id = current_orchestrator.state.session_id

    click.echo(f"\n{Fore.GREEN}[ORCHESTRATOR] New session started{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}Session ID: {session_id}{Style.RESET_ALL}")
    click.echo(f"\n{Fore.YELLOW}Next Step:{Style.RESET_ALL}")
    click.echo("  Run: orchestrator process-output A")
    click.echo("  Then paste Agent A (Executor) output and press Ctrl+D\n")


@cli.command('process-output')
@click.argument('agent', type=click.Choice(['A', 'B'], case_sensitive=False))
@click.option('--session', '-s', help='Session file to use (loads if exists)')
def process_output(agent, session):
    """
    Process output from an agent.

    AGENT: Either 'A' (Executor) or 'B' (Validator)
    """
    global current_orchestrator

    # Load session if specified
    if session:
        try:
            current_orchestrator = AIOrchestrator.load_session(session)
            click.echo(f"{Fore.GREEN}[ORCHESTRATOR] Loaded session from {session}{Style.RESET_ALL}\n")
        except FileNotFoundError:
            click.echo(f"{Fore.RED}[ERROR] Session file not found: {session}{Style.RESET_ALL}")
            return
        except Exception as e:
            click.echo(f"{Fore.RED}[ERROR] Failed to load session: {e}{Style.RESET_ALL}")
            return

    # Check if orchestrator is initialized
    if current_orchestrator is None:
        click.echo(f"{Fore.YELLOW}[WARNING] No active session. Starting new session...{Style.RESET_ALL}\n")
        current_orchestrator = AIOrchestrator()

    agent = agent.upper()

    # Get multi-line input
    click.echo(f"{Fore.CYAN}[ORCHESTRATOR] Paste Agent {agent} output below (Ctrl+D when done):{Style.RESET_ALL}\n")

    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break

        output = '\n'.join(lines)

        # Process based on agent
        if agent == 'A':
            _process_agent_a(output)
        elif agent == 'B':
            _process_agent_b(output)

    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}[ORCHESTRATOR] Operation cancelled{Style.RESET_ALL}")


def _process_agent_a(output: str):
    """Process Agent A (Executor) output."""
    global current_orchestrator

    try:
        prompt = current_orchestrator.process_executor_output(output, verbose=True)

        if prompt is None:
            click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No handoff detected in Agent A output{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Make sure output contains ==BEGIN_AGENT_OUTPUT== markers{Style.RESET_ALL}\n")
            return

        # Display prompt for Agent B
        click.echo(f"\n{Fore.GREEN}[ORCHESTRATOR] Handoff detected from Agent A{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}PROMPT FOR AGENT B (VALIDATOR){Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        click.echo(prompt)
        click.echo(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        click.echo(f"\n{Fore.YELLOW}Next Step:{Style.RESET_ALL}")
        click.echo("  1. Copy the prompt above")
        click.echo("  2. Paste into Agent B's Claude Code terminal")
        click.echo("  3. Run: orchestrator process-output B")
        click.echo("  4. Paste Agent B's response\n")

    except ParserError as e:
        click.echo(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}\n")
    except Exception as e:
        click.echo(f"{Fore.RED}[ERROR] Unexpected error: {e}{Style.RESET_ALL}\n")


def _process_agent_b(output: str):
    """Process Agent B (Validator) output."""
    global current_orchestrator

    try:
        prompt = current_orchestrator.process_validator_output(output, verbose=True)

        if prompt is None:
            # Check if validation was found but approved
            if current_orchestrator.is_complete():
                click.echo(f"\n{Fore.GREEN}[ORCHESTRATOR] ✓ Work APPROVED by Agent B{Style.RESET_ALL}")
                click.echo(f"{Fore.GREEN}Session complete!{Style.RESET_ALL}\n")

                # Show summary
                state = current_orchestrator.get_state()
                click.echo(f"{Fore.CYAN}Session Summary:{Style.RESET_ALL}")
                click.echo(f"  Total Iterations: {state['iteration']}")
                click.echo(f"  Total Handoffs: {state['total_handoffs']}")
                click.echo(f"  Total Validations: {state['total_validations']}\n")
                return
            else:
                click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No validation detected in Agent B output{Style.RESET_ALL}")
                click.echo(f"{Fore.YELLOW}Make sure output contains ==VALIDATION_FEEDBACK== markers{Style.RESET_ALL}\n")
                return

        # Display prompt for Agent A
        verdict = current_orchestrator.state.current_validation.get('verdict')
        click.echo(f"\n{Fore.YELLOW}[ORCHESTRATOR] Validation received: {verdict.upper()}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}PROMPT FOR AGENT A (EXECUTOR){Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        click.echo(prompt)
        click.echo(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        click.echo(f"\n{Fore.YELLOW}Next Step:{Style.RESET_ALL}")
        click.echo("  1. Copy the prompt above")
        click.echo("  2. Paste into Agent A's Claude Code terminal")
        click.echo("  3. Run: orchestrator process-output A")
        click.echo("  4. Paste Agent A's response\n")

    except ParserError as e:
        click.echo(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}\n")
    except Exception as e:
        click.echo(f"{Fore.RED}[ERROR] Unexpected error: {e}{Style.RESET_ALL}\n")


@cli.command()
def status():
    """Show current session status."""
    global current_orchestrator

    if current_orchestrator is None:
        click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No active session{Style.RESET_ALL}")
        click.echo("Run 'orchestrator start' to begin a new session\n")
        return

    click.echo(current_orchestrator.get_status_summary())


@cli.command()
@click.option('--full', '-f', is_flag=True, help='Show full history with raw outputs')
def history(full):
    """Show session history."""
    global current_orchestrator

    if current_orchestrator is None:
        click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No active session{Style.RESET_ALL}\n")
        return

    hist = current_orchestrator.get_history()

    if not hist:
        click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No history yet{Style.RESET_ALL}\n")
        return

    click.echo(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}SESSION HISTORY{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    for entry in hist:
        entry_type = entry['type']
        iteration = entry['iteration']
        timestamp = entry['timestamp']

        if entry_type == 'handoff':
            handoff = entry['handoff']
            work_type = handoff.get('work_product', {}).get('type', 'N/A')
            description = handoff.get('work_product', {}).get('description', 'N/A')

            click.echo(f"{Fore.YELLOW}Iteration {iteration}:{Style.RESET_ALL} Agent A → Agent B")
            click.echo(f"  Timestamp: {timestamp}")
            click.echo(f"  Work Type: {work_type}")
            click.echo(f"  Description: {description}")

        elif entry_type == 'validation':
            validation = entry['validation']
            verdict = validation.get('verdict', 'N/A')
            verdict_color = Fore.GREEN if verdict == 'approved' else Fore.YELLOW if verdict == 'approved_with_changes' else Fore.RED

            click.echo(f"{Fore.YELLOW}Iteration {iteration}:{Style.RESET_ALL} Agent B → Agent A")
            click.echo(f"  Timestamp: {timestamp}")
            click.echo(f"  Verdict: {verdict_color}{verdict.upper()}{Style.RESET_ALL}")

        if full:
            click.echo(f"\n  Raw Output Preview:")
            preview = entry['raw_output'][:200] + '...' if len(entry['raw_output']) > 200 else entry['raw_output']
            click.echo(f"  {preview}\n")

        click.echo()

    click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


@cli.command()
@click.argument('filepath', required=False)
def export(filepath):
    """Export session history to file."""
    global current_orchestrator

    if current_orchestrator is None:
        click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No active session{Style.RESET_ALL}\n")
        return

    if filepath is None:
        session_id = current_orchestrator.state.session_id
        filepath = f"ai-duo-validator/sessions/{session_id}_export.json"

    try:
        current_orchestrator.export_history(filepath)
        click.echo(f"{Fore.GREEN}[ORCHESTRATOR] Exported history to: {filepath}{Style.RESET_ALL}\n")
    except Exception as e:
        click.echo(f"{Fore.RED}[ERROR] Failed to export: {e}{Style.RESET_ALL}\n")


@cli.command()
@click.argument('filepath')
def load(filepath):
    """Load a saved session."""
    global current_orchestrator

    try:
        current_orchestrator = AIOrchestrator.load_session(filepath)
        click.echo(f"{Fore.GREEN}[ORCHESTRATOR] Loaded session from: {filepath}{Style.RESET_ALL}")
        click.echo(current_orchestrator.get_status_summary())
    except FileNotFoundError:
        click.echo(f"{Fore.RED}[ERROR] Session file not found: {filepath}{Style.RESET_ALL}\n")
    except Exception as e:
        click.echo(f"{Fore.RED}[ERROR] Failed to load session: {e}{Style.RESET_ALL}\n")


@cli.command()
@click.argument('filepath', required=False)
def save(filepath):
    """Save current session."""
    global current_orchestrator

    if current_orchestrator is None:
        click.echo(f"{Fore.YELLOW}[ORCHESTRATOR] No active session{Style.RESET_ALL}\n")
        return

    if filepath is None:
        session_id = current_orchestrator.state.session_id
        filepath = f"ai-duo-validator/sessions/{session_id}.json"

    try:
        current_orchestrator.save_session(filepath)
        click.echo(f"{Fore.GREEN}[ORCHESTRATOR] Saved session to: {filepath}{Style.RESET_ALL}\n")
    except Exception as e:
        click.echo(f"{Fore.RED}[ERROR] Failed to save: {e}{Style.RESET_ALL}\n")


if __name__ == '__main__':
    cli()
