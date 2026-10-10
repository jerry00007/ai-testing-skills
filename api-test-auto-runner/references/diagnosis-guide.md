# Bug Diagnosis Guide

## Purpose

This guide provides systematic failure classification patterns and decision trees for diagnosing test failures during Phase 4 (Result Analysis & Bug Diagnosis).

## Failure Classification System

### Type 1: Script Bug

**Definition**: The test script itself contains errors in logic, assertions, or data handling.

**Signatures**:
| Signature | Example | Root Cause |
|---|---|---|
| AssertionError with clearly wrong expected value | Expected "北京" but assertion compares against "beijing" | Copy-paste or encoding issue in test data |
| TypeError during parsing | `'NoneType' is not subscriptable` | Missing `or []` / `or {}` guard |
| KeyError on response field | `KeyError: 'entity_result'` | Using `['field']` instead of `.get('field')` |
| IndexError on list access | `list index out of range` | Not checking list length before indexing |
| All tests fail with same error pattern | Every case fails with "code=None" | API URL construction error |
| Test passes in verbose but fails in batch | Single query OK, batch fails | State leakage between iterations |

**Fix Pattern**:
```python
# BAD: Direct access
result = data['entity_result'][0]['name']

# GOOD: Safe access
result = (data.get('entity_result') or [{}])[0].get('name', '')
```

**Decision**: Fix the script → Re-run (Phase 3). Count towards retry limit (max 3).

---

### Type 2: API Change

**Definition**: The API response structure has changed (field renamed, removed, nested differently).

**Signatures**:
| Signature | How to Verify | Action |
|---|---|---|
| Field previously present now missing | Call API manually, check response | Update field path in assertions |
| Field renamed (e.g., `result` → `data`) | Compare with previous response snapshot | Update all references |
| New nesting level introduced | Check response JSON structure depth | Update dot-path traversal |
| Type change (list → dict, string → int) | `print(type(data['field']))` | Update type checks |
| Response envelope changed (code → status) | Check top-level keys | Update status check logic |

**Verification Pattern**:
```python
# Run this to diagnose API changes
import json
resp = requests.get(url, params=params)
data = resp.json()
print("Top-level keys:", list(data.keys()))
for key in data.keys():
    val = data[key]
    print(f"  {key}: type={type(val).__name__}, value={str(val)[:100]}")
```

**Decision**: Update assertions to match new API structure → Re-run. Document as breaking change.

---

### Type 3: Product Bug (REPORT TO DEVELOPER)

**Definition**: The API returns incorrect data, missing data, or violates business requirements.

**Signatures**:
| Signature | Severity | Classification |
|---|---|---|
| API returns wrong entity value | P0 | Business logic error |
| Expected field exists but is empty/null | P0/P1 | Data gap |
| Response contains stale/cached data | P1 | Cache invalidation issue |
| Ordering wrong (e.g., results not ranked) | P2 | Ranking/sorting bug |
| Partial data (some fields present, others missing) | P0 | Data completeness |
| Inconsistent behavior (same input, different output) | P0 | Non-deterministic bug |
| Edge case not handled (special chars, very long input) | P1 | Input validation gap |
| Cross-environment inconsistency (test vs prod differ) | P1 | Config/deployment issue |

**Three-Musketeers Analysis** (REQUIRED for Product Bugs):

#### Product Expert Perspective:
1. Does this violate explicit PRD requirements?
2. What user scenarios are impacted?
3. Is there a workaround?
4. What's the blast radius (how many users/queries affected)?

#### Architect Perspective:
1. Is this a data pipeline issue or service logic issue?
2. Does the data flow from upstream correctly?
3. Is this a caching layer problem?
4. Are there related services that might have the same issue?

#### QA Expert Perspective:
1. Is this 100% reproducible or intermittent?
2. What are the exact reproduction steps?
3. Are there related edge cases that also fail?
4. What's the minimal reproduction case?

**Bug Report Template**:
```
Bug ID: BUG-XXX
Severity: P0/P1/P2
Title: [concise description]
Reproduction: query="xxx", API endpoint, environment
Expected: [what PRD says should happen]
Actual: [what actually happens]
Evidence: [API response snippet]
Root Cause Analysis: [three-musketeers findings]
Impact: [affected users/scenarios]
```

**Decision**: Report to developer. Do NOT attempt to fix the API.

---

### Type 4: Environment Issue

**Definition**: Infrastructure or network problems preventing test execution.

**Signatures**:
| Signature | Likely Cause | Quick Fix |
|---|---|---|
| Connection refused | Service down or wrong host | Verify service status |
| Connection timed out | Network issue or overloaded service | Try again, increase timeout |
| 500 Internal Server Error | Server-side crash | Check server logs |
| 502/503/504 Gateway Error | Load balancer or upstream issue | Retry after delay |
| SSL certificate error | Test env cert expired | Use `verify=False` |
| DNS resolution failure | Network config issue | Try IP address directly |

**Decision**: Report to user. Cannot proceed until environment is fixed.

---

### Type 5: Test Design Gap

**Definition**: The test case expectation is ambiguous or the requirement is unclear.

**Signatures**:
| Signature | Example | Action |
|---|---|---|
| Unclear expected value | PRD says "返回城市" but doesn't specify format | Flag for PM clarification |
| Conflicting requirements | PRD says A, developer says B | Escalate to PM + developer |
| Subjective assertion | "结果应该合理" - no objective criteria | Define measurable criteria |
| Missing requirement coverage | Test found behavior not in PRD | Document as discovery, add to PRD |
| Ambiguous priority | Not clear if edge case is P0 or P2 | Ask PM to classify |

**Decision**: Document the ambiguity. Add as a warning in the report. Do NOT guess expected values.

---

## Diagnosis Decision Tree

```
Test Failure Detected
│
├── Script Error? (SyntaxError, TypeError, KeyError, IndexError)
│   ├── YES → Examine stack trace
│   │   ├── KeyError → Add .get() with default → Fix → Re-run
│   │   ├── TypeError → Add None guard (or [], or {}) → Fix → Re-run
│   │   ├── IndexError → Add length check → Fix → Re-run
│   │   └── SyntaxError → Fix syntax → Re-run
│   └── NO → Continue ↓
│
├── API Unreachable? (ConnectionError, Timeout, 5xx)
│   ├── YES → Environment Issue
│   │   ├── Try manual curl/requests
│   │   ├── If also fails → Report environment issue
│   │   └── If manual works → Check script URL construction
│   └── NO → Continue ↓
│
├── Response Structure Changed? (field missing, renamed, type changed)
│   ├── Call API manually with same params
│   ├── Compare response with expected structure
│   ├── If structure differs → API Change → Update assertions → Re-run
│   └── If structure matches → Continue ↓
│
├── API Response Value Wrong? (wrong data, missing data)
│   ├── Verify with multiple inputs
│   ├── Check PRD requirements
│   ├── If clearly violates PRD → Product Bug
│   │   ├── Apply Three-Musketeers analysis
│   │   ├── Generate BUG report
│   │   └── Add to final report
│   └── If PRD is ambiguous → Test Design Gap
│       ├── Document ambiguity
│       └── Flag for PM clarification
│
└── Assertion Logic Wrong? (expected value seems incorrect)
    ├── Review test case definition
    ├── Check if expected value is correct per PRD
    ├── If expected value is wrong → Script Bug → Fix → Re-run
    └── If expected value is correct → Product Bug
```

## Retry Protocol

```
Attempt 1: First run
├── Count failures by type
├── Fix Script Bugs → Attempt 2
└── Collect Product Bugs for analysis

Attempt 2: After script fixes
├── Verify previous Script Bugs are fixed
├── If new Script Bugs appear → Fix → Attempt 3
└── Collect remaining failures

Attempt 3: Final attempt
├── If Script Bugs persist → STOP, ask user for help
├── Collect all Product Bugs
└── Proceed to Phase 5 (Report)

MAX RETRY = 3. No exceptions.
```

## Common Anti-Patterns in Diagnosis

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Assuming all failures are Product Bugs | Wastes time reporting non-issues | Classify first, then act |
| Fixing Product Bugs by modifying expected values | Hides real bugs | Report to developer |
| Re-running without fixing | Same failure repeats | Fix root cause first |
| Ignoring intermittent failures | May be race conditions or cache issues | Run 3x to confirm reproducibility |
| Changing test query to make it pass | Defeats purpose of testing | Fix the API or the test logic |
| Skipping three-musketeers analysis | Shallow bug reports | Always analyze Product Bugs deeply |

## Quick Reference: Failure → Action

| You See | Do This |
|---|---|
| `KeyError: 'field'` | Change `['field']` → `.get('field', default)` |
| `TypeError: 'NoneType'` | Add `or []` or `or {}` or `or ""` guard |
| `AssertionError: expected X, got Y` | Check: is X correct per PRD? If yes → Product Bug. If no → fix script |
| `ConnectionError` | Try manual request. If fails → Environment Issue |
| All cases fail | Check base URL construction and default params |
| Some cases fail randomly | Run 3x. If inconsistent → report as intermittent Product Bug |
| Response has extra/unexpected data | Not necessarily a bug. Only flag if PRD specifies otherwise |
