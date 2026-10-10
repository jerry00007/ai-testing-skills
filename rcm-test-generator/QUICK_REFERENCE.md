# RCM Test Generator - 快速使用指南

## 技能位置
`/Users/zhanghaishan/.config/opencode/skills/rcm-test-generator/`

## 触发关键词
使用以下任一关键词即可自动激活此技能：
- "生成推荐测试用例"
- "推荐用例"
- "创建推荐系统测试"
- "生成RCM测试"
- "推荐引擎测试"
- "召回测试"
- "实验验证"
- "RCM测试用例"

## 最简单的使用方式

```
用户: 生成推荐测试用例，测试实验 test_exp_a
```

就这么简单！Claude会自动：
1. 分析需求
2. 创建测试目录
3. 生成所有必需文件
4. 提供下一步指引

## 生成的文件

每次生成都会创建7-8个文件：
1. `exp_info.py` - 实验配置（约50行）
2. `test_api.py` - 接口测试（约300行）
3. `test_log.py` - 日志验证（约350行）
4. `test_api_response.py` - API返回验证（可选，约300行）⭐ 推荐
5. `README.md` - 详细文档（约350行）
6. `INSTALL.md` - 安装配置（约100行）
7. `QUICKSTART.md` - 快速开始（约100行）
8. `SUMMARY.md` - 测试摘要（约50行）

**⭐ test_api_response.py（推荐但可选）**
- 直接从API返回验证，无需下载日志
- 适用于快速验证场景
- 可以作为 test_log.py 的补充

## 快速开始

### 1. 创建测试用例
```
生成推荐测试用例，测试新召回路 RecallColdForceV1
```

### 2. 修改配置
打开生成的 `test_api.py`，修改：
```python
device_id_path = r"/path/to/your/device_ids.csv"
```

### 3. 运行测试
```bash
cd test_cases/YYYYMMDD-test-name/
python test_api.py
```

### 4. 验证结果
```bash
# 推荐：先快速验证API返回
python test_api_response.py

# 或者：下载日志后验证
python test_log.py
```

## 技能包含内容

✅ **标准化模板**
- 遵循项目既定模式
- 一致的代码风格
- 清晰的注释说明

✅ **智能分析**
- 自动提取实验配置
- 识别关键参数
- 解析验证点

✅ **完整文档**
- 详细使用说明
- 快速开始指南
- 常见问题解答

✅ **灵活配置**
- 支持多种实验类型
- 可自定义验证逻辑
- 灵活的统计输出

## 参考示例

完整示例: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/20260204/`

这个示例展示了：
- 多个实验桶配置
- Operation参数模拟
- 过滤逻辑验证
- 完整文档体系

## 更多帮助

查看技能目录下的文件：
- `SKILL.md` - 完整技能文档
- `README.md` - 功能说明
- `EXAMPLES.md` - 使用示例

## 频道页测试

频道页使用 `/oneapi/v2` 端点，与首页完全不同。

### 首页 vs 频道页关键差异

| 特性 | 首页 | 频道页 |
|------|------|--------|
| API端点 | `/rcm/autohmpg2/v3.0/lands` | `/oneapi/v2` |
| 配置类 | `HomePage` + `common_url` | `PinDaoYeUrl` + `conf_XXXXX()` |
| URL占位符 | `deviceid=` + 拼接 | `%s` + `%` 操作符 |
| 数据位置 | `pv_info` (JSON string) | `resourceobj` (direct fields) |
| 解析方式 | jmespath | 直接 dict.get() |
| 召回类型字段 | pv_info.rway | resourceobj.rtype |

### 快速使用

```python
from configs.config_url import PinDaoYeUrl

recall_name, base_url = PinDaoYeUrl.conf_90100213()
req_url = base_url % device_id
```

### 参考用例
`test_cases/20260424-beijing-auto-show/`

## 完整流程 (v1.8.0)

```
Phase -1: 三剑客需求分析 (MANDATORY)
    ↓
Phase 0: 查询知识库 + 提取测试点 (MANDATORY)
    ↓
Phase 1: 理解需求
Phase 2: 创建 exp_info.py
Phase 3: 创建 test_api.py
Phase 4: 创建 test_log.py
Phase 4.5: 创建 test_api_response.py (可选)
Phase 5: 创建 README.md
Phase 6: 创建 INSTALL.md
Phase 7: 创建 QUICKSTART.md
Phase 8: 创建 SUMMARY.md
    ↓
Phase 9: 三剑客Review (MANDATORY)
    ↓
✅ 交付
```

### 三剑客机制 (v1.8.0 新增)

**Phase -1 (需求分析)**:
- 产品经理 + 架构师 + QA 三角色分析需求
- 输出分析报告 + 待确认问题
- 等待用户确认

**Phase 9 (Review)**:
- 产品经理 + 架构师 + QA 三角色Review生成结果
- 10项高频问题检查清单
- 自动修复 + 确认

### 知识库查询 (v1.8.0 新增)

知识库路径: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/doc/`

| 需求类型 | 重点查阅 |
|---------|---------|
| 召回逻辑 | `recall代码知识库.md` |
| 排序/过滤/干预 | `engine代码知识库.md` |
| 测试点覆盖 | `测试点文档.md` |
| 完整流程 | `推荐系统业务逻辑完整文档.md` |

## 版本

v1.8.0 - 2026-05-25
