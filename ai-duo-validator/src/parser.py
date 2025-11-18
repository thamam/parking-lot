"""
Parser module for extracting handoff and validation markers from agent output.
"""

import re
import json
from typing import Optional, Dict, Tuple


class ParserError(Exception):
    """Custom exception for parser errors."""
    pass


def extract_handoff(output: str) -> Optional[Dict]:
    """
    Extract handoff JSON from Agent A output.

    Looks for content between ==BEGIN_AGENT_OUTPUT== and ==END_AGENT_OUTPUT== markers,
    then parses the JSON content.

    Args:
        output: Raw terminal output from Agent A

    Returns:
        Parsed handoff dictionary or None if no valid handoff found

    Raises:
        ParserError: If markers found but JSON is malformed
    """
    pattern = r'==BEGIN_AGENT_OUTPUT==(.*?)==END_AGENT_OUTPUT=='
    match = re.search(pattern, output, re.DOTALL)

    if not match:
        return None

    json_content = match.group(1).strip()

    try:
        handoff = json.loads(json_content)
        _validate_handoff_schema(handoff)
        return handoff
    except json.JSONDecodeError as e:
        raise ParserError(f"Invalid JSON in handoff: {e}")
    except ValueError as e:
        raise ParserError(f"Invalid handoff schema: {e}")


def extract_validation(output: str) -> Optional[Dict]:
    """
    Extract validation feedback JSON from Agent B output.

    Looks for content between ==VALIDATION_FEEDBACK== and ==END_VALIDATION_FEEDBACK== markers,
    then parses the JSON content.

    Args:
        output: Raw terminal output from Agent B

    Returns:
        Parsed validation dictionary or None if no valid validation found

    Raises:
        ParserError: If markers found but JSON is malformed
    """
    pattern = r'==VALIDATION_FEEDBACK==(.*?)==END_VALIDATION_FEEDBACK=='
    match = re.search(pattern, output, re.DOTALL)

    if not match:
        return None

    json_content = match.group(1).strip()

    try:
        validation = json.loads(json_content)
        _validate_validation_schema(validation)
        return validation
    except json.JSONDecodeError as e:
        raise ParserError(f"Invalid JSON in validation: {e}")
    except ValueError as e:
        raise ParserError(f"Invalid validation schema: {e}")


def _validate_handoff_schema(handoff: Dict) -> None:
    """
    Validate handoff JSON against expected schema.

    Args:
        handoff: Parsed handoff dictionary

    Raises:
        ValueError: If schema validation fails
    """
    required_fields = ['agent', 'status', 'work_product', 'validation_request']

    for field in required_fields:
        if field not in handoff:
            raise ValueError(f"Missing required field: {field}")

    # Validate work_product structure
    work_product = handoff['work_product']
    required_wp_fields = ['type', 'description']

    for field in required_wp_fields:
        if field not in work_product:
            raise ValueError(f"Missing required work_product field: {field}")

    # Validate status
    valid_statuses = ['awaiting_validation', 'in_progress', 'completed']
    if handoff['status'] not in valid_statuses:
        raise ValueError(f"Invalid status: {handoff['status']}")

    # Validate work_product type
    valid_types = ['code', 'analysis', 'config', 'document']
    if work_product['type'] not in valid_types:
        raise ValueError(f"Invalid work_product type: {work_product['type']}")


def _validate_validation_schema(validation: Dict) -> None:
    """
    Validate validation JSON against expected schema.

    Args:
        validation: Parsed validation dictionary

    Raises:
        ValueError: If schema validation fails
    """
    required_fields = ['from', 'verdict', 'timestamp', 'verdict_rationale']

    for field in required_fields:
        if field not in validation:
            raise ValueError(f"Missing required field: {field}")

    # Validate verdict
    valid_verdicts = ['approved', 'approved_with_changes', 'rejected']
    if validation['verdict'] not in valid_verdicts:
        raise ValueError(f"Invalid verdict: {validation['verdict']}")

    # Validate issues structure if present
    if 'issues' in validation:
        for issue in validation['issues']:
            required_issue_fields = ['severity', 'category', 'description']
            for field in required_issue_fields:
                if field not in issue:
                    raise ValueError(f"Missing required issue field: {field}")

            # Validate severity
            valid_severities = ['critical', 'high', 'medium', 'low']
            if issue['severity'] not in valid_severities:
                raise ValueError(f"Invalid severity: {issue['severity']}")

            # Validate category
            valid_categories = ['security', 'correctness', 'performance', 'style']
            if issue['category'] not in valid_categories:
                raise ValueError(f"Invalid category: {issue['category']}")


def extract_first_marker(output: str, marker_type: str) -> Tuple[Optional[Dict], int]:
    """
    Extract the first occurrence of a marker from output.

    Useful when output contains multiple markers - returns the first one
    and its position in the text.

    Args:
        output: Raw terminal output
        marker_type: Either 'handoff' or 'validation'

    Returns:
        Tuple of (parsed_dict, position) or (None, -1) if not found
    """
    if marker_type == 'handoff':
        pattern = r'==BEGIN_AGENT_OUTPUT==(.*?)==END_AGENT_OUTPUT=='
        extractor = extract_handoff
    elif marker_type == 'validation':
        pattern = r'==VALIDATION_FEEDBACK==(.*?)==END_VALIDATION_FEEDBACK=='
        extractor = extract_validation
    else:
        raise ValueError(f"Invalid marker_type: {marker_type}")

    match = re.search(pattern, output, re.DOTALL)

    if not match:
        return None, -1

    try:
        parsed = extractor(output)
        return parsed, match.start()
    except ParserError:
        return None, -1
