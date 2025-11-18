#!/usr/bin/env python3
"""
Automated demo script for AI Duo Validator - runs without user input.
"""

import sys
import time
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
    time.sleep(1)


def main():
    print_section("AI DUO VALIDATOR - AUTOMATED DEMO")

    print(f"{Fore.YELLOW}Demonstrating complete validation loop with test fixtures{Style.RESET_ALL}\n")
    time.sleep(1)

    # Create orchestrator
    print(f"{Fore.GREEN}Creating orchestrator session...{Style.RESET_ALL}")
    orch = AIOrchestrator(session_id='demo_auto', auto_save=False)
    time.sleep(1)

    # Step 1: Process Agent A output
    print_section("ITERATION 1: Agent A → Orchestrator → Agent B")

    print(f"{Fore.YELLOW}Agent A completes authentication implementation...{Style.RESET_ALL}")
    time.sleep(1)

    with open('tests/fixtures/agent_a_output_1.txt', 'r') as f:
        agent_a_output = f.read()

    print(f"{Fore.GREEN}Orchestrator processing Agent A output...{Style.RESET_ALL}")
    prompt_for_b = orch.process_executor_output(agent_a_output, verbose=True)
    time.sleep(2)

    print(f"\n{Fore.GREEN}✓ Handoff extracted!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Prompt generated for Agent B (Validator){Style.RESET_ALL}")
    time.sleep(1)

    # Step 2: Process Agent B output
    print_section("Agent B Reviews Work")

    print(f"{Fore.YELLOW}Agent B analyzes code for security issues...{Style.RESET_ALL}")
    time.sleep(1)

    with open('tests/fixtures/agent_b_output_1.txt', 'r') as f:
        agent_b_output = f.read()

    print(f"{Fore.GREEN}Orchestrator processing Agent B validation...{Style.RESET_ALL}")
    prompt_for_a = orch.process_validator_output(agent_b_output, verbose=True)
    time.sleep(2)

    state = orch.get_state()
    verdict = state['current_validation']['verdict']

    print(f"\n{Fore.YELLOW}⚠ Verdict: {verdict.upper()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Feedback generated for Agent A{Style.RESET_ALL}")
    time.sleep(1)

    # Show issues found
    issues = state['current_validation'].get('issues', [])
    print(f"\n{Fore.YELLOW}Issues found by Agent B:{Style.RESET_ALL}")
    for issue in issues:
        severity_color = Fore.RED if issue['severity'] == 'high' else Fore.YELLOW
        print(f"  {severity_color}• [{issue['severity'].upper()}] {issue['description']}{Style.RESET_ALL}")
    time.sleep(2)

    # Simulate iteration 2
    print_section("ITERATION 2: Agent A Addresses Issues")

    print(f"{Fore.YELLOW}Agent A would now fix the issues and resubmit...{Style.RESET_ALL}")
    print(f"{Fore.WHITE}(In real workflow, Agent A fixes issues, emits new handoff){Style.RESET_ALL}")
    time.sleep(1)

    # Create mock approved validation
    print(f"\n{Fore.YELLOW}After fixes, Agent B approves the work...{Style.RESET_ALL}")
    time.sleep(1)

    approved_output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T15:00:00Z",
  "issues": [],
  "required_changes": [],
  "recommendations": ["Consider adding monitoring"],
  "verdict_rationale": "All security issues have been addressed. Implementation is production-ready."
}
==END_VALIDATION_FEEDBACK==
"""

    # Simulate handoff first
    handoff_2 = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Fixed all security issues from validation feedback",
    "files_modified": ["src/auth/login.py", "src/auth/validators.py"]
  },
  "validation_request": "Please verify fixes"
}
==END_AGENT_OUTPUT==
"""

    print(f"{Fore.GREEN}Orchestrator processing Agent A's fixes...{Style.RESET_ALL}")
    orch.process_executor_output(handoff_2, verbose=False)
    time.sleep(1)

    print(f"{Fore.GREEN}Orchestrator processing Agent B's approval...{Style.RESET_ALL}")
    result = orch.process_validator_output(approved_output, verbose=True)
    time.sleep(2)

    if result is None and orch.is_complete():
        print(f"\n{Fore.GREEN}✓✓✓ WORK APPROVED! Session complete ✓✓✓{Style.RESET_ALL}")
    time.sleep(1)

    # Final summary
    print_section("SESSION SUMMARY")

    final_state = orch.get_state()
    print(f"{Fore.CYAN}Session Statistics:{Style.RESET_ALL}")
    print(f"  Session ID: {final_state['session_id']}")
    print(f"  Total Iterations: {final_state['iteration']}")
    print(f"  Total Handoffs: {final_state['total_handoffs']}")
    print(f"  Total Validations: {final_state['total_validations']}")
    print(f"  Final Status: {Fore.GREEN}{final_state['status']}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}What This Demonstrated:{Style.RESET_ALL}")
    print("  ✓ Agent A implemented feature and emitted handoff")
    print("  ✓ Orchestrator extracted structured JSON from terminal output")
    print("  ✓ Agent B validated work and found 3 security issues")
    print("  ✓ Orchestrator routed feedback back to Agent A")
    print("  ✓ Agent A fixed issues and resubmitted")
    print("  ✓ Agent B approved - validation loop complete")

    print(f"\n{Fore.YELLOW}Benefits:{Style.RESET_ALL}")
    print("  • Caught security vulnerabilities before deployment")
    print("  • Enforced quality standards through validation")
    print("  • Structured communication between AI agents")
    print("  • Complete audit trail in session history")

    print(f"\n{Fore.GREEN}Demo completed successfully!{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Try it yourself:{Style.RESET_ALL}")
    print("  1. Run: ./orchestrator start")
    print("  2. Open two Claude Code terminals")
    print("  3. Paste agent prompts from prompts/ directory")
    print("  4. Give Agent A a task and follow the workflow!")
    print(f"\n{Fore.CYAN}Read examples/ for detailed walkthroughs.{Style.RESET_ALL}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Demo interrupted by user.{Style.RESET_ALL}\n")
        sys.exit(0)
