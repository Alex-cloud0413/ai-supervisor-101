"""拉取《给 AI 当监工》配套实战项目 `ai-radar` 的公开练习数据快照。

两个数据源均为官方免 Key 公开接口，无需登录、不含任何私人信息：
1. OpenRouter 模型目录与价格表：https://openrouter.ai/api/v1/models
2. Hacker News 首页热门讨论（Algolia 官方公开索引）：https://hn.algolia.com/api/v1/search?tags=front_page

运行方式：
    python3 practice/scripts/fetch_snapshots.py
"""

import json
import urllib.request
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

SOURCES = {
    "openrouter-models": "https://openrouter.ai/api/v1/models",
    "hn-frontpage": "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30",
}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-supervisor-101/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    for prefix, url in SOURCES.items():
        payload = fetch_json(url)
        out_path = DATA_DIR / f"{prefix}-{today}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved {out_path} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
