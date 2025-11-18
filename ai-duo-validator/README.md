# AI Duo Validator

> Orchestrate validation between two AI agents for higher quality code

AI Duo Validator is an orchestration framework that coordinates validation between two Claude Code agents:
- **Agent A (Executor)**: Implements solutions and writes code
- **Agent B (Validator)**: Reviews work, finds issues, validates quality

The orchestrator parses terminal output, extracts structured handoffs, and routes messages between agents through a CLI interface.

## 🚀 Try It Now! (30 seconds)

**Run the automated demo to see it in action:**

```bash
cd ai-duo-validator
pip install -r requirements.txt
python demo_auto.py
```

**Or try the interactive demo:**

```bash
python demo.py
```

Both demos show a complete validation loop using real test fixtures. See [QUICKSTART.md](QUICKSTART.md) for details.

## Why AI Duo Validator?

**Single AI Agent Limitations:**
- May miss security vulnerabilities
- No second opinion on design decisions
- Can develop blind spots

**AI Duo Benefits:**
- Catches critical issues before deployment
- Second pair of eyes on security/correctness
- Enforces quality standards through validation loop
- Knowledge transfer between agents

**Real Results from Examples:**
- JWT Auth: Caught 5 security vulnerabilities (2 critical) in 2 iterations
- Rate Limiting: Prevented race condition and IP spoofing vulnerabilities

## Quick Start (5 Minutes)

### 1. Installation

```bash
cd ai-duo-validator
pip install -r requirements.txt
```

### 2. Start Orchestrator

```bash
./orchestrator start
```

### 3. Open Two Claude Code Terminals

**Terminal 1 (Agent A - Executor):**
- Paste the Agent A prompt from `prompts/agent_a_executor.md`

**Terminal 2 (Agent B - Validator):**
- Paste the Agent B prompt from `prompts/agent_b_validator.md`

### 4. Give Agent A a Task

In Terminal 1:
```
Implement JWT authentication with token refresh
```

### 5. Capture Agent A's Handoff

When Agent A emits `==BEGIN_AGENT_OUTPUT==` markers:

```bash
./orchestrator process-output A
# Paste Agent A's full output
# Press Ctrl+D
```

### 6. Send to Agent B

Copy the generated prompt and paste into Terminal 2 (Agent B).

### 7. Capture Agent B's Validation

When Agent B emits `==VALIDATION_FEEDBACK==` markers:

```bash
./orchestrator process-output B
# Paste Agent B's full output
# Press Ctrl+D
```

### 8. Continue Loop

Repeat steps 5-7 until Agent B approves the work.

## How It Works

### Communication Flow

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Agent A    │────────>│ Orchestrator │────────>│  Agent B    │
│ (Executor)  │ Handoff │              │ Prompt  │ (Validator) │
└─────────────┘         └──────────────┘         └─────────────┘
       ^                                                  │
       │                                                  │
       └──────────────────Feedback───────────────────────┘
```

### Structured Markers

Agents communicate through JSON markers in terminal output:

**Agent A Handoff:**
```
==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": { ... },
  "validation_request": "Security review needed"
}
==END_AGENT_OUTPUT==
```

**Agent B Validation:**
```
==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "issues": [ ... ],
  "required_changes": [ ... ]
}
==END_VALIDATION_FEEDBACK==
```

### Validation Loop

1. **Agent A** completes work → emits handoff
2. **Orchestrator** extracts handoff → generates prompt for Agent B
3. **Agent B** reviews work → emits validation feedback
4. **Orchestrator** extracts feedback → generates prompt for Agent A
5. **Agent A** addresses issues → resubmits
6. Loop continues until **Agent B** approves (verdict: "approved")

## CLI Reference

### Commands

#### `./orchestrator start`
Start a new orchestration session.

```bash
./orchestrator start
```

#### `./orchestrator process-output <agent>`
Process output from Agent A or B.

```bash
# Process Agent A output
./orchestrator process-output A
[Paste output, then Ctrl+D]

# Process Agent B output
./orchestrator process-output B
[Paste output, then Ctrl+D]

# Load specific session
./orchestrator process-output A --session sessions/my_session.json
```

#### `./orchestrator status`
Show current session status.

```bash
./orchestrator status
```

**Output:**
```
============================================================
SESSION STATUS
============================================================

Session ID: session_20250117_140000
Started: 2025-01-17T14:00:00
Status: awaiting_validation

Active Agent: B
Current Iteration: 1
Total Handoffs: 1
Total Validations: 0
```

#### `./orchestrator history`
Show session history.

```bash
# Brief history
./orchestrator history

# Full history with raw outputs
./orchestrator history --full
```

#### `./orchestrator save [filepath]`
Save current session.

```bash
# Auto-named in sessions/
./orchestrator save

# Custom path
./orchestrator save my_session.json
```

#### `./orchestrator load <filepath>`
Load a saved session.

```bash
./orchestrator load sessions/session_20250117_140000.json
```

#### `./orchestrator export [filepath]`
Export session history with summary.

```bash
# Auto-named
./orchestrator export

# Custom path
./orchestrator export jwt_auth_session.json
```

## Agent Prompts

### Agent A (Executor)

**Location:** `prompts/agent_a_executor.md`

**Role:**
- Implement features and fixes
- Make technical decisions
- Emit handoffs when work is ready
- Respond to validation feedback

**Key Responsibilities:**
- Only emit handoffs for substantial, complete work
- Include file paths, decisions, and concerns
- Address all required changes from validation
- Iterate until approval

[Full prompt in `prompts/agent_a_executor.md`]

### Agent B (Validator)

**Location:** `prompts/agent_b_validator.md`

**Role:**
- Review work for security, correctness, performance
- Categorize issues by severity and category
- Provide specific, actionable feedback
- Make verdict decisions (approved/changes/rejected)

**Key Responsibilities:**
- Thorough inspection using available tools
- Distinguish required changes from recommendations
- Be constructive and fair
- Verify previous issues are fixed in iterations

[Full prompt in `prompts/agent_b_validator.md`]

## JSON Schemas

### Handoff Schema (Agent A)

```json
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code|analysis|config|document",
    "description": "Brief description",
    "files_modified": ["path/to/file1.py"],
    "key_decisions": ["Decision with rationale"]
  },
  "validation_request": "What needs validation",
  "concerns": ["Optional concerns"]
}
```

**Required Fields:**
- `agent`: Always "A"
- `status`: Always "awaiting_validation" for handoffs
- `work_product.type`: One of: code, analysis, config, document
- `work_product.description`: 1-2 sentences
- `validation_request`: Specific validation request

### Validation Schema (Agent B)

```json
{
  "from": "B",
  "verdict": "approved|approved_with_changes|rejected",
  "timestamp": "2025-01-17T14:30:00Z",
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "category": "security|correctness|performance|style",
      "description": "Clear description",
      "location": "file.py:line",
      "impact": "What could go wrong"
    }
  ],
  "required_changes": ["Change 1", "Change 2"],
  "recommendations": ["Optional improvement"],
  "verdict_rationale": "Explanation of verdict"
}
```

**Verdicts:**
- `approved`: Work is good, session ends
- `approved_with_changes`: Specific fixes needed, loop continues
- `rejected`: Major issues, different approach needed

## Examples

### Example 1: Rate Limiting

**Full walkthrough:** `examples/rate_limiting_task.md`

**Summary:**
- **Task**: Implement rate limiting for API
- **Iterations**: 2
- **Issues Caught**: Race condition, Redis failure handling, IP spoofing
- **Outcome**: Production-ready implementation

### Example 2: JWT Authentication

**Full walkthrough:** `examples/authentication_task.md`

**Summary:**
- **Task**: Implement JWT authentication
- **Iterations**: 2
- **Issues Caught**: 5 security vulnerabilities (2 critical)
  - None algorithm attack (critical)
  - No token revocation (high)
  - Missing refresh token rotation (medium)
- **Outcome**: Secure, production-ready auth system

## Testing

### Run All Tests

```bash
cd ai-duo-validator
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test Module

```bash
# Test parser
pytest tests/test_parser.py

# Test orchestrator
pytest tests/test_orchestrator.py
```

### Test Structure

```
tests/
├── __init__.py
├── test_parser.py          # Parser extraction tests
├── test_orchestrator.py    # Orchestrator logic tests
└── fixtures/               # Test data
    ├── agent_a_output_1.txt
    ├── agent_b_output_1.txt
    └── malformed_output.txt
```

## Project Structure

```
ai-duo-validator/
├── orchestrator              # Main CLI entry point
├── setup.py                 # Package installation
├── requirements.txt         # Dependencies
├── README.md                # This file
├── src/
│   ├── __init__.py
│   ├── orchestrator.py      # Core orchestrator class
│   ├── cli.py              # CLI interface
│   ├── parser.py           # Output parsing
│   ├── formatter.py        # Prompt formatting
│   └── state.py            # State management
├── prompts/
│   ├── agent_a_executor.md  # Agent A prompt
│   └── agent_b_validator.md # Agent B prompt
├── examples/
│   ├── rate_limiting_task.md
│   └── authentication_task.md
├── tests/
│   ├── test_parser.py
│   ├── test_orchestrator.py
│   └── fixtures/
└── sessions/               # Runtime session storage
```

## Troubleshooting

### No Handoff Detected

**Problem:** Orchestrator says "No handoff detected"

**Solutions:**
1. Verify Agent A included both markers: `==BEGIN_AGENT_OUTPUT==` and `==END_AGENT_OUTPUT==`
2. Check JSON is valid (use a JSON validator)
3. Ensure all required fields are present
4. Make sure you pasted the complete output

### Malformed JSON Error

**Problem:** `ParserError: Invalid JSON in handoff`

**Solutions:**
1. Check for missing commas in JSON
2. Verify all strings use double quotes (not single)
3. Ensure no trailing commas
4. No comments allowed in JSON (remove `//` or `/* */`)

### Session Not Saving

**Problem:** Auto-save not working

**Solutions:**
1. Check `sessions/` directory exists (should be auto-created)
2. Verify write permissions
3. Use manual save: `./orchestrator save`

### Agent Not Following Format

**Problem:** Agent outputs don't contain markers

**Solutions:**
1. Verify agent prompt was fully pasted
2. Check agent understood the marker format requirement
3. Explicitly ask agent: "Please emit handoff using the markers"
4. Show agent an example from the prompt

## Advanced Usage

### Custom Session Management

```bash
# Start with custom ID
./orchestrator start --session-id my_feature_v1

# Save at specific point
./orchestrator save checkpoints/before_refactor.json

# Load and continue
./orchestrator load checkpoints/before_refactor.json
./orchestrator process-output A
```

### Batch Processing

```bash
# Process multiple iterations
for i in {1..3}; do
    echo "Iteration $i"
    ./orchestrator process-output A < agent_a_output_$i.txt
    ./orchestrator process-output B < agent_b_output_$i.txt
done
```

### Integration with CI/CD

```python
from src.orchestrator import AIOrchestrator

# In your CI pipeline
orch = AIOrchestrator(session_id='ci_run_123')

# Process executor output
with open('agent_a_output.txt') as f:
    executor_output = f.read()
    prompt = orch.process_executor_output(executor_output)

# Process validator output
with open('agent_b_output.txt') as f:
    validator_output = f.read()
    prompt = orch.process_validator_output(validator_output)

# Check if approved
if orch.is_complete():
    print("✓ Validation passed")
    exit(0)
else:
    print("✗ Changes required")
    exit(1)
```

## Extension Ideas (Phase 2)

### Planned Enhancements

1. **Gemini Integration**
   - Support for Google Gemini agents
   - Multi-model validation

2. **Visual Validation**
   - Screenshot comparison
   - UI/UX review workflows

3. **Automated Fixes**
   - Agent A auto-applies simple fixes
   - Diff-based change verification

4. **Multi-Agent Support**
   - More than 2 agents in validation chain
   - Specialist validators (security, performance, etc.)

5. **Metrics Dashboard**
   - Track validation success rates
   - Issue heatmaps
   - Agent performance analytics

## Contributing

Contributions welcome! Areas for improvement:

- Additional agent prompts for specialized tasks
- More example workflows
- Integration with other AI platforms
- UI/dashboard for session visualization

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-duo-validator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-duo-validator/discussions)
- **Examples**: See `examples/` directory

---

**Built for coordinating AI agents to produce higher quality code through structured validation loops.**
