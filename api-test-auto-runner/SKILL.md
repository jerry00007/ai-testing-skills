---
name: api-test-auto-runner
description: This skill should be used when the user asks to "测试这个接口", "帮我测一下QP", "生成测试脚本并执行", "自动测试API", "跑一下测试", "测试需求", "接口自动化测试", "生成测试并出报告", or provides a PRD/requirement document and wants automated testing with execution and analysis. Generates executable Python test scripts, auto-executes them, analyzes results with three-musketeers methodology, diagnoses script bugs vs product bugs, and outputs final Excel/MD reports.
---

# API Test Auto-Runner

## Overview

Automate the full API testing lifecycle: generate executable test scripts from requirements, auto-execute, analyze results, diagnose failures, and output reports. The core differentiator from other test skills is **automatic execution + result analysis + bug diagnosis**.

## When to Use

Trigger when:
- User provides PRD/requirement doc + API endpoint and asks for testing
- User says "测一下这个接口" or "跑一下测试"
- User wants automated testing with execution and report output
- User has test cases but wants them executed automatically with analysis

## Prerequisites (MUST verify before starting)

| Prerequisite | How to Check | If Missing |
|---|---|---|
| API endpoint URL | Ask user or extract from context | MUST ask user |
| Response structure understanding | Call API with sample request | Cannot proceed without |
| Python3 + requests available | `python3 -c "import requests"` | `pip3 install requests` |
| Test environment accessible | Ping the API host | Warn user |

## Workflow (6 Phases - STRICTLY SEQUENTIAL)

### Phase 1: Context Gathering (MANDATORY FIRST)

**Objective**: Understand the API, requirements, and existing patterns.

**Steps**:
1. Read the requirement document (PRD/docx/text)
2. Extract API endpoint, parameters, and expected behavior
3. **Call the API with a sample request** to discover response structure
4. Explore project directory for existing test scripts and patterns
5. Identify key fields to validate from the response

**Output**: Internal understanding of API response structure and test requirements.

**CRITICAL**: Never skip calling the actual API. Response structure discovery is essential for writing correct assertions.

```
Pattern for API discovery:
1. Take the user-provided URL or construct from base_url + params
2. Send GET/POST request with python3 requests
3. Print all top-level keys
4. Print nested structure of relevant sections
5. Identify field paths for assertions (e.g., simple_result.entity_result[].class_name)
```

### Phase 2: Test Script Generation

**Objective**: Generate an executable Python test script.

**Requirements for generated script**:
- Self-contained Python3 script using `requests` library
- Test cases defined as data (list of dicts), not hardcoded
- Each test case has: name, query/params, expected values, priority
- Auto-executable via `python3 <script_name>.py`
- Supports `--env test/prod`, `--query <single>`, `--verbose`, `--export` flags
- Outputs: pass/fail/warn statistics + Excel report with `--export`
- Handles None/empty responses gracefully (use `or []`, `or {}`)

**Template reference**: See `references/test-script-template.md` for the standard script structure.

**MANDATORY: Complete Request Parameters**:
For `/rcm/` or `autohmpg2` endpoints, ALL test scripts MUST use the complete set of 35 production parameters.
Missing parameters causes SILENT logic failures (e.g., missing `appversion` → `se_version:[]` → ES returns 0 → all strategies fail with no error).
See **`references/standard-request-params.md`** for the parameter builder function and high-risk parameter list.
Reference knowledge base: `doc/线上请求标准参数模板.md` in RcmTestProject.

**MUST include in the script**:
```python
# Standard structure (6 sections):
# 1. Configuration (env URLs, default params with ALL 35 standard params, timeout)
# 2. Stats class (pass/fail/warn counters)
# 3. Test case definitions (data-driven)
# 4. API call function (with error handling)
# 5. Validation functions (per test type)
# 6. Main function (argparse + execution + summary)
```

**Test case coverage requirements**:
| Dimension | Minimum Cases | Priority |
|---|---|---|
| Core functionality | 3-5 | P0 |
| Edge cases | 3-5 | P1 |
| Error/boundary | 2-3 | P1 |
| Security (SQL injection, XSS) | 2-3 | P2 |
| Performance (timeout check) | 1-2 | P2 |

### Phase 3: Auto Execution

**Objective**: Run the generated test script immediately.

**Steps**:
1. Save the script to the project directory
2. Execute: `python3 <script_name>.py --export`
3. Capture full output
4. If script has syntax/import errors → fix and re-run (max 3 attempts)
5. If all tests pass → skip Phase 4 diagnosis, go to Phase 5 report

**Error handling for script bugs**:
```
If SyntaxError → fix the syntax, re-run
If ModuleNotFoundError → pip3 install the module, re-run
If ConnectionError → warn user about environment, continue with partial results
If TypeError/AttributeError → fix the assertion logic, re-run
```

**Max retry count**: 3. After 3 failures, report the script error and ask user for help.

### Phase 4: Result Analysis & Bug Diagnosis

**Objective**: Analyze test results using three-musketeers methodology and classify failures.

**Load three-musketeers skill** for structured analysis. For each failure:

#### Step 1: Classify Failure Type

| Failure Type | Signature | Action |
|---|---|---|
| **Script Bug** | AssertionError with wrong expected value, TypeError in parsing logic | Fix script, re-run |
| **API Change** | Response field renamed/removed, structure changed | Update assertions, note as breaking change |
| **Product Bug** | API returns incorrect data, missing fields, wrong values | Report as bug to developer |
| **Environment Issue** | Timeout, connection refused, 500 errors | Report infra issue |
| **Test Design Gap** | Unclear requirement, ambiguous expected value | Flag for PM clarification |

#### Step 2: Three-Musketeers Analysis (for Product Bugs only)

Apply structured analysis:
- **Product Expert**: Is this a business logic error? Does it affect user scenarios?
- **Architect**: Is this a data flow issue? Architecture limitation?
- **QA Expert**: Is this reproducible? What's the severity? Related edge cases?

#### Step 3: Diagnosis Decision Tree

```
Failure detected
├── Script crashes? → Fix script → Re-run (Phase 3)
├── Assertion wrong? → Check API response manually → Fix expected value → Re-run
├── API response unexpected? 
│   ├── Field missing → API change or bug?
│   │   ├── Check if field exists in verbose output → If yes: fix assertion
│   │   └── If truly missing → Product bug
│   └── Value wrong → Product bug
└── All assertions correct but failing → Check test logic → Fix
```

**Reference**: See `references/diagnosis-guide.md` for detailed diagnosis patterns.

### Phase 5: Report Output

**Objective**: Generate final test report.

**Always output BOTH formats**:

#### Markdown Report (inline in response)
```markdown
## Test Report: <Feature Name>
**Date**: YYYY-MM-DD HH:MM
**Environment**: <env> (<url>)
**API**: <endpoint>

### Summary
| Metric | Value |
|---|---|
| Total test cases | N |
| Passed | N (N%) |
| Failed | N (N%) |
| Warnings | N |

### Failed Cases Analysis
| Case | Expected | Actual | Root Cause | Type |
|---|---|---|---|---|
| ... | ... | ... | ... | Script Bug / Product Bug / ... |

### Bug Report (Product Bugs only)
| Bug ID | Severity | Description | Reproduction | Evidence |
|---|---|---|---|---|
| BUG-001 | P0 | ... | query=xxx | API response: ... |

### Key Findings
1. Finding 1
2. Finding 2
```

#### Excel Report (via --export flag)
The test script's `--export` flag already generates this. Reference the file path.

### Phase 6: Iteration (if applicable)

If user provides:
- Developer feedback (e.g., "开发说level=1/2/3代表省市县") → Update script assertions → Re-run
- New test cases → Add to script → Re-run
- Environment change → Update config → Re-run

## Anti-Patterns (MUST NOT do)

| Anti-Pattern | Why | Instead |
|---|---|---|
| Skip API discovery | Wrong assertions | Always call API first |
| Generate only markdown tables | Not executable | Generate Python script |
| Skip execution | No real results | Always run the script |
| Trust first run | Script bugs exist | Diagnose and fix |
| Only report pass/fail count | No actionable info | Include root cause analysis |
| Hardcode expected values | Fragile | Use configurable test data |
| Ignore None/empty responses | Script crashes | Use `or []`, `or {}`, `or ""` |

## Additional Resources

### Reference Files

- **`references/standard-request-params.md`** - MANDATORY complete parameter template for `/rcm/` endpoints (35 params, high-risk list)
- **`references/test-script-template.md`** - Complete Python test script template with all 6 sections
- **`references/diagnosis-guide.md`** - Detailed failure classification patterns and decision trees

### Related Skills

- **three-musketeers** - For structured multi-perspective analysis of test results
- **test-case-generator** - For generating test case design documents (analysis only, no execution)
- **xlsx** - For Excel report formatting when needed
