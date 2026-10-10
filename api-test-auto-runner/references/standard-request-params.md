# 推荐引擎标准请求参数规范

> **MANDATORY**: All test scripts targeting `autohmpg2` or any `/rcm/` endpoint MUST include the complete set of 35 production parameters. Missing parameters causes silent logic failures (e.g., missing `appversion` → `se_version:[]` → ES returns 0 results).

## Complete Parameter Template

Reference file: `doc/线上请求标准参数模板.md` in the RcmTestProject repository.

## Python Builder Function

```python
import base64, json, time

def build_standard_params(device_id, uid="0", platform="android"):
    is_ios = platform == "ios"
    if uid and uid != "0":
        uuid_val = f"u_{uid}"
    else:
        uuid_val = f"d_{device_id}"

    bsdata_raw = json.dumps({"RemainDqLen": 0, "pvordina": 1, "pvTime": int(time.time())})
    bsdata = base64.b64encode(bsdata_raw.encode()).decode()

    return {
        "devicetype": "ios" if is_ios else "android",
        "uid": uid,
        "deviceid": device_id,
        "blackarticlelist": "",
        "source": "app",
        "netstate": "5",
        "gps": "",
        "version": "3",
        "outmedia": "9180561404330507896",
        "outmedia1": "4086764837169780704",
        "outmedia2": "3626190930523365",
        "appversion": "11.84.5",
        "bsdata": bsdata,
        "restart": "0",
        "userip": "219.141.178.13",
        "pm": "1" if is_ios else "2",
        "cityid": "110100",
        "rnversion": "7.1.2",
        "uuid": uuid_val,
        "usercityid": "110100",
        "facilitytype": "1" if is_ios else "2",
        "globalrefreshtest": "",
        "dataformat": "2",
        "isclickfollowuser": "1",
        "osversion": "26.6" if is_ios else "16",
        "devicemodel": "iPhone17,2" if is_ios else "V2405A",
        "devicebrand": "apple" if is_ios else "vivo",
        "devicechannel": "pvdebug",
        "firsttime": str(int(time.time() * 1000) - 86400000 * 30),
        "newuserstate": "0",
        "newuserab": "X",
        "requestnumber": "1",
        "operation": "1",
        "number": "0",
        "appexp": "",
        "pid": "100011",
        "isDegradeReq": "2",
    }
```

## High-Risk Parameters (Missing = Silent Failure)

| Parameter | Failure Mode |
|-----------|-------------|
| `appversion` | `se_version:[]` → ES matches 0 docs → strategies return empty |
| `pm` / `facilitytype` | Platform mismatch → wrong business content |
| `cityid` / `usercityid` | Geo-recall disabled → no local content |
| `uid` / `uuid` | No user profile → degrades to cold-start |
| `outmedia` / `outmedia1` / `outmedia2` | Version filtering fails |
| `operation` | Defaults to 1 (pull-down) → may return HTTP 205 |

## Pre-Script Checklist

Before generating ANY test script for `/rcm/` endpoints:

1. Does the script include ALL 35 standard parameters?
2. Is `appversion` set to a valid value (not empty)?
3. Are `pm`/`facilitytype`/`devicetype` consistent with the target platform?
4. Is `uuid` correctly constructed (`u_{uid}` for logged-in, `d_{deviceid}` for anonymous)?
5. If testing experiments, is `testNeedExp` added?
6. Is `pid` correct for the target page?
