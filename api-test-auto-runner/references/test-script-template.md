# Test Script Template

## Standard Python API Test Script Structure

Generated test scripts MUST follow this 6-section structure. Each section is mandatory.

## Section 1: Configuration

```python
TEST_ENVS = {
    'test': 'http://test.xxx.com',
    'prod': 'http://xxx.com',
}
API_PATH = '/endpoint'
DEFAULT_PARAMS = {
    'qptype': '1',
    'uid': 'test_uid',
}
REQUEST_TIMEOUT = 10
```

## Section 2: Stats Class

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Stats:
    total: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    errors: List[str] = field(default_factory=list)
    costs: List[float] = field(default_factory=list)
    results: List[dict] = field(default_factory=list)

    def ok(self, msg):
        print(f"    ✅ {msg}")
        self.passed += 1
        self.total += 1

    def fail(self, msg):
        print(f"    ❌ {msg}")
        self.failed += 1
        self.total += 1
        self.errors.append(msg)

    def skip(self, msg):
        print(f"    ⚠️ {msg}")
        self.warnings += 1
        self.total += 1

    def check(self, condition, pass_msg, fail_msg):
        if condition:
            self.ok(pass_msg)
        else:
            self.fail(fail_msg)
```

## Section 3: Test Case Definitions

Test cases MUST be data-driven (list of dicts), not hardcoded logic.

```python
def define_test_cases():
    cases = []
    
    cases.append({
        'category': '分类名',       # Required: for grouping
        'name': 'TC-001-用例名',     # Required: unique identifier
        'query': '测试query',        # Required: input to API
        'expect_field': 'expected',  # Expected values for assertions
        'priority': 'P0',           # P0/P1/P2
        'desc': '描述',              # Human-readable description
    })
    
    return cases
```

**Coverage requirements per category**:

| Category | Description | Min Cases |
|---|---|---|
| Core functionality | Happy path, main features | 3-5 |
| Edge cases | Boundaries, empty input, long input | 3-5 |
| Error handling | Wrong params, missing fields | 2-3 |
| Security | SQL injection, XSS, special chars | 2-3 |
| Performance | Timeout checks, response time | 1-2 |

## Section 4: API Call Function

```python
import requests

def call_api(base_url: str, params: dict) -> tuple:
    """Call API and return (response_dict, error_string)"""
    url = base_url.rstrip('/') + API_PATH
    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT, verify=False)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.Timeout:
        return None, f"请求超时 ({REQUEST_TIMEOUT}s)"
    except requests.exceptions.ConnectionError as e:
        return None, f"连接失败: {e}"
    except Exception as e:
        return None, f"异常: {e}"
```

**MUST handle**:
- None responses (use `data or {}`)
- Missing fields (use `.get('field', default)`)
- Empty lists (use `or []`)
- Type mismatches (use `isinstance()` checks)

## Section 5: Validation Functions

```python
def run_single_test(base_url: str, test_case: dict, stats: Stats, verbose: bool = False):
    """Execute one test case and update stats"""
    query = test_case['query']
    params = dict(DEFAULT_PARAMS)
    params['q'] = query
    params.update(test_case.get('extra_params', {}))
    
    data, err = call_api(base_url, params)
    
    if err:
        stats.fail(f"[{test_case['name']}] 请求失败: {err}")
        stats.results.append({
            'name': test_case['name'], 'query': query,
            'status': 'ERROR', 'reason': err,
        })
        return
    
    # Validate response structure
    code = data.get('code', -1)
    stats.check(code == 0, f"[{test_case['name']}] code=0", f"[{test_case['name']}] code={code}")
    
    # Validate specific fields (CUSTOMIZE per API)
    # ... add domain-specific assertions here
    
    # Record result
    stats.results.append({
        'name': test_case['name'],
        'query': query,
        'status': 'PASS',  # or FAIL
        'cost': data.get('cost', 0),
    })
```

## Section 6: Main Function with argparse

```python
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    parser = argparse.ArgumentParser(description='API Test Script')
    parser.add_argument('--env', default='test', choices=['test', 'prod'])
    parser.add_argument('--query', default=None, help='单条query测试')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--export', action='store_true', help='导出Excel报告')
    args = parser.parse_args()
    
    base_url = TEST_ENVS[args.env]
    stats = Stats()
    
    if args.query:
        # Single query mode
        tc = {'name': '自定义', 'query': args.query, 'expect_field': None}
        run_single_test(base_url, tc, stats, verbose=True)
    else:
        # Full test suite - group by category
        all_tests = define_test_cases()
        categories = list(dict.fromkeys(t['category'] for t in all_tests))
        for cat in categories:
            cat_tests = [t for t in all_tests if t['category'] == cat]
            print(f"\n{'='*60}\n  {cat} ({len(cat_tests)}条)\n{'='*60}")
            for tc in cat_tests:
                run_single_test(base_url, tc, stats, verbose=args.verbose)
    
    # Print summary
    real_checks = stats.passed + stats.failed
    print(f"\n通过: {stats.passed}, 失败: {stats.failed}, 通过率: {stats.passed/max(real_checks,1)*100:.1f}%")
    
    # Export Excel if requested
    if args.export and stats.results:
        export_excel(stats.results, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

if __name__ == "__main__":
    main()
```

## Excel Export Template

```python
def export_excel(results: list, output_file: str):
    import pandas as pd
    df = pd.DataFrame(results)
    rename_map = {
        'name': '用例名', 'query': 'query', 'status': '状态',
        'recognized': '识别结果', 'mapped_city_name': '映射城市',
        'expect_city_name': '预期城市', 'cost': '耗时(ms)', 'reason': '原因',
    }
    existing = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df[list(existing.keys())].rename(columns=existing)
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='测试结果', index=False)
        ws = writer.sheets['测试结果']
        for col in ws.column_dimensions.values():
            col.width = 20
    print(f"✅ 报告已导出: {output_file}")
```

## Common Pitfalls to Avoid

1. **entity_result can be None**: Use `data.get('entity_result') or []`
2. **term can be None**: Use `data.get('term') or []`
3. **Fields may not exist**: Always use `.get('field', default)` not `['field']`
4. **Response may have different types**: Use `isinstance(x, list)` before iterating
5. **Encoding issues with Chinese**: Use `ensure_ascii=False` in json.dumps
6. **Excel column mismatch**: Use rename_map with `if k in df.columns` guard
