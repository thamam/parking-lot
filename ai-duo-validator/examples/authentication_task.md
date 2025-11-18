# Example Workflow: JWT Authentication Implementation

This example demonstrates validation workflow for implementing JWT authentication with security review.

## Initial Task

**Given to Agent A:** "Implement JWT-based authentication for the user API. Include token refresh mechanism and secure secret management."

---

## Iteration 1

### Agent A Output

```
I've implemented JWT authentication with access tokens and refresh tokens.

Implementation includes:
- JWT generation and validation with RS256 (asymmetric keys)
- Access token (15 min) and refresh token (7 days) pattern
- Middleware for protecting routes
- Token refresh endpoint
- Secrets loaded from environment variables
- Comprehensive test coverage

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "JWT authentication system with RS256 signing, token refresh, and environment-based secret management",
    "files_modified": [
      "src/auth/jwt_service.py",
      "src/auth/middleware.py",
      "src/auth/refresh_handler.py",
      "src/config/secrets.py",
      "tests/auth/test_jwt_auth.py",
      ".env.example"
    ],
    "key_decisions": [
      "Used RS256 (asymmetric) instead of HS256 - allows public key distribution for token verification",
      "15-minute access token with 7-day refresh token based on OWASP JWT cheatsheet",
      "Store secrets in environment variables, fail fast on startup if missing",
      "Refresh tokens stored in secure HTTP-only cookies"
    ]
  },
  "validation_request": "Security review: Please validate token generation, signature verification, secret management, and protection against common JWT vulnerabilities (none algorithm, key confusion, signature bypass)",
  "concerns": [
    "Should refresh tokens be rotated on each use?",
    "15-minute access token might be too short for UX"
  ]
}
==END_AGENT_OUTPUT==
```

### Agent B Output

```
I've reviewed the JWT authentication implementation with focus on security.

File inspection completed:
- src/auth/jwt_service.py: 180 lines
- src/auth/middleware.py: 95 lines
- src/auth/refresh_handler.py: 60 lines
- tests/auth/test_jwt_auth.py: 220 lines

Security analysis:
✓ RS256 properly configured
✓ Secrets validated at startup
✓ Token expiry implemented
✗ Several security issues found

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved_with_changes",
  "timestamp": "2025-01-17T14:00:00Z",
  "issues": [
    {
      "severity": "high",
      "category": "security",
      "description": "Token signature verification missing algorithm whitelist - vulnerable to 'none' algorithm attack",
      "location": "src/auth/jwt_service.py:67",
      "impact": "Attacker could forge tokens by changing algorithm to 'none', bypassing signature verification"
    },
    {
      "severity": "high",
      "category": "security",
      "description": "No logout mechanism - tokens remain valid until expiration",
      "location": "general",
      "impact": "Stolen tokens can't be invalidated, security breach window is 7 days (refresh token lifetime)"
    },
    {
      "severity": "medium",
      "category": "security",
      "description": "Refresh token not rotated on use",
      "location": "src/auth/refresh_handler.py:35",
      "impact": "If refresh token is stolen, attacker has extended access period"
    },
    {
      "severity": "medium",
      "category": "correctness",
      "description": "JWT library version not pinned in requirements.txt",
      "location": "requirements.txt:8",
      "impact": "Could pull version with known vulnerabilities"
    },
    {
      "severity": "low",
      "category": "security",
      "description": "No rate limiting on token refresh endpoint",
      "location": "src/auth/refresh_handler.py:20",
      "impact": "Attacker could brute force refresh tokens"
    }
  ],
  "required_changes": [
    "Add explicit algorithm=['RS256'] parameter to jwt.decode() to prevent algorithm confusion attacks",
    "Implement token blacklist using Redis with TTL matching token expiry for logout support",
    "Implement refresh token rotation: issue new refresh token on each use, invalidate old one",
    "Pin PyJWT version to specific version (check for latest without CVEs)"
  ],
  "recommendations": [
    "Add rate limiting to token refresh endpoint (5 requests/hour)",
    "Consider implementing token binding to user session for additional security",
    "Add security tests specifically for: none algorithm, expired token, algorithm confusion",
    "Log all refresh token usage for security monitoring",
    "Add jti (JWT ID) claim for better token tracking"
  ],
  "verdict_rationale": "Core JWT implementation is solid with good cryptographic choices (RS256, proper expiry). However, missing algorithm whitelist is a critical security vulnerability (CVE-class issue). Token revocation is also important for security. These are well-known issues with straightforward fixes."
}
==END_VALIDATION_FEEDBACK==
```

---

## Iteration 2

### Agent A Output

```
I've addressed all the security issues from the validation:

1. Added algorithm whitelist to jwt.decode() - prevents none algorithm attack
2. Implemented Redis-based token blacklist for logout
3. Added refresh token rotation (new token issued, old invalidated)
4. Pinned PyJWT to 2.8.0 (latest stable, no known CVEs)
5. Added rate limiting to refresh endpoint (5/hour)
6. Implemented security test suite for JWT vulnerabilities

All required changes completed plus the recommended security tests.

==BEGIN_AGENT_OUTPUT==
{
  "agent": "A",
  "status": "awaiting_validation",
  "work_product": {
    "type": "code",
    "description": "Fixed JWT security vulnerabilities: algorithm whitelist, token blacklist for logout, refresh token rotation, pinned dependencies, rate limiting",
    "files_modified": [
      "src/auth/jwt_service.py",
      "src/auth/blacklist.py",
      "src/auth/refresh_handler.py",
      "requirements.txt",
      "tests/auth/test_jwt_security.py",
      "tests/auth/test_jwt_auth.py"
    ],
    "key_decisions": [
      "Redis for token blacklist with TTL - automatic cleanup of expired tokens",
      "Refresh token rotation with 1-hour grace period for concurrent requests",
      "Algorithm whitelist set to ['RS256'] only - no other algorithms accepted",
      "Rate limiting via decorator (5 refreshes per hour per user) to prevent abuse"
    ]
  },
  "validation_request": "Please verify all security issues are properly addressed, especially algorithm whitelist and token revocation",
  "concerns": []
}
==END_AGENT_OUTPUT==
```

### Agent B Output

```
I've re-reviewed the JWT authentication implementation after security fixes.

Verification completed:
✓ Algorithm whitelist properly configured (lines 67, 89)
✓ Token blacklist implemented with Redis and proper TTL
✓ Refresh token rotation working correctly
✓ PyJWT pinned to 2.8.0 (verified no known CVEs)
✓ Rate limiting active on refresh endpoint
✓ Security test suite comprehensive

Tested edge cases:
- None algorithm attack blocked ✓
- Expired token rejected ✓
- Blacklisted token rejected ✓
- Algorithm substitution blocked ✓
- Refresh token reuse prevented ✓

The implementation now follows OWASP JWT security best practices.

==VALIDATION_FEEDBACK==
{
  "from": "B",
  "verdict": "approved",
  "timestamp": "2025-01-17T15:30:00Z",
  "issues": [],
  "required_changes": [],
  "recommendations": [
    "Consider adding token introspection endpoint for debugging (dev/staging only)",
    "Add monitoring alerts for high rates of token validation failures",
    "Document the token lifecycle in API documentation",
    "Consider implementing MFA (multi-factor auth) as future enhancement"
  ],
  "verdict_rationale": "All security vulnerabilities from previous iteration have been properly fixed. Algorithm whitelist prevents none/algorithm confusion attacks, token blacklist enables secure logout, refresh token rotation limits stolen token impact. Security test suite validates all fixes. Implementation is production-ready and follows industry best practices."
}
==END_VALIDATION_FEEDBACK==
```

### Orchestrator Output

```bash
$ orchestrator process-output B

[ORCHESTRATOR] ✓ Work APPROVED by Agent B
Session complete!

Session Summary:
  Total Iterations: 2
  Total Handoffs: 2
  Total Validations: 2
```

---

## Security Issues Caught

### Critical Vulnerabilities Prevented

1. **None Algorithm Attack** (CVE-class)
   - **Impact:** Attacker could forge any token
   - **Fix:** Algorithm whitelist in jwt.decode()

2. **No Token Revocation** (High Risk)
   - **Impact:** Stolen tokens valid for 7 days
   - **Fix:** Redis blacklist with logout support

3. **No Refresh Token Rotation** (Medium Risk)
   - **Impact:** Extended access for stolen refresh tokens
   - **Fix:** Issue new token on refresh, invalidate old

### Additional Improvements

4. **Pinned Dependencies:** Prevents pulling vulnerable versions
5. **Rate Limiting:** Prevents brute force on refresh endpoint
6. **Security Tests:** Validates fixes and prevents regression

---

## Key Metrics

- **Iterations to approval:** 2
- **Security issues caught:** 5 (2 high, 2 medium, 1 low)
- **Critical vulnerabilities prevented:** 2
- **Production-ready outcome:** Yes

---

## Process Insights

### Agent A Performance

- ✅ Good initial implementation (RS256, expiry, env vars)
- ✅ Responded thoroughly to all feedback
- ✅ Implemented beyond required (added security tests)
- ⚠️ Missed common JWT vulnerabilities in first pass

### Agent B Performance

- ✅ Identified critical security issues
- ✅ Provided specific, actionable feedback
- ✅ Referenced industry standards (OWASP)
- ✅ Verified fixes thoroughly in iteration 2

### Overall System

- ✅ Caught vulnerabilities before deployment
- ✅ Educated both agents through the process
- ✅ Resulted in production-grade security
- ✅ Efficient: only 2 iterations needed

---

## Export Session

```bash
$ orchestrator status
Current Session: session_20250117_140000
Active Agent: None (completed)
Iteration: 2
Total Handoffs: 2
Awaiting: Nothing - work approved

$ orchestrator export jwt_auth_session.json
Exported to: ai-duo-validator/sessions/jwt_auth_session.json
```

---

## Comparison: With vs Without Validation

### Without Validation Loop

- 5 security vulnerabilities shipped to production
- None algorithm attack possible (critical)
- No logout capability (major UX/security issue)
- Potential for CVE-class vulnerability

### With Validation Loop

- All vulnerabilities caught pre-deployment
- Security best practices enforced
- Production-ready implementation
- Knowledge transfer between agents

**ROI:** 2 iterations invested → Critical vulnerabilities prevented
