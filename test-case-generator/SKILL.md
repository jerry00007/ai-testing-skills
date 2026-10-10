---
name: test-case-generator
description: Generate comprehensive test cases from requirement documents using systematic testing methodologies. Use this skill when user asks to "generate test cases", "create test cases from requirements", "design test scenarios", "analyze testing points", or provides a requirement document and wants test coverage analysis. Supports 10 testing dimensions including functionality, input validation, boundary testing, business rules, state transitions, exceptions, concurrency/idempotency, fault tolerance, security, and performance testing. Includes comprehensive API testing coverage with 7 dimensions. **NEW v2.3**: Added Excel generation best practices, Python error prevention guidelines, and output file validation to prevent common syntax/runtime errors. **v2.2**: Enhanced document reading capability supporting text (with images), URLs (with auto-auth browser), and complete visual content extraction from UI mockups, diagrams, and configuration tables.
---

## ⚠️ 执行铁律 (MANDATORY ENFORCEMENT RULES)

**THIS SECTION IS NON-NEGOTIABLE. READ EVERY RULE BELOW. YOU WILL BE VERIFIED AGAINST THEM.**

1. **EVERY API endpoint MUST have at least 7 test cases** — one per API testing dimension (参数校验, 功能验证, 异常处理, 幂等性, 并发, 性能, 容错)
2. **EVERY input field MUST have at least 5 test cases** — valid value + boundary-low + boundary-high + invalid + empty/null
3. **ALL 10 testing dimensions MUST have test cases** — minimum 5 per dimension. No exceptions.
4. **Standard requirement documents should produce 150-300 test cases total**
5. **If total test cases < 80, your coverage is INCOMPLETE** — you MUST go back and supplement
6. **You MUST NOT skip any testing dimension** — even if it seems "not applicable", explain why and provide at least defensive test cases
7. **You MUST NOT use vague placeholders** like "等", "...", "etc.", "similar cases" to abbreviate test cases — every single case must be written out with full content
8. **You MUST read the complete requirement document before starting analysis** — no skimming, no guessing
9. **You MUST proceed through Steps 0→1→2→3→4→5→6→7 IN ORDER** — do not jump ahead
10. **You MUST stop at every ⛔ CHECKPOINT and verify before proceeding**

### 📊 Output Calibration (USE THIS TO SET YOUR TARGET)

Before generating, estimate complexity and set your target:

| Complexity | Characteristics | Expected Test Cases |
|-----------|-----------------|-------------------|
| **Simple** | 3-5 input fields, 1-2 APIs | 80-120 test cases |
| **Medium** | 5-10 input fields, 3-5 APIs | 150-250 test cases |
| **Complex** | 10+ input fields, 5+ APIs | 250-400+ test cases |
| **API-only** | N endpoints | Minimum 7 × N test cases |

**If your output falls below the calibration minimum, you have FAILED the enforcement rules. Go back.**

### 🚫 Prohibited Behaviors

- **MUST NOT** skip any of the 10 testing dimensions
- **MUST NOT** produce fewer than 5 test cases per dimension
- **MUST NOT** output only format examples without real content
- **MUST NOT** abbreviate test cases with "..." or "等"
- **MUST NOT** merge different test scenarios into a single test case
- **MUST NOT** proceed past a checkpoint without verification
- **MUST NOT** write "similar test cases apply" — write EACH case explicitly
- **MUST NOT** reduce output because of "token concerns" — completeness is mandatory

---

# Test Case Generator (Enhanced v3.0 — Enforcement Edition)

## Overview

Generate comprehensive, high-coverage, non-redundant test cases from requirement documents using systematic testing methodologies. This skill transforms textual requirements into structured test points and test cases across **10 testing dimensions**, ensuring thorough coverage while avoiding duplication.

**Enhanced Features:**
- ✅ **10 Testing Dimensions** with quantitative minimums per dimension
- ✅ **API Testing 7 Dimensions** with minimum 7 cases per endpoint
- ✅ **Self-Check Gate** (hard quantitative gates, not soft recommendations)
- ✅ **External Dependencies Analysis** (APIs, services, cache, DB)
- ✅ **Risk Point Identification** (high-risk logic)
- ✅ **Enforcement Checkpoints** between every step
- ✅ **Inlined Testing Methodology** (no external file reads needed)

## When to Use

Use this skill when:
- User provides a requirement document and asks for test cases
- User asks to "analyze testing points" from a specification
- User wants to "generate test scenarios" for a feature
- User needs "test coverage analysis" for requirements
- User asks about test design methodologies
- **User needs API/interface test cases**
- **User wants comprehensive security/performance testing**
- **User provides requirement document in text format (may include images)** — Must extract information from both text and images
- **User provides requirement document URL (e.g., internal doc system)** — Must open browser to read online documentation

---

## Testing Design Methods (INLINE REFERENCE)

**You MUST use these methods when generating test cases. Do NOT reference external files.**

### 1. Equivalence Partitioning (等价类划分法)

**Principle:** Divide input data into valid equivalence classes and invalid equivalence classes. Select one representative from each class.

**How to Apply:**
1. Identify valid classes (inputs that should be accepted) and invalid classes (inputs that should be rejected)
2. Choose typical values from each class (avoid boundary values — use BVA for those)
3. One test case per equivalence class

**Example — User age (1-120):**

| Class Type | Equivalence Class | Representative | Test Case |
|------------|------------------|----------------|-----------|
| Valid | 1-120 | 25 | TC-EQ-001 |
| Invalid | < 1 | 0 | TC-EQ-002 |
| Invalid | > 120 | 150 | TC-EQ-003 |
| Invalid | Non-numeric | "abc" | TC-EQ-004 |
| Invalid | Empty | "" | TC-EQ-005 |

> Testing one representative from each class is equivalent to testing all values in that class.

### 2. Boundary Value Analysis (边界值分析法)

**Principle:** Bugs concentrate at boundaries. Test boundary points and their neighbors.

**Standard Boundary Points for range [Min, Max]:**
- **Min-**: Just below minimum (invalid) → e.g., Min-1
- **Min**: Minimum value (valid)
- **Min+**: Just above minimum (valid) → e.g., Min+1
- **Nominal**: A normal middle value (valid)
- **Max-**: Just below maximum (valid) → e.g., Max-1
- **Max**: Maximum value (valid)
- **Max+**: Just above maximum (invalid) → e.g., Max+1

**Example — Product quantity (1-99):**

| Boundary Type | Input | Expected |
|---------------|-------|----------|
| Min- | 0 | Reject |
| Min | 1 | Accept |
| Min+ | 2 | Accept |
| Normal | 50 | Accept |
| Max- | 98 | Accept |
| Max | 99 | Accept |
| Max+ | 100 | Reject |

> Always test Min, Min+, Max-, Max. This yields 7 test cases per numeric range.

### 3. Decision Table (判定表驱动法)

**Principle:** List ALL condition combinations and their actions. Each column = one test case.

**Format:**

| | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|--------|--------|--------|--------|
| **Condition A** | T | T | F | F |
| **Condition B** | T | F | T | F |
| **Action X** | X | - | X | - |
| **Action Y** | - | X | - | - |

**Example — Loan approval (Credit>700, Income>50K, Debt<40%):**

| Rule | Credit>700 | Income>50K | Debt<40% | Action |
|------|-----------|-----------|---------|--------|
| R1 | Y | Y | Y | Approve |
| R2 | Y | Y | N | Manual review |
| R3 | Y | N | Y | Manual review |
| R4 | Y | N | N | Reject |
| R5 | N | Y | Y | Manual review |
| R6 | N | Y | N | Reject |
| R7 | N | N | Y | Reject |
| R8 | N | N | N | Reject |

> 3 conditions with 2 values each = 2³ = 8 rules = 8 test cases minimum.

### 4. State Transition Testing (状态迁移图法)

**Principle:** Model states and transitions. Test valid transitions AND invalid transitions.

**Transition Table Format:**

| Current State | Event | Action | Next State |
|--------------|-------|--------|------------|
| State A | Event 1 | Action 1 | State B |
| State B | Event 2 | Action 2 | State C |

**Example — Order lifecycle:**

| Current State | Event | Next State | Test Purpose |
|--------------|-------|------------|--------------|
| Pending | Pay | Paid | Valid transition |
| Paid | Ship | Shipped | Valid transition |
| Shipped | Deliver | Delivered | Valid transition |
| Delivered | Cancel | Error | Invalid transition |
| Pending | Cancel | Cancelled | Valid edge case |

> Test every valid transition + every invalid transition attempt. N states with M transitions typically yields N×M test cases.

### 5. Error Guessing (错误猜测法)

**Principle:** Use experience to anticipate likely defects. Supplement systematic methods.

**Common Error Patterns Table:**

| Category | Typical Errors to Test |
|----------|----------------------|
| **Input** | Empty, null, special characters, very long strings, Unicode/emoji |
| **Numeric** | Zero, negative, overflow, precision loss, scientific notation |
| **Date/Time** | Feb 29, year boundary, timezone issues, leap second, 23:59:59 |
| **Concurrency** | Race conditions, deadlocks, double-submit, stale data |
| **Network** | Timeout, disconnection, partial data, slow response |
| **Security** | SQL injection, XSS, path traversal, CSRF, IDOR |
| **Encoding** | UTF-8 edge cases, null bytes, BOM, mixed encoding |

### 6. Method Selection Guide (QUICK REFERENCE)

| Scenario | Primary Method | Secondary Method | Min Cases per Element |
|----------|---------------|------------------|----------------------|
| Form with input validation | Equivalence Partitioning | Boundary Value Analysis | 5 per field |
| Business rule engine | Decision Table | Cause-Effect Graphing | 2ⁿ (n=conditions) |
| Workflow system | State Transition | Error Guessing | N×M (states×transitions) |
| Configuration testing | Orthogonal Array | Pairwise | L4/L8/L9 array size |
| API with multiple parameters | Equivalence Partitioning | Pairwise | 7 per endpoint |
| Search/filter functionality | Boundary Value | Equivalence Partitioning | 5 per filter |
| User registration flow | State Transition | Error Guessing | 8+ per state |
| Payment processing | Decision Table | Boundary Value | 10+ per rule |

---

## Workflow (STRICT ORDER — DO NOT SKIP STEPS)

### Step 0: Document Reading and Analysis

**CRITICAL**: Before analyzing requirements, read the source document completely — DO NOT skip images or online content.

#### 0.1 Document Input Format Recognition

Identify the input format:

| Input Type | Detection Method | Processing Strategy |
|-----------|------------------|-------------------|
| **Text content** | Check if input is markdown, text, or file path | - If file path: Read with appropriate tool<br>- If text/markdown: Direct analysis<br>- **CRITICAL**: Extract ALL information including images/screenshots |
| **URL** | Check if input starts with http://, https://, or is a known doc system URL | - Use opencode browser (preferred - auto-auth)<br>- Fallback: playwright (wait for user login) |

#### 0.2 Document Reading Strategies

**Strategy A: Text/Markdown Input (with possible images)**

```python
# Workflow for text input
1. If file path provided:
   - Read file using appropriate tool (docx, read, etc.)
   - Check if file contains embedded images

2. Extract ALL content:
   - Text content (requirements, descriptions)
   - Tables (configuration items, parameters)
   - Images/Charts (UI mocks, workflows, data models)
   - Screenshots (example interfaces, edge cases)

3. For images/charts/screenshots:
   - Use look_at tool to analyze visual content
   - Extract: UI elements, data fields, workflows, constraints
   - Example: If showing NPS card UI screenshot → extract score range, button states, form fields
```

**Strategy B: URL Input (online documentation)**

```bash
# Preferred: opencode browser (auto-auth with cookies)
# Fallback: playwright (wait for user to login)

# Step 1: Open URL with opencode browser
# Step 2: Read complete page content (all sections, tables, images)
# Step 3: Extract requirements from:
#   - Text descriptions
#   - Configuration tables/parameters
#   - UI screenshots/diagrams
#   - Workflow charts
# Step 4: Proceed to Step 1 (Analyze Requirements)
```

**Critical Rules:**

1. **NEVER skip visual content** — Images/charts/screenshots contain critical requirements
2. **Read complete document** — Not just summary, all sections and details
3. **Extract from visual elements**:
   - UI mockups: Fields, buttons, labels, validation rules
   - Workflow diagrams: States, transitions, edge cases
   - Data models: Fields, types, constraints, relationships
   - Configuration tables: All rows and columns
4. **Verify no missing information**:
   - Cross-check text vs visual content
   - Ensure all UI panels/sections are covered
   - Check all configuration options are captured

**Output Format after Document Reading:**

```markdown
### 需求文档完整解析

**文档来源**: [file path or URL]
**文档格式**: [docx/markdown/URL]

**文本内容提取:**
- 功能点列表
- 输入参数表
- 业务规则
- 状态流转

**视觉内容提取（如适用）:**
- UI界面截图分析: [从图片中提取的UI元素]
- 工作流程图: [从图表中提取的流程]
- 配置项表: [从截图/表格中提取的详细配置]
- 数据模型: [从图表中提取的字段关系]

**完整度自检:**
- [ ] 所有文本需求已提取
- [ ] 所有图片/图表内容已分析
- [ ] 视觉内容与文本内容一致性验证
- [ ] 无遗漏的关键信息
```

### ⛔ CHECKPOINT 0: Before proceeding to Step 1

- [ ] Complete document has been read (every section, every page)
- [ ] All visual content (images, charts, screenshots) has been analyzed
- [ ] All input fields identified with their constraints
- [ ] All API endpoints identified
- [ ] All business rules captured
- [ ] If ANY check fails → STOP and re-read the document before proceeding

---

### Step 1: Analyze Requirements

Read and understand the requirement document thoroughly:

#### 1.1 Core Requirements
1. **Identify functional requirements** — What the system should do
2. **Identify non-functional requirements** — Performance, security, compatibility
3. **Identify constraints** — Limitations, boundaries, rules
4. **Identify business rules** — Logic, conditions, workflows
5. **Identify data requirements** — Input/output specifications, data types

#### 1.2 Enhanced Analysis
6. **Identify external dependencies**
   - External APIs/services
   - Cache systems (Redis, Memcached)
   - Databases (MySQL, MongoDB, etc.)
   - Third-party integrations
   - File systems/storage

7. **Identify risk points**
   - High-risk business logic (payment, permission changes)
   - Data consistency critical operations
   - Security-sensitive operations
   - Performance-critical paths
   - Complex conditional logic

8. **Identify ALL API endpoints (CRITICAL)**
   - List every REST API/GraphQL/WebSocket endpoint mentioned in requirements
   - Group by module (user-facing, admin backend, external services)
   - For each endpoint, capture: HTTP method, path, main purpose, key parameters
   - Example:
     ```
     ### API接口清单

     **用户端接口:**
     1. GET /api/nps/card - 获取NPS卡片数据
     2. POST /api/nps/submit - 提交用户评分
     3. POST /api/nps/exposure - 曝光上报
     4. POST /api/nps/close - 关闭卡片

     **后台管理接口:**
     1. GET /api/admin/scenes - 场景列表查询
     2. POST /api/admin/scenes - 创建场景
     3. PUT /api/admin/scenes/{id} - 编辑场景
     4. DELETE /api/admin/scenes/{id} - 删除场景
     5. POST /api/admin/mutex - 创建互斥配置
     6. POST /api/admin/blacklist - 黑名单配置
     ```

9. **Determine Output Calibration Target**
   - Count input fields → F
   - Count API endpoints → A
   - Minimum target = (F × 5) + (A × 7) + (10 dimensions × 5) = 5F + 7A + 50
   - Use calibration table from ⚠️ 执行铁律 section to set explicit target number

**Output Format:**
```markdown
### 需求解析

1. **功能点列表**
   - 功能1: [描述]
   - 功能2: [描述]

2. **输入参数**
   | 字段名 | 类型 | 必填 | 约束条件 | 说明 |
   |--------|------|------|----------|------|
   | field1 | String | 是 | 1-50字符 | 用户名 |

3. **业务规则**
   - 规则1: [条件 -> 结果]
   - 规则2: [条件 -> 结果]

4. **状态流转**
   [状态A] --事件1--> [状态B] --事件2--> [状态C]

5. **外部依赖**
   - 依赖1: [服务名称/接口]
   - 依赖2: [数据库/缓存]

6. **风险点识别**
   - 风险1: [高危逻辑]
   - 风险2: [数据一致性]

7. **API接口清单 (MANDATORY)**
   - Endpoint 1: [METHOD] [PATH] — [PURPOSE]
   - Endpoint 2: [METHOD] [PATH] — [PURPOSE]

8. **Output Calibration Target**
   - Input fields: [F] → expects [F × 5] minimum input test cases
   - API endpoints: [A] → expects [A × 7] minimum API test cases
   - Dimension baseline: 10 × 5 = 50 minimum
   - **TOTAL TARGET: [number] test cases minimum**
```

### ⛔ CHECKPOINT 1: Before proceeding to Step 2

- [ ] All functional requirements identified and listed
- [ ] ALL input fields captured with their types, constraints, and validation rules
- [ ] ALL API endpoints listed (no missing endpoints)
- [ ] All business rules documented
- [ ] State transitions mapped
- [ ] External dependencies identified
- [ ] Risk points identified
- [ ] Output calibration target calculated and stated explicitly
- [ ] If ANY check fails → STOP and re-analyze before proceeding

---

### Step 2: Extract Test Points

Extract testable elements from requirements across **10 testing dimensions**:

#### Testing Dimensions Checklist (MANDATORY — ALL 10 MUST BE COVERED)

| # | 测试维度 | 测试点 | Minimum Cases |
|---|---------|--------|---------------|
| **1. 功能测试** | | | **5+** |
| | 正常流程 | 主流程、分支流程 | |
| | 业务规则 | 条件组合、逻辑冲突 | |
| **2. 输入测试** | | | **5 per field** |
| | 合法输入 | 有效值、格式正确 | |
| | 非法输入 | 无效值、格式错误 | |
| | 空值/null | null、空字符串、缺失字段 | |
| | 超长/极值 | 最大长度、超大数值 | |
| | 特殊字符 | 转义字符、表情、HTML | |
| **3. 边界测试** | | | **5+** |
| | 临界值 | 上界、下界、边界值 | |
| | 边界外值 | 上界+1、下界-1 | |
| **4. 业务规则测试** | | | **5+** |
| | 多条件组合 | 判定表、决策树 | |
| | 逻辑冲突 | 矛盾条件、互斥规则 | |
| **5. 状态流转测试** | | | **5+** |
| | 正常流转 | 合法状态转换 | |
| | 非法跳转 | 跳过中间状态、回退 | |
| **6. 异常测试** | | | **5+** |
| | 参数缺失 | 必填参数为空 | |
| | 数据不存在 | 查询不存在记录 | |
| | 服务异常 | 外部服务不可用 | |
| **7. 并发与幂等性** | | | **5+** |
| | 重复请求 | 幂等性验证 | |
| | 并发请求 | 多用户同时操作 | |
| | 数据一致性 | 并发数据完整性 | |
| **8. 容错与稳定性** | | | **5+** |
| | 超时 | 请求超时处理 | |
| | 重试 | 失败重试机制 | |
| | 降级 | 服务降级策略 | |
| | 部分失败 | 部分成功处理 | |
| **9. 安全测试** | | | **5+** |
| | SQL注入 | 恶意SQL语句 | |
| | XSS | 跨站脚本攻击 | |
| | 越权访问 | 权限绕过 | |
| | Token校验 | 认证失效 | |
| **10. 性能测试** | | | **5+** |
| | 高并发 | 大量并发请求 | |
| | 大数据量 | 大数据集处理 | |

**TOTAL MINIMUM from dimensions alone: 50 test cases. This is BEFORE input fields and API endpoints are counted.**

### ⛔ CHECKPOINT 2: Before proceeding to Step 3

- [ ] All 10 testing dimensions have been evaluated for test points
- [ ] Each dimension has at least 5 test points identified
- [ ] Every input field from Step 1 has test points for: valid, boundary-low, boundary-high, invalid, empty/null
- [ ] Every API endpoint from Step 1 has test points for all 7 API dimensions
- [ ] Total test points count ≥ your calibration target
- [ ] If ANY check fails → STOP and identify missing test points before proceeding

---

### Step 3: Select Testing Methods

Choose appropriate testing design methods based on the nature of the requirements. Use the inlined methods reference above.

#### Testing Method Selection Matrix

| Scenario | Primary Methods | Secondary Methods | Coverage Focus |
|----------|-----------------|-------------------|----------------|
| Input validation with ranges | Equivalence Partitioning + Boundary Value Analysis | Error Guessing | 维度2,3 |
| Complex business rules | Decision Table + Cause-Effect Graphing | Scenario Testing | 维度4 |
| Multiple configuration options | Orthogonal Array Testing + Pairwise | Error Guessing | 组合测试 |
| Workflow/State-based system | State Transition Testing + Scenario Testing | Error Guessing | 维度5 |
| API/Interface testing | All methods + Concurrency + Security | Fault tolerance | All 10 dimensions |
| General coverage | Combine multiple methods | Self-check mechanism | All dimensions |

#### Enhanced Method Application

**1. Scenario Testing**
- **When to use**: User workflows, end-to-end testing
- **How to apply**:
  - Identify user personas and goals
  - Map user journeys through the system
  - Create scenarios covering happy path + error paths
  - Example: "用户登录 -> 浏览商品 -> 加入购物车 -> 下单支付"

**2. Error Guessing (Enhanced)**
- **When to use**: All scenarios, especially high-risk areas
- **How to apply**:
  - Leverage historical bug data
  - Consider common pitfalls (off-by-one, null pointer, race conditions)
  - Think about edge cases from user perspective
  - Use the Common Error Patterns Table from the inlined reference above

### ⛔ CHECKPOINT 3: Before proceeding to Step 4

- [ ] Testing methods selected for each dimension
- [ ] Equivalence Partitioning applied to all input fields
- [ ] Boundary Value Analysis applied to all numeric/range constraints
- [ ] Decision Table constructed for complex business rules
- [ ] State Transition diagram/table created for workflow elements
- [ ] Error Guessing applied to high-risk areas
- [ ] If ANY check fails → STOP and complete method selection before proceeding

---

### Step 4: Generate Test Cases (THE CORE OUTPUT — DO NOT ABBREVIATE)

**CRITICAL ENFORCEMENT RULES FOR THIS STEP:**
- **DO NOT** use "..." or "等" to skip cases — write every single test case
- **DO NOT** merge scenarios — each unique scenario gets its own row
- **DO NOT** write "similar to TC-XXX" — duplicate the full content
- **DO NOT** stop generating because output is long — completeness is mandatory

#### 4.1 Functional Test Cases

```markdown
| 用例ID | 用例标题 | 前置条件 | 测试步骤 | 输入数据 | 预期结果 | 用例类型 | 优先级 |
|--------|---------|---------|---------|---------|---------|---------|--------|
| TC-FUNC-001 | 功能测试-正常流程 | [前置条件] | 1. 步骤1<br>2. 步骤2 | [输入数据] | [预期结果] | 功能测试 | P0 |
```

**用例类型 (Test Type):**
- 功能测试 (FUNC)
- 输入测试 (INPUT)
- 边界测试 (BOUND)
- 业务规则 (BIZ)
- 状态流转 (STATE)
- 异常测试 (EX)
- 并发测试 (CONC)
- 容错测试 (FAULT)
- 安全测试 (SEC)
- 性能测试 (PERF)

#### 4.2 API Test Cases

For API/interface testing, use dedicated format covering 7 dimensions:

```markdown
| 用例ID | 接口名称 | 测试场景 | 请求方法 | 请求参数 | 预期结果 | 测试维度 | 优先级 |
|--------|---------|---------|---------|---------|---------|---------|--------|
| TC-API-001 | /api/endpoint | 参数校验-必填参数缺失 | POST | {} | HTTP 400<br>{"code":"PARAM_MISSING"} | 1.参数校验 | P0 |
```

**API Testing 7 Dimensions (EVERY endpoint MUST have cases for ALL 7):**

1. **参数校验 (Parameter Validation)**
   - 必填参数缺失
   - 类型错误
   - 长度/范围限制
   - 非法值/特殊字符

2. **功能验证 (Functional Validation)**
   - 正常请求返回正确数据
   - 业务逻辑正确执行
   - 数据正确存储/更新

3. **异常处理 (Exception Handling)**
   - 错误码正确性
   - 异常返回格式
   - 错误信息准确性

4. **幂等性 (Idempotency)**
   - 重复调用结果一致
   - 唯一标识正确处理
   - 防重复提交机制

5. **并发 (Concurrency)**
   - 多请求竞争
   - 数据一致性
   - 锁机制正确性

6. **性能 (Performance)**
   - 响应时间达标
   - QPS满足要求
   - 资源消耗合理

7. **容错 (Fault Tolerance)**
   - 超时处理
   - 重试机制
   - 服务降级
   - 部分失败处理

**Priority Guidelines:**
- **P0**: Core functionality, critical paths, must-pass scenarios, security vulnerabilities
- **P1**: Important features, edge cases, common error scenarios, concurrency issues
- **P2**: Nice-to-have, rare scenarios, cosmetic issues, performance optimization

#### 4.3 Generation Order (MANDATORY SEQUENCE)

Generate test cases in THIS exact order to ensure no dimension is skipped:

1. **功能测试 (FUNC)** — All happy paths + branch paths
2. **输入测试 (INPUT)** — For EACH input field: valid, boundary-low, boundary-high, invalid, empty/null
3. **边界测试 (BOUND)** — All boundary values from BVA analysis
4. **业务规则 (BIZ)** — All decision table rules + conflict scenarios
5. **状态流转 (STATE)** — All valid transitions + all invalid transition attempts
6. **异常测试 (EX)** — All exception scenarios (param missing, data not found, service down)
7. **并发与幂等性 (CONC)** — All concurrency + idempotency scenarios
8. **容错与稳定性 (FAULT)** — All timeout, retry, degradation scenarios
9. **安全测试 (SEC)** — SQL injection, XSS, authorization bypass, token validation
10. **性能测试 (PERF)** — Load testing, large data, response time

### ⛔ CHECKPOINT 4: Before proceeding to Step 5

- [ ] Total test cases generated ≥ calibration target from Step 1
- [ ] Every input field has ≥ 5 test cases (valid + boundary-low + boundary-high + invalid + empty/null)
- [ ] Every API endpoint has ≥ 7 test cases (one per API dimension)
- [ ] All 10 dimensions have ≥ 5 test cases each
- [ ] No test case uses "..." or "等" as placeholder
- [ ] No test cases are merged or abbreviated
- [ ] Count by dimension:
  - 功能测试 (FUNC): ___ cases
  - 输入测试 (INPUT): ___ cases
  - 边界测试 (BOUND): ___ cases
  - 业务规则 (BIZ): ___ cases
  - 状态流转 (STATE): ___ cases
  - 异常测试 (EX): ___ cases
  - 并发测试 (CONC): ___ cases
  - 容错测试 (FAULT): ___ cases
  - 安全测试 (SEC): ___ cases
  - 性能测试 (PERF): ___ cases
  - **TOTAL: ___ cases**
- [ ] If total < calibration target → STOP and go back to generate more cases

---

### Step 5: Coverage Analysis

Verify test coverage across all dimensions:

#### 5.1 Coverage Checklist

```markdown
### 测试覆盖度检查

#### 测试设计方法覆盖
- [ ] 等价类划分 (Equivalence Partitioning)
- [ ] 边界值分析 (Boundary Value Analysis)
- [ ] 判定表 (Decision Table)
- [ ] 状态迁移 (State Transition)
- [ ] 场景法 (Scenario Testing)
- [ ] 错误推测 (Error Guessing)
- [ ] 正交/组合测试 (Orthogonal/Pairwise)

#### 测试维度覆盖
- [ ] 1. 功能测试 (Functionality)
- [ ] 2. 输入测试 (Input)
- [ ] 3. 边界测试 (Boundary)
- [ ] 4. 业务规则 (Business Rules)
- [ ] 5. 状态流转 (State Transition)
- [ ] 6. 异常测试 (Exceptions)
- [ ] 7. 并发与幂等性 (Concurrency & Idempotency)
- [ ] 8. 容错与稳定性 (Fault Tolerance)
- [ ] 9. 安全测试 (Security)
- [ ] 10. 性能测试 (Performance)

#### API测试覆盖（如适用）
- [ ] 1. 参数校验
- [ ] 2. 功能验证
- [ ] 3. 异常处理
- [ ] 4. 幂等性
- [ ] 5. 并发
- [ ] 6. 性能
- [ ] 7. 容错
```

#### 5.2 Coverage Matrix

```markdown
| 测试设计方法 | 覆盖场景 | 用例数量 | 覆盖度评估 |
|------------|---------|---------|-----------|
| 等价类划分 | 输入验证、数据类型 | XX | 高/中/低 |
| 边界值分析 | 数值范围、长度限制 | XX | 高/中/低 |
| 判定表 | 多条件组合 | XX | 高/中/低 |
| 状态迁移 | 工作流、状态变更 | XX | 高/中/低 |
| 场景法 | 用户路径 | XX | 高/中/低 |
| 错误推测 | 异常情况 | XX | 高/中/低 |
```

### ⛔ CHECKPOINT 5: Before proceeding to Step 6

- [ ] Coverage checklist completed with ALL checkboxes ticked
- [ ] Coverage matrix filled with actual case counts (no "XX" placeholders)
- [ ] Every method listed has corresponding test cases
- [ ] Every dimension listed has ≥ 5 test cases
- [ ] If ANY dimension has 0 cases → STOP and generate cases for it NOW

---

### Step 6: Self-Check Gate (MANDATORY — YOU MUST NOT SKIP)

⛔ **STOP. Before finalizing, verify ALL of these hard gates:**

#### Gate 1: Total Count
```
Count total test cases: ___
Calibration minimum target: ___
PASS if total ≥ target, FAIL if total < target
```
**If FAIL → INCOMPLETE. Go back to Step 4 and supplement.**

#### Gate 2: API Endpoint Coverage
```
For EACH API endpoint:
  Count test cases for this endpoint: ___
  PASS if ≥ 7, FAIL if < 7

Endpoint 1: [name] → [count] cases → PASS/FAIL
Endpoint 2: [name] → [count] cases → PASS/FAIL
...
```
**If ANY endpoint FAILS → INCOMPLETE. Go back to Step 4 and supplement.**

#### Gate 3: Input Field Coverage
```
For EACH input field:
  Count test cases covering this field: ___
  PASS if ≥ 5, FAIL if < 5

Field 1: [name] → [count] cases → PASS/FAIL
Field 2: [name] → [count] cases → PASS/FAIL
...
```
**If ANY field FAILS → INCOMPLETE. Go back to Step 4 and supplement.**

#### Gate 4: Dimension Coverage
```
For EACH of 10 dimensions:
  Count test cases in this dimension: ___
  PASS if ≥ 5, FAIL if 0

1. 功能测试: ___ cases → PASS/FAIL
2. 输入测试: ___ cases → PASS/FAIL
3. 边界测试: ___ cases → PASS/FAIL
4. 业务规则: ___ cases → PASS/FAIL
5. 状态流转: ___ cases → PASS/FAIL
6. 异常测试: ___ cases → PASS/FAIL
7. 并发与幂等性: ___ cases → PASS/FAIL
8. 容错与稳定性: ___ cases → PASS/FAIL
9. 安全测试: ___ cases → PASS/FAIL
10. 性能测试: ___ cases → PASS/FAIL
```
**If ANY dimension has 0 cases → INCOMPLETE. Go back to Step 4 and supplement.**

#### Gate 5: Content Quality
- [ ] No test case uses placeholder text ("等", "...", "etc.")
- [ ] No test case says "similar to TC-XXX" without full content
- [ ] Every test case has specific input data (not vague descriptions)
- [ ] Every test case has specific expected result (not "should work")
- [ ] Every test case has clear test steps
**If ANY fails → INCOMPLETE. Fix before proceeding.**

#### Gate 6: Self-Check Questions

1. **是否覆盖所有功能点？**
   - [ ] 所有需求点都有对应测试用例
   - [ ] 正常流程和分支流程都覆盖
   - 遗漏功能点: [列出]

2. **是否遗漏边界情况？**
   - [ ] 输入边界值测试完整
   - [ ] 时间边界（开始/结束时间）
   - [ ] 数值边界（最大/最小值）
   - 遗漏边界: [列出]

3. **是否覆盖异常流程？**
   - [ ] 参数异常（缺失、错误、超限）
   - [ ] 业务异常（数据不存在、状态错误）
   - [ ] 系统异常（超时、服务不可用）
   - 遗漏异常: [列出]

4. **是否存在遗漏的高风险场景？**
   - [ ] 并发场景（重复提交、竞争条件）
   - [ ] 安全场景（注入、越权）
   - [ ] 数据一致性场景
   - 遗漏高风险: [列出]

5. **是否有冗余或重复用例？**
   - [ ] 检查重复测试点
   - [ ] 合并相似用例
   - 冗余用例: [列出]

6. **是否覆盖所有API接口？**
   - [ ] 每个识别出的API接口都有对应测试用例
   - [ ] 每个接口至少覆盖参数校验、功能验证2个维度（P0级）
   - [ ] 关键接口覆盖幂等性、并发、异常处理（P0/P1级）
   - 遗漏接口: [列出接口名称]
   - 遗漏接口的测试维度: [列出维度]

**Action**: If any question has "遗漏" items, **补充测试用例** before proceeding.

**Additional Action for API Coverage:**
- If question 6 has "遗漏接口", you MUST create test cases for those interfaces immediately
- Use the 7-dimension API testing framework for each missing endpoint
- Minimum coverage: 参数校验 + 功能验证 (P0)
- Recommended coverage: All 7 dimensions for critical endpoints

### ⛔ CHECKPOINT 6: Before proceeding to Step 7

- [ ] Gate 1 PASSED (total count ≥ target)
- [ ] Gate 2 PASSED (every API endpoint ≥ 7 cases)
- [ ] Gate 3 PASSED (every input field ≥ 5 cases)
- [ ] Gate 4 PASSED (every dimension has ≥ 5 cases, none has 0)
- [ ] Gate 5 PASSED (no placeholder text, all cases have specific data)
- [ ] Gate 6 PASSED (all 6 self-check questions answered, no 遗漏 items)
- [ ] If ANY gate FAILED → STOP, go back to Step 4, supplement, and re-run ALL gates

---

### Step 7: Review and Refine

Final review checklist:
- [ ] No redundant test cases
- [ ] All requirements have corresponding test cases
- [ ] Test cases are independent and executable
- [ ] Expected results are clear and verifiable
- [ ] Priority assignment is reasonable
- [ ] **Self-check Gate 6 completed — ALL 6 gates PASSED**
- [ ] **All 10 testing dimensions have ≥ 5 cases each**
- [ ] **API testing 7 dimensions covered for every endpoint**
- [ ] **ALL API endpoints identified in Step 1 have test cases**
- [ ] **Total test case count meets or exceeds calibration target**

---

## Output Format (COMPLETE OUTPUT TEMPLATE)

### 1. 测试点分析 (Test Points Analysis)

```markdown
### 测试点分析

**功能点:**
- 功能1: [描述]
- 功能2: [描述]

**API接口清单（CRITICAL — 必须）:**
**用户端接口:**
- 接口1: GET/POST /api/path1 - [功能描述]
- 接口2: GET/POST /api/path2 - [功能描述]

**后台管理接口:**
- 接口3: GET/POST /admin/path3 - [功能描述]
- 接口4: GET/POST /admin/path4 - [功能描述]

**输入参数:**
| 字段名 | 类型 | 必填 | 约束条件 |
|--------|------|------|----------|
| ... | ... | ... | ... |

**业务规则:**
- 规则1: [条件 -> 结果]

**状态流:**
[状态图或文字描述]

**外部依赖:**
- 依赖1: [描述]

**风险点:**
- 风险1: [高危逻辑]

**Output Calibration:**
- Input fields: [F] fields → [F × 5] minimum input cases
- API endpoints: [A] endpoints → [A × 7] minimum API cases
- Dimension baseline: 10 × 5 = 50 minimum
- **TOTAL TARGET: [number] test cases minimum**
```

### 2. 功能测试用例 (Functional Test Cases)

```markdown
### 功能测试用例

| 用例ID | 用例标题 | 前置条件 | 测试步骤 | 输入数据 | 预期结果 | 用例类型 | 优先级 |
|--------|---------|---------|---------|---------|---------|---------|--------|
| TC-FUNC-001 | [具体标题] | [具体条件] | [具体步骤] | [具体数据] | [具体结果] | 功能测试 | P0 |
```

### 3. 接口测试用例 (API Test Cases)

```markdown
### 接口测试用例

| 用例ID | 接口名称 | 测试场景 | 请求方法 | 请求参数 | 预期结果 | 测试维度 | 优先级 |
|--------|---------|---------|---------|---------|---------|---------|--------|
| TC-API-001 | /api/xxx | 参数校验-必填参数缺失 | POST | {} | HTTP 400 | 1.参数校验 | P0 |
```

### 4. 覆盖说明 (Coverage Report)

```markdown
### 覆盖说明

**测试设计方法:**
- [x] 等价类划分 ✔
- [x] 边界值分析 ✔
- [x] 判定表 ✔
- [x] 状态迁移 ✔
- [x] 场景法 ✔
- [x] 错误推测 ✔
- [x] 并发 ✔
- [x] 安全 ✔

**测试维度:**
- [x] 1. 功能测试 — [N] cases
- [x] 2. 输入测试 — [N] cases
- [x] 3. 边界测试 — [N] cases
- [x] 4. 业务规则 — [N] cases
- [x] 5. 状态流转 — [N] cases
- [x] 6. 异常测试 — [N] cases
- [x] 7. 并发与幂等性 — [N] cases
- [x] 8. 容错与稳定性 — [N] cases
- [x] 9. 安全测试 — [N] cases
- [x] 10. 性能测试 — [N] cases
```

### 5. 自检与补充 (Self-Check Gate Results)

```markdown
### 自检与补充

**Gate 1 - Total Count:** [PASS/FAIL] — [actual] / [target]
**Gate 2 - API Coverage:** [PASS/FAIL] — all endpoints ≥ 7 cases
**Gate 3 - Input Coverage:** [PASS/FAIL] — all fields ≥ 5 cases
**Gate 4 - Dimension Coverage:** [PASS/FAIL] — all dimensions ≥ 5 cases
**Gate 5 - Content Quality:** [PASS/FAIL] — no placeholders
**Gate 6 - Self-Check:** [PASS/FAIL] — no 遗漏 items

1. **是否覆盖所有功能点？**
   ✅ 所有需求点已覆盖
   - [列出已覆盖的功能点]

2. **是否遗漏边界情况？**
   ✅ 边界情况已完整覆盖
   - [列出边界测试用例]

3. **是否覆盖异常流程？**
   ✅ 异常流程已系统化覆盖
   - [列出异常测试用例]

4. **是否存在遗漏的高风险场景？**
   ✅ 高风险场景已覆盖
   - 并发场景: TC-CONC-001 ~ TC-CONC-XXX
   - 安全场景: TC-SEC-001 ~ TC-SEC-XXX

5. **是否有冗余或重复用例？**
   ✅ 已检查无冗余用例
   - [说明去重情况]

6. **是否覆盖所有API接口？**
   ✅ 所有接口已覆盖
   - [列出每个接口的用例数量]

**补充用例:** (如有遗漏)
- [补充的测试用例]
```

### 6. 测试总结报告 (Summary Report)

```markdown
### 测试总结

**用例统计:**
- 总用例数: XXX条
- P0用例: XX条 (XX%)
- P1用例: XX条 (XX%)
- P2用例: XX条 (XX%)

**按维度统计:**
- 功能测试: XX条
- 输入测试: XX条
- 边界测试: XX条
- 业务规则: XX条
- 状态流转: XX条
- 异常测试: XX条
- 并发测试: XX条
- 容错测试: XX条
- 安全测试: XX条
- 性能测试: XX条

**覆盖度评估:**
- 功能覆盖: 100%
- 输入覆盖: 100%
- 边界覆盖: 100%
- 异常覆盖: 100%
- 并发覆盖: 100%
- 安全覆盖: 100%

**风险点识别:**
- 风险1: [描述]
- 风险2: [描述]

**建议:**
- 建议1: [描述]
- 建议2: [描述]

**Gate Verification:**
- Total cases vs target: [actual] / [target] → PASS/FAIL
- All 6 self-check gates: PASS/FAIL
```

---

## Export Scripts (Optional)

### Excel Export
Use `scripts/export_to_excel.py` to export test cases to Excel format.

**Best Practices:**
- Always check data types before comparison (`isinstance(value, (int, float))`)
- Handle MergedCell exceptions when iterating columns
- Use proper imports (`from openpyxl.cell.cell import MergedCell`)
- Test code incrementally — don't generate all data at once
- Verify file creation with `ls -lh` before declaring success

### XMind Export
Use `scripts/export_to_xmind.py` to export test cases to XMind mind map format.

---

## Best Practices

1. **Start with requirements analysis** — Don't jump to test cases without understanding the system
2. **Use multiple methods** — No single method provides complete coverage
3. **Prioritize ruthlessly** — Focus on high-risk, high-value scenarios
4. **Avoid redundancy** — Each test case should test something unique
5. **Make tests independent** — Each test should be executable in isolation
6. **Specify expected results clearly** — Ambiguous expected results lead to unreliable tests
7. **Consider non-functional aspects** — Performance, security, compatibility
8. **Think about edge cases** — Boundaries, nulls, empty strings, maximums
9. **Include negative tests** — Not just happy path
10. **Document assumptions** — Make implicit requirements explicit
11. **Always run self-check gates** — Ensure completeness before finalizing
12. **Cover all 10 dimensions** — Don't skip concurrency, security, fault tolerance
13. **API testing must cover 7 dimensions** — Especially idempotency and concurrency
14. **Identify risk points early** — Focus on high-risk areas
15. **Excel generation best practices** — Avoid common Python/openpyxl errors:
    - Always check data types before comparison (`isinstance(value, (int, float))`)
    - Handle MergedCell exceptions when iterating columns
    - Use proper imports (`from openpyxl.cell.cell import MergedCell`)
    - Test code incrementally — don't generate all data at once
    - Verify file creation with `ls -lh` before declaring success
16. **Code quality in generation scripts** — Prevent syntax errors:
    - Verify all parentheses are matched
    - Use proper string escaping for newlines in cell values
    - Test simple version first, then add complexity
    - Use type checking before operations (`isinstance`, `type()`)
    - Handle exceptions gracefully with try-except
17. **Output file validation** — Always verify generated files:
    - Check file exists and size > 0
    - Validate sheet count and structure
    - Test opening file with pandas/openpyxl
    - Verify data integrity (row counts, priorities)
    - Provide summary statistics to user

---

## Example Usage

**User Input:**
```
分析一下这个需求文档，生成测试用例
[Requirement document content]
```

**Expected Output Sections:**
1. ✅ 需求解析（8个方面 — including API list and calibration target）
2. ✅ 测试点分析（10个维度，每个维度 ≥ 5 test points）
3. ✅ 功能测试用例（表格 — ALL cases written explicitly, no abbreviations）
4. ✅ 接口测试用例（表格 — ≥ 7 cases per endpoint）
5. ✅ 覆盖说明（清单 with actual case counts per dimension）
6. ✅ 自检与补充（6 gates PASS/FAIL + 6 questions）
7. ✅ 测试总结报告（with dimension-by-dimension statistics）

**Output Size Expectation:**
- Simple requirement → 80-120 test cases
- Medium requirement → 150-250 test cases
- Complex requirement → 250-400+ test cases
- **If you're producing < 80 test cases for any non-trivial requirement, you are ABBREVIATING and VIOLATING enforcement rules**

---

## Changelog

### v3.0 (Enforcement Edition — CURRENT)
- ✅ Added ⚠️ 执行铁律 (Mandatory Enforcement Rules) section at top
- ✅ Added quantitative output calibration (Simple/Medium/Complex targets)
- ✅ Added 🚫 Prohibited Behaviors section
- ✅ Added ⛔ CHECKPOINTS between EVERY step (Checkpoints 0-6)
- ✅ Inlined ALL essential testing methodology (Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition, Error Guessing, Method Selection Guide)
- ✅ Converted Step 6 Self-Check from soft recommendations to hard quantitative gates (6 gates)
- ✅ Added mandatory generation order in Step 4 (dimension-by-dimension)
- ✅ Added per-dimension minimum case counts in Step 2
- ✅ Added Gate Verification to output format
- ✅ Made file completely self-contained (no required external reads)
- ✅ Enhanced calibration target calculation formula

### v2.3 (Code Quality & Output Validation)
- ✅ Added Excel generation best practices (MergedCell handling, type checking)
- ✅ Added Python script error prevention guidelines
- ✅ Added output file validation checklist

### v2.2 (Document Reading Enhancement)
- ✅ Added Step 0: Document Reading and Analysis
- ✅ Enhanced document input format recognition
- ✅ Added visual content extraction strategy

### v2.1 (Critical Fix)
- ✅ Added API endpoint identification in Step 1.2 (MANDATORY)
- ✅ Added 6th self-check question: "是否覆盖所有API接口？"
- ✅ Added automatic API coverage validation mechanism

### v2.0 (Enhanced)
- ✅ Added 10 testing dimensions (vs. 6 in v1.0)
- ✅ Added API testing 7 dimensions
- ✅ Added self-check mechanism
- ✅ Added external dependencies analysis
- ✅ Added risk point identification
