"""
Tests for parser module.
"""

import pytest
from pathlib import Path
from src.parser import (
    extract_handoff,
    extract_validation,
    ParserError,
    extract_first_marker
)


# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures'


def load_fixture(filename):
    """Load a test fixture file."""
    filepath = FIXTURES_DIR / filename
    with open(filepath, 'r') as f:
        return f.read()


class TestExtractHandoff:
    """Tests for extract_handoff function."""

    def test_extract_valid_handoff(self):
        """Test extracting valid handoff from Agent A output."""
        output = load_fixture('agent_a_output_1.txt')
        handoff = extract_handoff(output)

        assert handoff is not None
        assert handoff['agent'] == 'A'
        assert handoff['status'] == 'awaiting_validation'
        assert 'work_product' in handoff
        assert handoff['work_product']['type'] == 'code'
        assert 'validation_request' in handoff

    def test_extract_handoff_no_markers(self):
        """Test extracting handoff from output without markers."""
        output = "This is just regular output without any markers."
        handoff = extract_handoff(output)

        assert handoff is None

    def test_extract_handoff_malformed_json(self):
        """Test extracting handoff with malformed JSON."""
        output = load_fixture('malformed_output.txt')

        with pytest.raises(ParserError) as exc_info:
            extract_handoff(output)

        assert "Invalid JSON" in str(exc_info.value)

    def test_extract_handoff_missing_required_fields(self):
        """Test handoff with missing required fields."""
        output = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation"
}
==END_AGENT_OUTPUT==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_handoff(output)

        assert "Missing required field" in str(exc_info.value)

    def test_extract_handoff_invalid_status(self):
        """Test handoff with invalid status value."""
        output = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "invalid_status",
  "work_product": {
    "type": "code",
    "description": "Test"
  },
  "validation_request": "Test"
}
==END_AGENT_OUTPUT==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_handoff(output)

        assert "Invalid status" in str(exc_info.value)

    def test_extract_handoff_invalid_work_product_type(self):
        """Test handoff with invalid work_product type."""
        output = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "invalid_type",
    "description": "Test"
  },
  "validation_request": "Test"
}
==END_AGENT_OUTPUT==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_handoff(output)

        assert "Invalid work_product type" in str(exc_info.value)

    def test_extract_handoff_with_surrounding_text(self):
        """Test extracting handoff with text before and after markers."""
        output = """
Some preamble text here.

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Test implementation"
  },
  "validation_request": "Please review"
}
==END_AGENT_OUTPUT==

Some text after the handoff.
"""
        handoff = extract_handoff(output)

        assert handoff is not None
        assert handoff['agent'] == 'A'


class TestExtractValidation:
    """Tests for extract_validation function."""

    def test_extract_valid_validation(self):
        """Test extracting valid validation from Agent B output."""
        output = load_fixture('agent_b_output_1.txt')
        validation = extract_validation(output)

        assert validation is not None
        assert validation['from'] == 'B'
        assert validation['verdict'] == 'approved_with_changes'
        assert 'timestamp' in validation
        assert 'issues' in validation
        assert len(validation['issues']) == 3
        assert 'required_changes' in validation

    def test_extract_validation_no_markers(self):
        """Test extracting validation from output without markers."""
        output = "This is just regular output without any markers."
        validation = extract_validation(output)

        assert validation is None

    def test_extract_validation_approved_verdict(self):
        """Test validation with approved verdict."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T10:00:00Z",
  "issues": [],
  "required_changes": [],
  "recommendations": [],
  "verdict_rationale": "All good"
}
==END_VALIDATION_FEEDBACK==
"""
        validation = extract_validation(output)

        assert validation is not None
        assert validation['verdict'] == 'approved'
        assert validation['issues'] == []

    def test_extract_validation_invalid_verdict(self):
        """Test validation with invalid verdict value."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "invalid_verdict",
  "timestamp": "2025-01-17T10:00:00Z",
  "verdict_rationale": "Test"
}
==END_VALIDATION_FEEDBACK==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_validation(output)

        assert "Invalid verdict" in str(exc_info.value)

    def test_extract_validation_missing_required_fields(self):
        """Test validation with missing required fields."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved"
}
==END_VALIDATION_FEEDBACK==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_validation(output)

        assert "Missing required field" in str(exc_info.value)

    def test_extract_validation_invalid_issue_severity(self):
        """Test validation with invalid issue severity."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "timestamp": "2025-01-17T10:00:00Z",
  "issues": [
    {
      "severity": "invalid_severity",
      "category": "security",
      "description": "Test issue"
    }
  ],
  "verdict_rationale": "Test"
}
==END_VALIDATION_FEEDBACK==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_validation(output)

        assert "Invalid severity" in str(exc_info.value)

    def test_extract_validation_invalid_issue_category(self):
        """Test validation with invalid issue category."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "timestamp": "2025-01-17T10:00:00Z",
  "issues": [
    {
      "severity": "high",
      "category": "invalid_category",
      "description": "Test issue"
    }
  ],
  "verdict_rationale": "Test"
}
==END_VALIDATION_FEEDBACK==
"""
        with pytest.raises(ParserError) as exc_info:
            extract_validation(output)

        assert "Invalid category" in str(exc_info.value)


class TestExtractFirstMarker:
    """Tests for extract_first_marker function."""

    def test_extract_first_handoff_marker(self):
        """Test extracting first handoff when multiple present."""
        output = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "First handoff"
  },
  "validation_request": "Test"
}
==END_AGENT_OUTPUT==

Some text in between.

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Second handoff"
  },
  "validation_request": "Test"
}
==END_AGENT_OUTPUT==
"""
        handoff, position = extract_first_marker(output, 'handoff')

        assert handoff is not None
        assert handoff['work_product']['description'] == 'First handoff'
        assert position >= 0

    def test_extract_first_validation_marker(self):
        """Test extracting first validation when multiple present."""
        output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T10:00:00Z",
  "verdict_rationale": "First validation"
}
==END_VALIDATION_FEEDBACK==

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "rejected",
  "timestamp": "2025-01-17T11:00:00Z",
  "verdict_rationale": "Second validation"
}
==END_VALIDATION_FEEDBACK==
"""
        validation, position = extract_first_marker(output, 'validation')

        assert validation is not None
        assert validation['verdict'] == 'approved'
        assert validation['verdict_rationale'] == 'First validation'

    def test_extract_first_marker_not_found(self):
        """Test extract_first_marker when no marker found."""
        output = "No markers here"

        handoff, position = extract_first_marker(output, 'handoff')

        assert handoff is None
        assert position == -1

    def test_extract_first_marker_invalid_type(self):
        """Test extract_first_marker with invalid marker type."""
        output = "Some output"

        with pytest.raises(ValueError) as exc_info:
            extract_first_marker(output, 'invalid_type')

        assert "Invalid marker_type" in str(exc_info.value)


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_empty_output(self):
        """Test parsing empty output."""
        output = ""

        handoff = extract_handoff(output)
        validation = extract_validation(output)

        assert handoff is None
        assert validation is None

    def test_whitespace_only_output(self):
        """Test parsing output with only whitespace."""
        output = "   \n\n\t  "

        handoff = extract_handoff(output)
        validation = extract_validation(output)

        assert handoff is None
        assert validation is None

    def test_incomplete_markers(self):
        """Test parsing output with incomplete markers."""
        output = """
==BEGIN_AGENT_OUTPUT==
{"agent": "A"}
"""
        handoff = extract_handoff(output)
        assert handoff is None  # No closing marker

    def test_json_with_extra_whitespace(self):
        """Test parsing JSON with extra whitespace."""
        output = """
==BEGIN_AGENT_OUTPUT==

{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Test"
  },
  "validation_request": "Test"
}

==END_AGENT_OUTPUT==
"""
        handoff = extract_handoff(output)

        assert handoff is not None
        assert handoff['agent'] == 'A'
