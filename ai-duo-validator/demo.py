#!/usr/bin/env python3
"""
Demo script for AI Duo Validator - shows complete workflow using test fixtures.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.orchestrator import AIOrchestrator
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def print_section(title):
    """Print a section header."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title.center(70)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def main():
    print_section("AI DUO VALIDATOR - DEMO")

    print(f"{Fore.YELLOW}This demo shows a complete validation loop using test fixtures.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Agent A implements authentication, Agent B validates it.{Style.RESET_ALL}\n")

    input(f"{Fore.GREEN}Press ENTER to start...{Style.RESET_ALL}")

    # Create orchestrator
    orch = AIOrchestrator(session_id='demo_session', auto_save=False)

    # Step 1: Load Agent A output
    print_section("STEP 1: Agent A (Executor) Completes Work")

    print(f"{Fore.YELLOW}Agent A has implemented user authentication.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Loading Agent A's output from test fixture...{Style.RESET_ALL}\n")

    with open('tests/fixtures/agent_a_output_1.txt', 'r') as f:
        agent_a_output = f.read()

    print(f"{Fore.WHITE}Agent A Output (excerpt):{Style.RESET_ALL}")
    print("-" * 70)
    # Show first 500 chars
    preview = agent_a_output[:500] + "..." if len(agent_a_output) > 500 else agent_a_output
    print(preview)
    print("-" * 70)

    input(f"\n{Fore.GREEN}Press ENTER to process Agent A's output...{Style.RESET_ALL}")

    # Process Agent A output
    print_section("ORCHESTRATOR PROCESSING")

    prompt_for_b = orch.process_executor_output(agent_a_output, verbose=True)

    if prompt_for_b:
        print(f"\n{Fore.GREEN}✓ Handoff detected and extracted!{Style.RESET_ALL}")

        state = orch.get_state()
        print(f"\n{Fore.CYAN}Session State:{Style.RESET_ALL}")
        print(f"  Status: {state['status']}")
        print(f"  Active Agent: {state['active_agent']}")
        print(f"  Iteration: {state['iteration']}")

    input(f"\n{Fore.GREEN}Press ENTER to see prompt for Agent B...{Style.RESET_ALL}")

    # Show prompt for Agent B (truncated)
    print_section("PROMPT GENERATED FOR AGENT B (VALIDATOR)")

    print(f"{Fore.WHITE}This is what would be sent to Agent B:{Style.RESET_ALL}\n")
    print("-" * 70)
    prompt_preview = prompt_for_b[:800] + "\n\n[... full prompt truncated for demo ...]"
    print(prompt_preview)
    print("-" * 70)

    input(f"\n{Fore.GREEN}Press ENTER to continue...{Style.RESET_ALL}")

    # Step 2: Load Agent B output
    print_section("STEP 2: Agent B (Validator) Reviews Work")

    print(f"{Fore.YELLOW}Agent B reviews the code and finds security issues.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Loading Agent B's validation feedback...{Style.RESET_ALL}\n")

    with open('tests/fixtures/agent_b_output_1.txt', 'r') as f:
        agent_b_output = f.read()

    print(f"{Fore.WHITE}Agent B Output (excerpt):{Style.RESET_ALL}")
    print("-" * 70)
    preview = agent_b_output[:500] + "..." if len(agent_b_output) > 500 else agent_b_output
    print(preview)
    print("-" * 70)

    input(f"\n{Fore.GREEN}Press ENTER to process Agent B's validation...{Style.RESET_ALL}")

    # Process Agent B output
    print_section("ORCHESTRATOR PROCESSING")

    prompt_for_a = orch.process_validator_output(agent_b_output, verbose=True)

    if prompt_for_a:
        print(f"\n{Fore.YELLOW}⚠ Changes required - feedback sent back to Agent A{Style.RESET_ALL}")

        state = orch.get_state()
        print(f"\n{Fore.CYAN}Session State:{Style.RESET_ALL}")
        print(f"  Status: {state['status']}")
        print(f"  Active Agent: {state['active_agent']}")
        print(f"  Total Validations: {state['total_validations']}")
        print(f"  Verdict: {state['current_validation']['verdict']}")

    input(f"\n{Fore.GREEN}Press ENTER to see feedback for Agent A...{Style.RESET_ALL}")

    # Show prompt for Agent A (truncated)
    print_section("FEEDBACK SENT TO AGENT A (EXECUTOR)")

    print(f"{Fore.WHITE}This is what would be sent back to Agent A:{Style.RESET_ALL}\n")
    print("-" * 70)
    feedback_preview = prompt_for_a[:800] + "\n\n[... full feedback truncated for demo ...]"
    print(feedback_preview)
    print("-" * 70)

    input(f"\n{Fore.GREEN}Press ENTER to see final summary...{Style.RESET_ALL}")

    # Final summary
    print_section("DEMO COMPLETE - SESSION SUMMARY")

    print(orch.get_status_summary())

    history = orch.get_history()
    print(f"{Fore.CYAN}History Entries:{Style.RESET_ALL}")
    for i, entry in enumerate(history, 1):
        print(f"\n  {i}. {entry['type'].upper()}")
        print(f"     From: Agent {entry['from_agent']}")
        if entry['to_agent']:
            print(f"     To: Agent {entry['to_agent']}")
        print(f"     Timestamp: {entry['timestamp']}")

    print(f"\n{Fore.GREEN}✓ Demo completed successfully!{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}What happened:{Style.RESET_ALL}")
    print("  1. Agent A implemented authentication feature")
    print("  2. Orchestrator extracted handoff and sent to Agent B")
    print("  3. Agent B found 3 security issues")
    print("  4. Orchestrator sent feedback back to Agent A")
    print("  5. Agent A would now fix issues and resubmit")

    print(f"\n{Fore.YELLOW}Next Steps:{Style.RESET_ALL}")
    print("  • Read the agent prompts in prompts/")
    print("  • Review full examples in examples/")
    print("  • Try with real Claude Code terminals!")
    print(f"\n{Fore.CYAN}Run './orchestrator start' to begin a real session.{Style.RESET_ALL}\n")


if __name__ == '__main__':
    main()
