"""
Main orchestrator class for AI-to-AI coordination.
"""

from typing import Optional, Dict
from .parser import extract_handoff, extract_validation, ParserError
from .state import SessionState
from .formatter import (
    format_handoff_for_validator,
    format_validation_for_executor,
    pretty_print_handoff,
    pretty_print_validation
)


class AIOrchestrator:
    """
    Orchestrator for coordinating validation between Agent A (Executor) and Agent B (Validator).
    """

    def __init__(self, session_id: Optional[str] = None, auto_save: bool = True):
        """
        Initialize orchestrator.

        Args:
            session_id: Optional session ID. If None, creates a new session.
            auto_save: Whether to automatically save session after each operation
        """
        self.state = SessionState(session_id)
        self.auto_save = auto_save
        self.sessions_dir = 'ai-duo-validator/sessions'

    def extract_handoff(self, output: str) -> Optional[Dict]:
        """
        Extract handoff JSON from Agent A output.

        Args:
            output: Raw terminal output from Agent A

        Returns:
            Parsed handoff dictionary or None if no valid handoff found

        Raises:
            ParserError: If handoff markers found but JSON is malformed
        """
        return extract_handoff(output)

    def extract_validation(self, output: str) -> Optional[Dict]:
        """
        Extract validation JSON from Agent B output.

        Args:
            output: Raw terminal output from Agent B

        Returns:
            Parsed validation dictionary or None if no valid validation found

        Raises:
            ParserError: If validation markers found but JSON is malformed
        """
        return extract_validation(output)

    def process_executor_output(self, output: str, verbose: bool = True) -> Optional[str]:
        """
        Process Agent A output and generate prompt for Agent B.

        Args:
            output: Raw terminal output from Agent A
            verbose: Whether to print handoff details

        Returns:
            Formatted prompt for Agent B, or None if no handoff found

        Raises:
            ParserError: If handoff found but malformed
        """
        # Extract handoff
        handoff = extract_handoff(output)

        if handoff is None:
            return None

        # Record in state
        self.state.record_handoff(handoff, output)

        # Auto-save if enabled
        if self.auto_save:
            self.state.auto_save(self.sessions_dir)

        # Pretty-print handoff if verbose
        if verbose:
            pretty_print_handoff(handoff)

        # Generate prompt for Agent B
        prompt = format_handoff_for_validator(handoff)

        return prompt

    def process_validator_output(self, output: str, verbose: bool = True) -> Optional[str]:
        """
        Process Agent B output and generate prompt for Agent A.

        Args:
            output: Raw terminal output from Agent B
            verbose: Whether to print validation details

        Returns:
            Formatted prompt for Agent A, or None if validation verdict is 'approved'

        Raises:
            ParserError: If validation found but malformed
        """
        # Extract validation
        validation = extract_validation(output)

        if validation is None:
            return None

        # Record in state
        self.state.record_validation(validation, output)

        # Auto-save if enabled
        if self.auto_save:
            self.state.auto_save(self.sessions_dir)

        # Pretty-print validation if verbose
        if verbose:
            pretty_print_validation(validation)

        # Generate prompt for Agent A if changes needed
        verdict = validation.get('verdict')

        if verdict == 'approved':
            return None  # Work is done, no further action needed

        # Generate prompt for Agent A to address feedback
        prompt = format_validation_for_executor(validation)

        return prompt

    def get_state(self) -> Dict:
        """
        Return current orchestrator state.

        Returns:
            Dictionary containing current session state
        """
        return self.state.get_state()

    def get_history(self) -> list:
        """
        Get full interaction history.

        Returns:
            List of history entries
        """
        return self.state.get_history()

    def export_history(self, filepath: str) -> None:
        """
        Export session history to file.

        Args:
            filepath: Path to export history
        """
        self.state.export_history(filepath)

    def save_session(self, filepath: str) -> None:
        """
        Save current session for later resume.

        Args:
            filepath: Path to save session
        """
        self.state.save_session(filepath)

    @classmethod
    def load_session(cls, filepath: str) -> 'AIOrchestrator':
        """
        Load a previously saved session.

        Args:
            filepath: Path to session file

        Returns:
            AIOrchestrator instance with loaded session
        """
        state = SessionState.load_session(filepath)
        orchestrator = cls(session_id=state.session_id, auto_save=False)
        orchestrator.state = state
        return orchestrator

    def is_complete(self) -> bool:
        """
        Check if the orchestration session is complete.

        Returns:
            True if work has been approved, False otherwise
        """
        return self.state.status == 'completed'

    def get_next_agent(self) -> Optional[str]:
        """
        Get the next agent that should act.

        Returns:
            'A' for Agent A (Executor), 'B' for Agent B (Validator), or None if complete
        """
        return self.state.active_agent

    def get_status_summary(self) -> str:
        """
        Get a human-readable status summary.

        Returns:
            Formatted status string
        """
        from .formatter import format_session_status
        return format_session_status(self.state.get_state())
