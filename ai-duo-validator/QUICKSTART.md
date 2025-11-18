# Quick Start Guide

## Try the Demo First!

We provide two demo scripts you can run immediately:

### Option 1: Automated Demo (No Input Required)

```bash
cd ai-duo-validator
python demo_auto.py
```

This runs a complete validation loop showing:
- Agent A implementing authentication
- Orchestrator extracting handoff
- Agent B finding 3 security issues
- Feedback loop and final approval

**Duration:** ~20 seconds

### Option 2: Interactive Demo (Step-by-Step)

```bash
cd ai-duo-validator
python demo.py
```

This shows the same workflow but lets you:
- Press ENTER to advance through steps
- See what's happening at each stage
- Read the actual prompts being generated

**Duration:** ~2-3 minutes

## What You'll See

Both demos use real test fixtures showing:

**Agent A Output:**
```
I've completed authentication implementation...

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "work_product": { ... },
  "validation_request": "Security review"
}
==END_AGENT_OUTPUT==
```

**Agent B Output:**
```
I found 3 security issues...

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "issues": [ ... ]
}
==END_VALIDATION_FEEDBACK==
```

## After the Demo

### 1. Read the Agent Prompts

```bash
cat prompts/agent_a_executor.md
cat prompts/agent_b_validator.md
```

These show exactly how to format agent communication.

### 2. Run Tests

```bash
pytest tests/ -v
```

All 40 tests should pass.

### 3. Try with Real Claude Code Terminals

```bash
# Terminal 1: Start orchestrator
./orchestrator start

# Terminal 2: Agent A (Executor)
# Paste: prompts/agent_a_executor.md

# Terminal 3: Agent B (Validator)
# Paste: prompts/agent_b_validator.md
```

Then follow the workflow:
1. Give Agent A a task
2. Capture Agent A's handoff: `./orchestrator process-output A`
3. Send prompt to Agent B
4. Capture Agent B's validation: `./orchestrator process-output B`
5. Repeat until approved

### 4. Read Full Examples

- `examples/rate_limiting_task.md` - Complete rate limiting implementation
- `examples/authentication_task.md` - JWT auth with security review

## Common Commands

```bash
# Start new session
./orchestrator start

# Process agent output
./orchestrator process-output A  # Agent A handoff
./orchestrator process-output B  # Agent B validation

# Check status
./orchestrator status
./orchestrator history

# Save/load sessions
./orchestrator save my_session.json
./orchestrator load my_session.json

# Export history
./orchestrator export
```

## Troubleshooting

**No markers detected?**
- Verify agent prompt was fully pasted
- Check JSON is valid (no syntax errors)
- Ensure both markers are present

**Malformed JSON?**
- Check for missing commas
- Use double quotes (not single)
- No trailing commas
- No comments in JSON

## What's Next?

1. **Try real validation:** Use with actual Claude Code terminals
2. **Read examples:** See complete workflows in `examples/`
3. **Customize prompts:** Adapt agent prompts for your use case
4. **Share results:** Show us what you validate!

## Quick Tips

✅ **Do:**
- Read the agent prompts first
- Start with the demos
- Use test fixtures to understand format
- Save sessions for complex work

❌ **Don't:**
- Skip the demos (they're quick!)
- Try to memorize JSON schema (agents do this)
- Forget to paste complete agent prompts
- Give up if first try isn't perfect

---

**Need help?** Check the full README.md or review examples/
