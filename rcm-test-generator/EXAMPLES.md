# RCM Test Generator - 使用示例

本文档展示如何使用 RCM Test Generator 技能来生成推荐系统测试用例。

## 基本使用

### 示例1: 简单的实验测试用例

**用户请求：**
```
生成推荐测试用例，测试新召回路 test_recall_v1
```

**Claude 会：**
1. 分析需求
2. 创建 `test_cases/YYYYMMDD-test_recall_v1/` 目录
3. 生成所有必要的文件：
   - `exp_info.py` - 配置实验
   - `test_api.py` - 发起请求
   - `test_log.py` - 验证日志
   - 完整的文档

### 示例2: 基于需求文档生成

**用户请求：**
```
请帮我生成推荐测试用例，需求如下：

需求背景：
目前有一个新的召回策略，需要验证其效果。

实验配置：
- 实验桶1: test_new_recall_a (权重0.7)
- 实验桶2: test_new_recall_b (权重0.5)
- 对照桶: 默认 (权重1.0)

验证点：
1. 实验是否正确命中
2. 新召回路是否生效
3. 召回数量是否符合预期

测试环境：
- 引擎分支: new_recall_v1
- Apollo: uat
```

**Claude 会：**
1. 解析需求文档
2. 提取关键信息（实验配置、验证点、环境）
3. 生成完整的测试用例

### 示例3: 复杂的多参数测试

**用户请求：**
```
生成推荐测试用例，需要测试请求曝光限制

实验配置：
- isFilter60: 限制60条
- isFilter150: 限制150条
- isFilter300: 限制300条
- isFilter30: 限制30条
- isFilter500: 限制500条（对照）

Operation参数：
- 0: 首页打开（只取最近100条兜底）
- 1: 底部导航栏点击（只取最近100条兜底）
- 2: 上拉加载（可以累积）
- 4: 手动下拉刷新（只取最近100条兜底）

需要模拟不同的operation参数来测试过滤逻辑
```

**Claude 会：**
1. 识别复杂的operation参数逻辑
2. 在 `test_api.py` 中添加operation模拟
3. 在 `test_log.py` 中添加过滤逻辑验证
4. 生成完整的文档说明

## 高级使用

### 指定参考测试用例

**用户请求：**
```
生成推荐测试用例，参考 20260204 的测试用例结构
需求：测试新的排序策略 rank_v1
```

**Claude 会：**
1. 读取参考测试用例 `20260204`
2. 复用相同的结构模式
3. 根据新需求调整实验配置和验证逻辑

### 指定特定功能

**用户请求：**
```
生成推荐测试用例，专门测试冷启动召回路
需要验证：
1. 冷启动召回是否正确
2. 画像字段是否正确使用
3. 召回物料是否符合预期
```

**Claude 会：**
1. 专注于冷启动测试特点
2. 添加画像字段验证
3. 添加召回路验证逻辑

## 实际对话示例

### 场景1: 快速创建测试用例

```
用户: 我需要生成一个推荐测试用例，测试新实验 test_exp_a

Claude: [自动激活 RCM Test Generator 技能]
正在创建测试用例...

[分析需求]
测试目的: 验证实验 test_exp_a
实验配置: 单个实验

[生成文件]
✅ 已创建: test_cases/20260205-test_exp_a/
✅ 已创建: exp_info.py
✅ 已创建: test_api.py
✅ 已创建: test_log.py
✅ 已创建: README.md
✅ 已创建: INSTALL.md
✅ 已创建: QUICKSTART.md
✅ 已创建: SUMMARY.md

测试用例已创建完成！

下一步:
1. 修改 test_api.py 中的 device_id_path
2. 运行 python test_api.py
3. 下载日志后运行 python test_log.py
```

### 场景2: 基于详细需求

```
用户: 请帮我生成推荐测试用例，需求文档如下：

需求背景：
目前feed的召回策略需要优化，添加了新的召回路
RecallSemanticColdForceV1
RecallColdSeriesEEV1

实验配置：
实验名称: Product_category_2026test_a
实验桶1: test_a (权重0.7)
实验桶2: test_b (权重0.5)
对照桶: 默认 (1.0)

验证点：
1. 实验是否正确命中
2. 新召回路是否生效
3. 召回数量 > 0
4. 召回物料类型符合预期

环境信息：
引擎分支: new_recall_semantic_v1
Apollo配置: uat
测试环境: UAT

Claude: [自动激活 RCM Test Generator 技能]
正在分析需求...

[提取关键信息]
实验配置:
- test_a: 0.7
- test_b: 0.5
- 默认: 1.0

验证点:
- 实验命中
- 召回路生效
- 召回数量
- 物料类型

[生成测试用例]
✅ exp_info.py - 配置实验和召回路
✅ test_api.py - 添加召回路验证
✅ test_log.py - 验证召回路逻辑
✅ README.md - 详细文档

测试用例已创建在: test_cases/20260206-new_recall_semantic/

[特别说明]
已在 test_log.py 中添加召回路验证:
✅ 检查 RecallSemanticColdForceV1
✅ 检查 RecallColdSeriesEEV1
✅ 统计各召回路数量
```

### 场景3: 指定operation参数

```
用户: 生成推荐测试用例，需要测试operation过滤

实验配置:
实验名称: operation_filter_test
实验桶1: isFilter50 (限制50条)
实验桶2: isFilter100 (限制100条)
对照桶: isFilter500 (限制500条)

Operation逻辑:
- operation=0: 首页打开，只取最近100条
- operation=1: 底部导航，只取最近100条
- operation=2: 上拉加载，可以累积
- operation=4: 下拉刷新，只取最近100条

请模拟不同operation进行测试

Claude: [自动激活 RCM Test Generator 技能]
正在创建operation过滤测试...

[分析operation逻辑]
- 需要在 test_api.py 中随机选择operation
- 需要在 test_log.py 中验证过滤逻辑

[生成代码]
✅ test_api.py: 添加operation参数模拟
✅ test_log.py: 添加过滤逻辑验证

[operation分布示例]
- operation=0 (首页打开): 20%
- operation=1 (底部导航): 20%
- operation=2 (上拉加载): 30%
- operation=4 (下拉刷新): 30%

[验证逻辑]
✅ operation=0,1,4: 验证过滤上限为100
✅ operation=2: 验证可以累积到实验限制
```

## 技能触发条件

以下关键词会自动激活此技能：

- "生成推荐测试用例"
- "推荐用例"
- "创建推荐系统测试"
- "生成RCM测试"
- "推荐引擎测试"
- "召回测试"
- "实验验证"
- "RCM测试用例"

## 生成后的后续步骤

1. **修改配置**
    ```python
    # 在 test_api.py 中
    device_id_path = r"/path/to/your/device_ids.csv"
    ```

2. **验证结构**
    ```bash
    cd test_cases/YYYYMMDD-test-name/
    python -m py_compile test_api.py
    python -m py_compile test_log.py
    python -m py_compile test_api_response.py  # 如果生成
    ```

3. **小规模测试**
    ```python
    # 修改为10次请求
    tr = TheadRun(device_id_path, 10, 0)
    ```

4. **完整测试**
    ```bash
    python test_api.py

    # 推荐：快速验证API返回（无需下载日志）
    python test_api_response.py

    # 或者：下载日志后深度验证
    python test_log.py
    ```

## 常见问题

### Q: 如何修改实验比例？
A: 修改 `test_api.py` 中的随机选择逻辑：
```python
exp_rand = random.random()
if exp_rand < 0.3:  # 30%
    exp_choice = "test_a"
elif exp_rand < 0.6:  # 30%
    exp_choice = "test_b"
else:  # 40%
    exp_choice = ""
```

### Q: 如何添加自定义验证？
A: 在 `test_log.py` 的测试类中添加方法：
```python
def check_custom_validation(self, log_uuid: str, req_info: Dict) -> bool:
    # 自定义验证逻辑
    return True
```

### Q: 如何生成不同类型的测试用例？
A: 在请求中明确说明测试类型：
- "召回测试" - 专注于召回策略
- "实验验证" - 专注于实验命中
- "排序测试" - 专注于排序算法
- "过滤测试" - 专注于过滤逻辑
- "API返回验证" - 专注于API字段验证（推荐生成test_api_response.py）

## 常见问题示例

### 示例4: 修复API返回null问题

**用户请求：**
```
运行test_api.py后，api_return.txt为空，API返回null
```

**问题原因：**
```python
# 错误的URL构造（缺少必需参数）
test_url = (
    "http://test-api.example.com/rcm/autohmpg2/v3.0/lands?" +
    f"deviceid={device_id}" +
    f"&number={num_choice}" +
    f"&appexp={exp_choice}" +
    f"&autorefresh={autorefresh}&operation={operation}"
)
# 结果：API返回null，因为缺少bsdata、outmedia、gps等必需参数
```

**正确做法：**
```python
# 参考configs/config_url.py中的HomePage.common_url定义
# 包含所有必需参数
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
    f"devicetype=android&" +
    f"uid=174085853"
)
```

**关键点：**
- 参考`configs/config_url.py`第412-414行查看完整的参数列表
- 不要手动构造URL，使用`HomePage.test_domain + HomePage.common_url`模式
- 确保所有参数都用`&`连接

### 示例5: 修复日志解析NotADirectoryError问题

**用户请求：**
```
运行test_log.py时报错：
[Errno 20] Not a directory: '/path/engine_monitor.txt/engine_monitor.txt'
```

**问题原因：**
```python
# 错误的日志解析（传入文件路径）
def parse_monitor_data(self):
    monitor_file = os.path.join(self.test_dir, "engine_monitor.txt")
    self.monitor_data = collection_monitor(monitor_file)  # 错误：传入文件路径
    
# collection_monitor期望在目录下查找engine_monitor.txt
# 实际尝试打开：/path/engine_monitor.txt/engine_monitor.txt
```

**正确做法：**
```python
def parse_monitor_data(self):
    monitor_file = os.path.join(self.test_dir, "engine_monitor.txt")
    
    if not os.path.exists(monitor_file):
        print(f"⚠️  monitor日志文件不存在: {monitor_file}")
        print(f"   请先将日志文件下载到: {self.test_dir}")
        return
    
    print("正在解析monitor日志...")
    self.monitor_data = collection_monitor(
        self.test_dir,  # 正确：传入目录路径
        node_path="hit_study1_name_map"
    )
    
# 同样，debug日志解析：
def parse_debug_data(self):
    debug_file = os.path.join(self.test_dir, "engine_debug.txt")
    
    if not os.path.exists(debug_file):
        print(f"⚠️  debug日志文件不存在: {debug_file}")
        print(f"   请先将日志文件下载到: {self.test_dir}")
        return
    
    print("正在解析debug日志...")
    self.debug_data = collection_debug(self.test_dir)  # 正确：传入目录路径
```

**关键点：**
- `collection_monitor()`和`collection_debug()`期望传入**目录路径**
- 函数会在目录下自动查找`engine_monitor.txt`和`engine_debug.txt`
- 在解析前检查文件是否存在，给出友好的错误提示

### 示例6: 静默刷新测试用例（完整示例）

**用户请求：**
```
生成静默刷新3.0迭代测试用例
- 实验：103471_A, 103471_B, 空实验
- 需求：num参数返回指定数量，过滤商业内容
```

**完整配置：**

exp_info.py:
```python
# -*- coding: utf-8 -*-
"""
@author: lujia
@time: 2026/2/4
@Desc: 20260204测试用例 - 静默刷新3.0迭代
"""

class Exp:
    exps_list = {
        "103471_A": True,   # 实验桶A：启用非商业内容过滤
        "103471_B": True,   # 实验桶B：启用非商业内容过滤
        "": False          # 空实验（默认行为）
    }
    
    testNeedExps = ["", "103471_A", "103471_B"]
    
    exp_descriptions = {
        "103471_A": "实验桶A - 启用非商业内容过滤（不含北斗置顶）",
        "103471_B": "实验桶B - 启用非商业内容过滤（不含北斗置顶）",
        "": "空实验（默认行为，返回所有内容）"
    }
    
    num_options = [10, 15, 20, 30]
    
    business_content_types = ["beidou_top", "business_ad", "sponsored"]
```

test_api.py（URL构造关键部分）:
```python
# 构造完整的URL，包含所有必需参数
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

test_log.py（日志解析关键部分）:
```python
def parse_monitor_data(self):
    monitor_file = os.path.join(self.test_dir, "engine_monitor.txt")
    
    if not os.path.exists(monitor_file):
        print(f"⚠️  monitor日志文件不存在: {monitor_file}")
        print(f"   请先将日志文件下载到: {self.test_dir}")
        return
    
    print("正在解析monitor日志...")
    self.monitor_data = collection_monitor(
        self.test_dir,  # 传入目录路径
        node_path="hit_study1_name_map"
    )
    print(f"✅ 成功解析monitor日志，共 {len(self.monitor_data)} 条记录")

def parse_debug_data(self):
    debug_file = os.path.join(self.test_dir, "engine_debug.txt")
    
    if not os.path.exists(debug_file):
        print(f"⚠️  debug日志文件不存在: {debug_file}")
        print(f"   请先将日志文件下载到: {self.test_dir}")
        return
    
    print("正在解析debug日志...")
    self.debug_data = collection_debug(self.test_dir)  # 传入目录路径
    print(f"✅ 成功解析debug日志，共 {len(self.debug_data)} 条记录")
```

### 示例7: 修复AttributeError: 'int' object has no attribute 'get'

**用户请求：**
```
运行test_log.py时报错：
AttributeError: 'int' object has no attribute 'get'
```

**问题原因：**
```python
# 错误的初始化
class Jingmo30Tester:
    def __init__(self):
        self.stats = defaultdict(int)  # ❌ 错误：嵌套字段会返回int

# 访问时出错
self.stats["exp_stats"][hit_exp] = self.stats["exp_stats"].get(hit_exp, 0) + 1
# ↑ self.stats["exp_stats"] 是 int(0)，不是defaultdict
```

**正确做法：**
```python
# 正确的初始化 - 嵌套字段也使用defaultdict
class Jingmo30Tester:
    def __init__(self):
        self.stats = {
            "total_requests": 0,
            "success_checks": 0,
            "failed_checks": 0,
            "exp_stats": defaultdict(int),  # ✅ 嵌套defaultdict
            "num_stats": defaultdict(int)
        }

# 正确的访问
self.stats["exp_stats"][hit_exp] = self.stats["exp_stats"].get(hit_exp, 0) + 1
# ↑ self.stats["exp_stats"] 是 defaultdict(int)，可以使用 .get()
 ```

**关键点：**
- 嵌套的统计字段（如`exp_stats`、`num_stats`）也需要是`defaultdict`
- 顶层使用普通字典，嵌套使用`defaultdict`
- 确保初始化结构正确，避免访问时类型错误

### 示例8: 使用 test_api_response.py 验证 uniq_series_id

**用户请求：**
```
生成推荐测试用例，验证无车系内容过滤
- 实验：is_without_series_d（索引层过滤）
- 验证点：非商业数据的 uniq_series_id 不能为空
```

**完整配置：**

test_api.py（关键部分 - 保存完整API返回）:
```python
# 在 Check.check_thread_line() 方法中
results_collection = {}

# 发送请求
req_url, req_json, result, log_uuid, requestid = req(test_url, kwargs.get("f_inter_err"))

# 检查空值
if not log_uuid or not result:
    write_error_log_file(kwargs.get("f_inter_err"), {
        "err": "返回数据为空",
        "device_id": device_id
    })
    return results_collection

# 保存完整API返回（重要！）
results_collection[log_uuid] = {
    "device_id": device_id,
    "hit_exp": exp_choice,
    "response": result,  # 完整的API返回字典
    "request_url": test_url
}

# 在主测试函数中保存到文件
api_response_file = os.path.join(cur_path, "api_response_full.json")
with open(api_response_file, "w", encoding="utf-8") as f:
    json.dump(results_collection, f, ensure_ascii=False, indent=2)
```

test_api_response.py（验证逻辑）:
```python
def validate_item_uniq_series_id(self, log_uuid: str, device_id: str, hit_exp: str,
                                 item: Dict, index: int, request_url: str = "") -> bool:
    # 使用jmespath解析物料信息
    pv_info_str = jmespath.search(HomePage.pvinfo_path, item) or "{}"
    try:
        pv_info = json.loads(pv_info_str)
    except:
        pv_info = {}

    # 提取字段
    biz_type = jmespath.search(HomePage.pvinfo_biz_type_path, pv_info)
    biz_id = jmespath.search(HomePage.pvinfo_biz_id_path, pv_info)
    rway = jmespath.search(HomePage.pvinfo_rway_path, pv_info) or ""
    uniq_series_id = jmespath.search(HomePage.uniq_series_id_path, item) or ""

    # 类型转换
    try:
        biz_type_int = int(biz_type) if biz_type is not None else 0
    except:
        biz_type_int = 0

    # 判断是否为非商业数据
    is_non_commercial = biz_type_int in Exp.non_commercial_biztypes

    # 验证：is_without_series_d 实验桶，非商业数据必须有车系
    if hit_exp == "is_without_series_d":
        if is_non_commercial:
            has_series = bool(uniq_series_id and uniq_series_id.strip())
            if not has_series:
                # 记录错误
                err_msg = {
                    "error": "is_without_series_d实验桶：非商业数据存在无车系物料",
                    "log_uuid": log_uuid,
                    "device_id": device_id,
                    "exp": hit_exp,
                    "item_index": index,
                    "item_info": {
                        "biz_type": biz_type_int,
                        "biz_id": biz_id,
                        "rway": rway,
                        "uniq_series_id": uniq_series_id,
                        "is_non_commercial": True
                    },
                    "request_url": request_url
                }
                file_util.write_error_log(f_err, err_msg)
                return False

    return True

def print_summary(self):
    # 打印不符合预期的请求URL列表
    if self.stats["error_request_urls"]:
        print("\n" + "=" * 60)
        print("不符合预期的请求URL列表 (is_without_series_d 实验桶)")
        print("=" * 60)
        for i, err_info in enumerate(self.stats["error_request_urls"], 1):
            print(f"\n[{i}] device_id: {err_info['device_id']}")
            print(f"    log_uuid: {err_info['log_uuid']}")
            print(f"    item_index: {err_info['item_index']}, biz_type: {err_info['biz_type']}, biz_id: {err_info.get('biz_id', 'N/A')}, rway: {err_info.get('rway', 'N/A')}")
            print(f"    请求URL:")
            print(f"    {err_info['request_url']}")
```

**输出示例：**
```
============================================================
API返回验证统计摘要
============================================================

总请求数: 100
成功检查: 98
失败检查: 2
无车系过滤错误: 2

【is_without_series_d】- 实验桶4 - 索引层过滤无车系内容
  请求数: 20次
  错误数: 2个
  物料总数: 400个
  非商业物料: 300个 (75.0%)
    ├─ 有车系: 298个 (99.3%)
    └─ 无车系: 2个 (0.7%)

============================================================
不符合预期的请求URL列表 (is_without_series_d 实验桶)
============================================================

[1] device_id: 83EDACA7_6A3B_4CC5_B929_ABE53E520B7D
    log_uuid: d6ki40url3rqqc7aujdg
    item_index: 10, biz_type: 14, biz_id: xxx, rway: RecallDSSMNewItemSdk_Video
    请求URL:
    http://test-api.example.com/rcm/autohmpg2/v3.0/lands?...
```

**关键点：**
- **test_api.py** 必须保存完整API返回到 `api_response_full.json`
- **test_api_response.py** 直接解析API返回，无需日志文件
- **验证逻辑**：根据实验桶要求验证特定字段
- **错误报告**：包含 device_id, log_uuid, item_index, biz_type, biz_id, rway, request_url
- **快速验证**：运行 `python test_api_response.py` 立即查看结果

### 示例9: 两种验证方法的对比

**用户请求：**
```
什么时候使用 test_api_response.py，什么时候使用 test_log.py？
```

**对比说明：**

| 特性 | test_api_response.py | test_log.py |
|------|---------------------|-------------|
| **速度** | ⚡ 快速 | 🐌 较慢 |
| **需要日志** | ❌ 不需要 | ✅ 必需 |
| **验证内容** | API返回字段 | 引擎内部行为 |
| **适用场景** | 快速验证字段 | 深度调试问题 |
| **验证范围** | response字段 | 实验命中、召回、排序等 |
| **依赖** | test_api.py输出 | 日志文件 |

**推荐流程：**
```
1. 运行 test_api.py（发起请求）
   ↓
2. 立即运行 test_api_response.py（快速验证）
   - 发现问题 → 定位到具体请求和物料
   - 无问题 → 可选择是否继续深度验证
   ↓
3. （可选）下载日志后运行 test_log.py（深度验证）
   - 验证实验命中
   - 查看召回详情
   - 深度调试问题
```

**何时使用 test_api_response.py:**
- ✅ 快速验证字段值（如 uniq_series_id、biz_type、biz_id）
- ✅ 不想等待日志下载
- ✅ 只关心API返回结果
- ✅ 需要查看完整的请求URL和响应
- ✅ 快速迭代测试

**何时使用 test_log.py:**
- ✅ 需要验证实验是否正确命中
- ✅ 需要查看召回详情和召回路
- ✅ 需要调试引擎内部逻辑
- ✅ 需要查看完整的debug日志
- ✅ 深度分析问题根因

**最佳实践：**
- **日常测试**：使用 `test_api_response.py` 快速验证
- **问题调试**：结合 `test_log.py` 深度分析
- **正式测试**：两者都运行，确保全面覆盖

### 示例10: 静默刷新完整测试用例（参考）

RCM Test Generator 技能可以：

✅ 自动化测试用例生成
✅ 遵循项目既定模式
✅ 生成完整的文档体系
✅ 支持多种测试类型
✅ 提供灵活的配置选项
✅ 包含详细的验证逻辑

使用此技能可以大大提高测试用例开发的效率！

### 示例11: 频道页测试（车展/专题页）

**用户请求：**
```
生成推荐测试用例，测试车展专题页推荐
- 场景1: 车展专题页 (pid: 90100213)，包含文章、视频、快讯等多种内容
- 场景2: 车展沉浸流 (pid: 90100214)，仅包含视频类型
- 测试数据: 用户提供Excel文件包含各类型测试ID
```

**Claude 会：**
1. 使用 `PinDaoYeUrl` 配置类获取频道页URL
2. 创建多场景测试（专题页+沉浸流）
3. 使用 `resourceobj` 解析物料（不是 pv_info）
4. 创建 `test_data_config.py` 保存Excel测试数据
5. 在 `test_api_response.py` 中验证测试数据召回

**exp_info.py（关键配置）:**
```python
class Exp:
    test_scenarios = {
        "90100213": {"name": "车展专题", "recall_types": ["RecallRtype", "RecallNewCarLatest"]},
        "90100214": {"name": "车展沉浸流", "recall_types": ["RecallForceType"]}
    }
    
    biz_type_distribution = {
        "90100213": {"expected_types": [1, 3, 5, 12, 13, 14, 66, 700112, 610110, 610120, 610121]},
        "90100214": {"expected_types": [3, 14, 66]}
    }
```

**test_api.py（频道页关键代码）:**
```python
from configs.config_url import PinDaoYeUrl

# 多场景选择
scenario_rand = random.random()
scenario_key = "90100213" if scenario_rand < 0.5 else "90100214"

if scenario_key == "90100213":
    recall_name, base_url = PinDaoYeUrl.conf_90100213()
else:
    recall_name, base_url = PinDaoYeUrl.conf_90100214()

req_url = base_url % device_id
```

**test_api_response.py（频道页数据提取）:**
```python
def extract_item_info(item):
    # 频道页数据在 resourceobj 中，不在 pv_info 中！
    resourceobj = item.get("resourceobj", {})
    biz_id = str(resourceobj.get("biz_id", ""))
    biz_type = str(resourceobj.get("biz_type", ""))
    rtype = resourceobj.get("rtype", "")
    return biz_id, biz_type, rtype
```

**test_data_config.py（Excel测试数据）:**
```python
TEST_DATA = {
    "原创图文": {"biztype": 1, "opu": "O", "ids": [1313417, 1313416], "scene": "90100213"},
    "原创视频": {"biztype": 3, "opu": "O", "ids": [2257517, 2257516], "scene": "90100213"},
    "车家号视频": {"biztype": 14, "opu": "P", "ids": [25160236, 25159649], "scene": "90100213"},
}
```

**关键点：**
- 频道页使用 `/oneapi/v2` 端点，**不是** `/rcm/autohmpg2/v3.0/lands`
- 数据在 `resourceobj` 中，**不能**使用 jmespath + pv_info_path
- 使用 `PinDaoYeUrl.conf_XXXX()` 获取URL配置
- 支持多场景测试（一次运行覆盖多个pid）
- 使用 `test_data_config.py` 管理Excel测试数据


## 三剑客分析流程 (v1.8.0 新增)

### 示例12: 三剑客需求分析

**用户请求：**
```
生成推荐测试用例，需求文档如下：
[需求文档内容]
```

**Claude 会 (Phase -1: 三剑客需求分析):**
1. 自动执行三剑客需求分析
2. 从三个角色分析需求：
   - 🗡️ 产品经理: 核心价值、影响范围、成功标准
   - 🗡️ 架构师: 涉及模块、数据流向、配置依赖
   - 🗡️ QA: 正向/异常/边界场景、回归风险
3. 输出分析报告，包含需要人工确认的问题
4. 等待用户确认后继续

**输出格式示例:**
```
## 三剑客需求分析报告

### 🗡️ 产品经理分析
- **核心价值**: 验证产品力标签2.0功能
- **影响范围**: 首页推荐流
- **待确认问题**: 实验桶是否只涉及test_a?

### 🗡️ 架构师分析
- **涉及模块**: 召回+排序
- **配置依赖**: Apollo实验配置

### 🗡️ QA分析
- **正向场景**: 标签正常展示
- **异常场景**: 无标签数据时的兜底

### ⚠️ 需要人工确认的问题
1. 实验桶范围？
2. 标签数据来源？
```

### 示例13: 三剑客Review

**所有文件生成后，Claude 会自动执行 (Phase 9: 三剑客Review):**

1. 完整阅读所有生成的文件
2. 三个角色Review:
   - 🗡️ 产品经理: 功能覆盖、实验配置、验证点一致性
   - 🗡️ 架构师: URL构造、数据流、代码bug
   - 🗡️ QA: 正反向测试、边界条件、统计逻辑
3. 输出Review报告
4. 自动修复发现的问题
5. 确认修复完成

**高频问题检查清单:**
- exp_info.py实验配置是否与需求匹配
- test_api.py URL是否包含所有必要参数
- 空值处理是否完善
- jmespath路径是否正确
- validation_points是否与实际验证一致

### 示例14: 知识库查询流程

**用户请求涉及召回逻辑时:**

```
1. 读取 doc/recall代码知识库.md → 找到召回相关架构
2. 读取 doc/测试点文档.md → 找到相关测试点
3. 如果找不到 → 输出 "⚠️ 知识库中未找到的信息" 并等待人工确认
```

**查询策略:**
- 召回逻辑 → `recall代码知识库.md`
- 排序/过滤/干预 → `engine代码知识库.md`
- 测试点覆盖 → `测试点文档.md`
- 完整流程 → `推荐系统业务逻辑完整文档.md`


---

## 技能版本

v1.8.0 - 2026-05-25
