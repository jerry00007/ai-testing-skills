---
name: test-report-generator
description: "Generates professional software test reports following industry best practices (IEEE 829, ISTQB, Minto Pyramid). This skill should be used when the user asks to 'generate test report', 'create test summary', 'write QA report', '测试报告', '测试总结', '生成报告', 'write release test report', or needs to document testing outcomes for stakeholders. Supports both Chinese and English reports. Produces structured Markdown reports with executive summary, test execution results, risk assessment, coverage analysis, and Go/No-Go recommendations."
---

# Test Report Generator

## Overview

Generate professional, stakeholder-ready test reports that follow industry best practices. Reports use the Minto Pyramid principle (verdict first, details second) and cover all essential sections from IEEE 829 and ISTQB standards, adapted for Chinese tech company conventions.

## When to Use

Trigger this skill when:
- User asks for a test report, test summary, QA report, or release report
- User says "生成测试报告", "测试总结", "生成报告", "write test report"
- Testing is complete and results need to be documented
- A release decision requires a formal test sign-off document

## Report Generation Workflow

### Step 1: Determine Report Type

Ask or infer the report type based on context:

| Type | Trigger | Length | Key Focus |
|------|---------|--------|-----------|
| **Sprint 测试摘要** | Sprint/迭代结束 | 1-2 pages | Pass/fail summary, new defects |
| **发布测试报告** | 上线前正式报告 | 5-10 pages | Full coverage, risk, Go/No-Go |
| **回归测试报告** | 版本间回归 | 2-3 pages | Regression comparison, trend |
| **功能验证报告** | 单功能验证 | 3-5 pages | Feature-specific deep dive |

Default to **发布测试报告** if unspecified.

### Step 2: Gather Information

Collect from the user or conversation context:
1. **Project metadata**: Name, branch, environment, API path, target PID/scene
2. **Requirements**: What was the business goal? What changed?
3. **Test data**: How many tests/cases/devices/requests? Pass/fail counts?
4. **Metrics**: Key quantitative evidence (pass rates, similarity scores, response times)
5. **Defects/Issues**: What problems were found? Severity? Status?
6. **Risks**: Known risks, mitigations, open concerns
7. **Coverage**: What was tested? What was NOT tested and why?

### Step 3: Apply the Minto Pyramid

**Verdict first.** The report must lead with the Go/No-Go decision, not bury it on the last page.

```
Structure:
┌─────────────────────────────────────────┐
│ Table Header: 结论 = PASS/CONDITIONAL/FAIL │  ← First thing seen
├─────────────────────────────────────────┤
│ Section 一: 执行摘要 (3 paragraphs)       │  ← Executive summary
├─────────────────────────────────────────┤
│ Section 二~七: Supporting evidence         │  ← Details
├─────────────────────────────────────────┤
│ Section 八~九: Open items & Conclusion     │  ← Recommendations
├─────────────────────────────────────────┤
│ Appendix: Raw data, env info, glossary     │  ← Reference
└─────────────────────────────────────────┘
```

### Step 4: Write Each Section

Use the template at `@assets/test_report_template.md` as the structural guide. Below are quality requirements per section:

#### 执行摘要 (Executive Summary)
- **Length**: 3-5 sentences (1 paragraph for sprint, 2-3 for release)
- **Must contain**: Test scope, total volume, pass rate, key finding, Go/No-Go
- **Audience**: Executives who only read this section
- **Write LAST** (after all other sections are complete)

#### 需求背景与业务逻辑
- Explain the "why" before the "what"
- Include experiment design table if AB testing
- Define acronyms on first use

#### 代码改动分析
- Show actual code snippet with file path and line numbers
- Quantify the change scope (e.g., "3 lines changed", "1 function modified")
- Distinguish between logic change vs config/field swap

#### 测试策略与方法论
- Explain the verification approach in plain language
- Define judgment criteria with thresholds
- Explain WHY the chosen method was used (and why alternatives were rejected)

#### 测试执行与结果
- Use tables for quantitative data (not paragraphs)
- Include multi-round comparison if applicable
- Always show BOTH absolute numbers AND percentages
- Highlight anomalies and edge cases explicitly
- Add interpretation after each table (what does this number mean?)

#### 风险评估
- Every risk needs: ID, description, severity, probability, status, mitigation
- Use traffic light indicators (🟢🟡🔴)
- Include exit criteria checklist
- Be honest about limitations — hiding risks destroys credibility

#### 测试覆盖度评估
- Two subsections: "Covered" and "Not Covered"
- For uncovered items: state reason, impact, and recommendation
- This section is critical for building trust with readers

#### 测试结论
- Rating matrix across dimensions (functionality, coverage, risk)
- Explicit Go/No-Go with conditions
- Deliverables list for traceability

### Step 5: Quality Checklist

Before finalizing, verify:

```
Content Quality:
[ ] Verdict (Go/No-Go) appears in the FIRST screen (header table)
[ ] Executive summary is ≤ 5 sentences and contains the verdict
[ ] Every claim is backed by data (no "feels good" statements)
[ ] Risks are honest and include mitigations
[ ] Uncovered areas are explicitly stated with reasons
[ ] Exit criteria are checked (or noted as unmet)

Formatting:
[ ] Tables use consistent column alignment
[ ] Traffic lights (🟢🟡🔴) used for status indicators
[ ] Code snippets include file path and line numbers
[ ] Acronyms defined on first use
[ ] Appendix contains environment info and glossary

Audience Check:
[ ] An executive can understand the conclusion from the header + summary alone
[ ] A developer can trace from conclusion → evidence → raw data
[ ] A QA peer can reproduce the test from the methodology section
[ ] No section exceeds 2 pages (break up or move to appendix if longer)
```

### Step 6: Output

- Default output format: **Markdown** (`.md`)
- File naming: `TEST_REPORT.md` or `{project}_TEST_REPORT_{date}.md`
- Language: Match user's language (Chinese or English)
- Length target: 5-10 pages for release reports, 1-2 for sprint summaries

## Key Principles

### Principle 1: Verdict First (Minto Pyramid)
> A test report is a **decision document**, not an execution log. Lead with the Go/No-Go verdict.

### Principle 2: Data Over Adjectives
> Replace "excellent performance" with "pass rate 99.5%, 5000 requests, 0 critical defects". Use numbers, not opinions.

### Principle 3: Risks Are Mandatory
> Every report must include a risk assessment. Hiding risks to get a "pass" destroys trust permanently.

### Principle 4: Audience Layering
> Executives read the summary. Engineers read the details. Auditors read the appendix. Design for all three.

### Principle 5: Trends Over Snapshots
> Compare with previous baselines whenever possible. "Pass rate improved from 92% to 98%" is more valuable than "Pass rate is 98%".

## Resources

### references/
- `@references/best_practices.md` — Industry best practices compiled from IEEE 829, ISTQB, ForaSoft, TestRail, VirtuosoQA. Contains the 7 core metrics framework, risk matrix standards, exit criteria patterns, and common mistakes to avoid. Load this reference when needing detailed guidance on report structure or metric selection.

### assets/
- `@assets/test_report_template.md` — Fillable Markdown template with all sections, placeholders, and formatting guidance. Copy this template as the starting point for each report, then fill in with actual data.

## Defect Severity Standards

Use consistent severity taxonomy throughout the report:

| 等级 | 英文 | 中文 | 定义 |
|:----:|------|------|------|
| S1 | Blocker | 致命 | 系统崩溃、数据丢失、安全漏洞 |
| S2 | Critical | 严重 | 核心功能不可用，无绕过方案 |
| S3 | Major | 一般 | 功能缺陷，有绕过方案 |
| S4 | Minor | 轻微 | UI/体验问题，不影响功能 |

> Lock one taxonomy and use it consistently across all reports. Do not mix S1-S4 with Blocker/Critical.

## Adaptation Guidelines

### For API/Business Logic Testing
- Emphasize: parameter coverage, boundary testing, exception handling
- Key metrics: API response correctness, error rate, response time
- Include: API request/response examples in appendix

### For AB Experiment Testing
- Emphasize: experiment bucket isolation, control vs treatment comparison
- Key metrics: similarity scores, distribution differences, statistical significance
- Include: experiment configuration table, bucket assignment verification

### For Performance Testing
- Emphasize: baseline comparison, resource utilization trends
- Key metrics: P95/P99 latency, throughput, error rate under load
- Include: performance trend charts, bottleneck analysis

### For Regression Testing
- Emphasize: comparison with previous release baseline
- Key metrics: new failures count, resolved issues count, stability trend
- Include: regression matrix (module × test type × result)
