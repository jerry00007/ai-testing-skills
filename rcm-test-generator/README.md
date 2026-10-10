# RCM Test Generator Skill

生成推荐系统测试用例的技能。

## 环境要求

### Python版本
- **Python 3.6+**: 必须使用Python 3.6或更高版本
- **使用python3命令**: 系统默认`python`可能是Python 2.7，请使用`python3`运行脚本

### 依赖包安装
```bash
pip3 install pandas requests tqdm loguru jmespath
```

## 功能说明

这个技能帮助您创建完整的推荐系统测试用例，包括：

### Phase 0: 文档查询与测试点提取（⭐ 新增）

**重要**: 在生成任何测试用例文件之前，技能会自动：
1. 查询 `/Users/zhanghaishan/Documents/workspace/RcmTestProject/doc/` 目录
2. 从测试点文档、业务逻辑文档中提取相关测试点
3. 生成测试覆盖矩阵
4. 确保测试用例覆盖全面

**关键文档**:
- `测试点文档.md` - 包含完整的测试点列表（1200行）
- `推荐系统业务逻辑完整文档.md` - 召回、过滤、排序、干预流程（747行）

### 生成的文件

- `exp_info.py` - 实验配置（包含 validation_points）
- `test_api.py` - 接口测试脚本（发起请求并保存完整API返回）
- `test_api_response.py` - API返回验证脚本（直接从API返回验证，无需日志）⭐ 推荐
- `README.md` - 详细文档（包含测试覆盖矩阵）
- `INSTALL.md` - 安装配置说明
- `QUICKSTART.md` - 快速开始指南
- `SUMMARY.md` - 测试用例摘要

## 使用方法

当您需要生成推荐系统测试用例时，可以使用以下关键词触发此技能：

- "生成推荐测试用例"
- "推荐用例"
- "创建推荐系统测试"
- "生成RCM测试"
- "推荐引擎测试"
- "召回测试"
- "实验验证"
- "RCM测试用例"

## 示例请求

### 示例1: 创建新的测试用例
```
用户: 我需要生成一个新的推荐测试用例，需求如下：
- 实验名称：test_exp_a
- 测试目的：验证新召回路
- 引擎分支：new_recall_v1
```

Claude会自动使用此技能，创建完整的测试用例结构。

### 示例2: 基于需求文档生成
```
用户: 请帮我生成推荐测试用例，需求文档内容如下：
[粘贴需求文档]
```

Claude会分析需求文档，提取关键信息，生成相应的测试用例。

### 示例3: 指定测试类型
```
用户: 我需要一个召回测试用例，要测试3个实验桶
```

Claude会根据召回测试的特点，生成合适的测试脚本。

## 生成的文件结构

```
test_cases/YYYYMMDD-test-name/
├── exp_info.py          # 实验配置（50行左右）
├── test_api.py          # 接口测试（300行左右）
├── test_log.py          # 日志验证（350行左右）
├── test_api_response.py # API返回验证（可选，300行左右）⭐
├── README.md            # 详细文档（350行左右）
├── INSTALL.md           # 安装配置（100行左右）
├── QUICKSTART.md        # 快速开始（100行左右）
└── SUMMARY.md           # 摘要（50行左右）
```

**⭐ test_api_response.py（可选但推荐）**
- **用途**：直接从API返回验证数据，不需要下载日志
- **优点**：快速验证、独立验证、完整数据保存
- **适用场景**：快速检查 uniq_series_id、biz_type、biz_id 等字段
- **是否必需**：可选，根据需求决定是否生成

## 技能特性

### 智能需求分析
- 自动提取实验配置
- 识别operation参数
- 解析过滤逻辑
- 提取验证点

### 标准化结构
- 遵循项目既定模式
- 一致的代码风格
- 完整的文档体系
- 清晰的注释说明

### 灵活配置
- 支持多种实验类型
- 可自定义operation分布
- 灵活的验证逻辑
- 可扩展的统计信息

## 项目上下文

### 关键路径
- 测试用例目录: `/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/`
- 配置文件: `configs/config.py`
- 工具库: `test_utils/`

### 常用导入
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

## 频道页测试

频道页（如车展专题页、沉浸流等）使用完全不同的API端点和数据结构。

### 与首页的区别

- **首页**: `/rcm/autohmpg2/v3.0/lands`，数据在 `pv_info` (JSON字符串)，使用 `jmespath` 解析
- **频道页**: `/oneapi/v2`，数据在 `resourceobj` (直接字段)，使用 `dict.get()` 解析

### 配置类

频道页配置在 `configs/config_url.py` 的 `PinDaoYeUrl` 类中：

```python
from configs.config_url import PinDaoYeUrl

# 获取配置（返回 recall_name 和 base_url）
recall_name, base_url = PinDaoYeUrl.conf_90100213()
req_url = base_url % device_id  # 替换 %s 占位符
```

### 参考用例
- 车展专题页: `test_cases/20260424-beijing-auto-show/`

## 参考示例

完整的测试用例示例：`/Users/zhanghaishan/Documents/workspace/RcmTestProject/test_cases/20260204/`

这个示例展示了：
- 多个实验桶配置（isFilter60/150/300/30/500）
- Operation参数模拟（首页打开、上拉加载、下拉刷新等）
- 过滤逻辑验证
- 完整的文档体系

## 最佳实践

1. **需求理解**: 清晰描述测试目的、实验配置、验证点
2. **完整信息**: 提供需求文档或详细的需求描述
3. **参考示例**: 如果有类似测试用例，可以指定参考
4. **验证测试**: 生成后运行小规模测试验证

## 常见问题

### Q: Python报SyntaxError怎么办？
A: 系统默认`python`命令可能是Python 2.7，请使用`python3`运行：
```bash
python3 test_api.py
python3 test_log.py
```

### Q: req()函数报错missing argument？
A: `req()`函数需要2个参数，返回5个值：
```python
# 正确用法
req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))

# 检查空值
if not log_uuid or not result:
    # 处理空结果
    return results_collection
```

### Q: 报NoneType object has no attribute 'get'？
A: `result`可能为None，添加检查：
```python
req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))

# 添加空值检查
if not log_uuid or not result:
    write_error_log_file(kwargs.get("f_inter_err"), {
        "err": "返回数据为空",
        "device_id": device_id
    })
    return results_collection

# 然后才能安全使用
item_list = result.get("itemlist", [])
```

### Q: _parse_item_info报BIZ_TYPE_TO_CONTENT_NAME未定义？
A: 该函数有bug，建议直接使用jmespath解析：
```python
import jmespath

# 获取pv_info
pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
pv_info = json.loads(pv_info_str)

# 提取字段（提供默认值避免NoneType错误）
biz_type = str(jmespath.search(HomePage.pvinfo_biz_type_path, pv_info) or "")
biz_id = str(jmespath.search(HomePage.pvinfo_biz_id_path, pv_info) or "")
rway = jmespath.search(HomePage.pvinfo_rway_path, pv_info) or ""
```

### Q: API返回null怎么办？
A: 参考技能的Troubleshooting章节，确保URL包含所有必需参数：
- 使用`HomePage.test_domain + HomePage.common_url`作为基础
- 参考`configs/config_url.py`第412-414行
- 包含bsdata、outmedia、gps、netstate等参数

### Q: 日志解析报NotADirectoryError？
A: 检查test_log.py中的日志解析：
- `collection_monitor()`和`collection_debug()`期望**目录路径**
- 正确方式：`collection_monitor(self.test_dir, node_path="...")`
- 错误方式：`collection_monitor(monitor_file)` # monitor_file是完整路径

### Q: 生成的测试用例可以直接运行吗？
A: 需要修改 `test_api.py` 中的 `device_id_path` 为实际的device_id文件路径。

### Q: 如何调整实验比例？
A: 修改 `test_api.py` 中的随机选择逻辑，调整各实验的概率。

### Q: 如何添加自定义验证？
A: 在 `test_log.py` 的测试类中添加自定义验证方法。

### Q: 如何调试测试用例？
A: 先使用少量请求（如10次）验证流程，确认无误后再扩大规模。

## 技能版本

- 版本: 1.9.0
- 创建时间: 2026-02-04
- 作者: OpenCode

## 更新日志

### v1.9.0 (2026-08-07)
- **重大新增**：Phase 0.5 场景识别与PID/URL校验
  - 7大场景自动识别（首页/点后推/静默刷新/车展/车系页/频道页/新APP）
  - PID-API路径-解析方式-实验参数 四维校验矩阵
- **重要新增**：踩坑防护清单扩展至15项
- **新增文档关联**：`doc/测试场景分类与参数配置指南.md` 列为最先必查文档

### v1.8.0 (2026-05-25)
- 三剑客需求分析 + Review 双重保障机制
- 知识库查询机制优化

### v1.6.0 (2026-04-13)
- 频道页(Channel Page)测试支持
- 测试数据召回验证模式

### v1.5.0 (2026-03-24)
- **重大更新**：新增 Phase 0 - 文档查询与测试点提取
  - 自动查询 `/Users/zhanghaishan/Documents/workspace/RcmTestProject/doc/` 目录
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
- **新增**：test_api_response.py 支持和说明
  - 添加 test_api_response.py 的功能说明
  - 区分 test_api_response.py 和 test_log.py 的使用场景
  - 更新生成的文件列表结构
  - 推荐先使用 test_api_response.py 快速验证
- **改进**：文档结构优化
  - 更新示例和最佳实践
  - 添加 API返回验证相关的说明

### v1.3.0 (2026-03-04)
- **重要修复**：req()函数使用说明
  - 添加req()函数的完整参数和返回值说明
  - 强调必须传递f_err参数
  - 强调返回5个值：req_url, req_json, result, log_uuid, requestid
- **重要修复**：NoneType错误处理
  - 添加`if not log_uuid or not result:`检查
  - 避免在None对象上调用.get()方法
- **重要修复**：物料解析问题
  - 明确指出_parse_item_info函数有bug
  - 建议直接使用jmespath解析
  - 添加安全访问示例
- **新增**：Python版本要求
  - 明确需要Python 3.6+
  - 强调使用python3命令
- **新增**：依赖包列表
  - 添加loguru和jmespath

### v1.2.0 (2026-02-04)
- **新增**：AttributeError: 'int' object has no attribute 'get'问题
  - 添加self.stats初始化错误的解决方案
  - 强调嵌套字段也使用defaultdict
- **改进**：TROUBLESHOOTING章节添加详细的错误说明
- **新增**：EXAMPLES.md添加示例7和示例8

### v1.1.0 (2026-02-04)
- **新增**：URL构造和日志解析的常见问题
  - 添加API返回null的解决方案
  - 强调参考`configs/config_url.py`中的`HomePage.common_url`
  - 添加完整的URL参数示例
- **新增**：日志解析常见问题
  - 添加NotADirectoryError的解决方案
  - 强调`collection_monitor`和`collection_debug`期望目录路径
- **改进**：Common Patterns添加完整的URL构造示例
- **改进**：Best Practices添加URL构造和日志解析最佳实践
- **改进**：Checklist添加额外检查项（URL参数、日志路径）
- **新增**：EXAMPLES.md添加常见问题修复示例

### v1.0.0 (2026-02-04)
- 初始版本
- 支持基本测试用例生成
- 包含完整文档模板
- 支持多种实验类型
