#!/usr/bin/env python3
"""
Unit tests for Conversation Review Agent
"""

import json
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from conversation_review_agent import (
    ConversationParser,
    ConversationAnalyzer,
    VoiceInteractionFacilitator,
    OutputFormatter,
    OpenItem,
    Decision,
    ConversationAnalysis,
    SessionSummary,
)


class TestConversationParser:
    """Test conversation parsing functionality."""

    def test_parse_json_string(self):
        """Test parsing JSON conversation from string."""
        json_str = '{"messages": [{"role": "user", "content": "Hello"}]}'
        result = ConversationParser.parse_raw(json_str)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0]["role"] == "user"

    def test_parse_text_string(self):
        """Test parsing plain text conversation."""
        text = "USER: Question\nASSISTANT: Answer"
        result = ConversationParser.parse_raw(text)

        assert "raw_text" in result
        assert result["format"] == "text"


class TestConversationAnalyzer:
    """Test conversation analysis functionality."""

    def test_extract_context_from_messages(self):
        """Test extracting context from JSON messages."""
        conversation = {
            "messages": [
                {"role": "user", "content": "I want to build a REST API for my blog"}
            ]
        }

        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze(conversation)

        assert "REST API" in analysis.context
        assert "blog" in analysis.context

    def test_identify_questions(self):
        """Test identifying questions in conversation."""
        conversation = {
            "messages": [
                {
                    "role": "assistant",
                    "content": "Which framework would you like to use? Express or Fastify?"
                }
            ]
        }

        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze(conversation)

        assert len(analysis.open_items) > 0
        assert any("framework" in item.description.lower() for item in analysis.open_items)

    def test_priority_detection_high(self):
        """Test high priority detection."""
        text = "This is critical and must be decided now."
        analyzer = ConversationAnalyzer()
        priority = analyzer._determine_priority(text)

        assert priority == "high"

    def test_priority_detection_low(self):
        """Test low priority detection."""
        text = "This is optional and nice to have later."
        analyzer = ConversationAnalyzer()
        priority = analyzer._determine_priority(text)

        assert priority == "low"

    def test_priority_detection_medium(self):
        """Test medium priority detection (default)."""
        text = "Should we implement this feature?"
        analyzer = ConversationAnalyzer()
        priority = analyzer._determine_priority(text)

        assert priority == "medium"

    def test_extract_options(self):
        """Test extracting options from text."""
        text = "Would you like Express.js or Fastify?"
        analyzer = ConversationAnalyzer()
        options = analyzer._extract_options(text)

        assert len(options) >= 2
        # Should extract "Express.js" and "Fastify" or similar

    def test_extract_numbered_options(self):
        """Test extracting numbered list options."""
        text = "Choose: 1. PostgreSQL 2. MySQL 3. MongoDB"
        analyzer = ConversationAnalyzer()
        options = analyzer._extract_options(text)

        assert len(options) >= 3


class TestOutputFormatter:
    """Test output formatting functionality."""

    def test_format_analysis_xml(self):
        """Test XML formatting of analysis."""
        analysis = ConversationAnalysis(
            context="Building a REST API",
            open_items=[
                OpenItem(
                    priority="high",
                    description="Which database to use?",
                    context="Database choice affects architecture",
                    options=["PostgreSQL", "MySQL"]
                )
            ]
        )

        xml_output = OutputFormatter.format_analysis_xml(analysis)

        assert "<analysis>" in xml_output
        assert "<context>" in xml_output
        assert "REST API" in xml_output
        assert "Which database" in xml_output
        assert 'priority="high"' in xml_output

    def test_format_summary_json(self):
        """Test JSON formatting of summary."""
        summary = SessionSummary(
            conversation_context="Building REST API",
            items_addressed=2,
            total_items=3,
            session_duration="5 minutes",
            decisions=[
                Decision(
                    question="Which database?",
                    user_response="PostgreSQL",
                    interpretation="User chose PostgreSQL",
                    action_items=["Set up PostgreSQL"]
                )
            ],
            deferred_items=["Rate limiting decision"],
            recommended_next_message="Proceed with PostgreSQL setup"
        )

        json_output = OutputFormatter.format_summary_json(summary)
        data = json.loads(json_output)

        assert "session_summary" in data
        assert data["session_summary"]["items_addressed"] == 2
        assert len(data["decisions"]) == 1
        assert data["decisions"][0]["user_response"] == "PostgreSQL"

    def test_format_summary_markdown(self):
        """Test Markdown formatting of summary."""
        summary = SessionSummary(
            conversation_context="Building REST API",
            items_addressed=1,
            total_items=2,
            session_duration="3 minutes",
            decisions=[
                Decision(
                    question="Which database?",
                    user_response="PostgreSQL",
                    interpretation="User chose PostgreSQL",
                    action_items=["Set up PostgreSQL", "Configure connection"]
                )
            ],
            deferred_items=[],
            recommended_next_message="Use PostgreSQL"
        )

        md_output = OutputFormatter.format_summary_markdown(summary)

        assert "# Conversation Review Session Summary" in md_output
        assert "## Session Overview" in md_output
        assert "## Decisions Made" in md_output
        assert "PostgreSQL" in md_output
        assert "Set up PostgreSQL" in md_output


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_analysis_workflow(self):
        """Test complete analysis workflow."""
        # Create a sample conversation
        conversation = {
            "messages": [
                {"role": "user", "content": "Build a blog API"},
                {
                    "role": "assistant",
                    "content": "I can help. Which framework: Express or Fastify? "
                               "Which database: PostgreSQL or MySQL?"
                }
            ]
        }

        # Parse and analyze
        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze(conversation)

        # Verify results
        assert "blog" in analysis.context.lower()
        assert len(analysis.open_items) >= 2  # Should detect both questions

        # Test XML output
        xml_output = OutputFormatter.format_analysis_xml(analysis)
        assert "<analysis>" in xml_output
        assert len(analysis.open_items) > 0


def run_tests():
    """Run all tests manually (for environments without pytest)."""
    print("Running Conversation Review Agent Tests...\n")

    test_classes = [
        TestConversationParser,
        TestConversationAnalyzer,
        TestOutputFormatter,
        TestIntegration,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        print("-" * 50)

        test_instance = test_class()
        methods = [m for m in dir(test_instance) if m.startswith("test_")]

        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {e}")

    print("\n" + "=" * 50)
    print(f"Results: {passed_tests}/{total_tests} tests passed")
    print("=" * 50)

    return passed_tests == total_tests


if __name__ == "__main__":
    # Can run with pytest or standalone
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        print("Run with pytest: pytest tests/test_agent.py")
        print("Or run manually: python tests/test_agent.py --manual")
