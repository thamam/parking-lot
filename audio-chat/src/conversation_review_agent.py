#!/usr/bin/env python3
"""
Conversation Review Agent
Analyzes Claude Code conversations and facilitates decision-making through voice interaction.
"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom


@dataclass
class OpenItem:
    """Represents a question or decision point that needs addressing."""
    priority: Literal["high", "medium", "low"]
    description: str
    context: str
    options: List[str] = field(default_factory=list)


@dataclass
class Decision:
    """Represents a decision made during the review session."""
    question: str
    user_response: str
    interpretation: str
    action_items: List[str] = field(default_factory=list)


@dataclass
class ConversationAnalysis:
    """Results of analyzing a conversation."""
    context: str
    open_items: List[OpenItem] = field(default_factory=list)


@dataclass
class SessionSummary:
    """Summary of a review session."""
    conversation_context: str
    items_addressed: int
    total_items: int
    session_duration: str
    decisions: List[Decision] = field(default_factory=list)
    deferred_items: List[str] = field(default_factory=list)
    recommended_next_message: str = ""


class ConversationParser:
    """Parses Claude Code conversation files."""

    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        """Parse conversation from file (JSON or text)."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Conversation file not found: {file_path}")

        content = path.read_text(encoding='utf-8')

        # Try parsing as JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fall back to text parsing
            return {"raw_text": content, "format": "text"}

    @staticmethod
    def parse_raw(content: str) -> Dict[str, Any]:
        """Parse raw conversation content."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_text": content, "format": "text"}


class ConversationAnalyzer:
    """Analyzes conversations to identify open questions and decisions."""

    # Keywords that indicate questions or pending decisions
    QUESTION_MARKERS = [
        r'\?',
        r'\bshould\s+(?:i|we)\b',
        r'\bwould\s+you\s+like\b',
        r'\bdo\s+you\s+want\b',
        r'\bwhich\s+(?:one|approach|option)\b',
        r'\bplease\s+(?:choose|decide|clarify)\b',
        r'\bnot\s+sure\b',
        r'\bambiguous\b',
        r'\bneed\s+(?:to|your)\s+(?:decide|input|clarification)\b',
        r'\bwaiting\s+for\b',
        r'\blet\s+me\s+know\b',
        r'\bconfirm\b.*\bpreference\b',
    ]

    # Keywords indicating high priority
    HIGH_PRIORITY_MARKERS = [
        'critical', 'urgent', 'blocker', 'blocking', 'must', 'required',
        'necessary', 'important', 'breaking', 'error', 'fail'
    ]

    # Keywords indicating low priority
    LOW_PRIORITY_MARKERS = [
        'optional', 'nice to have', 'future', 'later', 'eventually',
        'cosmetic', 'minor', 'suggestion'
    ]

    def analyze(self, conversation: Dict[str, Any]) -> ConversationAnalysis:
        """Analyze conversation to extract context and open items."""

        # Extract conversation context
        context = self._extract_context(conversation)

        # Find open questions and decisions
        open_items = self._identify_open_items(conversation)

        return ConversationAnalysis(context=context, open_items=open_items)

    def _extract_context(self, conversation: Dict[str, Any]) -> str:
        """Extract high-level context about what's being built/discussed."""

        if "raw_text" in conversation:
            text = conversation["raw_text"]
            # Get first few lines as context
            lines = text.split('\n')[:10]
            return ' '.join(lines).strip()[:500]

        # For structured JSON conversations
        if "messages" in conversation:
            messages = conversation["messages"]
            if messages and len(messages) > 0:
                first_user_msg = next((m for m in messages if m.get("role") == "user"), None)
                if first_user_msg:
                    content = first_user_msg.get("content", "")
                    return content[:500] if isinstance(content, str) else str(content)[:500]

        return "Conversation context could not be automatically extracted."

    def _identify_open_items(self, conversation: Dict[str, Any]) -> List[OpenItem]:
        """Identify questions and decisions that need addressing."""

        open_items = []

        if "raw_text" in conversation:
            text = conversation["raw_text"]
            items = self._extract_from_text(text)
            open_items.extend(items)
        elif "messages" in conversation:
            for message in conversation["messages"]:
                if message.get("role") == "assistant":
                    content = message.get("content", "")
                    if isinstance(content, str):
                        items = self._extract_from_text(content)
                        open_items.extend(items)

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        open_items.sort(key=lambda x: priority_order[x.priority])

        return open_items

    def _extract_from_text(self, text: str) -> List[OpenItem]:
        """Extract open items from text content."""
        items = []

        # Split into sentences/paragraphs
        sentences = re.split(r'[.!?]\s+|\n\n', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if this looks like a question or decision point
            is_question = any(re.search(marker, sentence, re.IGNORECASE)
                            for marker in self.QUESTION_MARKERS)

            if is_question:
                priority = self._determine_priority(sentence)

                # Extract context (previous sentence if available)
                context_match = re.search(r'(.{0,200})' + re.escape(sentence[:50]), text)
                context = context_match.group(1).strip() if context_match else "From conversation"

                # Try to extract options
                options = self._extract_options(sentence)

                items.append(OpenItem(
                    priority=priority,
                    description=sentence[:300],
                    context=context[:200],
                    options=options
                ))

        return items

    def _determine_priority(self, text: str) -> Literal["high", "medium", "low"]:
        """Determine priority based on text content."""
        text_lower = text.lower()

        if any(marker in text_lower for marker in self.HIGH_PRIORITY_MARKERS):
            return "high"
        elif any(marker in text_lower for marker in self.LOW_PRIORITY_MARKERS):
            return "low"
        else:
            return "medium"

    def _extract_options(self, text: str) -> List[str]:
        """Try to extract options from text (e.g., 'A or B', '1. X 2. Y')."""
        options = []

        # Pattern: "X or Y"
        or_pattern = r'(\w+(?:\s+\w+)*)\s+or\s+(\w+(?:\s+\w+)*)'
        or_matches = re.findall(or_pattern, text, re.IGNORECASE)
        if or_matches:
            for match in or_matches[:3]:  # Limit to first 3
                options.extend(match)

        # Pattern: numbered list
        numbered_pattern = r'\d+[\.)]\s*([^\d\n]{3,50})'
        numbered_matches = re.findall(numbered_pattern, text)
        if numbered_matches:
            options.extend([m.strip() for m in numbered_matches[:5]])

        return options[:5]  # Max 5 options


class VoiceInteractionFacilitator:
    """Facilitates voice interaction for decision making."""

    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.session_start = datetime.now()

    def conduct_session(self, analysis: ConversationAnalysis) -> SessionSummary:
        """Conduct interactive session to gather decisions."""

        decisions = []
        deferred_items = []

        print("\n" + "="*70)
        print("CONVERSATION REVIEW SESSION")
        print("="*70)
        print(f"\nContext: {analysis.context}\n")
        print(f"Found {len(analysis.open_items)} items requiring attention.\n")

        if not analysis.open_items:
            print("No open questions or decisions found.")
            return self._create_summary(analysis, decisions, deferred_items)

        for idx, item in enumerate(analysis.open_items, 1):
            print(f"\n[{idx}/{len(analysis.open_items)}] Priority: {item.priority.upper()}")
            print("-" * 70)

            decision = self._handle_item(item)

            if decision:
                decisions.append(decision)
            else:
                deferred_items.append(item.description)

            # Check if user wants to continue
            if self.interactive and idx < len(analysis.open_items):
                continue_response = input("\nContinue to next item? (y/n/q to quit): ").strip().lower()
                if continue_response in ['n', 'q', 'quit', 'exit']:
                    # Add remaining items to deferred
                    deferred_items.extend([i.description for i in analysis.open_items[idx:]])
                    break

        return self._create_summary(analysis, decisions, deferred_items)

    def _handle_item(self, item: OpenItem) -> Optional[Decision]:
        """Handle a single item - ask question and record decision."""

        print(f"\nQuestion: {item.description}")
        print(f"Context: {item.context}")

        if item.options:
            print("\nOptions:")
            for i, option in enumerate(item.options, 1):
                print(f"  {i}. {option}")

        if not self.interactive:
            print("\n[Non-interactive mode - skipping]")
            return None

        # Get user response
        print("\nYour response (or 'skip' to defer):")
        user_response = input("> ").strip()

        if user_response.lower() in ['skip', 'defer', 'later', 's']:
            print("⏭️  Deferred")
            return None

        if not user_response:
            print("⏭️  No response - deferred")
            return None

        # Clarify if needed
        if len(user_response) < 10 or user_response.lower() in ['yes', 'no', 'y', 'n']:
            clarification = input("Could you elaborate? ").strip()
            if clarification:
                user_response = f"{user_response} - {clarification}"

        # Confirm understanding
        interpretation = self._interpret_response(user_response, item)
        print(f"\n✓ Understood: {interpretation}")
        confirm = input("Is this correct? (y/n): ").strip().lower()

        if confirm not in ['y', 'yes', '']:
            revised = input("Please clarify: ").strip()
            if revised:
                user_response = revised
                interpretation = self._interpret_response(revised, item)

        # Generate action items
        action_items = self._generate_action_items(interpretation, item)

        return Decision(
            question=item.description,
            user_response=user_response,
            interpretation=interpretation,
            action_items=action_items
        )

    def _interpret_response(self, response: str, item: OpenItem) -> str:
        """Interpret user's response in context of the question."""

        # Simple interpretation - in production this could use LLM
        response_lower = response.lower()

        if any(word in response_lower for word in ['yes', 'approve', 'agree', 'correct', 'proceed']):
            return f"User approved: {item.description.split('?')[0]}"
        elif any(word in response_lower for word in ['no', 'reject', 'disagree', 'different']):
            return f"User rejected: {item.description.split('?')[0]} - {response}"
        else:
            return f"User decided: {response}"

    def _generate_action_items(self, interpretation: str, item: OpenItem) -> List[str]:
        """Generate concrete action items based on decision."""

        # Basic action item generation
        actions = []

        if "approved" in interpretation.lower():
            actions.append(f"Proceed with: {item.description.split('?')[0]}")
        elif "rejected" in interpretation.lower():
            actions.append(f"Do not implement: {item.description.split('?')[0]}")
            actions.append("Explore alternative approach")
        else:
            actions.append(f"Implement decision: {interpretation}")

        return actions

    def _create_summary(self, analysis: ConversationAnalysis,
                       decisions: List[Decision],
                       deferred_items: List[str]) -> SessionSummary:
        """Create final session summary."""

        duration = datetime.now() - self.session_start
        duration_str = f"{duration.seconds // 60} minutes"

        # Generate recommended message
        recommended_msg = self._generate_recommended_message(decisions)

        return SessionSummary(
            conversation_context=analysis.context,
            items_addressed=len(decisions),
            total_items=len(analysis.open_items),
            session_duration=duration_str,
            decisions=decisions,
            deferred_items=deferred_items,
            recommended_next_message=recommended_msg
        )

    def _generate_recommended_message(self, decisions: List[Decision]) -> str:
        """Generate message to send back to Claude Code."""

        if not decisions:
            return "I've reviewed the conversation but haven't made any decisions yet. I'll get back to you."

        lines = ["Based on my review, here are my decisions:\n"]

        for i, decision in enumerate(decisions, 1):
            lines.append(f"{i}. {decision.interpretation}")

        lines.append("\nPlease proceed with implementing these decisions.")

        return "\n".join(lines)


class OutputFormatter:
    """Formats output in various formats (XML, JSON, Markdown)."""

    @staticmethod
    def format_analysis_xml(analysis: ConversationAnalysis) -> str:
        """Format analysis as XML."""
        root = ET.Element("analysis")

        context = ET.SubElement(root, "context")
        context.text = analysis.context

        open_items_elem = ET.SubElement(root, "open_items")
        for item in analysis.open_items:
            item_elem = ET.SubElement(open_items_elem, "item", priority=item.priority)

            desc = ET.SubElement(item_elem, "description")
            desc.text = item.description

            ctx = ET.SubElement(item_elem, "context")
            ctx.text = item.context

            if item.options:
                opts = ET.SubElement(item_elem, "options")
                opts.text = ", ".join(item.options)

        return OutputFormatter._prettify_xml(root)

    @staticmethod
    def format_summary_xml(summary: SessionSummary) -> str:
        """Format session summary as XML."""
        root = ET.Element("formal_response")

        # Session summary
        session_elem = ET.SubElement(root, "session_summary")

        conv_ctx = ET.SubElement(session_elem, "conversation_context")
        conv_ctx.text = summary.conversation_context

        items_addr = ET.SubElement(session_elem, "items_addressed")
        items_addr.text = f"{summary.items_addressed} of {summary.total_items} items discussed"

        duration = ET.SubElement(session_elem, "session_duration")
        duration.text = summary.session_duration

        # Decisions
        decisions_elem = ET.SubElement(root, "decisions")
        for decision in summary.decisions:
            dec_elem = ET.SubElement(decisions_elem, "decision")

            q = ET.SubElement(dec_elem, "question")
            q.text = decision.question

            resp = ET.SubElement(dec_elem, "user_response")
            resp.text = decision.user_response

            interp = ET.SubElement(dec_elem, "interpretation")
            interp.text = decision.interpretation

            actions = ET.SubElement(dec_elem, "action_items")
            actions.text = "; ".join(decision.action_items)

        # Deferred items
        if summary.deferred_items:
            deferred_elem = ET.SubElement(root, "deferred_items")
            for item in summary.deferred_items:
                item_elem = ET.SubElement(deferred_elem, "item")
                item_elem.text = item

        # Recommended message
        rec_msg = ET.SubElement(root, "recommended_next_message")
        rec_msg.text = summary.recommended_next_message

        return OutputFormatter._prettify_xml(root)

    @staticmethod
    def format_summary_json(summary: SessionSummary) -> str:
        """Format session summary as JSON."""
        data = {
            "session_summary": {
                "conversation_context": summary.conversation_context,
                "items_addressed": summary.items_addressed,
                "total_items": summary.total_items,
                "session_duration": summary.session_duration
            },
            "decisions": [
                {
                    "question": d.question,
                    "user_response": d.user_response,
                    "interpretation": d.interpretation,
                    "action_items": d.action_items
                } for d in summary.decisions
            ],
            "deferred_items": summary.deferred_items,
            "recommended_next_message": summary.recommended_next_message
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def format_summary_markdown(summary: SessionSummary) -> str:
        """Format session summary as Markdown."""
        lines = [
            "# Conversation Review Session Summary",
            "",
            "## Session Overview",
            f"- **Context**: {summary.conversation_context}",
            f"- **Items Addressed**: {summary.items_addressed} of {summary.total_items}",
            f"- **Duration**: {summary.session_duration}",
            "",
            "## Decisions Made",
            ""
        ]

        for i, decision in enumerate(summary.decisions, 1):
            lines.extend([
                f"### {i}. {decision.question[:100]}...",
                f"**Your Response**: {decision.user_response}",
                "",
                f"**Interpretation**: {decision.interpretation}",
                "",
                "**Action Items**:",
            ])
            for action in decision.action_items:
                lines.append(f"- {action}")
            lines.append("")

        if summary.deferred_items:
            lines.extend([
                "## Deferred Items",
                ""
            ])
            for item in summary.deferred_items:
                lines.append(f"- {item}")
            lines.append("")

        lines.extend([
            "## Recommended Next Message",
            "",
            "```",
            summary.recommended_next_message,
            "```"
        ])

        return "\n".join(lines)

    @staticmethod
    def _prettify_xml(elem: ET.Element) -> str:
        """Return a pretty-printed XML string."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def main():
    """Main entry point for CLI usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: conversation_review_agent.py <conversation_file_or_json>")
        print("       conversation_review_agent.py --interactive <conversation_file>")
        sys.exit(1)

    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    file_arg = [arg for arg in sys.argv[1:] if not arg.startswith('-')]

    if not file_arg:
        print("Error: No conversation file specified")
        sys.exit(1)

    conversation_path = file_arg[0]

    try:
        # Parse conversation
        parser = ConversationParser()
        conversation = parser.parse_file(conversation_path)

        # Analyze
        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze(conversation)

        # Display analysis
        print(OutputFormatter.format_analysis_xml(analysis))

        # Conduct interactive session
        facilitator = VoiceInteractionFacilitator(interactive=interactive)
        summary = facilitator.conduct_session(analysis)

        # Display summary
        print("\n" + "="*70)
        print("SESSION COMPLETE")
        print("="*70)
        print(OutputFormatter.format_summary_markdown(summary))

        # Save outputs
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        xml_file = output_dir / f"summary_{timestamp}.xml"
        json_file = output_dir / f"summary_{timestamp}.json"
        md_file = output_dir / f"summary_{timestamp}.md"

        xml_file.write_text(OutputFormatter.format_summary_xml(summary))
        json_file.write_text(OutputFormatter.format_summary_json(summary))
        md_file.write_text(OutputFormatter.format_summary_markdown(summary))

        print(f"\n✓ Outputs saved to:")
        print(f"  - {xml_file}")
        print(f"  - {json_file}")
        print(f"  - {md_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
