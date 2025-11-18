# Example Workflow: Rate Limiting Implementation

This example demonstrates a complete validation loop for implementing rate limiting on API endpoints.

## Initial Task

**Given to Agent A:** "Implement rate limiting for our REST API to prevent abuse. Focus on authentication endpoints first."

---

## Iteration 1

### Agent A Output

```
I've implemented rate limiting using Redis-based token bucket algorithm for authentication endpoints.

The implementation includes:
- Configurable rate limits per endpoint
- Redis for distributed rate limiting (works across multiple servers)
- Custom middleware for Express.js
- Clear error responses when rate limit exceeded
- Tests for rate limiting logic

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Implemented token bucket rate limiting using Redis for authentication endpoints with configurable limits",
    "files_modified": [
      "src/middleware/rate_limiter.js",
      "src/config/rate_limits.js",
      "src/app.js",
      "tests/middleware/test_rate_limiter.js"
    ],
    "key_decisions": [
      "Used token bucket algorithm for smooth rate limiting vs fixed window",
      "Chose Redis for storage to support distributed deployments",
      "Set default limit to 5 requests/minute for auth endpoints based on typical user behavior",
      "Return 429 status code with Retry-After header per RFC 6585"
    ]
  },
  "validation_request": "Please review for correctness, security, and potential race conditions in the Redis token bucket implementation",
  "concerns": [
    "Wondering if 5 req/min is too restrictive for legitimate users",
    "Not sure if we need separate limits for different auth operations (login vs password reset)"
  ]
}
==END_AGENT_OUTPUT==
```

### Orchestrator Processing

```bash
$ orchestrator process-output A
```

**Output:**
```
[ORCHESTRATOR] Handoff detected from Agent A

Work Product: Token bucket rate limiting with Redis
Status: awaiting_validation
Validation Request: Correctness, security, race conditions

[ORCHESTRATOR] Generated prompt for Agent B:
============================================================
[Full Agent B prompt with handoff details...]
============================================================

Copy the prompt above and paste into Agent B's Claude Code terminal.
```

### Agent B Output

```
I've reviewed the rate limiting implementation and found several issues that need to be addressed.

File inspection:
- src/middleware/rate_limiter.js: 95 lines
- src/config/rate_limits.js: 20 lines
- tests/middleware/test_rate_limiter.js: 150 lines

Issues found:
1. Race condition in token bucket check-and-decrement
2. No handling for Redis connection failures
3. Hard-coded Redis host (not configurable)
4. Missing test for distributed scenario

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "timestamp": "2025-01-17T10:15:00Z",
  "issues": [
    {
      "severity": "high",
      "category": "correctness",
      "description": "Race condition between GET and DECR operations on token bucket",
      "location": "src/middleware/rate_limiter.js:45-50",
      "impact": "Multiple concurrent requests could bypass rate limit by reading token count before it's decremented"
    },
    {
      "severity": "medium",
      "category": "correctness",
      "description": "No fallback behavior when Redis is unavailable",
      "location": "src/middleware/rate_limiter.js:30",
      "impact": "Application will fail all requests if Redis is down instead of gracefully degrading"
    },
    {
      "severity": "medium",
      "category": "security",
      "description": "Rate limit key uses user-provided IP address without validation",
      "location": "src/middleware/rate_limiter.js:38",
      "impact": "Attacker could spoof X-Forwarded-For header to bypass rate limiting"
    },
    {
      "severity": "low",
      "category": "correctness",
      "description": "Redis connection URL hard-coded instead of from environment config",
      "location": "src/middleware/rate_limiter.js:12",
      "impact": "Cannot configure for different environments"
    }
  ],
  "required_changes": [
    "Use Redis Lua script or MULTI/EXEC transaction to make token check and decrement atomic",
    "Implement circuit breaker pattern for Redis: if unavailable, allow requests (fail open) with logging",
    "Trust only server-detected IP (req.connection.remoteAddress) not headers, or validate proxy chain",
    "Move Redis URL to environment variable with fallback to localhost for dev"
  ],
  "recommendations": [
    "Add test case simulating concurrent requests to verify race condition fix",
    "Consider adding rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining) per draft RFC",
    "Add metrics/logging for rate limit hits to monitor abuse patterns",
    "Document rate limiting behavior in API documentation"
  ],
  "verdict_rationale": "Core implementation approach is sound (token bucket + Redis), but the race condition is a significant correctness issue and the IP spoofing is a security concern. Changes are specific and straightforward to implement."
}
==END_VALIDATION_FEEDBACK==
```

### Orchestrator Processing

```bash
$ orchestrator process-output B
```

**Output:**
```
[ORCHESTRATOR] Validation received: APPROVED_WITH_CHANGES

============================================================
PROMPT FOR AGENT A (EXECUTOR)
============================================================
[Full Agent A prompt with validation feedback...]
============================================================

Next Step:
  1. Copy the prompt above
  2. Paste into Agent A's Claude Code terminal
  3. Address required changes
  4. Resubmit with: orchestrator process-output A
```

---

## Iteration 2

### Agent A Output

```
I've addressed all the required changes from the validation feedback:

1. Fixed race condition using Redis Lua script for atomic check-and-decrement
2. Implemented circuit breaker for Redis failures (fails open with logging)
3. Changed IP detection to use trusted req.ip instead of headers
4. Moved Redis URL to environment variable

I also implemented the recommended rate limit headers and added concurrent request tests.

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Fixed race condition with Lua script, added circuit breaker for Redis failures, secured IP detection, and made Redis URL configurable",
    "files_modified": [
      "src/middleware/rate_limiter.js",
      "src/middleware/rate_limiter.lua",
      "src/config/redis.js",
      "tests/middleware/test_rate_limiter.js",
      "tests/middleware/test_race_condition.js"
    ],
    "key_decisions": [
      "Used Redis Lua script (EVALSHA) for atomic operations - guarantees no race conditions",
      "Circuit breaker fails open (allows requests) when Redis down to prevent total outage",
      "Trust Express trust proxy setting for IP detection - prevents header spoofing",
      "Added X-RateLimit-* headers following GitHub API convention for transparency"
    ]
  },
  "validation_request": "Please verify that race condition is properly fixed and circuit breaker behavior is correct",
  "concerns": []
}
==END_AGENT_OUTPUT==
```

### Agent B Output

```
I've re-reviewed the rate limiting implementation after the changes.

All previous issues have been properly addressed:
- Lua script correctly implements atomic check-and-decrement ✓
- Circuit breaker properly logs and fails open on Redis errors ✓
- IP detection now uses trusted source ✓
- Redis URL configurable via environment ✓

The concurrent request test suite validates the race condition fix. Code quality is high with good documentation and error handling.

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T11:05:00Z",
  "issues": [],
  "required_changes": [],
  "recommendations": [
    "Consider adding Redis connection pooling for high-traffic scenarios",
    "Future enhancement: per-user rate limits in addition to per-IP"
  ],
  "verdict_rationale": "All required changes from previous iteration have been properly implemented. The Lua script eliminates the race condition, circuit breaker provides resilience, and IP detection is secure. Implementation is production-ready."
}
==END_VALIDATION_FEEDBACK==
```

### Orchestrator Processing

```bash
$ orchestrator process-output B
```

**Output:**
```
[ORCHESTRATOR] ✓ Work APPROVED by Agent B
Session complete!

Session Summary:
  Total Iterations: 2
  Total Handoffs: 2
  Total Validations: 2
```

---

## Key Takeaways

### What Went Well

1. **Agent A** provided comprehensive handoffs with clear decisions
2. **Agent B** gave specific, actionable feedback with severity ratings
3. **Iteration 2** addressed all required changes thoroughly
4. **Communication** was structured and efficient through JSON markers

### Lessons Learned

- **First iteration** caught real issues (race condition, security flaw)
- **Specific feedback** helped Agent A fix issues without guessing
- **Verdict rationale** explained the decision clearly
- **Recommendations** distinguished nice-to-have from required changes

### Process Efficiency

- **Total time:** 2 iterations to approval
- **Issues caught:** 4 (1 high, 2 medium, 1 low severity)
- **Critical security/correctness issues** caught before deployment
- **Final quality:** Production-ready with all issues resolved

---

## Session Export

```bash
$ orchestrator export rate_limiting_session.json
Exported to: ai-duo-validator/sessions/rate_limiting_session.json
```

**Contents:**
```json
{
  "session_id": "session_20250117_100000",
  "started_at": "2025-01-17T10:00:00Z",
  "summary": {
    "total_iterations": 2,
    "total_handoffs": 2,
    "total_validations": 2,
    "final_status": "completed"
  },
  "history": [...]
}
```
