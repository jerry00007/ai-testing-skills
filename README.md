# AI Testing Skills — AI 测试全链路技能集

[English](#english) | 中文

基于 OpenCode / Claude Code 等 AI 编程助手的 **Skill 体系**，覆盖测试全流程：**需求评审 → 用例设计 → 自动执行 → 结果分析 → 测试报告 → 反馈文档 → 代码审查**。将资深测试工程师的方法论沉淀为可复用、可分发、可组合的 AI 技能，实现"需求文档进、测试报告出"的全链路 AI 化。

## 效率收益（实测）

| 指标 | 传统方式 | 使用 Skill | 提升 |
|------|---------|-----------|------|
| 需求问题发现率 | ~10% | ≥60% | **6 倍** |
| 用例编写耗时 | ~4 小时 | ~10 分钟 | **25 倍** |
| 测试全流程 | ~3 天 | ~半天 | **6 倍** |
| 用例覆盖维度 | 3-5 维 | 10 维系统覆盖 | **2-3 倍** |

## 技能总览（9 个）

| 技能 | 定位 | 核心能力 |
|------|------|---------|
| [three-musketeers](three-musketeers/) | 需求评审 | 产品/架构/QA 三角色深度剖析 + 红蓝对抗互质询，提前发现需求缺陷 |
| [requirement-review](requirement-review/) | PRD 评审 | 知识库交叉验证协议，先基于代码库自动解答、再聚焦真正需要产品确认的问题 |
| [test-case-generator](test-case-generator/) | 测试设计 | 10 维度系统化用例生成（功能/输入/边界/业务规则/状态/异常/并发幂等/容错/安全/性能）+ 6 项量化硬门禁，支持 Excel/XMind 导出 |
| [api-test-auto-runner](api-test-auto-runner/) | 自动化执行 | 生成 Python 测试脚本 → 自动执行（3 次自修复）→ Bug 归因决策树（区分脚本 Bug/产品 Bug/API 变更/环境问题）→ Excel/MD 报告 |
| [rcm-test-generator](rcm-test-generator/) | 推荐系统测试 | 推荐引擎实验测试用例生成：exp_info / test_api / test_log 三件套，AB 多桶对比、召回通路验证 |
| [test-result-analysis](test-result-analysis/) | 结果分析 | 证据驱动：实际运行命令取原始输出、基线对比区分增量、失败归因四分类、PASS/FAIL/PARTIAL 结论 |
| [test-feedback-doc](test-feedback-doc/) | 反馈文档 | 需求原文 + 代码实现逻辑 + 修复建议 + 脚本真实执行数据四要素齐全，Go/No-Go 结论先行 |
| [test-report-generator](test-report-generator/) | 测试报告 | IEEE 829 / ISTQB / Minto 金字塔结构化测试报告，支持中英文 |
| [code-review](code-review/) | 代码审查 | 多视角代码审查（产品/架构/QA）+ 社区最佳实践，内置定级校准机制防止严重性虚高 |

## 全链路工作流

```
需求文档 / PRD
     │
     ▼
[three-musketeers] 需求评审 —— 发现需求缺陷、风险点
     │
     ▼
[test-case-generator] 用例生成 —— 10 维度全覆盖 + 量化门禁
     │
     ▼
[api-test-auto-runner] 自动执行 —— 脚本生成 → 执行 → Bug 归因
     │
     ▼
[test-result-analysis] 结果分析 —— 基线对比 + 增量归因
     │
     ▼
[test-feedback-doc / test-report-generator] 反馈文档 / 测试报告
```

三个环节可独立使用，也可串联形成完整测试流程；[code-review](code-review/) 贯穿开发阶段，[requirement-review](requirement-review/) 与 [rcm-test-generator](rcm-test-generator/) 面向专项场景。

## 安装

```bash
# OpenCode
cp -r <skill-dir> ~/.config/opencode/skills/

# Claude Code
cp -r <skill-dir> ~/.claude/skills/
```

重启 AI 助手会话后技能自动加载，使用各技能文档中的触发词调用。

## 依赖

- [test-case-generator]：Python 3.8+，`pip3 install openpyxl`（Excel 导出）
- [api-test-auto-runner]：Python 3.8+，`pip3 install requests pandas openpyxl`
- 其余技能：无额外依赖

## 目录结构

```
ai-testing-skills/
├── three-musketeers/       # 三剑客需求评审
├── requirement-review/     # PRD 评审 + 知识库交叉验证
├── test-case-generator/    # 用例自动生成 V3.x
├── api-test-auto-runner/   # 脚本执行出报告
├── rcm-test-generator/     # 推荐系统测试生成
├── test-result-analysis/   # 测试结果分析
├── test-feedback-doc/      # 测试反馈文档
├── test-report-generator/  # 测试报告生成
└── code-review/            # 代码审查
```

---

<a id="english"></a>

# AI Testing Skills (English)

A collection of 9 production-grade AI agent skills for OpenCode / Claude Code that cover the **end-to-end testing workflow**: requirement review, test case design (10-dimension systematic coverage with quantitative gates), automated script execution with bug triage, evidence-driven result analysis, feedback docs, and structured test reports (IEEE 829 / ISTQB / Minto Pyramid).

Measured impact: 25x faster test case authoring, 6x faster end-to-end testing cycle, 6x more requirement defects found before development starts.

See the table above for per-skill details. Copy any skill directory into `~/.config/opencode/skills/` (OpenCode) or `~/.claude/skills/` (Claude Code) and restart your session.

## License

MIT
