# Testing Design Methods Reference

This document provides detailed explanations of testing design methodologies used for generating comprehensive test cases.

---

## 1. Equivalence Partitioning (等价类划分法)

### Principle
Divide input data into valid equivalence classes (valid inputs) and invalid equivalence classes (invalid inputs). Select one representative value from each class for testing. If one value in a class passes, all values in that class should pass.

### Applicability
- Input fields with defined ranges or formats
- Large input domains where exhaustive testing is impossible
- Data type validation scenarios

### How to Apply

**Step 1:** Identify equivalence classes
- **Valid classes:** Inputs that should be accepted
- **Invalid classes:** Inputs that should be rejected

**Step 2:** Identify class representatives
- Choose typical values from each class
- Avoid boundary values (use Boundary Value Analysis for those)

**Step 3:** Create test cases
- One test case per equivalence class

### Example

**Requirement:** User age input (1-120 years)

| Class Type | Equivalence Class | Representative | Test Case ID |
|------------|------------------|----------------|--------------|
| Valid | 1-120 | 25 | TC-EQ-001 |
| Invalid | < 1 | 0 | TC-EQ-002 |
| Invalid | > 120 | 150 | TC-EQ-003 |
| Invalid | Non-numeric | "abc" | TC-EQ-004 |
| Invalid | Empty | "" | TC-EQ-005 |

### Key Principle
> Testing one representative from each class is equivalent to testing all values in that class.

---

## 2. Boundary Value Analysis (边界值分析法)

### Principle
Test the boundaries and neighboring points of input ranges. Bugs frequently occur at boundaries rather than in the middle of ranges.

### Applicability
- Numeric ranges (e.g., 1-100)
- Date ranges (e.g., last 30 days)
- String length limits (e.g., max 50 characters)
- Array/list size limits

### How to Apply

**Standard Boundary Points:**
- **Min:** Minimum value of the range
- **Min-:** Just below minimum (invalid)
- **Min+:** Just above minimum
- **Max:** Maximum value of the range
- **Max-:** Just below maximum
- **Max+:** Just above maximum (invalid)

**Example Boundary Points for Range [1, 100]:**
- Min- = 0
- Min = 1
- Min+ = 2
- Max- = 99
- Max = 100
- Max+ = 101

### Example

**Requirement:** Product quantity input (1-99 items)

| Test Case ID | Boundary Type | Input | Expected Result |
|--------------|---------------|-------|-----------------|
| TC-BV-001 | Min- | 0 | Reject |
| TC-BV-002 | Min | 1 | Accept |
| TC-BV-003 | Min+ | 2 | Accept |
| TC-BV-004 | Normal | 50 | Accept |
| TC-BV-005 | Max- | 98 | Accept |
| TC-BV-006 | Max | 99 | Accept |
| TC-BV-007 | Max+ | 100 | Reject |

### Golden Rule
> "Boundary values are where bugs concentrate." Always test Min, Min+, Max-, Max.

---

## 3. Decision Table Testing (判定表驱动法)

### Principle
Create a table listing all possible combinations of input conditions and their corresponding actions. Ensures complete coverage of condition-action combinations.

### Applicability
- Complex business rules with multiple conditions
- Logic with interdependent inputs
- Workflows with branching logic
- Systems with multiple conditional outputs

### How to Apply

**Step 1:** Identify conditions (inputs) and actions (outputs)
**Step 2:** List all possible values for each condition
**Step 3:** Create rules (columns) for each combination
**Step 4:** Determine actions for each rule
**Step 5:** Simplify by combining rules with same actions

### Decision Table Format

| | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|--------|--------|--------|--------|
| **Conditions** | | | | |
| Condition A | T | T | F | F |
| Condition B | T | F | T | F |
| **Actions** | | | | |
| Action X | X | - | X | - |
| Action Y | - | X | - | - |
| Action Z | - | - | - | X |

### Example

**Requirement:** Loan approval system
- Conditions: Credit score > 700 (C1), Income > $50K (C2), Debt ratio < 40% (C3)
- Actions: Approve (A1), Manual review (A2), Reject (A3)

| Rule | C1 | C2 | C3 | Action |
|------|----|----|----|----|
| R1 | Y | Y | Y | A1 (Approve) |
| R2 | Y | Y | N | A2 (Manual) |
| R3 | Y | N | Y | A2 (Manual) |
| R4 | Y | N | N | A3 (Reject) |
| R5 | N | Y | Y | A2 (Manual) |
| R6 | N | Y | N | A3 (Reject) |
| R7 | N | N | Y | A3 (Reject) |
| R8 | N | N | N | A3 (Reject) |

### Key Principle
> Each column in a decision table becomes a test case. This ensures all logical combinations are covered.

---

## 4. Cause-Effect Graphing (因果图法)

### Principle
Use Boolean logic graphs to describe relationships between causes (inputs) and effects (outputs), then convert to decision tables.

### Applicability
- Complex input-output relationships
- Systems with conditional dependencies
- When decision tables become too large
- Verification of logical constraints

### How to Apply

**Step 1:** Identify causes (inputs) and effects (outputs)
**Step 2:** Draw cause-effect graph showing relationships
**Step 3:** Identify logical relationships:
- **AND:** Effect = true if ALL causes are true
- **OR:** Effect = true if ANY cause is true
- **NOT:** Effect = true if cause is false
- **IMPLIES:** If cause A, then cause B
**Step 4:** Convert graph to decision table
**Step 5:** Generate test cases from decision table

### Example

**Requirement:** Login system
- Causes: Valid username (C1), Valid password (C2), Account not locked (C3)
- Effect: Login successful (E1)

**Logical Relationship:** E1 = C1 AND C2 AND C3

| Test Case | C1 | C2 | C3 | E1 | Description |
|-----------|----|----|----|----|----|
| TC-CE-001 | Y | Y | Y | Y | All valid |
| TC-CE-002 | N | Y | Y | N | Invalid username |
| TC-CE-003 | Y | N | Y | N | Invalid password |
| TC-CE-004 | Y | Y | N | N | Account locked |

### Key Principle
> Cause-effect graphs help visualize complex logic before converting to testable decision tables.

---

## 5. Orthogonal Array Testing (正交实验法)

### Principle
Use orthogonal arrays to select representative combinations from a large number of possible configurations. Ensures balanced coverage with minimal test cases.

### Applicability
- Configuration testing (OS × Browser × Resolution)
- Multi-factor experiments
- When exhaustive testing is impractical
- System testing with multiple variables

### How to Apply

**Step 1:** Identify factors (variables) and levels (values per variable)
**Step 2:** Select appropriate orthogonal array (L4, L8, L9, L16, etc.)
**Step 3:** Map factors and levels to the array
**Step 4:** Generate test cases from the array

### Orthogonal Array Selection

| Factors | Levels | Recommended Array |
|---------|--------|-------------------|
| 2-3 | 2 | L4 |
| 4-7 | 2 | L8 |
| 3-4 | 3 | L9 |
| 8-15 | 2 | L16 |

### Example

**Requirement:** Test website on different configurations
- Browser: Chrome, Firefox, Safari (3 levels)
- OS: Windows, macOS (2 levels)
- Resolution: 1920x1080, 1366x768 (2 levels)

**L4 Orthogonal Array:**

| Test Case | Browser | OS | Resolution |
|-----------|---------|----|----|
| TC-OA-001 | Chrome | Windows | 1920x1080 |
| TC-OA-002 | Chrome | macOS | 1366x768 |
| TC-OA-003 | Firefox | Windows | 1366x768 |
| TC-OA-004 | Firefox | macOS | 1920x1080 |

### Key Principle
> Orthogonal arrays ensure each pair of factor-level combinations appears at least once. Total combinations: 3×2×2=12, but L4 needs only 4 tests.

---

## 6. State Transition Testing (状态迁移图法)

### Principle
Model system states and transitions between them. Test cases verify correct behavior when events trigger state changes.

### Applicability
- Order systems (Pending → Paid → Shipped → Delivered)
- Workflow systems (Draft → Submitted → Approved → Published)
- Session management (Logged out → Logged in → Active → Timeout)
- Any system with defined states and transitions

### How to Apply

**Step 1:** Identify all possible states
**Step 2:** Identify events that trigger transitions
**Step 3:** Draw state transition diagram
**Step 4:** Create state transition table
**Step 5:** Generate test cases for:
- Valid transitions (happy path)
- Invalid transitions (error handling)
- State invariants (what should remain true in each state)

### State Transition Diagram Format

```
[State A] --event1/action1--> [State B]
[State B] --event2/action2--> [State C]
[State B] --event3/action3--> [State A]
```

### Example

**Requirement:** Order lifecycle

| Current State | Event | Action | Next State |
|--------------|-------|--------|------------|
| Pending | Pay | Process payment | Paid |
| Paid | Ship | Generate tracking | Shipped |
| Shipped | Deliver | Update status | Delivered |
| Pending | Cancel | Refund | Cancelled |
| Paid | Cancel | Refund | Cancelled |

**Test Cases:**

| Test Case ID | Initial State | Event | Expected State | Verification |
|--------------|---------------|-------|----------------|--------------|
| TC-ST-001 | Pending | Pay | Paid | Payment processed |
| TC-ST-002 | Paid | Ship | Shipped | Tracking generated |
| TC-ST-003 | Shipped | Deliver | Delivered | Status updated |
| TC-ST-004 | Delivered | Cancel | Error | Invalid transition |
| TC-ST-005 | Shipped | Cancel | Error | Invalid transition |

### Key Principle
> Test both valid transitions and invalid ones. Systems often fail when handling unexpected state changes.

---

## 7. Error Guessing (错误猜测法)

### Principle
Use experience and intuition to anticipate likely defects. Based on knowledge of common error patterns and historical bug data.

### Applicability
- Supplement to systematic methods
- Experienced testers' intuition
- Domain-specific common issues
- Historical bug analysis

### Common Error Patterns

| Category | Typical Errors |
|----------|---------------|
| **Input** | Empty, null, special characters, very long strings |
| **Numeric** | Zero, negative, overflow, precision loss |
| **Date/Time** | Feb 29, year boundary, timezone issues |
| **Concurrency** | Race conditions, deadlocks |
| **Memory** | Leaks, buffer overflows |
| **Network** | Timeout, disconnection, partial data |

### How to Apply

**Step 1:** Review requirements for error-prone areas
**Step 2:** Consider historical bugs in similar systems
**Step 3:** Think about edge cases developers might miss
**Step 4:** Create test cases for anticipated errors

### Example

**Requirement:** File upload feature

| Test Case ID | Scenario | Expected Behavior |
|--------------|----------|-------------------|
| TC-EG-001 | Empty file | Handle gracefully |
| TC-EG-002 | File > size limit | Reject with message |
| TC-EG-003 | Invalid extension | Reject with message |
| TC-EG-004 | Virus-infected file | Scan and reject |
| TC-EG-005 | Network interruption | Resume or retry |
| TC-EG-006 | Same filename exists | Overwrite or rename |
| TC-EG-007 | Special chars in filename | Sanitize or reject |

### Key Principle
> Error guessing is not systematic but can catch bugs that structured methods miss. Use as a supplement, not replacement.

---

## 8. Pairwise Testing (成对测试法)

### Principle
Test all pairs of parameter values rather than all combinations. Based on research showing most bugs are caused by interactions of at most two parameters.

### Applicability
- Large number of configuration options
- Combinatorial explosion (too many combinations)
- When orthogonal arrays are too restrictive
- Software configuration testing

### How to Apply

**Step 1:** Identify parameters and their values
**Step 2:** Generate pairwise combinations using tools or algorithms
**Step 3:** Create test cases covering all pairs
**Step 4:** Validate coverage

### Example

**Requirement:** Test form with multiple fields
- Browser: Chrome, Firefox, Safari (3)
- Language: EN, CN, JP (3)
- Theme: Light, Dark (2)

**All combinations:** 3 × 3 × 2 = 18
**Pairwise:** 9 test cases (using AllPairs algorithm)

| TC | Browser | Language | Theme |
|----|---------|----------|-------|
| 1 | Chrome | EN | Light |
| 2 | Chrome | CN | Dark |
| 3 | Chrome | JP | Light |
| 4 | Firefox | EN | Dark |
| 5 | Firefox | CN | Light |
| 6 | Firefox | JP | Dark |
| 7 | Safari | EN | Light |
| 8 | Safari | CN | Dark |
| 9 | Safari | JP | Light |

**Pair Coverage Verification:**
- Browser-Language pairs: All 9 pairs covered ✓
- Browser-Theme pairs: All 6 pairs covered ✓
- Language-Theme pairs: All 6 pairs covered ✓

### Key Principle
> Pairwise testing provides strong coverage with significantly fewer test cases. Research shows 90%+ of bugs involve only 1-2 parameters.

---

## Method Selection Guide

| Scenario | Primary Method | Secondary Method |
|----------|---------------|------------------|
| Form with input validation | Equivalence Partitioning | Boundary Value Analysis |
| Business rule engine | Decision Table | Cause-Effect Graphing |
| Workflow system | State Transition | Error Guessing |
| Configuration testing | Orthogonal Array | Pairwise |
| API with multiple parameters | Equivalence Partitioning | Pairwise |
| Search/filter functionality | Boundary Value | Equivalence Partitioning |
| User registration flow | State Transition | Error Guessing |
| Payment processing | Decision Table | Boundary Value |

---

## Coverage Metrics

### Statement Coverage
Percentage of code statements executed by test cases.

### Branch Coverage
Percentage of decision branches (if/else) executed.

### Path Coverage
Percentage of all possible execution paths covered.

### Condition Coverage
Percentage of individual conditions tested for both true and false.

### For Test Case Design
| Metric | Target |
|--------|--------|
| Requirement Coverage | 100% |
| Boundary Coverage | 100% |
| Valid/Invalid Class Coverage | 100% |
| State Transition Coverage | 100% valid + key invalid |
| Error Scenario Coverage | Based on risk assessment |
