---
name: rcm-test-generator
description: This skill should be used when user asks to "生成推荐测试用例", "推荐用例", "创建推荐系统测试", "生成RCM测试", or mentions "推荐引擎测试", "召回测试", "实验验证". Helps create test cases for recommendation system including exp_info.py, test_api.py, test_log.py, and documentation. Uses three-musketeers analysis for requirement review and test script QA.
version: 2.2.0
---

# RCM Test Case Generator

This skill helps create automated test cases for the recommendation system (RCM).

## Overview

Generates complete test case structure for recommendation system testing, including:
- Experimental configuration (exp_info.py)
- API testing (test_api.py)
- Log validation (test_log.py)
- API response validation (test_api_response.py) - Optional but recommended
- Documentation (README.md, INSTALL.md, etc.)

## When This Skill Applies

Activate when user requests:
- "生成推荐测试用例"
- "推荐用例"
- "创建推荐系统测试"
- "生成RCM测试"
- "推荐引擎测试"
- "召回测试"
- "实验验证"
- "RCM测试用例"

## Test Case Structure

Standard RCM test case directory structure:

```
test_cases/YYYYMMDD-test-name/
├── exp_info.py          # Experimental configuration
├── test_api.py          # API testing (发起请求并保存完整API返回)
├── test_log.py          # Log validation (需要下载日志文件)
├── test_api_response.py # API response validation (可选，直接从API返回验证)
├── README.md            # Detailed documentation
├── INSTALL.md           # Installation and configuration
├── QUICKSTART.md        # Quick start guide
└── SUMMARY.md           # Test case summary
```

**Note on test_api_response.py:**
- **Optional** test script that validates API responses directly without requiring log files
- **Recommended** for quick validation of fields like `uniq_series_id`, `biz_type`, `biz_id`
- **Complements** `test_log.py` - use both for thorough validation
- **When to generate**: Include if the test case needs to validate response fields directly

## Step-by-Step Guide

### Phase -1: 三剑客需求分析 (MANDATORY - 第一步)

**重要**: 这是整个流程的第一步。在生成任何测试用例之前，必须先使用三剑客方法（产品经理、架构师、QA）对需求进行多角度分析。

#### -1.1 三剑客角色定义

对需求文档进行三个角色的分析：

**🗡️ 产品经理视角**:
- 需求的核心业务价值是什么？
- 影响哪些用户群体？用户行为会发生什么变化？
- 有哪些前置条件和依赖关系？
- 成功标准是什么？如何衡量功能上线效果？
- 是否存在与已有功能的冲突或兼容性问题？

**🗡️ 架构师视角**:
- 需求涉及系统的哪些模块（召回/过滤/排序/干预）？
- 数据流向：请求参数 → 召回逻辑 → 过滤逻辑 → 排序逻辑 → 返回结果
- 是否有性能影响？超时/并发需要关注的点？
- 配置依赖：需要哪些实验参数？ACM/Apollo配置？
- 代码改动范围：新增代码还是修改已有逻辑？

**🗡️ QA视角**:
- 正向测试：功能正常工作的场景有哪些？
- 异常测试：什么条件下功能会失效？
- 边界测试：极限值、空值、特殊字符等
- 兼容性：对不同PID/频道页/设备类型的影响
- 回归测试：是否影响已有功能？
- 测试数据准备：需要什么样的测试账号/设备ID？

#### -1.2 执行方式

1. **阅读需求文档** — 完整理解需求内容
2. **逐一角色分析** — 按上述三个视角输出分析结果
3. **输出关键发现**:
   - 需要确认的问题（提交给用户确认）
   - 关键测试关注点（用于后续Phase）
   - 潜在风险点（需要在测试中重点覆盖）
4. **等待用户确认** — 对发现的问题，等待用户回复后再继续

#### -1.3 输出格式

```markdown
## 三剑客需求分析报告

### 🗡️ 产品经理分析
- **核心价值**: ...
- **影响范围**: ...
- **成功标准**: ...
- **待确认问题**: ...

### 🗡️ 架构师分析
- **涉及模块**: ...
- **数据流向**: ...
- **配置依赖**: ...
- **潜在风险**: ...

### 🗡️ QA分析
- **正向场景**: ...
- **异常场景**: ...
- **边界条件**: ...
- **回归风险**: ...

### ⚠️ 需要人工确认的问题
1. ...
2. ...

### ✅ 关键测试关注点（用于后续Phase）
1. ...
2. ...
```

#### -1.4 注意事项

- **如果需求不明确**: 在"需要人工确认的问题"中列出，等待用户回复
- **如果需求有矛盾**: 指出矛盾点，建议解决方案
- **如果发现代码问题**: 记录在架构师分析的"潜在风险"中
- **不要跳过此步骤**: 即使需求看起来很简单，也要快速过一遍三剑客分析

---

### Phase 0: Query Documentation and Extract Test Points (MANDATORY)

**重要**: 在生成任何测试用例文件之前，必须先完成此阶段，确保测试覆盖全面。

#### 0.1 查询文档目录

在生成测试用例前，**必须**查询以下文档目录，提取测试点和功能点：

**文档目录**: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/doc/`

**关键文档**:
- `测试场景分类与参数配置指南.md` - **必查(最先读)**，7大场景分类、PID/URL/参数配置、踩坑防护清单、脚本标准模板
- `测试点文档.md` - **必查**，包含完整的测试点列表（1200行）
- `推荐系统业务逻辑完整文档.md` - **必查**，召回、过滤、排序、干预流程（747行）
- `recall代码知识库.md` - **必查**，召回项目代码架构和逻辑详解（新增）
- `engine代码知识库.md` - **必查**，引擎项目代码架构和逻辑详解（新增）
- `参数值业务逻辑映射文档.md` - 可选，参数映射
- `参数驱动测试文档.md` - 可选，参数驱动测试
- `业务逻辑文档.md` - 可选，业务逻辑说明

#### 0.2 知识库查询流程

**重要**: 知识库查询必须按照以下顺序进行，如果在知识库中找不到相关信息，需要明确提出让用户确认。

```
Step 1: 根据Phase -1的输出，确定需要查询的知识领域
Step 2: 在doc/目录中搜索相关文档
Step 3: 优先查阅"必查"文档
Step 4: 如果找不到，查阅"可选"文档
Step 5: 如果仍然找不到关键信息 → 在"需要人工确认的问题"中列出
```

**查询策略**:
- 如果需求涉及**召回逻辑** → 重点查 `recall代码知识库.md`
- 如果需求涉及**排序/过滤/干预** → 重点查 `engine代码知识库.md`
- 如果需求涉及**测试点覆盖** → 重点查 `测试点文档.md`
- 如果需求涉及**完整流程** → 重点查 `推荐系统业务逻辑完整文档.md`
- 如果需求涉及**参数映射** → 查 `参数值业务逻辑映射文档.md`

**找不到信息时的处理**:
```markdown
### ⚠️ 知识库中未找到的信息

以下信息在当前知识库文档中未找到明确说明，需要人工确认：

1. **[问题描述]**
   - 已查阅文档: [文档列表]
   - 建议: [可能的解决方案或需要咨询的人员]

2. **[问题描述]**
   - ...
```

#### 0.3 提取测试点

使用 Read 工具读取测试点文档，提取相关测试点：

```
1. 读取测试点文档
2. 根据需求关键词搜索相关章节
3. 提取测试模块和测试点列表
4. 记录代码位置信息
```

**关键测试模块**（从测试点文档中提取）:

| 模块 | 文件位置 | 测试优先级 |
|------|---------|----------|
| **召回模块** | `commonrecommend/algorithm/recallengine/` | P0 |
| **过滤模块** | `commonrecommend/algorithm/filter/` (32个过滤器) | P0 |
| **排序模块** | `commonrecommend/algorithm/rank.go` | P0 |
| **干预处理** | `commonrecommend/algorithm/handler/intervention/` (51个文件) | P0 |
| **占位逻辑** | `rank_topn_placeholder.go` | P0 |

#### 0.4 从文档中提取的关键信息

**召回模块测试点**:
- 普通召回：车系召回、品牌召回、作者召回、标签召回
- CF召回：CF召回流程、过滤逻辑、后置截断
- 商业投放召回：投放计划匹配、人群包过滤、城市过滤

**过滤模块测试点**:
- 负反馈过滤：不感兴趣过滤、屏蔽作者过滤
- 曝光过滤：7天曝光过滤、曝光去重
- 业务类型过滤：biztype过滤、优先级排序

**排序模块测试点**:
- 精排排序：RankScore排序、归一化打分、权重计算
- 多样性：召回路多样性、biztype多样性、冷热内容分布
- 硬规则：北斗置顶、第一位biztype限制

**干预处理测试点**:
- 运营干预：置顶内容、屏蔽内容
- 占位逻辑：Top N占位、位置插入
- 无车系过滤：NoAllowTitleSeriesEmpty（top2expC实验）

#### 0.5 生成测试覆盖矩阵

基于提取的测试点，生成测试覆盖矩阵：

| 测试模块 | 测试点 | API验证 | 日志验证 | 优先级 |
|---------|-------|---------|---------|--------|
| 排序模块 | RankScore排序 | ✅ | ✅ | P0 |
| 排序模块 | 归一化打分 | ✅ | ❌ | P1 |
| 排序模块 | Top2占位 | ✅ | ✅ | P0 |
| 过滤模块 | Rtype过滤 | ✅ | ✅ | P0 |
| 过滤模块 | 无车系过滤 | ✅ | ✅ | P1 |
| 干预处理 | 硬规则排除 | ✅ | ✅ | P0 |

#### 0.6 代码位置映射

从文档中提取的代码位置，用于注释和文档：

```python
code_locations = {
    "rank_topn_placeholder": "rank_topn_placeholder.go",
    "isItemValid": "rank_topn_placeholder.go:105-111",
    "filter_no_series": "commonrecommend/algorithm/handler/intervention/handler_intervention.go:872",
    "recall_engine": "commonrecommend/algorithm/recallengine/",
    "filter_module": "commonrecommend/algorithm/filter/",
    "sort_handler": "commonrecommend/algorithm/handler/sort/"
}
```

#### 0.7 输出测试覆盖报告

在 exp_info.py 中添加验证点说明：

```python
validation_points = {
    "rank_score_sorting": "验证Top2位置按RankScore降序排列",
    "rtype_filtering": "验证Top2位置的rtype是否在支持列表中",
    "hard_rule_checking": "验证第一位物料是否符合硬规则要求",
    "normalization": "验证冷启、热点内容的归一化打分",
    "diversity": "验证Top2位置的召回路多样性",
    "no_series_handling": "验证无车系内容是否被正确处理"
}
```

**重要提示**:
1. ✅ 每个测试用例必须在 exp_info.py 中包含 `validation_points`
2. ✅ README.md 中必须说明测试覆盖的测试点
3. ✅ test_api_response.py 中必须实现对应的验证逻辑
4. ✅ 错误日志中必须记录详细的验证失败信息

---

### Phase 0.6: 条件逻辑测试覆盖分析 (MANDATORY)

**重要**: 此阶段确保条件判断逻辑的正反两面都被覆盖。源自实际教训：退场判断条件 `cIdx >= nearIdx && cIdx <= farIdx` 只检查了两次曝光之间的点击，漏掉了最近曝光后的点击，导致已点击用户被误退场。

#### 0.6.1 强制反向用例规则

**每一条 "X 条件 → Y 行为" 的用例，必须配一条 "X 不满足 → Y 不发生" 的反向用例。**

| 正向用例 | 反向用例（必须存在） |
|---------|-------------------|
| 2次曝光 + 0点击 → 退场 | 2次曝光 + 1点击 → **不退场** |
| 实验组触发探索召回 | 对照组 **不触发**探索召回 |
| 探索物料不出现在 top3 | 探索物料 **可以出现**在 top4+ |
| 单 feed ≤ 2 条探索物料 | 单 feed **可以** > 2 条非探索物料 |
| 退场后 series 消失 | 未退场 series **仍然存在** |

**检查方法**: 对覆盖矩阵中的每个 ✅ PASS 项，检查是否有对应的 "不发生" 验证。缺失则标记 `⚠️ 缺反向用例`。

#### 0.6.2 条件分区表（对范围/边界判断强制生成）

对代码中任何 `>=`、`<=`、`&&`、`||` 的条件判断，生成输入分区表：

**示例（退场条件 `cIdx <= farIdx`）:**

| 分区 | cIdx 取值范围 | 含义 | 期望行为 | 需要用例 |
|------|-------------|------|---------|---------|
| A | cIdx < nearIdx | 最近曝光后的点击 | 检测到点击，不退场 | ✅ 必须 |
| B | cIdx == nearIdx | 正好在最近曝光位置 | 检测到点击，不退场 | ✅ 必须 |
| C | nearIdx < cIdx < farIdx | 两次曝光之间 | 检测到点击，不退场 | ✅ 必须 |
| D | cIdx == farIdx | 正好在较早曝光位置 | 检测到点击，不退场 | ⚠️ 建议 |
| E | cIdx > farIdx | 两次曝光之前 | 跳过，可退场 | ✅ 必须 |

**生成规则**:
1. 找出代码中所有条件判断点（if/switch/比较运算符）
2. 对每个条件，列出输入空间的**所有分区**（不只是满足的分区）
3. 为每个分区标注期望行为
4. 标注是否已有用例覆盖
5. 未覆盖的分区 → 必须补充用例或标记为已知盲区

#### 0.6.3 事件序列测试（对时序逻辑强制覆盖）

当功能涉及**事件顺序**（曝光→点击→退场），必须测试多种事件排列：

**退场机制事件序列矩阵:**

| 序列模式 | 事件顺序（新→旧） | 期望结果 | 需要用例 |
|---------|-----------------|---------|---------|
| 纯曝光 | [Exp, Exp] | 退场 | ✅ |
| 曝光+点击(后) | [Click, Exp, Exp] | **不退场** | ✅ 关键 |
| 曝光+点击(中) | [Exp, Click, Exp] | 不退场 | ✅ |
| 曝光+点击(前) | [Exp, Exp, Click] | 退场 | ✅ |
| 单次曝光 | [Exp] | 不退场 | ✅ |
| 曝光+点击(交替) | [Click, Exp, Click, Exp] | 不退场 | ⚠️ 建议 |
| 3次曝光 | [Exp, Exp, Exp] | 退场 | ⚠️ 建议 |

**造数工具要求**: 测试脚本必须支持注入**混合事件类型**（event_type=0 曝光 + event_type=1 点击），不能只注入单类型数据。

#### 0.6.4 代码变更回归验证

当开发修改条件逻辑后，必须：

1. **重新审查新条件**: 不只是验证"修复有效"，要验证新条件的**所有分支**
2. **diff review**: 对比修改前后的条件，确认新条件覆盖了旧条件的所有场景
3. **分区表更新**: 条件变更后重新生成分区表，重新评估覆盖度
4. **反向用例优先**: 修复通常是让"应该生效"的情况生效，但要确认"不应该生效"的情况仍然不生效

#### 0.6.5 输出格式

```markdown
### 条件逻辑覆盖分析

#### 条件1: [条件描述]
- **代码位置**: 文件:行号
- **条件表达式**: `if cIdx >= nearIdx && cIdx <= farIdx`
- **分区表**: [上述表格]
- **反向用例**: [列出]
- **覆盖状态**: ✅ 全覆盖 / ⚠️ 部分覆盖（缺少分区X）

#### 条件2: [条件描述]
- ...
```

---

**重要**: 在进入 Phase 1 之前，必须确定测试场景类型，并据此校验 PID、API路径、实验参数风格、数据解析方式。场景选错 = 全盘皆错。

#### 0.5.1 读取场景分类文档

**必须先读取**: `doc/测试场景分类与参数配置指南.md`

#### 0.5.2 场景自动识别

根据需求关键词自动匹配场景：

| 需求关键词 | 场景 | PID | API路径 | 解析方式 | 实验参数 |
|-----------|------|-----|---------|---------|---------|
| 首页/信息流/推荐实验/召回/排序/调权 | A: 首页推荐 | 100011 | `/rcm/autohmpg2/v3.0/lands` | pv_info+jmespath | `&isDegradeReq=2&testNeedExp={}` (ACM) |
| 点后推/产品力标签 | B: 点后推 | 90100106 | `/rcm/autohmpg2/v3.0/lands` | pv_info+jmespath | `&appexp={}` (**AB平台**) |
| 静默刷新/商业过滤/静默3.0 | C: 静默刷新 | 100011 | `/rcm/autohmpg2/v3.0/lands` | pv_info+jmespath | `&appexp={}` + `autorefresh=1` (**AB平台**) |
| 车展/专题页/沉浸流 | D: 车展 | 90100213/214 | `/oneapi/v2` | resourceobj | 无实验 |
| 车系页/系列页 | E: 车系页 | 90100255等 | `/oneapi/v2` | resourceobj | 内联build |
| 频道页/人群包/车家号/长文 | F: 频道页 | 90100254等 | `/oneapi/v2` | resourceobj | 视情况 |
| 新APP/906 | G: 新APP | 906xxxxx | `/oneapi/v2` | resourceobj | `&appexp={}` |

#### 0.5.3 校验清单（生成代码前逐条检查）

生成 exp_info.py 和 test_api.py 之前，**必须**通过以下校验。任何一项不通过，需在输出中明确标注并修正：

| # | 校验项 | 规则 | 违反后果 |
|---|--------|------|---------|
| 1 | **PID与API路径匹配** | 100011 → `/rcm/autohmpg2/v3.0/lands`; 901/906开头 → `/oneapi/v2` | 接口404 |
| 2 | **PID与解析方式匹配** | 100011/90100106 → pv_info+jmespath; 901/906频道段 → resourceobj+dict.get() | 数据全部为空 |
| 3 | **实验参数风格** | 实验名含字母+下划线 → ACM(`testNeedExp`); 实验名含纯数字+横杠 → AB(`appexp`) | 实验不生效 |
| 4 | **域名** | 默认 `test-api.example.com`; config_url返回线上域名时替换 | 打到线上 |
| 5 | **rec_engine_addr** | 必须填写对应分支召回服务地址(IP:6667) | 打到错误召回引擎 |
| 6 | **operation匹配** | 首页: [0,2,4]; 点后推: 固定0+number=1; 静默刷新: autorefresh=1 | 召回策略不触发 |
| 7 | **频道页ext参数** | 频道页/车系页需 `json.dumps`+`urllib.parse.quote` 编码ext参数 | 参数解析失败 |

#### 0.5.4 输出场景识别结果

在 Phase 1 之前，输出明确的场景判定：

```markdown
### 场景识别结果
- **场景类型**: [A/B/C/D/E/F/G]
- **PID**: [具体PID]
- **API路径**: [具体路径]
- **实验平台**: [ACM/AB/无实验]
- **数据解析**: [pv_info+jmespath / resourceobj]
- **参考用例**: [test_cases/目录名]
- **参考文档**: doc/测试场景分类与参数配置指南.md 第[X]节
```

---

### Phase 1: Understand Requirements

Extract from requirements document:
1. **Test purpose**: What feature/functionality to test?
2. **Test scope**: Which branch, environment, experiments?
3. **Key points**: What to verify?
4. **Experimental configuration**: Bucket names, limits, logic
5. **Request parameters**: operation, filter conditions

### Phase 2: Create exp_info.py

Template:

```python
# -*- coding: utf-8 -*-
"""
@author: lujia
@time: YYYY/M/D
@Desc: 测试用例 - 实验名称
"""

class Exp:
    """
    实验配置类
    """
    # 实验列表：key为实验名称，value为配置值（权重、限制数量等）
    exps_list = {
        "experiment_a": value_a,
        "experiment_b": value_b,
        "experiment_c": value_c,
        "": default_value  # 空实验（未命中）
    }

    # 测试需要用到的实验
    testNeedExps = ["experiment_a", "experiment_b", ""]

    # 实验描述
    exp_descriptions = {
        "experiment_a": "实验A说明",
        "experiment_b": "实验B说明",
        "": "空实验（默认值）"
    }

    # 其他配置
    # operation映射、过滤条件等
```

**Key fields:**
- `exps_list`: Experiment name → value mapping
- `testNeedExps`: List of experiments to test
- `exp_descriptions`: Human-readable descriptions
- Custom fields: operation maps, filter conditions, etc.

### Phase 3: Create test_api.py

Template structure:

```python
# -*- coding: utf-8 -*-
"""
@author: lujia
@time: YYYY/M/D
@Desc: 接口测试 - 实验说明
"""
import json
import os
import sys
import random
import threading

# 获取项目根目录并添加到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from configs.config import HomePage, HomeShell
from exp_info import Exp
from test_utils.file_util import write_res, write_error_log
from test_utils.rcm_utils.api_utils.get_item_key import _parse_item_info
from test_utils.request_util import req
from test_utils.threads_util import TheadRun

# 获取当前目录
cur_path = os.path.abspath(os.path.dirname(__file__))

# 线程锁
results_lock = threading.Lock()

class Check:
    @staticmethod
    def check_thread_line(line, **kwargs):
        """
        处理每个device_id的请求
        """
        # 1. 获取device_id
        # 2. 随机选择实验
        # 3. 构造请求URL（可添加operation等参数）
        # 4. 发送请求
        # 5. 收集结果
        # 6. 返回结果

def test_pro():
    """
    主测试函数
    """
    # 1. 创建输出文件
    # 2. 创建多线程运行器
    # 3. 运行多线程
    # 4. 保存结果
    # 5. 生成日志查询脚本
    # 6. 输出统计信息

if __name__ == "__main__":
    test_pro()
```

**⚠️ 重要：数据保存模式（必读）**

**错误模式（会导致数据丢失）：**
```python
# ❌ 错误：从文件读取数据
thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

if os.path.exists(api_response_file):
    with open(api_response_file, "r") as f:
        all_results = json.load(f)  # ❌ 文件不存在或为空
else:
    all_results = {}

with open(api_response_file, "w") as f:
    json.dump(all_results, f)  # ❌ 写入空数据
```

**正确模式：**
```python
# ✅ 正确：直接使用内存中已收集的数据
full_response_collection = {}
kwargs = {
    "f_err": f_err,
    "results_collection": results_collection,
    "full_response_collection": full_response_collection  # 传递空字典
}

thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

print(f"✅ 收集到 {len(full_response_collection)} 个API响应")

# 直接保存内存数据
with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(full_response_collection, f, ensure_ascii=False, indent=2)

all_results = full_response_collection  # 使用内存数据
```

**URL构造最佳实践:**
- 始终参考`configs/config_url.py`中的`HomePage.common_url`定义
- 包含所有必需参数（bsdata、outmedia、gps、netstate、version、devicetype、uid等）
- 使用`HomePage.test_domain + HomePage.common_url`作为基础URL

**频道页 test_api.py 注意事项:**

```python
from configs.config_url import PinDaoYeUrl

# 频道页场景选择
scenario_rand = random.random()
if scenario_rand < 0.5:
    scenario_key = "90100213"  # 车展专题页
else:
    scenario_key = "90100214"  # 车展沉浸流

# 获取配置
if scenario_key == "90100213":
    recall_name, base_url = PinDaoYeUrl.conf_90100213()
else:
    recall_name, base_url = PinDaoYeUrl.conf_90100214()

req_url = base_url % device_id

# 保存完整API返回时，包含 scenario 和 recall_name
full_response_collection[log_uuid] = {
    "device_id": device_id,
    "scenario": scenario_key,
    "recall_name": recall_name,
    "response": result,
}
```

**Key components:**
- `Check.check_thread_line()`: Process each request
- Random experiment selection with distribution
- Custom request parameters (operation, filters, etc.)
- Thread-safe result collection
- Statistics output

### Phase 4: Create test_log.py

Template structure:

```python
# -*- coding: utf-8 -*-
"""
@author: lujia
@time: YYYY/M/D
@Desc: 日志验证 - 实验说明
功能：
1. 验证实验是否正确命中
2. 验证其他业务逻辑
3. 输出统计信息
"""
import os
import sys
import json
from collections import defaultdict
from typing import Dict

# 获取项目根目录并添加到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from exp_info import Exp
from test_utils import file_util
from test_utils.rcm_utils.parse_utils.parse_engine_util import (
    collection_debug,
    collection_monitor,
)

# 获取当前目录
CUR_PATH = os.path.abspath(os.path.dirname(__file__))

# 创建错误日志文件
f_err = file_util.write_res(CUR_PATH, "err_log_info.txt")

class CustomTester:
    """
    自定义测试类
    """

    def __init__(self):
        self.test_dir = CUR_PATH
        self.api_data = {}
        self.debug_data = {}
        self.monitor_data = {}
        self.stats = defaultdict(int)

    def load_api_data(self):
        """
        加载接口返回数据
        """

    def parse_monitor_data(self):
        """
        解析monitor日志
        """
        monitor_file = os.path.join(self.test_dir, "engine_monitor.txt")
        if not os.path.exists(monitor_file):
            print(f"⚠️  monitor日志文件不存在: {monitor_file}")
            print(f"   请先将日志文件下载到: {self.test_dir}")
            return

        print("正在解析monitor日志...")
        self.monitor_data = collection_monitor(
            self.test_dir,  # 重要：传入目录路径，不是文件路径
            node_path="hit_study1_name_map"
        )

    def parse_debug_data(self):
        """
        解析debug日志
        """
        debug_file = os.path.join(self.test_dir, "engine_debug.txt")
        if not os.path.exists(debug_file):
            print(f"⚠️  debug日志文件不存在: {debug_file}")
            print(f"   请先将日志文件下载到: {self.test_dir}")
            return

        print("正在解析debug日志...")
        self.debug_data = collection_debug(self.test_dir)  # 重要：传入目录路径

    def check_custom_logic(self, log_uuid: str, req_info: Dict) -> bool:
        """
        自定义验证逻辑
        """

    def run_test(self):
        """
        运行完整测试
        """
        # 1. 加载数据
        # 2. 遍历每个请求进行验证
        # 3. 输出统计信息

def test_check():
    """
    主测试函数
    """
    try:
        tester = CustomTester()
        tester.run_test()
    except Exception as e:
        print(f"❌ 测试异常: {e}")
    finally:
        f_err.close()

if __name__ == "__main__":
    test_check()
```

**重要提示：日志解析**
- `collection_monitor()`和`collection_debug()`期望传入**目录路径**，函数会在目录下查找`engine_monitor.txt`和`engine_debug.txt`
- 不要传入完整文件路径（如`"../engine_monitor.txt"`）
- 正确方式：`collection_monitor(self.test_dir, node_path="hit_study1_name_map")`

**Key components:**
- Load and parse log files
- Custom validation logic based on requirements
- Statistics collection
- Error logging
- Summary output

### Phase 4.5: Create test_api_response.py (Optional but Recommended)

Template structure:

```python
# -*- coding: utf-8 -*-
"""
@author: lujia
@time: YYYY/M/D
@Desc: API返回验证 - 实验说明
功能：
1. 直接从API返回中验证字段（不依赖日志文件）
2. 根据实验桶验证字段是否符合预期
3. 统计各实验桶的数据分布
"""
import os
import sys
import json
from collections import defaultdict
from typing import Dict

# 获取项目根目录并添加到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from configs.config import HomePage
from exp_info import Exp
from test_utils import file_util
import jmespath

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
f_err = file_util.write_res(CUR_PATH, "err_api_response.txt")

class ApiResponseValidator:
    """
    API返回验证类
    """

    def __init__(self):
        self.test_dir = CUR_PATH
        self.full_response_data = {}
        self.stats = {
            "total_requests": 0,
            "success_checks": 0,
            "failed_checks": 0,
            "exp_stats": defaultdict(int),
            "exp_errors": defaultdict(int),
            "total_items": defaultdict(int),
            # 添加更多统计字段...
        }

    def load_full_response(self):
        """
        加载完整API返回数据（test_api.py生成的api_response_full.json）
        """
        api_file = os.path.join(self.test_dir, "api_response_full.json")
        if not os.path.exists(api_file):
            print(f"❌ 完整API返回文件不存在: {api_file}")
            print(f"   请先运行 test_api.py 生成该文件")
            return False

        print("正在加载完整API返回数据...")
        try:
            with open(api_file, "r", encoding="utf-8") as f:
                self.full_response_data = json.load(f)
            print(f"✅ 成功加载 {len(self.full_response_data)} 条API数据")
            return True
        except Exception as e:
            print(f"❌ 加载API数据失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def validate_item_field(self, log_uuid: str, device_id: str, hit_exp: str,
                           item: Dict, index: int, request_url: str = "") -> bool:
        """
        验证单个物料的字段
        """
        # 获取pv_info
        pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
        try:
            pv_info = json.loads(pv_info_str)
        except:
            pv_info = {}

        # 提取字段
        biz_type = jmespath.search(HomePage.pvinfo_biz_type_path, pv_info)
        biz_id = jmespath.search(HomePage.pvinfo_biz_id_path, pv_info)
        rway = jmespath.search(HomePage.pvinfo_rway_path, pv_info) or ""

        # 验证字段（根据实验桶要求）
        # ...

        return True

    def validate_request(self, log_uuid: str, req_data: Dict) -> bool:
        """
        验证单个请求
        """
        device_id = req_data.get("device_id", "")
        hit_exp = req_data.get("hit_exp", "")
        response = req_data.get("response", {})
        request_url = req_data.get("request_url", "")

        if not response:
            err_msg = {
                "error": "API返回数据为空",
                "log_uuid": log_uuid,
                "device_id": device_id,
                "exp": hit_exp
            }
            file_util.write_error_log(f_err, err_msg)
            self.stats["exp_errors"][hit_exp] += 1
            return False

        item_list = response.get("itemlist", [])
        if not item_list:
            err_msg = {
                "error": "API返回物料列表为空",
                "log_uuid": log_uuid,
                "device_id": device_id,
                "exp": hit_exp
            }
            file_util.write_error_log(f_err, err_msg)
            self.stats["exp_errors"][hit_exp] += 1
            return False

        self.stats["exp_stats"][hit_exp] += 1

        all_items_valid = True
        for index, item in enumerate(item_list):
            is_valid = self.validate_item_field(
                log_uuid, device_id, hit_exp, item, index, request_url
            )
            if not is_valid:
                all_items_valid = False

        return all_items_valid

    def run_validation(self):
        """
        运行完整验证
        """
        print("\n" + "=" * 60)
        print("开始API返回验证")
        print("=" * 60 + "\n")

        if not self.load_full_response():
            return

        self.stats["total_requests"] = len(self.full_response_data)
        print(f"开始验证 {self.stats['total_requests']} 个请求...\n")

        for log_uuid, req_data in self.full_response_data.items():
            is_valid = self.validate_request(log_uuid, req_data)
            if is_valid:
                self.stats["success_checks"] += 1
            else:
                self.stats["failed_checks"] += 1

        self.print_summary()

    def print_summary(self):
        """
        打印统计摘要
        """
        print("\n" + "=" * 60)
        print("API返回验证统计摘要")
        print("=" * 60 + "\n")

        print(f"总请求数: {self.stats['total_requests']}")
        print(f"成功检查: {self.stats['success_checks']}")
        print(f"失败检查: {self.stats['failed_checks']}")

        # 打印各实验桶的统计信息
        # ...

def test_api_response():
    """
    主测试函数
    """
    try:
        validator = ApiResponseValidator()
        validator.run_validation()
    except Exception as e:
        print(f"❌ 验证异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        f_err.close()

if __name__ == "__main__":
    test_api_response()
```

**重要提示：test_api.py 需要保存完整API返回**
- `test_api.py` 必须生成 `api_response_full.json` 文件
- 该文件包含所有请求的完整API返回数据
- 格式：`{log_uuid: {device_id, hit_exp, response, request_url}}`
- 示例：
  ```python
  # 在 test_api.py 中保存完整返回
  results_collection[log_uuid] = {
      "device_id": device_id,
      "hit_exp": exp_choice,
      "response": result,  # 完整的API返回字典
      "request_url": test_url
  }

  # 保存到文件
  with open(api_response_file, "w", encoding="utf-8") as f:
      json.dump(results_collection, f, ensure_ascii=False, indent=2)
  ```

**Key components:**
- Load complete API response from `api_response_full.json`
- Validate fields directly from response (no log parsing needed)
- Use jmespath to extract item information
- Statistics collection
- Error logging to `err_api_response.txt`
- Summary output

**When to use test_api_response.py:**
- **Quick validation**: Validate response fields immediately after `test_api.py`
- **No log files**: When log files are not available or not needed
- **Direct verification**: When you need to verify specific fields (uniq_series_id, biz_type, biz_id, etc.)
- **Complement to test_log.py**: Use both for comprehensive validation

**Difference from test_log.py:**
| Feature | test_api_response.py | test_log.py |
|---------|---------------------|-------------|
| Requires log files | No | Yes |
| Validation source | API response directly | Log files (debug/monitor) |
| Speed | Fast (no log download) | Slower (needs logs) |
| Validation scope | Response fields | Full engine behavior |
| Dependencies | test_api.py output | log files |

### Phase 5: Create README.md

Template sections:

```markdown
# YYYYMMDD测试用例说明文档 - 测试名称

## 📋 测试概述

### 测试目的
列出要验证的功能点

### 测试范围
- 引擎分支：xxx
- Apollo配置：uat
- 测试环境：UAT

## 🎯 需求背景
详细描述需求背景和问题

## 📊 实验配置

### Operation参数说明
表格形式说明各个operation的含义

### 实验桶配置
表格形式说明各个实验桶的配置

## 🚀 使用步骤
1. 修改配置
2. 运行接口测试
3. 下载日志
4. 运行日志验证

## 📁 目录结构
文件列表和说明

## 🔍 检查点说明
详细的验证点说明

## ⚠️ 注意事项
重要的注意事项

## 🔍 错误排查
常见错误和解决方法
```

### Phase 6: Create INSTALL.md

Include:
- Environment requirements
- Installation steps
- Configuration instructions
- Common issues

### Phase 7: Create QUICKSTART.md

Include:
- Quick configuration steps
- Example command (e.g., 10 requests)
- Expected output
- Common errors

### Phase 8: Create SUMMARY.md

Include:
- File list and sizes
- Feature overview
- Usage flow
- Key validation points

## Common Patterns

### Experiment Configuration

**Simple experiment with weight:**
```python
exps_list = {
    "test_exp": 0.7,
    "": 1.0
}
```

**Experiment with limit value:**
```python
exps_list = {
    "isFilter60": 60,
    "isFilter150": 150,
    "isFilter500": 500
}
```

**Multiple experiment groups:**
```python
exps_list = {
    "group_a_exp1": 0.5,
    "group_a_exp2": 0.7,
    "group_b_exp1": 0.5,
    "group_b_exp2": 0.7,
    "": 1.0
}
```

### Request Parameter Simulation

**req()函数调用（重要）:**
```python
# req()函数需要2个参数，返回5个值
req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))

# 必须检查log_uuid和result是否为空
if not log_uuid or not result:
    write_error_log_file(
        kwargs.get("f_inter_err"),
        {
            "err": "返回数据为空",
            "device_id": device_id,
            "log_uuid": log_uuid,
            "has_result": result is not None,
            "req_url": test_url,
        },
    )
    return results_collection

# 获取itemlist（result是字典，直接使用.get()）
item_list = result.get("itemlist", [])
if not item_list:
    # 处理空物料列表
    return results_collection
```

**物料信息解析（避免使用_parse_item_info）:**
```python
import jmespath

# 直接使用jmespath解析物料信息（避免_parse_item_info的bug）
for index, item in enumerate(item_list):
    # 获取pv_info
    pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
    pv_info = json.loads(pv_info_str)
    
    # 提取字段（使用or提供默认值）
    biz_type = str(jmespath.search(HomePage.pvinfo_biz_type_path, pv_info) or "")
    biz_id = str(jmespath.search(HomePage.pvinfo_biz_id_path, pv_info) or "")
    rway = jmespath.search(HomePage.pvinfo_rway_path, pv_info) or ""
    
    # 存储物料信息
    log_data["itemlist"][index] = [biz_type, biz_id, rway]
```

**Random operation parameter:**
```python
op_rand = random.random()
if op_rand < 0.2:
    operation = 0  # 首页打开
elif op_rand < 0.5:
    operation = 2  # 上拉加载
else:
    operation = 4  # 手动下拉刷新

# 添加到URL
operation_param = f"&operation={operation}"
```

**Custom filter parameters:**
```python
filter_param = f"&filter_type={filter_type}&limit={limit}"
```

**Complete URL construction (重要):**
```python
# 使用HomePage.common_url作为基础，添加所有必需参数
test_url = (
    HomePage.test_domain +
    f"/rcm/autohmpg2/v3.0/lands?" +
    f"autorefresh={autorefresh}&" +
    f"appexp={exp_choice}&" +
    f"deviceid={device_id}&" +
    f"number={num_choice}&" +
    f"operation={operation}&" +
    f"bsdata=eyJSZW1haW5EcUxlbiI6MCwicHZvcmRpbmEiOjEsInB2VGltZSI6MTYxODQ2MDY0Mn0%3D&" +
    f"blackarticlelist=&" +
    f"source=app&" +
    f"netstate=3&" +
    f"gps=121.49469393166493,39.798810978403125&" +
    f"version=3&" +
    f"outmedia=7883524092098756216&" +
    f"outmedia1=4086764837169416160&" +
    f"outmedia2=3626190930523365&" +
    f"appversion=14.18.5&" +
    f"restart=0&" +
    f"userip=&" +
    f"pm=2&" +
    f"cityid=210200&" +
    f"devicetype=android&" +
    f"uid=174085853"
)
```

**注意事项：**
- 不要手动构造完整URL，应该使用`HomePage.test_domain`和参考`common_url`
- 参考`configs/config_url.py`第412-414行的完整参数列表
- 确保所有参数都用`&`连接

**频道页(Channel Page) URL construction:**
```python
from configs.config_url import PinDaoYeUrl

# 频道页使用 /oneapi/v2 端点（不是首页的 /rcm/autohmpg2/v3.0/lands）
# 配置在 configs/config_url.py 的 PinDaoYeUrl 类中
# 每个方法返回 (recall_name, base_url) 或 (biz_type_list, base_url)
# URL 中使用 %s 或 %{} 作为 device_id/uuid 的占位符

recall_name, base_url = PinDaoYeUrl.conf_90100213()  # 车展专题页
req_url = base_url % device_id  # 替换占位符

recall_name, base_url = PinDaoYeUrl.conf_90100214()  # 车展沉浸流
req_url = base_url % device_id
```

**频道页物料解析（关键差异）:**

⚠️ 频道页 `/oneapi/v2` 的响应结构与首页 `/rcm/autohmpg2/v3.0/lands` **完全不同**：

```python
# 首页响应结构 - 数据在 pv_info 中（JSON字符串）
# item -> pv_info (JSON string) -> biz_id, biz_type, rway

# 频道页响应结构 - 数据在 resourceobj 中（直接字段）
# item -> resourceobj -> biz_id, biz_type, rtype
# item -> resourceobj -> show -> title, author, cms_tags 等

def extract_item_info(item):
    resourceobj = item.get("resourceobj", {})
    biz_id = str(resourceobj.get("biz_id", ""))
    biz_type = str(resourceobj.get("biz_type", ""))
    rtype = resourceobj.get("rtype", "")

    # 顶层字段作为备用
    if not biz_id:
        biz_id = str(item.get("bizid", ""))
    if not biz_type:
        biz_type = str(item.get("biztype", ""))
    if not rtype:
        rtype = item.get("rtype", "")

    return biz_id, biz_type, rtype
```

**注意**: 频道页**不能使用** `jmespath` + `HomePage.pvinfo_path`，因为数据不在 pv_info 中。

**测试数据召回验证（Excel数据 → API返回验证）:**

当用户提供 Excel 测试数据文件时，需要创建 `test_data_config.py` 并在 `test_api_response.py` 中验证：

```python
# test_data_config.py - 从Excel提取的测试数据
TEST_DATA = {
    "原创图文": {
        "biztype": 1,
        "opu": "O",
        "ids": [1313417, 1313416, 1313371],
        "scene": "90100213",
    },
    # ... 更多类型
}

# test_api_response.py - 验证逻辑
def compute_per_content_stats(self):
    for content_type, data in all_test_configs.items():
        scene = data["scene"]
        expected_ids = set(str(id) for id in data["ids"])
        scene_ids = self.scenario_recalled_ids.get(scene, set())
        hit = expected_ids & scene_ids
        miss = expected_ids - scene_ids
        # 记录命中/未命中
```

### Validation Logic

**Check experiment hit:**
```python
def check_exp_hit(self, log_uuid: str, req_info: Dict) -> bool:
    hit_exp = req_info.get("hit_exp", "")
    monitor_exp = self.monitor_data.get(log_uuid, {})

    # Build dicts
    hit_exp_dict = {exp: True for exp in hit_exp.split(",") if exp}
    monitor_hit_exp = {exp: True for exp in monitor_exp.keys() if exp}

    return hit_exp_dict == monitor_hit_exp
```

**Check custom field:**
```python
def check_custom_field(self, log_uuid: str, req_info: Dict) -> bool:
    expected_value = req_info.get("expected_value")
    actual_value = self.debug_data.get(log_uuid, {}).get("field_name")

    if expected_value != actual_value:
        err_msg = {
            "err": "字段值不匹配",
            "log_uuid": log_uuid,
            "expected": expected_value,
            "actual": actual_value
        }
        file_util.write_error_log(f_err, err_msg)
        return False

    return True
```

**Statistics collection:**
```python
self.stats["total_requests"] = len(self.api_data)
self.stats["exp_stats"][exp_name] = self.stats["exp_stats"].get(exp_name, 0) + 1
```

### API Response Validation (test_api_response.py)

**Load and validate API responses:**
```python
def load_full_response(self):
    api_file = os.path.join(self.test_dir, "api_response_full.json")
    if not os.path.exists(api_file):
        print(f"❌ 完整API返回文件不存在: {api_file}")
        return False

    with open(api_file, "r", encoding="utf-8") as f:
        self.full_response_data = json.load(f)
    return True
```

**Extract item information:**
```python
import jmespath

def validate_item_field(self, log_uuid: str, device_id: str, hit_exp: str,
                       item: Dict, index: int, request_url: str = ""):
    # 获取pv_info
    pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
    try:
        pv_info = json.loads(pv_info_str)
    except:
        pv_info = {}

    # 提取字段
    biz_type = jmespath.search(HomePage.pvinfo_biz_type_path, pv_info)
    biz_id = jmespath.search(HomePage.pvinfo_biz_id_path, pv_info)
    rway = jmespath.search(HomePage.pvinfo_rway_path, pv_info) or ""

    # 验证逻辑
    # ...
```

**Save complete API response in test_api.py:**
```python
# 在 test_api.py 中，保存完整API返回
results_collection = {}

# 处理每个请求后
req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))

if log_uuid and result:
    results_collection[log_uuid] = {
        "device_id": device_id,
        "hit_exp": exp_choice,
        "response": result,  # 完整的API返回字典
        "request_url": test_url
    }

# 保存到文件
api_response_file = os.path.join(cur_path, "api_response_full.json")
with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(results_collection, f, ensure_ascii=False, indent=2)
```

## Project Context

**环境要求:**
- **Python版本**: Python 3.6+ (必须使用`python3`命令，不要使用`python`)
- **必需依赖**: 
  ```
  pip3 install pandas requests tqdm loguru jmespath
  ```

**Key paths:**
- Test cases: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/`
- Configs: `configs/config.py`, `configs/config_url.py`
- Utils: `test_utils/` directory
  - `request_util.py`: HTTP requests
  - `threads_util.py`: Multi-threading
  - `file_util.py`: File operations
  - `rcm_utils/parse_utils/parse_engine_util.py`: Log parsing

**Common imports:**
```python
import json
import jmespath  # 用于解析物料信息

from configs.config import HomePage, HomeShell
from test_utils.file_util import write_res, write_error_log
# 注意：避免导入 _parse_item_info，该函数有bug
from test_utils.request_util import req
from test_utils.threads_util import TheadRun
from test_utils.rcm_utils.parse_utils.parse_engine_util import (
    collection_debug,
    collection_monitor,
)
```

**File naming convention:**
- Directory: `YYYYMMDD-test-name/`
- Files: `exp_info.py`, `test_api.py`, `test_log.py`, `README.md`

## Example Test Case

See: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/20260204/`

This test case demonstrates:
- Multiple experiment buckets with different limits
- Operation parameter simulation
- Filter logic validation
- Complete documentation set

**Example with test_api_response.py:**

See: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/20260304-noseries-demotion/`

This test case demonstrates:
- API response validation without log files
- Field validation (uniq_series_id, biz_type, biz_id)
- Detailed error reporting with device_id, log_uuid, request_url
- Integration with test_api.py (saves complete responses)
- Recommended validation workflow

**频道页测试用例参考:** `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/20260424-beijing-auto-show/`

This test case demonstrates:
- 频道页 API endpoint `/oneapi/v2` usage (NOT `/rcm/autohmpg2/v3.0/lands`)
- `PinDaoYeUrl` config class usage
- Multi-scenario testing (90100213 专题页 + 90100214 沉浸流)
- `resourceobj` based data extraction (NOT pv_info/jmespath)
- Test data validation from Excel (`test_data_config.py`)
- Per-content-type hit/miss statistics

## Best Practices

1. **Follow existing patterns**: Reference similar test cases in `test_cases/`
2. **Use consistent structure**: Maintain the standard file structure
3. **Write clear comments**: Explain what each section does
4. **Include statistics**: Always output test statistics
5. **Document thoroughly**: README should cover all use cases
6. **Handle errors gracefully**: Use try-catch and log errors
7. **Make it configurable**: Allow easy parameter adjustments
8. **Thread-safe**: Use locks when accessing shared data

**验证流程最佳实践:**
9. **推荐流程**：先运行 `test_api.py` → 立即运行 `test_api_response.py` 快速验证 → 根据需要运行 `test_log.py` 深度验证
10. **test_api_response.py 优势**：快速验证、无需下载日志、独立验证、完整数据保存
11. **test_log.py 适用场景**：需要验证实验命中、召回详情、引擎内部行为
12. **两者结合**：`test_api_response.py` 用于快速发现问题，`test_log.py` 用于深度调试

**test_api.py 保存完整API返回:**
13. **必需保存**：生成 `api_response_full.json` 供 `test_api_response.py` 使用
14. **完整返回**：保存完整的API返回字典，包括所有字段
15. **日志关联**：包含 log_uuid 以便关联后续日志验证
16. **格式统一**：使用标准JSON格式，确保可读性
17. **⚠️ 关键**：**直接使用内存数据，不要从文件读取**（见下方警告）

**test_api.py 数据保存警告（⚠️ 必读）:**
```
❌ 错误模式：从文件读取数据
===========================================
thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

if os.path.exists(api_response_file):
    with open(api_response_file, "r") as f:
        all_results = json.load(f)  # ❌ 文件不存在或为空！
else:
    all_results = {}

with open(api_response_file, "w") as f:
    json.dump(all_results, f)  # ❌ 写入空数据！

问题：线程运行后，数据已在 full_response_collection 中，
      但代码去读文件（空），然后写回空数据，导致数据丢失！

✅ 正确模式：直接使用内存数据
===========================================
thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

print(f"✅ 收集到 {len(full_response_collection)} 个API响应")

# 直接保存内存数据
with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(full_response_collection, f, ensure_ascii=False, indent=2)

all_results = full_response_collection  # ✅ 使用内存数据

原理：
1. kwargs 传递 full_response_collection 字典给线程
2. 线程在 check_thread_line 中填充数据到该字典
3. 运行完成后，数据已在内存中
4. 直接从内存保存到文件，不要读取文件
```

**URL构造最佳实践:**
17. **Reference HomePage.common_url**: 始终参考`configs/config_url.py`中的URL定义，不要手动构造
18. **Include all required parameters**: 确保包含bsdata、outmedia、gps、netstate等所有必需参数
19. **Use f-strings for URLs**: 使用f-string清晰格式化URL，避免字符串拼接错误

**日志解析最佳实践:**
20. **Pass directory paths**: `collection_monitor`和`collection_debug`期望目录路径，不是文件路径
21. **Check file existence**: 在解析前检查日志文件是否存在，给出友好的错误提示
22. **Separate parsing methods**: monitor和debug日志解析分开，便于调试

**req()函数使用最佳实践:**
23. **必需参数**: `req()`函数需要2个参数：`req(req_url, f_err)`
24. **返回值处理**: 返回5个值 `req_url, req_json, result, log_uuid, requestid`
25. **空值检查**: 检查`log_uuid`和`result`是否为空，避免NoneType错误
26. **错误日志**: 使用`kwargs.get("f_inter_err")`传递错误日志文件句柄

**物料解析最佳实践:**
27. **避免_parse_item_info**: 该函数有bug（BIZ_TYPE_TO_CONTENT_NAME未定义），建议直接使用jmespath解析
28. **直接解析**: 使用`jmespath.search(HomePage.pvinfo_path, item)`获取pv_info
29. **安全访问**: 使用`or ""`或`or "{}"`提供默认值，避免NoneType错误

**Python版本要求:**
30. **Python 3.6+**: 必须使用Python 3.6或更高版本
31. **使用python3命令**: 系统默认`python`可能是Python 2.7，使用`python3`运行脚本

## Checklist

Before completing test case:
- [ ] exp_info.py has correct experiment configuration
- [ ] test_api.py can send requests successfully
- [ ] test_api.py generates correct output files
- [ ] test_api.py saves api_response_full.json (if using test_api_response.py)
- [ ] test_log.py can parse log files
- [ ] test_log.py validates correctly
- [ ] test_api_response.py validates correctly (if generated)
- [ ] README.md has all necessary sections
- [ ] INSTALL.md provides clear setup instructions
- [ ] QUICKSTART.md has working examples
- [ ] All imports resolve correctly
- [ ] File paths are correct
- [ ] Error handling is in place
- [ ] Statistics are collected and displayed

**额外检查项（基于常见问题）:**
- [ ] **test_api.py**: URL构造包含所有必需参数（参考HomePage.common_url）
  - 检查是否包含bsdata、outmedia、gps、netstate、version、devicetype、uid等
- [ ] **test_api.py**: ⚠️ **数据保存逻辑正确（关键！）**
  - 创建 `full_response_collection = {}` 并通过 kwargs 传递
  - 在 `check_thread_line()` 中填充数据到 `full_response_collection`
  - 在 `run_threads()` 后**直接使用** `full_response_collection`（不要读文件）
  - 保存时使用 `json.dump(full_response_collection, f, ...)`
  - **不要**在保存前去读取文件（文件还不存在或为空）
- [ ] **test_api.py**: 保存完整API返回（如果使用test_api_response.py）
  - 生成 `api_response_full.json` 文件
  - 包含完整的 response 字典
  - 包含 log_uuid, device_id, hit_exp, request_url
- [ ] **test_log.py**: 日志解析传入目录路径
  - `collection_monitor(self.test_dir, ...)` 而不是 `collection_monitor(monitor_file)`
  - `collection_debug(self.test_dir)` 而不是 `collection_debug(debug_file)`
- [ ] **test_api_response.py**: 正确加载和解析api_response_full.json
  - 检查文件是否存在，不存在时给出友好提示
  - 使用jmespath解析物料信息
  - 统计信息完整
- [ ] **req()函数调用**: 正确传递参数和处理返回值
  - `req(test_url, kwargs.get("f_inter_err"))` - 2个参数
  - `req_url, req_json, result, log_uuid, requestid = req(...)` - 5个返回值
  - 检查`if not log_uuid or not result:`避免NoneType错误
- [ ] **物料解析**: 避免使用_parse_item_info，直接使用jmespath
  - 导入jmespath：`import jmespath`
  - 安全访问：`jmespath.search(...) or ""` 提供默认值
- [ ] **Python版本**: 使用python3运行，不要使用python
  - 运行命令：`python3 test_api.py`
  - 检查版本：`python3 --version` 应该是3.6+
- [ ] **依赖包**: 安装所有必需的包
  - `pip3 install pandas requests tqdm loguru jmespath`
- [ ] **⚠️ 防卡死 - HTTP连接**: test_api.py 中不得使用裸 `requests.get()`，必须通过 `req()` 函数（已使用 Session）
- [ ] **⚠️ 防卡死 - 线程join**: 不得添加 `while alive_threads: t.join()` 循环，`threads_util.py` 已内置 `join(timeout=30)`
- [ ] **⚠️ 防卡死 - 文件关闭**: `test_pro()` 中所有 `write_res()` 打开的文件句柄必须放在 `try/finally` 的 `finally` 块中关闭
- [ ] **⚠️ 防卡死 - stdout刷新**: `test_pro()` 的 `finally` 块和 `if __name__` 块末尾必须调用 `sys.stdout.flush()` 和 `sys.stderr.flush()`
- [ ] **⚠️ 防卡死 - 禁止os._exit**: 代码中不得出现 `os._exit()`，只能用 `sys.exit()` 或 `return`
- [ ] **⚠️ 防卡死 - 执行加超时**: 执行 test_api.py 必须用 `timeout 300 python3 test_api.py 2>/dev/null`
- [ ] **⚠️ 防卡死 - 禁止读大文件**: 绝对不能直接读取 `api_response_full.json`（50-150MB），通过 test_api_response.py 间接分析
- [ ] **⚠️ 防卡死 - 大文件路径警告输出** (v2.2): 最终统计打印 >1MB 文件路径时，必须附带文件大小(MB) + "禁止直接读取"警告 + `python3 test_api_response.py` 替代提示（规则6，防 2026-09-18 类 TUI 假死事故）
- [ ] **⚠️ 防卡死 - 分步执行**: 不要链式执行多个脚本（`a && b && c`），每个脚本单独执行、单独检查结果

**条件逻辑测试检查项（基于实际教训）:**
- [ ] **⚠️ 反向用例**: 每个正向用例（X→Y）是否有对应的反向用例（非X→非Y）
- [ ] **⚠️ 条件分区表**: 对所有 `>=`/`<=`/`&&`/`||` 条件判断，是否生成了输入分区表
- [ ] **⚠️ 分区覆盖**: 分区表中每个分区是否都有用例覆盖（或有明确的盲区标注）
- [ ] **⚠️ 事件序列**: 对时序逻辑（如退场机制），是否测试了多种事件排列（不只是单一类型）
- [ ] **⚠️ 混合造数**: 测试脚本是否支持注入混合事件类型（如曝光+点击），而非只注入单一类型
- [ ] **⚠️ 代码变更回归**: 开发改条件后，是否重新审查了新条件的所有分支
- [ ] **⚠️ 写读一致性**: 数据生产者（写入端）和数据消费者（读取端）的数据格式是否验证一致

**操作生效性验证检查项（v2.1 NEW）:**
- [ ] **⚠️ 直接标记断言**: 对过滤/排序/干预操作，是否使用标记字段（reduce_type/disabled/rway）断言，而非仅用间接数据推断
- [ ] **⚠️ 负向存在性**: 对每个"过滤/排除/屏蔽"操作，是否有对应的"被过滤元素不出现在返回中"的断言
- [ ] **⚠️ 数据流传播**: 是否交叉验证了 debug 日志中的中间结果与 API 返回的最终结果（中间过滤了N个，API返回是否少了N个）
- [ ] **⚠️ 样本量充足**: 对过滤/屏蔽类操作，样本量是否≥50（30条样本在2%缺陷率下有45%漏检概率）
- [ ] **⚠️ 标记字段清单**: 是否已识别 API 返回中的所有操作标记字段，并在验证逻辑中使用

## Troubleshooting

**Python版本错误 - SyntaxError:**
- **原因**：系统默认`python`命令指向Python 2.7，不支持f-strings等Python 3语法
- **解决方案**：使用`python3`命令运行脚本
  ```bash
  python3 test_api.py
  python3 test_log.py
  ```

**依赖包缺失 - ModuleNotFoundError:**
- **原因**：缺少必需的Python包（loguru、jmespath等）
- **解决方案**：安装所有依赖包
  ```bash
  pip3 install pandas requests tqdm loguru jmespath
  ```

**req()函数错误 - missing required positional argument:**
- **原因**：`req()`函数需要2个参数，但只传了1个
- **解决方案**：添加`f_err`参数
  ```python
  # 错误
  res = req(test_url)
  
  # 正确
  req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))
  ```

**NoneType错误 - 'NoneType' object has no attribute 'get':**
- **原因**：`result`为None时调用`.get()`方法
- **解决方案**：添加空值检查
  ```python
  # 错误
  item_list = result.get("itemlist", [])
  
  # 正确
  if not log_uuid or not result:
      # 记录错误并返回
      return results_collection
  item_list = result.get("itemlist", [])
  ```

**_parse_item_info错误 - name 'BIZ_TYPE_TO_CONTENT_NAME' is not defined:**
- **原因**：`_parse_item_info`函数内部使用了未定义的变量
- **解决方案**：不使用该函数，直接用jmespath解析
  ```python
  # 错误
  from test_utils.rcm_utils.api_utils.get_item_key import _parse_item_info
  item_info = _parse_item_info(item, index, rways)
  
  # 正确
  import jmespath
  pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
  pv_info = json.loads(pv_info_str)
  biz_type = str(jmespath.search(HomePage.pvinfo_biz_type_path, pv_info) or "")
  ```

**Import errors:**
- Ensure project_root path is correct
- Check that sys.path.insert(0, project_root) is included
- Verify file structure matches expected layout

**API returns null / empty results:**
- **原因**：URL构造缺少必需参数（bsdata、outmedia、gps等）
- **解决方案**：使用HomePage.common_url作为基础，添加完整参数：
  ```python
  test_url = (
      HomePage.test_domain +
      f"/rcm/autohmpg2/v3.0/lands?" +
      f"autorefresh={autorefresh}&" +
      f"appexp={exp_choice}&" +
      f"deviceid={device_id}&" +
      f"number={num_choice}&" +
      f"operation={operation}&" +
      f"bsdata=eyJSZW1haW5EcUxlbiI6MCwicHZvcmRpbmEiOjEsInB2VGltZSI6MTYxODQ2MDY0Mn0%3D&" +
      # ... 其他必需参数
  )
  ```
- **参考**：检查`configs/config_url.py`中的`common_url`定义，确保包含所有参数

**Thread safety issues:**
- Always use `with results_lock:` when modifying shared data
- Return modified collection, not separate variable

**Log parsing errors - NotADirectoryError:**
- **原因**：`collection_monitor`和`collection_debug`函数期望传入**目录路径**，然后在目录下查找`engine_monitor.txt`等文件
- **解决方案**：传入目录路径而不是完整文件路径：
  ```python
  # 错误（传入文件路径）
  self.monitor_data = collection_monitor(monitor_file)  # monitor_file = ".../engine_monitor.txt"

  # 正确（传入目录路径）
  self.monitor_data = collection_monitor(
      self.test_dir,  # 传入目录路径
      node_path="hit_study1_name_map"
  )
  ```
- **参考**：查看`test_utils/rcm_utils/parse_utils/parse_engine_util.py`第119-121行的实现

**Log parsing errors - AttributeError: 'int' object has no attribute 'get'**
- **原因**：`self.stats`初始化为`defaultdict(int)`时，访问不存在的键会返回默认值`int`而不是`defaultdict`
- **错误示例**：
  ```python
  # 错误的初始化
  self.stats = defaultdict(int)
  
  # 当访问 self.stats["exp_stats"] 时
  # 由于 "exp_stats" 键不存在，返回默认值 int(0)
  result = self.stats["exp_stats"]  # 结果是 int(0)，不是字典
  
  # 后续调用时出错
  result[hit_exp]  # int[hit_exp] - AttributeError!
  ```
- **解决方案**：使用嵌套的字典结构，确保嵌套字段是`defaultdict`：
  ```python
  # 正确的初始化
  self.stats = {
      "total_requests": 0,
      "success_checks": 0,
      "failed_checks": 0,
      "exp_stats": defaultdict(int),  # 嵌套defaultdict
      "num_stats": defaultdict(int)
  }
  
  # 这样 self.stats["exp_stats"] 就是 defaultdict(int)，可以正确使用 .get() 方法
  self.stats["exp_stats"][hit_exp] = self.stats["exp_stats"].get(hit_exp, 0) + 1
  ```

**Log parsing errors:**
- Check that log files exist before parsing
- Handle empty log files gracefully
- Use try-catch for JSON parsing

**Configuration errors:**
- Verify device_id_path points to valid file
- Check that test_domain is correct for environment
- Ensure experiment names match Apollo configuration

**test_api_response.py errors:**

**⚠️ 关键错误：api_response_full.json 为空或数据丢失**

**症状：**
- `test_api.py` 运行后显示 "✅ 收集到 398 个API响应"
- 但 `api_response_full.json` 文件只有 2 bytes（空字典 `{}`）
- `test_api_response.py` 报告 "成功加载 0 条API数据"

**根本原因：**
代码在 `run_threads()` 后，错误地从文件读取数据而不是使用内存中已收集的数据。

**错误代码示例：**
```python
# ❌ 错误：从文件读取（文件还不存在或为空）
thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

if os.path.exists(api_response_file):
    with open(api_response_file, "r", encoding="utf-8") as f:
        all_results = json.load(f)  # ❌ 读到空数据
else:
    all_results = {}

with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)  # ❌ 写入空数据
```

**正确代码示例：**
```python
# ✅ 正确：直接使用内存中已收集的数据
thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

print(f"\n✅ 收集到 {len(full_response_collection)} 个API响应")

# 直接保存内存数据
with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(full_response_collection, f, ensure_ascii=False, indent=2)

all_results = full_response_collection  # ✅ 使用内存数据
```

**原理解释：**
1. `kwargs` 传递 `full_response_collection` 字典给线程函数
2. 线程在 `check_thread_line()` 中向该字典填充数据
3. `run_threads()` 完成后，数据已在内存的 `full_response_collection` 中
4. **直接从内存保存到文件**，不要去读取文件（文件还不存在或为旧数据）

**检查清单：**
- [ ] 确认 `test_api.py` 中创建了 `full_response_collection = {}`
- [ ] 确认通过 `kwargs` 传递了 `full_response_collection`
- [ ] 确认在 `check_thread_line()` 中使用 `full_response_collection[log_uuid] = {...}`
- [ ] 确认在 `run_threads()` 后直接使用 `full_response_collection`，不要读文件
- [ ] 确认保存时使用 `json.dump(full_response_collection, f, ...)`

**api_response_full.json 文件不存在:**
- **原因**：`test_api.py` 没有生成完整的API返回文件
- **解决方案**：
  1. 检查 `test_api.py` 是否有保存完整返回的代码
  2. 确保在请求成功后保存数据：
     ```python
     if log_uuid and result:
         results_collection[log_uuid] = {
             "device_id": device_id,
             "hit_exp": exp_choice,
             "response": result,  # 完整的API返回
             "request_url": test_url
         }
     ```
  3. 检查是否在最后保存到文件：
     ```python
     api_response_file = os.path.join(cur_path, "api_response_full.json")
     with open(api_response_file, "w", encoding="utf-8") as f:
         json.dump(results_collection, f, ensure_ascii=False, indent=2)
     ```

**api_response_full.json 格式错误:**
- **原因**：保存的数据结构不正确
- **解决方案**：
  - 确保每个记录包含所有必需字段：
    ```python
    {
        "device_id": "...",
        "hit_exp": "...",
        "response": {...},  # 完整的API返回字典
        "request_url": "..."
    }
    ```
  - 使用 `ensure_ascii=False, indent=2` 保持可读性

**jmespath 解析错误:**
- **原因**：物料结构变化或路径不正确
- **解决方案**：
  - 检查 `HomePage.pvinfo_path` 等路径是否正确
  - 添加调试信息查看原始数据：
    ```python
    print(f"Debug item: {item}")  # 查看原始物料结构
    pv_info_str = jmespath.search(HomePage.pvinfo_path, item)
    print(f"Debug pv_info_str: {pv_info_str}")
    ```
  - 使用 `or "{}"` 提供默认值避免解析失败

**验证逻辑不生效:**
- **原因**：条件判断或字段提取错误
- **解决方案**：
  - 添加调试输出：
    ```python
    print(f"hit_exp: {hit_exp}")
    print(f"biz_type: {biz_type}")
    print(f"uniq_series_id: {uniq_series_id}")
    ```
  - 确保字段类型转换正确（如 `int(biz_type)`）
  - 检查实验桶名称是否匹配

---

## 人群包定向召回场景 (Crowd Recall Pattern)

### 适用场景
当需求涉及"人群包定向召回"（如 RecallFollowByCrowd）时，需要特殊的测试数据准备流程。

### 数据流
```
Redis(device_id → crowdId) → getCrowdAndArticleRelation(crowdId → itemId列表) → 引擎RecallFollowByCrowd召回 → API返回(pvinfo.crowd_id埋点)
```

### redistest 工具链
用于办公网无法直接操作Redis时，通过HTTP接口中转操作Redis测试数据。

**服务地址**: `http://mock-redis-api.example.com`

**常用接口**:
- `GET /vr-online/get?key=<ZNGZ_device_id>` — 查询Redis值
- `POST /vr-online/batch-set` — 批量写入（JSON数组 `[{"key":"...", "value":"..."}]`）
- `GET /check_redis_data?key=<device_id>` — 自动补ZNGZ_前缀查询

**注意**: Redis key 格式为 `ZNGZ_` + device_id，引擎API接收裸 device_id。

### exp_info.py 人群包配置

```python
class Exp:
    # redistest服务地址
    redistest_api = "http://mock-redis-api.example.com"

    # 人群包测试数据：Redis key(ZNGZ_+device_id) → crowdId
    known_crowd_data = {
        "ZNGZ_DEVICE_ID_1": "1000001",
        "ZNGZ_DEVICE_ID_2": "1000002",
        "ZNGZ_DEVICE_ID_3": "1000001,1000002",  # 多人群包（逗号分隔）
    }

    # 物料接口
    material_api = "http://material-api.example.com/smartmarket-bg/api/task/getCrowdAndArticleRelation"

    # 人群包ID映射（含样本物料）
    crowd_info = {
        1000001: {
            "name": "人群包1",
            "sample_items": ["010250020020004-25379102", "010180020010092-2257977"],
        },
        1000002: {
            "name": "人群包2",
            "sample_items": ["010040130880046-90010870"],
        },
    }

    expected_recall_name = "RecallFollowByCrowd"
```

### test_api.py 人群包模式

**关键区别**：人群包场景需要"已知设备 + 随机对照"双轨测试。

```python
CONTROL_RANDOM_COUNT = 50  # 随机对照组数量

def test_pro():
    # 1. 准备Redis数据（通过redistest）
    prepare_redis_data()

    # 2. 随机对照组（验证未命中设备不触发召回）
    thread_runner = TheadRun(device_id_path, CONTROL_RANDOM_COUNT)
    thread_runner.run_threads(Check(), "check_thread_line", **kwargs)

    # 3. 已知设备全参数覆盖（每个op × 每个number）
    for did in Exp.known_crowd_data.keys():
        for op in Exp.test_params["operations"]:
            for num in Exp.test_params["numbers"]:
                Check.check_thread_line(did, **{**kwargs, "force_op": op, "force_num": num})
```

**check_thread_line 支持 force_op/force_num**：
```python
operation = kwargs.get("force_op")
if operation is None:
    # 随机选择
    op_rand = random.random()
    operation = 0 if op_rand < 0.2 else (2 if op_rand < 0.5 else 4)

num_choice = kwargs.get("force_num") or random.choice([10, 20, 30])
```

**Redis数据准备函数**：
```python
def prepare_redis_data():
    batch_data = [{"key": did, "value": crowd_id}
                  for did, crowd_id in Exp.known_crowd_data.items()]
    resp = requests.post(f"{Exp.redistest_api}/vr-online/batch-set",
                         json=batch_data, timeout=10)
```

### test_api_response.py 人群包验证项

```python
# 必须验证的5个验证点：
# 1. RecallFollowByCrowd 的 trace_crowd_id 非空
# 2. trace_crowd_id 与 crowd_id 一致
# 3. 召回物料在物料接口返回列表中
# 4. 未命中人群包的设备不出现 RecallFollowByCrowd
# 5. 多人群包设备 trace_crowd_id 正确
```

### 参考用例
- 人群包召回: `test_cases/20260518-smart-follow-crowd/`

---

## threads_util.py 注意事项

### tqdm 刷屏问题
`threads_util.py` L67 的 `tqdm.write(f"Progress: {pbar.format_dict}")` 会每4个请求打印一次完整字典，**导致输出看起来像卡住**。这是正常行为，脚本实际在正常运行。

### 并发控制
- `ACTIVRCOUNT = 20` 控制最大并发线程数（定义在 `configs/config.py`）
- 线程设置为 daemon=True，主线程退出时子线程会被终止
- 如果总请求数大于 20，线程会分批执行

### 进度条
- 进度条会输出大量 format_dict 信息，不影响功能
- 如果需要干净输出，可重定向 stderr：`python3 test_api.py 2>/dev/null`

---

### Phase 0.7: 操作生效性验证 (Action Effectiveness Verification) (MANDATORY)

**重要**: 此阶段确保"过滤/排序/干预/降级"等操作不仅在引擎内部执行了，而且结果真正传播到 API 返回。源自实际教训：分层治理 filter 词泄露——Go void 函数中 `ret = filterLowCtr(ret)` 只改局部变量，标记了 `Disabled=true` + `reduce_type=filter_T4` 的词仍出现在 API 返回中。测试脚本用间接数据（s28d/c 值）推断过滤是否生效，而非直接检查标记字段，导致 1.9% 泄露率未被 30 条样本检测到。

#### 0.7.1 直接标记字段断言规则（CRITICAL）

**规则**: 当 API 返回或引擎 debug 日志中存在**操作标记字段**时，测试脚本**必须**使用标记字段进行断言，**不可**仅用间接数据推断。

**常见标记字段对照表**:

| 系统 | 标记字段 | 间接推断（❌ 不可靠） | 直接断言（✅ 推荐） |
|------|---------|---------------------|-------------------|
| 分层治理 | `reduce_type` | `s28d >= 900 AND c == 0` | `"filter_" not in reduce_type` |
| 推荐引擎 | `pvinfo.rway` | 通过 biz_type 推断召回路 | 直接匹配 rway 值 |
| 推荐引擎 | `pvinfo.is_explore` | 通过 rtype 推测是否探索物料 | 直接检查 `is_explore == 1` |
| 通用 | `disabled` / `status` | 通过 score 推断是否被处理 | 直接检查 `disabled == false` |

**判断方法**:
1. 读取 API 返回中每个 item 的所有字段（含 debug 字段）
2. 识别哪些字段是**操作结果标记**（reduce_type, rway, is_explore, disabled, flag...）
3. 对每个操作验证点，优先使用标记字段断言
4. 如果没有标记字段 → 退而求其次用间接推断，但需在 README 中标注"间接验证，可能有盲区"

#### 0.7.2 负向存在性断言模式

**何时必须生成**:

| 触发条件 | 示例 | test_api_response.py 中的断言 |
|----------|------|------------------------------|
| 需求含"过滤/屏蔽/移除" | "T4以下词应被过滤" | `assert not any("filter_" in w.get("reduce_type","") for w in keywords)` |
| 需求含"排除/排除项" | "排除已下架内容" | `assert not any(w.get("biz_type") == DOWNCAST for w in items)` |
| 需求含"降级/不可见" | "退场用户不可见" | `assert not any(w.get("is_explore") == 1 for w in items)` |
| 需求含"禁止/不允许" | "黑名单内容不出现" | `assert not any(w.get("biz_id") in BLACKLIST for w in items)` |
| 代码中有 filter/remove | `filterLowCtr(ret)` | 在 API 返回中断言 `Disabled=true` 的元素不存在 |

**test_api_response.py 负向断言模板**:

```python
def validate_negative_existence(self, log_uuid: str, items: list) -> bool:
    """
    负向存在性验证：断言被过滤/排除的元素不出现在返回中
    """
    # 1. 收集所有返回元素的标记字段
    leaked_items = []
    for idx, item in enumerate(items):
        reduce_type = item.get("reduce_type", "")  # 或从 pvinfo/debug 字段获取
        disabled = item.get("disabled", False)
        
        # 2. 断言：不应出现 filter 标记的元素
        if "filter_" in str(reduce_type):
            leaked_items.append({
                "index": idx,
                "reduce_type": reduce_type,
                "keyword": item.get("keyword", ""),
            })
        if disabled:
            leaked_items.append({
                "index": idx,
                "disabled": disabled,
                "keyword": item.get("keyword", ""),
            })
    
    # 3. 如果有泄露，记录错误
    if leaked_items:
        file_util.write_error_log(f_err, {
            "error": "负向存在性验证失败：被过滤的元素出现在返回中",
            "log_uuid": log_uuid,
            "leaked_count": len(leaked_items),
            "leaked_items": leaked_items[:5],  # 只记录前5个
        })
        return False
    
    return True
```

#### 0.7.3 数据流传播验证

**目标**: 验证引擎内部多步骤流水线（过滤→排序→截断→返回）的每一步结果都正确传播到下一步。

**验证方法**:

```
1. 从 debug 日志获取中间结果（如有）
   - 过滤前的物料数 vs 过滤后的物料数
   - 排序前的分数列表 vs 排序后的顺序
   
2. 从 API 返回验证最终结果
   - 返回物料数是否等于预期（过滤后数量）
   - 返回中是否有应被过滤的物料（负向断言）
   - 返回中物料的排序是否与预期一致

3. 交叉验证
   - debug 日志中的过滤结果 vs API 返回的实际内容
   - 如果 debug 说"过滤了 6 个"但 API 返回数量没有减少 → 🔴 数据流断裂
```

**test_log.py 中的数据流验证模板**:

```python
def validate_data_flow(self, log_uuid: str, api_items: list) -> bool:
    """
    验证引擎内部操作结果是否传播到 API 返回
    """
    debug_data = self.debug_data.get(log_uuid, {})
    
    # 从 debug 日志获取过滤前后的数量
    before_filter = debug_data.get("before_filter_count", 0)
    after_filter = debug_data.get("after_filter_count", 0)
    filtered_count = before_filter - after_filter
    
    # 从 API 返回获取实际数量
    api_count = len(api_items)
    
    # 交叉验证
    if filtered_count > 0 and api_count >= before_filter:
        # API 返回数量 >= 过滤前数量 → 过滤结果未传播
        file_util.write_error_log(f_err, {
            "error": "数据流传播验证失败",
            "log_uuid": log_uuid,
            "before_filter": before_filter,
            "after_filter": after_filter,
            "api_return_count": api_count,
            "expected": after_filter,
            "actual": api_count,
            "diagnosis": "过滤操作可能未传播到 API 返回（数据流断裂）",
        })
        return False
    
    return True
```

#### 0.7.4 样本量充足性指导

**问题**: 当缺陷率较低时（如 filter 泄露率 1.9%），常规 30 条样本可能检测不到。

| 预期缺陷率 | 最少样本量 | 30条样本检出概率 | 说明 |
|-----------|-----------|----------------|------|
| >10% | 10 | ~96% | 高频问题，常规样本足够 |
| 5% | 30 | ~79% | 中频问题，常规样本基本够 |
| 2% | 50 | ~55% ⚠️ | 低频问题，30条样本有45%漏检 |
| 1% | 100 | ~26% ❌ | 极低频，需扩大样本或白盒测试 |
| <1% | 200+ | ❌ | 建议代码级白盒测试 |

**建议**:
- 对过滤/屏蔽类操作（缺陷率未知时），建议至少 **50 个请求**
- 如果无法扩大样本量，建议在 README 中标注"样本量限制：低频泄露（<5%）可能未被检测"
- 对于关键路径，建议配合 Go/Java 单元测试（直接调用函数验证返回值）

#### 0.7.5 输出格式

```markdown
### 操作生效性验证分析

#### 操作1: [操作名称，如"T4低CTR词过滤"]
- **代码位置**: [文件:行号]
- **标记字段**: reduce_type (filter_T4)
- **正向断言**: ✅ 已有（检查过滤后的词在返回中）
- **负向断言**: [✅ 已有 / ❌ 缺失 → 需补充]
- **直接标记检查**: [✅ 使用 reduce_type / ⚠️ 使用 s28d 间接推断]
- **数据流验证**: [✅ debug vs API 交叉验证 / ❌ 仅检查 API]
- **样本量**: [当前N条，建议N条]
- **风险等级**: [🟢 低 / 🟡 中 / 🔴 高]
```

---

**判断标准**：如果验证点全部在 API 返回的 pvinfo/物料数据中可以获取，则不需要 test_log.py。

| 需要验证的内容 | test_api_response.py | test_log.py |
|---|---|---|
| 召回类型 (rway) | ✅ pvinfo.rway | ✅ |
| 埋点字段 (如 crowd_id) | ✅ pvinfo.crowd_id | ✅ |
| 物料 biz_type/biz_id | ✅ pvinfo | ✅ |
| 实验命中详情 | ❌ | ✅ monitor日志 |
| 引擎内部排序分数 | ❌ | ✅ debug日志 |
| 召回耗时/超时 | ❌ | ✅ monitor日志 |

**结论**：如果只需验证"召回类型+埋点+物料正确性"，test_api_response.py 足够，不需要 test_log.py。

---

## test_api.py 职责分离原则

**推荐模式**：
- `test_api.py` — 纯数据收集（发送请求、保存原始响应），不做任何验证判断
- `test_api_response.py` — 纯验证（读取 api_response_full.json，做 PASS/FAIL 判定）

**好处**：
1. 职责清晰，一个脚本只做一件事
2. 可以反复运行验证脚本而不重新发请求
3. 验证逻辑独立修改，不影响请求逻辑

---

## 防卡死规范 (Anti-Hang Rules) ⚠️ MANDATORY

**背景**: test_api.py 在多线程 + 高并发请求场景下反复出现进程挂起（hang）问题，根因是：HTTP连接未关闭、线程join无限等待、文件句柄泄漏、stdout缓冲未刷新。以下规范是**强制性的**，生成的每个 test_api.py 都必须遵守。

### 规则 1: HTTP 请求必须使用 Session（自动关闭连接）

```python
# ✅ 正确：使用 with requests.Session() 自动关闭连接
def req(url, f_err=None):
    with requests.Session() as session:
        response = session.get(url, timeout=10)
        # ...
    # Session 自动关闭，连接池释放

# ❌ 错误：裸 requests.get() 不关闭连接，高并发下连接池耗尽导致挂起
def req(url, f_err=None):
    response = requests.get(url, timeout=10)  # 连接不会被显式关闭
```

**说明**: `request_util.py` 已修复为使用 `with requests.Session()`。生成的 test_api.py 通过 `from test_utils.request_util import req` 引用，无需自行处理。但如果你在 test_api.py 中直接使用 `requests.get()`，必须包裹在 `with requests.Session()` 中。

### 规则 2: 线程 join 必须有 timeout（禁止无限等待）

```python
# ✅ 正确：join(timeout=30)，最多等 30 秒
for t in threads:
    t.join(timeout=30)

# ❌ 错误：无限 join，如果子线程卡住则主线程永远阻塞
for t in threads:
    t.join()  # 没有 timeout！
```

**说明**: `threads_util.py` 已修复，`run_threads()` 内部对每个线程调用 `t.join(timeout=30)`。**禁止在 test_api.py 或任何地方添加额外的 `while alive_threads: join()` 循环**——这会导致无限等待。

### 规则 3: 文件句柄必须用 try/finally 关闭

```python
# ✅ 正确：try/finally 保证异常时也能关闭
def test_pro():
    f_info = write_res(cur_path, "api_return.txt")
    f_err = write_res(cur_path, "err_api_info.txt")
    try:
        # ... 所有业务逻辑 ...
        f_info.write(json.dumps(results))
    finally:
        f_info.close()
        f_err.close()
        sys.stdout.flush()
        sys.stderr.flush()

# ❌ 错误：文件句柄在函数末尾才关闭，中间出异常则永不关闭
def test_pro():
    f_info = write_res(cur_path, "api_return.txt")
    # ... 业务逻辑（如果这里抛异常，f_info 永远不会 close）...
    f_info.close()  # 只有正常执行才会到达这里
```

### 规则 4: 主函数末尾和 if __name__ 块必须 flush stdout

```python
# ✅ 正确：确保所有输出被刷新到终端/日志
if __name__ == "__main__":
    test_pro()
    sys.stdout.flush()
    sys.stderr.flush()

# ❌ 错误：依赖 Python 默认退出时 flush，多线程下可能丢失输出
if __name__ == "__main__":
    test_pro()  # 没有 flush，如果进程被 kill 则输出丢失
```

### 规则 5: 禁止使用 os._exit()

```python
# ❌ 绝对禁止：os._exit() 会跳过 finally 块、不关闭文件、不 flush 缓冲
import os
os._exit(0)  # 这会导致文件损坏和输出丢失

# ✅ 正确：使用 sys.exit() 或 return，让 Python 正常清理
import sys
sys.exit(0)  # 触发 finally 块和 atexit handlers
```

### 规则 6: 大文件路径输出必须带大小与禁读警告（脚本自防护）⚠️ v2.2

**背景**: 2026-09-18 TUI 假死事故——test_api.py 跑完后最后一行打印 `完整返回: ...api_response_full.json`（裸路径），执行 agent 顺手读取该 98MB 文件，巨型内容堵死 TUI 事件循环，**ESC 无响应，只能 kill -9 恢复**。此前的"禁止读大文件"规则无法防止此类事故，因为诱惑点在脚本自身输出里。**防线必须设在诱惑点：让脚本自己警告。**

生成的每个测试脚本，凡最终输出中包含 >1MB 文件的路径，**必须**按以下模式打印：

```python
# ✅ 正确：路径 + 文件大小(MB) + 禁读警告 + 替代方案
resp_size_mb = os.path.getsize(api_response_file) / 1024 / 1024
print(f"完整返回: {api_response_file} ({resp_size_mb:.1f}MB)")
print("⚠️ 禁止直接读取该文件(会卡死TUI)! 分析请运行: python3 test_api_response.py")

# ❌ 错误：裸路径输出，等于邀请 agent 去读它
print(f"完整返回: {api_response_file}")
```

**适用文件**: `api_response_full.json`（50-150MB）、`api_info.txt`/`api_return.txt`（数百KB，同样不建议直接读）、任何生成的超过 1MB 的输出文件路径。

### test_api.py 模板（防卡死版）

生成 test_api.py 时，`test_pro()` 函数必须遵循以下结构：

```python
def test_pro():
    # 1. 打开所有文件句柄
    f_inter_info = write_res(cur_path, "api_return.txt")
    f_inter_err = write_res(cur_path, "err_api_info.txt")
    
    try:
        # 2. 所有业务逻辑（请求、线程、写入等）
        # ...
        pass

        # 3. 统计摘要 + 大文件路径安全输出（规则6：路径必须带大小与禁读警告）
        resp_size_mb = os.path.getsize(api_response_file) / 1024 / 1024
        print(f"完整返回: {api_response_file} ({resp_size_mb:.1f}MB)")
        print("⚠️ 禁止直接读取该文件(会卡死TUI)! 分析请运行: python3 test_api_response.py")
    finally:
        # 4. 关闭所有文件句柄
        f_inter_info.close()
        f_inter_err.close()
        # 5. 刷新输出缓冲
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    test_pro()
    sys.stdout.flush()
    sys.stderr.flush()
```

---

## 脚本执行规范 (Agent Anti-Stuck Rules) ⚠️ MANDATORY

**背景**: Agent 执行 test_api.py 后反复出现"Thinking"无限转圈问题。根因是：tqdm 刷屏 stderr 被 bash 工具全量捕获（数百行）+ api_response_full.json 可达 100MB+ → agent context 爆炸 → LLM 卡死。以下规范是**强制性的**，执行测试脚本时必须遵守。

### 执行规则 1: 必须抑制 stderr + 设置超时

```bash
# ✅ 正确：stderr 丢弃 + 5 分钟超时
timeout 300 python3 test_api.py 2>/dev/null

# ❌ 错误：裸跑，tqdm 刷屏 stderr 全量捕获导致 agent 卡死
python3 test_api.py
```

**说明**: `threads_util.py` 已修改为非 TTY 环境自动禁用 tqdm 动态刷新。但作为双重保险，执行时仍必须加 `2>/dev/null`。

### 执行规则 2: 禁止直接读取大文件

```python
# ❌ 绝对禁止：api_response_full.json 可达 100MB+，直接读取会撑爆 context
read("api_response_full.json")

# ✅ 正确：通过 test_api_response.py 间接分析
# 运行验证脚本来读取和分析，不要在 agent context 中加载原始 JSON
```

**文件大小参考**:
| 文件 | 典型大小 | 可直接读取? |
|------|---------|------------|
| `api_response_full.json` | 50-150 MB | ❌ 绝对不行 |
| `api_return.txt` | 1-5 MB | ❌ 不建议 |
| `err_api_info.txt` | 10-500 KB | ⚠️ 仅查看前 50 行 |
| `log_shell.sh` | < 1 KB | ✅ 可以 |
| `exp_info.py` | < 5 KB | ✅ 可以 |

### 执行规则 3: 分步执行，不要一次全跑

```
# ✅ 正确：每步只做一件事，检查结果后再继续

Step 1: python3 test_api.py 2>/dev/null
        → 检查退出码和 stdout 最后几行（实验分布统计）
        → 确认 "All tasks completed!" 出现

Step 2: python3 test_api_response.py 2>/dev/null  
        → 检查验证结果（PASS/FAIL）

Step 3: python3 test_log.py 2>/dev/null（如果需要）
        → 检查日志验证结果

# ❌ 错误：一条命令链式执行所有脚本
python3 test_api.py && python3 test_api_response.py && python3 test_log.py
```

### 执行规则 4: 检查输出只看尾部摘要

```bash
# ✅ 正确：只看最后 20 行（包含统计摘要）
python3 test_api.py 2>/dev/null
# 然后检查 stdout 的最后部分（实验分布、Operation分布、探索物料数）

# ❌ 错误：尝试解析全部 stdout 输出
# tqdm 进度条 + 每个请求的调试信息 = 大量噪音
```

### 执行规则 5: 如果脚本卡住超过 2 分钟，立即中断

- test_api.py 正常执行 500 请求约需 1-3 分钟
- 如果超过 5 分钟无输出，说明引擎无响应或网络问题
- **立即 ESC 中断**，检查引擎服务状态，不要傻等

---

## Phase 9: 三剑客Review (MANDATORY - 最后一步)

**重要**: 在所有测试文件生成完成后，必须使用三剑客方法对生成的测试脚本进行Review，找出潜在问题并调优。

### 9.1 Review角色定义

**🗡️ 产品经理Review**:
- 测试用例是否覆盖了需求中的所有功能点？
- 实验桶配置是否正确？是否遗漏了关键实验？
- 验证点是否与需求文档一致？
- 是否有需求的细节被遗漏？

**🗡️ 架构师Review**:
- API请求URL构造是否正确？参数是否完整？
- 数据流向是否正确：请求 → 响应 → 解析 → 验证？
- 是否存在性能问题（如并发数过高/过低）？
- 代码是否有潜在bug（空值处理/类型转换/异常捕获）？
- 是否与项目现有代码风格一致？
- 是否存在导入错误或依赖问题？

**🗡️ QA Review**:
- 正向/反向测试用例是否均衡？
- 边界条件是否覆盖（空返回/异常返回/无数据）？
- 错误处理是否完善（error_log记录/统计信息）？
- 统计逻辑是否正确（总数/成功数/失败数/各实验桶分布）？
- 脚本是否可以直接运行？（路径/依赖/配置）
- 是否需要额外的测试数据准备？

### 9.2 执行方式

1. **完整阅读** 所有生成的文件（exp_info.py, test_api.py, test_api_response.py, test_log.py）
2. **逐一角色Review** — 按上述三个视角审查
3. **输出Review报告**:
   ```markdown
   ## 三剑客Review报告

   ### 🗡️ 产品经理Review
   - ✅ 覆盖良好的点: ...
   - ❌ 遗漏的点: ...
   - ⚠️ 需要确认的点: ...

   ### 🗡️ 架构师Review
   - ✅ 代码质量: ...
   - 🐛 发现的Bug: ...
   - ⚠️ 潜在风险: ...

   ### 🗡️ QA Review
   - ✅ 测试覆盖: ...
   - ❌ 缺失场景: ...
   - ⚠️ 建议补充: ...

   ### 🔧 需要修复的问题
   1. [问题描述] → [修复方案]
   2. ...
   ```

4. **自动修复** — 对发现的问题直接修改代码
5. **确认修复** — 修复后再次确认问题已解决

### 9.3 常见Review发现

**高频问题清单**（检查时重点关注）:

| # | 问题类型 | 检查方式 | 修复方案 |
|---|---------|---------|---------|
| 1 | exp_info.py实验配置与需求不匹配 | 对比需求文档和exps_list | 修正实验名/值 |
| 2 | test_api.py URL缺少必要参数 | 对比config_url.py | 补充缺失参数 |
| 3 | 空值处理缺失 | 检查所有.get()调用 | 添加默认值或检查 |
| 4 | 统计逻辑错误 | 检查计数逻辑 | 修正统计字段 |
| 5 | 导入路径错误 | 检查所有import语句 | 修正模块路径 |
| 6 | jmespath路径错误 | 对比HomePage常量 | 修正解析路径 |
| 7 | 文件保存路径问题 | 检查所有open()调用 | 使用os.path.join |
| 8 | 线程安全问题 | 检查共享变量访问 | 添加锁或使用线程安全结构 |
| 9 | 频道页用了首页的解析方式 | 检查API endpoint | 使用resourceobj而非pvinfo |
| 10 | validation_points与实际验证不一致 | 对比exp_info.py和test_api_response.py | 统一验证点 |
| 11 | **PID与场景不匹配** | 需求说首页但PID写成901xxxx | 对照场景分类指南修正PID |
| 12 | **ACM/AB实验参数混用** | 首页静默刷新用testNeedExp(应appexp) | 按实验名格式判断平台 |
| 13 | **进程退出用了os._exit()** | 检查`__main__`块 | 删除os._exit，改为正常退出+flush |
| 14 | **defaultdict嵌套访问** | `defaultdict(int)`下访问嵌套key | 用`defaultdict(lambda: defaultdict(int))` |
| 15 | **collection_monitor传文件路径** | 检查参数是目录还是文件 | 传`cur_path`不是文件路径 |
| 16 | **间接推断替代直接标记** (v2.1) | 验证逻辑用s28d/c推断而非reduce_type | 改用标记字段直接断言 |
| 17 | **缺少负向存在性断言** (v2.1) | 只验证"该出现的出现"，无"不该出现的不出现" | 补充 `assert not any(...)` 断言 |
| 18 | **未交叉验证数据流** (v2.1) | 仅检查API返回，未对比debug中间结果 | 添加 test_log.py 数据流验证 |

### 9.4 Review流程图

```
所有文件生成完毕
    ↓
Phase 9: 三剑客Review
    ├── 产品经理Review → 功能覆盖检查
    ├── 架构师Review → 代码质量检查
    └── QA Review → 测试完整性检查
    ↓
输出Review报告
    ↓
自动修复发现的问题
    ↓
确认修复完成
    ↓
✅ 测试用例交付
```

### 9.5 注意事项

- **不要跳过Review**: 即使之前流程已经很仔细，Review仍然可能发现问题
- **修复后需验证**: 修改代码后运行lsp_diagnostics确认无语法错误
- **记录Review结果**: 在README.md中记录Review发现和修复情况
- **如果发现需求问题**: 回到Phase -1，更新三剑客分析报告

---

## 技能版本

- 版本: 2.2.0
- 创建时间: 2026-02-04
- 作者: OpenCode

## 更新日志

### v2.2.0 (2026-09-18)
- **重要新增**：防卡死规范 规则6 — 大文件路径输出必须带大小与禁读警告（脚本自防护）
  - 生成的脚本凡最终输出 >1MB 文件路径（api_response_full.json 等），必须附带文件大小(MB) + "⚠️ 禁止直接读取"警告 + `python3 test_api_response.py` 替代提示
  - 防卡死模板（test_pro 结构）同步加入安全输出块
  - Checklist 新增"大文件路径警告输出"检查项
- **教训来源**：2026-09-18 TUI 假死事故——test_api.py 完成后打印 98MB `api_response_full.json` 裸路径，执行 agent 读取后 TUI 事件循环堵塞，ESC 无响应，只能 kill -9 恢复。此前的"禁止读大文件"规则（v2.0 执行规则2）无法防止此类事故，因为诱惑点在脚本自身输出里——防线必须设在诱惑点。事故完整记录与恢复手册见项目 AGENTS.md 红线#4 踩坑记录

### v2.1.0 (2026-08-13)
- **重大新增**：Phase 0.7 操作生效性验证 (Action Effectiveness Verification) — MANDATORY
  - 新增「直接标记字段断言规则」— 测试脚本必须使用标记字段（reduce_type/disabled/rway）断言操作结果，不可仅用间接数据推断
  - 新增「负向存在性断言模式」— 对每个过滤/排除/屏蔽操作，必须断言被过滤元素不出现在返回中
  - 新增「数据流传播验证」— 交叉验证 debug 日志中间结果与 API 最终返回（过滤了N个，API返回应少N个）
  - 新增「样本量充足性指导」— 缺陷率-样本量对照表（2%缺陷率需≥50样本，30条样本漏检概率45%）
  - 含 test_api_response.py 负向断言模板和 test_log.py 数据流验证模板
- **新增**：Checklist 增加5项操作生效性验证检查项
- **教训来源**：分层治理 filter 词泄露——Go void 函数 `ret = filterLowCtr(ret)` 只改局部变量，标记了 Disabled+filter_T4 的词仍出现在 API 返回。测试用间接数据（s28d/c 值）推断而非直接检查 reduce_type，30条样本未检出1.9%泄露率

### v2.0.0 (2026-08-13)
- **重大新增**：防卡死规范 (Anti-Hang Rules) — MANDATORY
  - 新增「防卡死规范」完整章节，包含5条代码规则 + test_api.py 防卡死模板
  - 规则1：HTTP 请求必须使用 `with requests.Session()`（禁止裸 `requests.get()`）
  - 规则2：线程 join 必须有 `timeout=30`（禁止 `while alive_threads: join()` 无限等待）
  - 规则3：文件句柄必须用 `try/finally` 关闭（异常时也能关闭）
  - 规则4：主函数末尾和 `if __name__` 块必须 `sys.stdout.flush()` + `sys.stderr.flush()`
  - 规则5：禁止 `os._exit()`，只能用 `sys.exit()` 或 `return`
- **重大新增**：脚本执行规范 (Agent Anti-Stuck Rules) — MANDATORY
  - 新增「脚本执行规范」完整章节，包含5条执行规则
  - 执行规则1：必须 `timeout 300 python3 test_api.py 2>/dev/null`（抑制 tqdm stderr + 超时保护）
  - 执行规则2：禁止直接读取 `api_response_full.json`（50-150MB），通过 test_api_response.py 间接分析
  - 执行规则3：分步执行，不要链式 `a && b && c`
  - 执行规则4：检查输出只看尾部摘要
  - 执行规则5：超过 2 分钟无输出立即中断
  - 含文件大小参考表（哪些文件可读/不可读）
- **修复**：request_util.py 改用 `with requests.Session()` 自动关闭连接池
- **修复**：threads_util.py 移除无限 `while alive_threads:` join 循环
- **修复**：threads_util.py 非 TTY 环境自动禁用 tqdm 动态刷新（防 stderr 刷屏导致 agent context 爆炸）
- **修复**：threads_util.py `tqdm.write()` 替换为 `sys.stderr.write()`（减少依赖和输出噪音）
- **Checklist 扩展**：新增 10 项防卡死检查项（⚠️ 标记，6 项代码级 + 4 项执行级）

### v2.0.0 (2026-08-13)
- **重大新增**：Phase 0.6 条件逻辑测试覆盖分析
  - 强制反向用例规则（每个正向用例必须配反向用例）
  - 条件分区表（对范围/边界判断强制生成输入分区覆盖表）
  - 事件序列测试（对时序逻辑强制覆盖多种事件排列）
  - 代码变更回归验证（开发改条件后重新审查所有分支）
  - 混合造数要求（测试脚本必须支持注入混合事件类型）
- **新增**：Checklist 增加7项条件逻辑测试检查项
- **教训来源**：兴趣探索2.0退场条件 `cIdx >= nearIdx && cIdx <= farIdx` 漏掉最近曝光后点击，正向用例全通过但反向用例缺失导致 bug 上线

### v1.9.0 (2026-08-07)
- **重大新增**：Phase 0.5 场景识别与PID/URL校验（MANDATORY）
  - 新增7大场景自动识别（首页/点后推/静默刷新/车展/车系页/频道页/新APP）
  - 新增PID-API路径-解析方式-实验参数 四维校验矩阵
  - 新增场景识别结果输出模板
- **重要新增**：踩坑防护清单
  - Phase 9高频问题表从10项扩展至15项
  - 新增PID场景不匹配、ACM/AB混用、os._exit泄漏、defaultdict嵌套、collection_monitor路径 等5项
- **新增文档关联**：`doc/测试场景分类与参数配置指南.md` 列为Phase 0最先必查文档
- **改进**：threads_util.py共享工具已修复join超时问题（防进程卡死）

### v1.8.0 (2026-05-25)
- **重大新增**：三剑客需求分析 + Review 双重保障机制
  - 新增 Phase -1: 三剑客需求分析（产品经理+架构师+QA三角色分析需求）
  - 新增 Phase 9: 三剑客Review（生成后用三角色Review测试脚本）
  - 两个新Phase为MANDATORY，不可跳过
- **重要新增**：知识库查询机制优化
  - 新增 `recall代码知识库.md` 和 `engine代码知识库.md` 到必查文档
  - 新增知识库查询流程（按领域优先级查询）
  - 新增"找不到信息时的处理"机制（明确输出需要人工确认的问题）
  - 新增查询策略（按需求类型选择重点文档）
- **改进**：Phase 0重编号
  - Phase 0.2 原"提取测试点"改为"知识库查询流程"
  - Phase 0.3 原"从文档中提取的关键信息"改为"提取测试点"

### v1.7.0 (2026-05-18)
- **重大新增**：人群包定向召回场景完整支持
  - 新增 redistest 工具链说明（Redis数据准备）
  - 新增 exp_info.py 人群包配置模板
  - 新增 test_api.py 双轨测试模式（已知设备 + 随机对照）
  - 新增 force_op/force_num 全参数覆盖模式
  - 新增 test_api_response.py 5项验证点
  - 新增参考用例 20260518-smart-follow-crowd/
- **新增**：threads_util.py 注意事项
  - tqdm 刷屏问题说明
  - 并发控制机制
  - 输出优化建议
- **新增**：何时不需要 test_log.py 的判断标准
  - 基于验证点内容选择验证方式
  - 对比 test_api_response.py 和 test_log.py 的能力边界
- **新增**：test_api.py 职责分离原则
  - 收集脚本 vs 验证脚本的分工
  - 好处说明

### v1.6.0 (2026-04-13)
- **重要新增**：频道页(Channel Page)测试支持
  - 新增频道页 API endpoint `/oneapi/v2` 的使用说明
  - 区分首页(`/rcm/autohmpg2/v3.0/lands`)和频道页(`/oneapi/v2`)的响应结构
  - 频道页数据在 `resourceobj` 中，不在 `pv_info` 中
  - 频道页不能使用 jmespath + HomePage.pvinfo_path 解析
  - 新增 `PinDaoYeUrl` 配置类使用说明
  - 新增频道页 `test_api.py` 模板（多场景选择）
- **重要新增**：测试数据召回验证模式
  - 新增 `test_data_config.py` 配置模式（从Excel提取测试ID）
  - 新增 test_api_response.py 中验证 Excel 测试ID是否被召回
  - 按 content_type 统计命中/未命中，输出详细报告
- **新增**：频道页测试参考用例 `20260424-beijing-auto-show/`

### v1.5.0 (2026-03-24)
- **重大更新**：新增 Phase 0 - 文档查询与测试点提取
  - 自动查询文档目录 `/Users/zhanghaishan/Documents/workspace/RcmTestProject/doc/`
  - 从测试点文档提取相关测试点
  - 从业务逻辑文档提取代码位置
  - 生成测试覆盖矩阵
  - 确保测试用例覆盖全面
- **新增**：测试覆盖矩阵生成
  - 自动生成测试覆盖矩阵表格
  - 标注 API 验证和日志验证支持
  - 标注优先级（P0/P1）
- **新增**：验证点列表
  - 在 exp_info.py 中添加 validation_points
  - 在 README.md 中说明验证逻辑
  - 在 test_api_response.py 中实现对应验证
- **改进**：文档结构优化
  - 更新 SKILL.md 添加 Phase 0 详细说明
  - 更新 README.md 添加文档查询说明
  - 更新模板文件

### v1.4.0 (2026-03-06)
- **新增**：test_api_response.py 完整支持
  - 添加 test_api_response.py 的完整模板和说明
  - 区分 test_api_response.py 和 test_log.py 的使用场景
  - 添加 test_api.py 保存完整API返回的最佳实践
  - 更新生成的文件列表结构，标记 test_api_response.py 为可选但推荐
- **新增**：验证流程最佳实践
  - 推荐流程：test_api.py → test_api_response.py → test_log.py
  - 说明 test_api_response.py 的优势（快速、无需日志、独立验证）
  - 说明 test_log.py 的适用场景（实验命中、召回详情）
- **改进**：Project Context 添加完整示例
  - 添加 20260304-noseries-demotion 示例
  - 展示 test_api_response.py 的完整使用方法
- **改进**：Checklist 添加新检查项
  - 检查 test_api.py 是否保存 api_response_full.json
  - 检查 test_api_response.py 的文件解析
  - 验证流程的完整性
- **改进**：Troubleshooting 添加新问题
  - api_response_full.json 不存在的解决方案
  - 文件格式错误的解决方案
  - jmespath 解析错误的解决方案
  - 验证逻辑不生效的解决方案
- **改进**：Common Patterns 添加新模式
  - 添加 API Response Validation 模式
  - 添加提取物料信息的模式
  - 添加保存完整API返回的模式

### v1.3.0 (2026-03-04)
- **重要修复**：req()函数使用说明
  - 添加req()函数的完整参数和返回值说明
  - 强调必须传递f_err参数
  - 强调返回5个值：req_url, req_json, result, log_uuid, requestid
- **重要修复**：NoneType错误处理
  - 添加`if not log_uuid or not result:`检查
  - 避免在None对象上调用.get()方法
- **重要修复**：物料解析问题
  - 明确指出_parse_item_info函数有bug（BIZ_TYPE_TO_CONTENT_NAME未定义）
  - 提供直接使用jmespath解析的正确方法
  - 移除Common imports中的_parse_item_info导入
- **新增**：Python版本要求
  - 明确要求Python 3.6+
  - 强调使用python3命令，不要使用python
- **新增**：依赖包列表
  - 添加loguru和jmespath到依赖列表
  - 提供完整的安装命令：`pip3 install pandas requests tqdm loguru jmespath`
- **改进**：Best Practices添加req()和物料解析最佳实践
- **改进**：Checklist添加新的检查项（req函数、物料解析、Python版本、依赖包）
- **改进**：Troubleshooting添加新的错误类型和解决方案

### v1.2.0 (2026-02-04)
- **新增**：AttributeError: 'int' object has no attribute 'get'问题
  - 添加self.stats初始化错误的解决方案
  - 强调嵌套字段也使用defaultdict
- **改进**：TROUBLESHOOTING章节添加详细的错误说明
- **新增**：EXAMPLES.md添加示例7和示例8

### v1.1.0 (2026-02-04)
- **重要修复**：req()函数使用说明
  - 添加req()函数的完整参数和返回值说明
  - 强调必须传递f_err参数
  - 强调返回5个值：req_url, req_json, result, log_uuid, requestid
- **重要修复**：NoneType错误处理
  - 添加`if not log_uuid or not result:`检查
  - 避免在None对象上调用.get()方法
- **重要修复**：物料解析问题
  - 明确指出_parse_item_info函数有bug（BIZ_TYPE_TO_CONTENT_NAME未定义）
  - 建议直接使用jmespath解析
  - 添加安全访问示例
- **新增**：Python版本要求
  - 明确需要Python 3.6+
  - 强调使用python3命令
- **新增**：依赖包列表
  - 添加loguru和jmespath
- **改进**：Common Patterns添加req()函数使用示例
- **改进**：Best Practices添加req()函数和物料解析最佳实践
- **改进**：Checklist添加新的检查项
- **改进**：Common imports更新，移除_parse_item_info
- **改进**：TROUBLESHOOTING添加详细的问题和解决方案

### v1.0.0 (2026-02-04)
- 初始版本
- 支持基本测试用例生成
- 包含完整文档模板
- 支持多种实验类型
