"""
State management module for orchestrator sessions.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class SessionState:
    """Manages orchestrator session state and persistence."""

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize session state.

        Args:
            session_id: Unique session identifier. If None, generates a new one.
        """
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.session_id = session_id
        self.started_at = datetime.now().isoformat()
        self.active_agent: Optional[str] = None  # 'A' or 'B'
        self.iteration = 0
        self.total_handoffs = 0
        self.total_validations = 0
        self.history: List[Dict] = []
        self.current_handoff: Optional[Dict] = None
        self.current_validation: Optional[Dict] = None
        self.status = 'initialized'  # initialized, awaiting_validation, awaiting_fixes, completed

    def record_handoff(self, handoff: Dict, agent_output: str) -> None:
        """
        Record a handoff from Agent A.

        Args:
            handoff: Parsed handoff dictionary
            agent_output: Raw agent output (for logging)
        """
        self.current_handoff = handoff
        self.active_agent = 'B'  # Now waiting for Agent B
        self.status = 'awaiting_validation'
        self.total_handoffs += 1
        self.iteration += 1

        self.history.append({
            'type': 'handoff',
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat(),
            'from_agent': 'A',
            'to_agent': 'B',
            'handoff': handoff,
            'raw_output': agent_output
        })

    def record_validation(self, validation: Dict, agent_output: str) -> None:
        """
        Record a validation from Agent B.

        Args:
            validation: Parsed validation dictionary
            agent_output: Raw agent output (for logging)
        """
        self.current_validation = validation
        self.total_validations += 1

        verdict = validation.get('verdict')

        if verdict == 'approved':
            self.active_agent = None
            self.status = 'completed'
        else:
            self.active_agent = 'A'  # Agent A needs to make changes
            self.status = 'awaiting_fixes'

        self.history.append({
            'type': 'validation',
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat(),
            'from_agent': 'B',
            'to_agent': 'A' if verdict != 'approved' else None,
            'validation': validation,
            'raw_output': agent_output
        })

    def get_state(self) -> Dict:
        """
        Get current state as dictionary.

        Returns:
            Dictionary containing current session state
        """
        return {
            'session_id': self.session_id,
            'started_at': self.started_at,
            'active_agent': self.active_agent,
            'iteration': self.iteration,
            'total_handoffs': self.total_handoffs,
            'total_validations': self.total_validations,
            'status': self.status,
            'current_handoff': self.current_handoff,
            'current_validation': self.current_validation,
            'history_count': len(self.history)
        }

    def get_history(self) -> List[Dict]:
        """
        Get full session history.

        Returns:
            List of history entries
        """
        return self.history

    def save_session(self, filepath: str) -> None:
        """
        Save session to file.

        Args:
            filepath: Path to save session JSON
        """
        session_data = {
            'session_id': self.session_id,
            'started_at': self.started_at,
            'active_agent': self.active_agent,
            'iteration': self.iteration,
            'total_handoffs': self.total_handoffs,
            'total_validations': self.total_validations,
            'status': self.status,
            'current_handoff': self.current_handoff,
            'current_validation': self.current_validation,
            'history': self.history
        }

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

    @classmethod
    def load_session(cls, filepath: str) -> 'SessionState':
        """
        Load session from file.

        Args:
            filepath: Path to session JSON file

        Returns:
            SessionState instance loaded from file
        """
        with open(filepath, 'r') as f:
            session_data = json.load(f)

        # Create new instance
        state = cls(session_id=session_data['session_id'])

        # Restore state
        state.started_at = session_data['started_at']
        state.active_agent = session_data['active_agent']
        state.iteration = session_data['iteration']
        state.total_handoffs = session_data['total_handoffs']
        state.total_validations = session_data['total_validations']
        state.status = session_data['status']
        state.current_handoff = session_data['current_handoff']
        state.current_validation = session_data['current_validation']
        state.history = session_data['history']

        return state

    def export_history(self, filepath: str) -> None:
        """
        Export history to file with formatted output.

        Args:
            filepath: Path to export history
        """
        export_data = {
            'session_id': self.session_id,
            'started_at': self.started_at,
            'summary': {
                'total_iterations': self.iteration,
                'total_handoffs': self.total_handoffs,
                'total_validations': self.total_validations,
                'final_status': self.status
            },
            'history': self.history
        }

        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

    def auto_save(self, sessions_dir: str = 'sessions') -> None:
        """
        Automatically save session to sessions directory.

        Args:
            sessions_dir: Directory to save sessions
        """
        filepath = os.path.join(sessions_dir, f"{self.session_id}.json")
        self.save_session(filepath)
