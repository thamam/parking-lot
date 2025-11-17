"""
Formatter module for generating prompts and formatting output.
"""

import json
from typing import Dict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def format_handoff_for_validator(handoff: Dict, prompt_file: str = 'prompts/agent_b_validator.md') -> str:
    """
    Format a handoff as a prompt for Agent B (Validator).

    Args:
        handoff: Parsed handoff dictionary from Agent A
        prompt_file: Path to Agent B prompt file

    Returns:
        Formatted prompt string to paste into Agent B terminal
    """
    # Read the validator prompt template
    try:
        with open(prompt_file, 'r') as f:
            base_prompt = f.read()
    except FileNotFoundError:
        base_prompt = "# Agent B (Validator)\n\nYou are the validator agent."

    work_product = handoff.get('work_product', {})

    prompt = f"""{base_prompt}

---

## NEW VALIDATION REQUEST

Agent A has completed work and is requesting validation.

### Work Product Details:
- **Type**: {work_product.get('type', 'N/A')}
- **Description**: {work_product.get('description', 'N/A')}
- **Status**: {handoff.get('status', 'N/A')}

### Files Modified:
{_format_list(work_product.get('files_modified', []))}

### Key Decisions:
{_format_list(work_product.get('key_decisions', []))}

### Validation Request:
{handoff.get('validation_request', 'General validation requested')}

### Agent A's Concerns:
{_format_list(handoff.get('concerns', ['No concerns listed']))}

---

**Please proceed with validation and provide your feedback using the ==VALIDATION_FEEDBACK== markers.**
"""

    return prompt


def format_validation_for_executor(validation: Dict, prompt_file: str = 'prompts/agent_a_executor.md') -> str:
    """
    Format validation feedback as a prompt for Agent A (Executor).

    Args:
        validation: Parsed validation dictionary from Agent B
        prompt_file: Path to Agent A prompt file

    Returns:
        Formatted prompt string to paste into Agent A terminal
    """
    # Read the executor prompt template
    try:
        with open(prompt_file, 'r') as f:
            base_prompt = f.read()
    except FileNotFoundError:
        base_prompt = "# Agent A (Executor)\n\nYou are the executor agent."

    verdict = validation.get('verdict', 'unknown')
    verdict_color = _get_verdict_color(verdict)

    prompt = f"""{base_prompt}

---

## VALIDATION FEEDBACK RECEIVED

{verdict_color}**Verdict**: {verdict.upper()}{Style.RESET_ALL}

### Rationale:
{validation.get('verdict_rationale', 'No rationale provided')}

"""

    # Add issues if present
    issues = validation.get('issues', [])
    if issues:
        prompt += "### Issues Found:\n\n"
        for i, issue in enumerate(issues, 1):
            severity_color = _get_severity_color(issue.get('severity', 'medium'))
            prompt += f"{i}. {severity_color}[{issue.get('severity', 'N/A').upper()}]{Style.RESET_ALL} "
            prompt += f"**{issue.get('category', 'N/A')}**: {issue.get('description', 'N/A')}\n"
            if 'location' in issue:
                prompt += f"   - Location: {issue['location']}\n"
            if 'impact' in issue:
                prompt += f"   - Impact: {issue['impact']}\n"
            prompt += "\n"

    # Add required changes
    required_changes = validation.get('required_changes', [])
    if required_changes:
        prompt += "### Required Changes:\n"
        prompt += _format_list(required_changes)
        prompt += "\n"

    # Add recommendations
    recommendations = validation.get('recommendations', [])
    if recommendations:
        prompt += "### Recommendations (Optional):\n"
        prompt += _format_list(recommendations)
        prompt += "\n"

    # Add next steps based on verdict
    if verdict == 'approved':
        prompt += "---\n\n**Status**: Work is approved! No further action needed.\n"
    elif verdict == 'approved_with_changes':
        prompt += "---\n\n**Next Steps**: Please address the required changes above and resubmit.\n"
    elif verdict == 'rejected':
        prompt += "---\n\n**Next Steps**: Please review the issues and implement a different approach.\n"

    return prompt


def pretty_print_handoff(handoff: Dict) -> None:
    """
    Pretty-print a handoff dictionary with colors.

    Args:
        handoff: Parsed handoff dictionary
    """
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}HANDOFF FROM AGENT A{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    work_product = handoff.get('work_product', {})

    print(f"{Fore.YELLOW}Work Product:{Style.RESET_ALL}")
    print(f"  Type: {work_product.get('type', 'N/A')}")
    print(f"  Description: {work_product.get('description', 'N/A')}")
    print(f"  Status: {handoff.get('status', 'N/A')}")

    if work_product.get('files_modified'):
        print(f"\n{Fore.YELLOW}Files Modified:{Style.RESET_ALL}")
        for f in work_product['files_modified']:
            print(f"  - {f}")

    if work_product.get('key_decisions'):
        print(f"\n{Fore.YELLOW}Key Decisions:{Style.RESET_ALL}")
        for d in work_product['key_decisions']:
            print(f"  - {d}")

    print(f"\n{Fore.YELLOW}Validation Request:{Style.RESET_ALL}")
    print(f"  {handoff.get('validation_request', 'N/A')}")

    if handoff.get('concerns'):
        print(f"\n{Fore.YELLOW}Concerns:{Style.RESET_ALL}")
        for c in handoff['concerns']:
            print(f"  - {c}")

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def pretty_print_validation(validation: Dict) -> None:
    """
    Pretty-print a validation dictionary with colors.

    Args:
        validation: Parsed validation dictionary
    """
    verdict = validation.get('verdict', 'unknown')
    verdict_color = _get_verdict_color(verdict)

    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}VALIDATION FROM AGENT B{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

    print(f"{verdict_color}Verdict: {verdict.upper()}{Style.RESET_ALL}")
    print(f"\nRationale: {validation.get('verdict_rationale', 'N/A')}")

    issues = validation.get('issues', [])
    if issues:
        print(f"\n{Fore.YELLOW}Issues:{Style.RESET_ALL}")
        for i, issue in enumerate(issues, 1):
            severity_color = _get_severity_color(issue.get('severity', 'medium'))
            print(f"\n  {i}. {severity_color}[{issue.get('severity', 'N/A').upper()}]{Style.RESET_ALL} "
                  f"{issue.get('category', 'N/A')}")
            print(f"     {issue.get('description', 'N/A')}")
            if 'location' in issue:
                print(f"     Location: {issue['location']}")
            if 'impact' in issue:
                print(f"     Impact: {issue['impact']}")

    required_changes = validation.get('required_changes', [])
    if required_changes:
        print(f"\n{Fore.YELLOW}Required Changes:{Style.RESET_ALL}")
        for change in required_changes:
            print(f"  - {change}")

    recommendations = validation.get('recommendations', [])
    if recommendations:
        print(f"\n{Fore.YELLOW}Recommendations:{Style.RESET_ALL}")
        for rec in recommendations:
            print(f"  - {rec}")

    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")


def format_session_status(state_dict: Dict) -> str:
    """
    Format session state as human-readable status.

    Args:
        state_dict: State dictionary from SessionState.get_state()

    Returns:
        Formatted status string
    """
    status = f"""
{Fore.CYAN}{'='*60}{Style.RESET_ALL}
{Fore.CYAN}SESSION STATUS{Style.RESET_ALL}
{Fore.CYAN}{'='*60}{Style.RESET_ALL}

Session ID: {state_dict.get('session_id', 'N/A')}
Started: {state_dict.get('started_at', 'N/A')}
Status: {state_dict.get('status', 'N/A')}

Active Agent: {state_dict.get('active_agent', 'None')}
Current Iteration: {state_dict.get('iteration', 0)}
Total Handoffs: {state_dict.get('total_handoffs', 0)}
Total Validations: {state_dict.get('total_validations', 0)}

{Fore.CYAN}{'='*60}{Style.RESET_ALL}
"""
    return status


def _format_list(items: list) -> str:
    """Helper function to format a list as bullet points."""
    if not items:
        return "  - None"
    return "\n".join(f"  - {item}" for item in items)


def _get_verdict_color(verdict: str) -> str:
    """Get color code for verdict."""
    colors = {
        'approved': Fore.GREEN,
        'approved_with_changes': Fore.YELLOW,
        'rejected': Fore.RED
    }
    return colors.get(verdict, Fore.WHITE)


def _get_severity_color(severity: str) -> str:
    """Get color code for issue severity."""
    colors = {
        'critical': Fore.RED,
        'high': Fore.LIGHTRED_EX,
        'medium': Fore.YELLOW,
        'low': Fore.LIGHTBLUE_EX
    }
    return colors.get(severity, Fore.WHITE)
