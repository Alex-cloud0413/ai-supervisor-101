"""《给 AI 当监工》M3–M5 参考脚本：读取 config.yaml，融合 OpenRouter 与 Hacker News 快照生成每日 AI 简报。

读取：
  - practice/config.yaml
  - practice/data/openrouter-models-2026-11-24.json
  - practice/data/hn-frontpage-2026-11-24.json
输出：
  - practice/output/daily-briefing.md

运行方式：
  python3 practice/scripts/daily_briefing.py
"""

import json
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config.yaml"


def load_config(config_path: Path) -> dict:
    """读取 YAML 配置文件。"""
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def pick_cheapest_vision_models(data_path: Path, cfg: dict) -> list[dict]:
    """按 config.yaml 的 model_pricing 口径筛出性价比最高的实时多模态对话模型。"""
    with data_path.open("r", encoding="utf-8") as f:
        models = json.load(f).get("data", [])

    rate = float(cfg["exchange_rate"])
    prefixes = tuple(cfg.get("exclude_prefixes") or [])
    suffixes = tuple(cfg.get("exclude_suffixes") or [])
    top_n = int(cfg.get("top_n", 5))

    rows = []
    for m in models:
        mid = m.get("id", "")
        if prefixes and mid.startswith(prefixes):
            continue
        if any(s in mid for s in suffixes):
            continue

        arch = m.get("architecture") or {}
        inputs = arch.get("input_modalities") or []
        outputs = arch.get("output_modalities") or []
        if "image" not in inputs or outputs != ["text"]:
            continue

        pricing = m.get("pricing") or {}
        try:
            p_usd = float(pricing.get("prompt") or 0)
            c_usd = float(pricing.get("completion") or 0)
        except (ValueError, TypeError):
            continue
        if p_usd <= 0 or c_usd <= 0:
            continue

        p_cny = p_usd * 1_000_000 * rate
        c_cny = c_usd * 1_000_000 * rate
        rows.append({
            "id": mid,
            "prompt_cny": p_cny,
            "completion_cny": c_cny,
            "avg_cny": (p_cny + c_cny) / 2.0,
        })

    rows.sort(key=lambda x: (x["avg_cny"], x["prompt_cny"]))
    return rows[:top_n]


def pick_hn_ai_stories(data_path: Path, cfg: dict) -> list[dict]:
    """按 config.yaml 的 keywords 与 min_points 筛出高热 AI 讨论。"""
    with data_path.open("r", encoding="utf-8") as f:
        hits = json.load(f).get("hits", [])

    min_points = int(cfg.get("min_points", 50))
    max_items = int(cfg.get("max_items", 8))
    keywords = [k.lower() for k in (cfg.get("keywords") or [])]

    matched = []
    for item in hits:
        title = item.get("title") or ""
        points = int(item.get("points") or 0)
        if points < min_points:
            continue
        if any(k in title.lower() for k in keywords):
            matched.append({
                "title": title,
                "points": points,
                "comments": int(item.get("num_comments") or 0),
                "url": item.get("url") or f"https://news.ycombinator.com/item?id={item.get('objectID', '')}",
            })

    matched.sort(key=lambda x: x["points"], reverse=True)
    return matched[:max_items]


def render_markdown(models: list[dict], stories: list[dict], cfg: dict) -> str:
    """把结果拼装成 Markdown 每日早报。"""
    rate = cfg["model_pricing"]["exchange_rate"]
    min_pts = cfg["daily_briefing"]["min_points"]

    lines = [
        "# ai-radar 每日 AI 选型与情报简报",
        "",
        f"> 口径来源：`config.yaml`（汇率 `1 USD = {rate} RMB`，HN 热度门槛 `>= {min_pts}` 分）",
        "",
        f"## 一、商用实时多模态低价 Top {len(models)}（每百万 Token）",
        "",
        "| 排名 | 模型 ID | 输入价 (¥/M) | 输出价 (¥/M) | 综合均价 (¥/M) |",
        "|---|---|---|---|---|",
    ]
    for rank, m in enumerate(models, start=1):
        lines.append(
            f"| {rank} | `{m['id']}` | ¥{m['prompt_cny']:.4f} | ¥{m['completion_cny']:.4f} | ¥{m['avg_cny']:.4f} |"
        )

    lines.extend([
        "",
        f"## 二、Hacker News 首页 AI 热点（命中 {len(stories)} 条）",
        "",
    ])
    for idx, s in enumerate(stories, start=1):
        lines.append(f"{idx}. **[{s['title']}]({s['url']})**（{s['points']} 分 · {s['comments']} 条讨论）")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cfg = load_config(CONFIG_PATH)
    data_dir = BASE_DIR / cfg["project"]["data_dir"]
    output_dir = BASE_DIR / cfg["project"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    models = pick_cheapest_vision_models(
        data_dir / cfg["model_pricing"]["snapshot_file"],
        cfg["model_pricing"],
    )
    stories = pick_hn_ai_stories(
        data_dir / cfg["daily_briefing"]["snapshot_file"],
        cfg["daily_briefing"],
    )

    out_path = output_dir / cfg["daily_briefing"]["output_file"]
    out_path.write_text(render_markdown(models, stories, cfg), encoding="utf-8")
    print(f"已按 config.yaml 生成简报：{out_path.relative_to(BASE_DIR)}（模型 {len(models)} 条，HN 热点 {len(stories)} 条）")


if __name__ == "__main__":
    main()
