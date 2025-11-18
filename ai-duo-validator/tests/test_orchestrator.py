"""
Tests for orchestrator module.
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.orchestrator import AIOrchestrator
from src.parser import ParserError


# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures'


def load_fixture(filename):
    """Load a test fixture file."""
    filepath = FIXTURES_DIR / filename
    with open(filepath, 'r') as f:
        return f.read()


class TestOrchestratorBasics:
    """Tests for basic orchestrator functionality."""

    def test_orchestrator_initialization(self):
        """Test orchestrator initializes with default state."""
        orch = AIOrchestrator(auto_save=False)

        state = orch.get_state()
        assert state['iteration'] == 0
        assert state['total_handoffs'] == 0
        assert state['total_validations'] == 0
        assert state['status'] == 'initialized'
        assert state['active_agent'] is None

    def test_orchestrator_custom_session_id(self):
        """Test orchestrator with custom session ID."""
        orch = AIOrchestrator(session_id='test_session_123', auto_save=False)

        state = orch.get_state()
        assert state['session_id'] == 'test_session_123'

    def test_get_next_agent_initial(self):
        """Test get_next_agent returns None initially."""
        orch = AIOrchestrator(auto_save=False)

        assert orch.get_next_agent() is None

    def test_is_complete_initial(self):
        """Test is_complete returns False initially."""
        orch = AIOrchestrator(auto_save=False)

        assert not orch.is_complete()


class TestProcessExecutorOutput:
    """Tests for processing Agent A (Executor) output."""

    def test_process_valid_executor_output(self):
        """Test processing valid Agent A handoff."""
        orch = AIOrchestrator(auto_save=False)
        output = load_fixture('agent_a_output_1.txt')

        prompt = orch.process_executor_output(output, verbose=False)

        assert prompt is not None
        assert 'Agent B' in prompt or 'Validator' in prompt

        state = orch.get_state()
        assert state['iteration'] == 1
        assert state['total_handoffs'] == 1
        assert state['active_agent'] == 'B'
        assert state['status'] == 'awaiting_validation'

    def test_process_executor_output_no_handoff(self):
        """Test processing Agent A output without handoff."""
        orch = AIOrchestrator(auto_save=False)
        output = "Just some regular output without markers"

        prompt = orch.process_executor_output(output, verbose=False)

        assert prompt is None

        state = orch.get_state()
        assert state['iteration'] == 0
        assert state['total_handoffs'] == 0

    def test_process_executor_output_malformed(self):
        """Test processing Agent A output with malformed JSON."""
        orch = AIOrchestrator(auto_save=False)
        output = load_fixture('malformed_output.txt')

        with pytest.raises(ParserError):
            orch.process_executor_output(output, verbose=False)

    def test_process_executor_output_updates_history(self):
        """Test that processing executor output adds to history."""
        orch = AIOrchestrator(auto_save=False)
        output = load_fixture('agent_a_output_1.txt')

        orch.process_executor_output(output, verbose=False)

        history = orch.get_history()
        assert len(history) == 1
        assert history[0]['type'] == 'handoff'
        assert history[0]['from_agent'] == 'A'
        assert history[0]['to_agent'] == 'B'


class TestProcessValidatorOutput:
    """Tests for processing Agent B (Validator) output."""

    def test_process_valid_validator_output_approved_with_changes(self):
        """Test processing validation with approved_with_changes verdict."""
        orch = AIOrchestrator(auto_save=False)

        # First process executor output
        executor_output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(executor_output, verbose=False)

        # Then process validator output
        validator_output = load_fixture('agent_b_output_1.txt')
        prompt = orch.process_validator_output(validator_output, verbose=False)

        assert prompt is not None
        assert 'Agent A' in prompt or 'Executor' in prompt

        state = orch.get_state()
        assert state['total_validations'] == 1
        assert state['active_agent'] == 'A'
        assert state['status'] == 'awaiting_fixes'

    def test_process_validator_output_approved(self):
        """Test processing validation with approved verdict."""
        orch = AIOrchestrator(auto_save=False)

        # Setup with executor output
        executor_output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(executor_output, verbose=False)

        # Process approved validation
        validator_output = """
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
        prompt = orch.process_validator_output(validator_output, verbose=False)

        assert prompt is None  # No further action needed

        state = orch.get_state()
        assert state['status'] == 'completed'
        assert state['active_agent'] is None
        assert orch.is_complete()

    def test_process_validator_output_rejected(self):
        """Test processing validation with rejected verdict."""
        orch = AIOrchestrator(auto_save=False)

        # Setup with executor output
        executor_output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(executor_output, verbose=False)

        # Process rejected validation
        validator_output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "rejected",
  "timestamp": "2025-01-17T10:00:00Z",
  "issues": [
    {
      "severity": "critical",
      "category": "security",
      "description": "Major flaw"
    }
  ],
  "required_changes": ["Redesign approach"],
  "recommendations": [],
  "verdict_rationale": "Fundamental issue"
}
==END_VALIDATION_FEEDBACK==
"""
        prompt = orch.process_validator_output(validator_output, verbose=False)

        assert prompt is not None

        state = orch.get_state()
        assert state['active_agent'] == 'A'
        assert state['status'] == 'awaiting_fixes'

    def test_process_validator_output_updates_history(self):
        """Test that processing validator output adds to history."""
        orch = AIOrchestrator(auto_save=False)

        # Setup
        executor_output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(executor_output, verbose=False)

        # Process validation
        validator_output = load_fixture('agent_b_output_1.txt')
        orch.process_validator_output(validator_output, verbose=False)

        history = orch.get_history()
        assert len(history) == 2
        assert history[1]['type'] == 'validation'
        assert history[1]['from_agent'] == 'B'


class TestValidationLoop:
    """Tests for complete validation loop."""

    def test_full_validation_loop_two_iterations(self):
        """Test complete loop with two iterations to approval."""
        orch = AIOrchestrator(auto_save=False)

        # Iteration 1: Agent A handoff
        a1_output = load_fixture('agent_a_output_1.txt')
        prompt = orch.process_executor_output(a1_output, verbose=False)
        assert prompt is not None
        assert orch.get_next_agent() == 'B'

        # Iteration 1: Agent B validation (changes needed)
        b1_output = load_fixture('agent_b_output_1.txt')
        prompt = orch.process_validator_output(b1_output, verbose=False)
        assert prompt is not None
        assert orch.get_next_agent() == 'A'

        # Iteration 2: Agent A fixes
        a2_output = """
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Fixed all issues from validation"
  },
  "validation_request": "Please verify fixes"
}
==END_AGENT_OUTPUT==
"""
        prompt = orch.process_executor_output(a2_output, verbose=False)
        assert prompt is not None
        assert orch.get_next_agent() == 'B'

        # Iteration 2: Agent B approval
        b2_output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T11:00:00Z",
  "issues": [],
  "required_changes": [],
  "recommendations": [],
  "verdict_rationale": "All issues resolved"
}
==END_VALIDATION_FEEDBACK==
"""
        prompt = orch.process_validator_output(b2_output, verbose=False)
        assert prompt is None
        assert orch.is_complete()

        state = orch.get_state()
        assert state['iteration'] == 2
        assert state['total_handoffs'] == 2
        assert state['total_validations'] == 2
        assert state['status'] == 'completed'

    def test_history_tracks_full_loop(self):
        """Test that history correctly tracks full validation loop."""
        orch = AIOrchestrator(auto_save=False)

        # Complete loop
        a_output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(a_output, verbose=False)

        b_output = """
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T10:00:00Z",
  "verdict_rationale": "Good work"
}
==END_VALIDATION_FEEDBACK==
"""
        orch.process_validator_output(b_output, verbose=False)

        history = orch.get_history()
        assert len(history) == 2

        # Check first entry (handoff)
        assert history[0]['type'] == 'handoff'
        assert history[0]['iteration'] == 1
        assert 'timestamp' in history[0]

        # Check second entry (validation)
        assert history[1]['type'] == 'validation'
        assert history[1]['iteration'] == 1
        assert 'timestamp' in history[1]


class TestSessionPersistence:
    """Tests for session save/load functionality."""

    def test_save_and_load_session(self):
        """Test saving and loading a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test_session.json')

            # Create and populate orchestrator
            orch1 = AIOrchestrator(session_id='test_save_load', auto_save=False)
            output = load_fixture('agent_a_output_1.txt')
            orch1.process_executor_output(output, verbose=False)

            # Save session
            orch1.save_session(filepath)

            # Load into new orchestrator
            orch2 = AIOrchestrator.load_session(filepath)

            # Verify state is preserved
            state1 = orch1.get_state()
            state2 = orch2.get_state()

            assert state2['session_id'] == state1['session_id']
            assert state2['iteration'] == state1['iteration']
            assert state2['total_handoffs'] == state1['total_handoffs']
            assert state2['status'] == state1['status']

            # Verify history is preserved
            history1 = orch1.get_history()
            history2 = orch2.get_history()
            assert len(history2) == len(history1)

    def test_export_history(self):
        """Test exporting session history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'history_export.json')

            orch = AIOrchestrator(auto_save=False)
            output = load_fixture('agent_a_output_1.txt')
            orch.process_executor_output(output, verbose=False)

            # Export history
            orch.export_history(filepath)

            # Verify file exists and contains data
            assert os.path.exists(filepath)

            import json
            with open(filepath, 'r') as f:
                exported = json.load(f)

            assert 'session_id' in exported
            assert 'summary' in exported
            assert 'history' in exported
            assert exported['summary']['total_handoffs'] == 1


class TestStatusSummary:
    """Tests for status summary functionality."""

    def test_get_status_summary(self):
        """Test getting status summary string."""
        orch = AIOrchestrator(auto_save=False)

        summary = orch.get_status_summary()

        assert isinstance(summary, str)
        assert 'SESSION STATUS' in summary
        assert 'Session ID' in summary

    def test_status_summary_after_handoff(self):
        """Test status summary reflects handoff state."""
        orch = AIOrchestrator(auto_save=False)
        output = load_fixture('agent_a_output_1.txt')
        orch.process_executor_output(output, verbose=False)

        summary = orch.get_status_summary()

        assert 'Active Agent: B' in summary or 'Active Agent: B' in summary
        assert 'Total Handoffs: 1' in summary
