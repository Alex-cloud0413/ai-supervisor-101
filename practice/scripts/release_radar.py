"""《给 AI 当监工》M6 毕业项目参考脚本：追踪关注开源仓库的最新 GitHub Release 动态。

读取：
  - practice/release-radar.yaml（仓库清单、超时秒数与输出文件名）
输出：
  - practice/output/release-radar.md

特点：
  - 严格遵循 practice/AGENTS.md：仅使用 Python 标准库（urllib.request / xml.etree.ElementTree）
    + 已有依赖 PyYAML，不新增第三方库、不触碰 practice/data/ 原始快照；
  - 优先调用 GitHub 公开 API；若遇到公司共享 IP 403 限流且未配置 GITHUB_TOKEN，
    自动降级读取 GitHub 官方公开 Atom 订阅源（/releases.atom），确保免 Key 也能稳定跑通；
  - 网络超时或 404 时优雅跳过并写入清晰中文提示，绝不中断主流程。

运行方式：
  python3 practice/scripts/release_radar.py
"""

import json
import os
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "release-radar.yaml"
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def load_config(path: Path) -> dict:
    """读取 YAML 配置文件。"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_from_atom(repo: str, timeout: int = 10) -> dict | None:
    """兜底方案：从 GitHub 官方公开 releases.atom 订阅源读取最新版本（免 Token、不占 API 限额）。"""
    url = f"https://github.com/{repo}/releases.atom"
    req = urllib.request.Request(url, headers={"User-Agent": "ai-radar-supervisor-101/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            root = ET.fromstring(resp.read())
            entry = root.find("a:entry", ATOM_NS)
            if entry is None:
                return {"repo": repo, "ok": False, "error": "仓库暂无公开 Release"}
            title = (entry.findtext("a:title", default="", namespaces=ATOM_NS) or "").strip()
            updated = (entry.findtext("a:updated", default="", namespaces=ATOM_NS) or "")[:10] or "未知日期"
            link_el = entry.find("a:link", ATOM_NS)
            href = link_el.attrib.get("href", "") if link_el is not None else ""
            tag = href.rstrip("/").split("/")[-1] if "/releases/tag/" in href else (title or "未标版本号")
            return {
                "repo": repo,
                "ok": True,
                "tag": tag,
                "published_at": updated,
                "note": "Atom 公开源",
                "url": href or f"https://github.com/{repo}/releases",
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"repo": repo, "ok": False, "error": "仓库不存在或暂无公开 Release（404）"}
        return None
    except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError):
        return None


def fetch_latest_release(repo: str, timeout: int = 10) -> dict:
    """拉取单个 GitHub 仓库的最新 Release（API 优先，403 限流时自动切官方 Atom 源）。"""
    headers = {
        "User-Agent": "ai-radar-supervisor-101/1.0",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token and not token.startswith("your_"):
        headers["Authorization"] = f"Bearer {token}"

    endpoints = [
        f"https://api.github.com/repos/{repo}/releases/latest",
        f"https://api.github.com/repos/{repo}/releases?per_page=1",
    ]
    last_error = "未知异常"
    for idx, url in enumerate(endpoints):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                item = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else None)
                if not item:
                    return {"repo": repo, "ok": False, "error": "仓库暂无公开 Release"}
                pub = (item.get("published_at") or "")[:10] or "未知日期"
                badge = "预发布" if item.get("prerelease") else "正式版"
                return {
                    "repo": repo,
                    "ok": True,
                    "tag": item.get("tag_name") or "未标版本号",
                    "published_at": pub,
                    "note": badge,
                    "url": item.get("html_url") or f"https://github.com/{repo}/releases",
                }
        except urllib.error.HTTPError as e:
            if e.code == 404 and idx == 0:
                continue
            if e.code == 403:
                atom_res = fetch_from_atom(repo, timeout=timeout)
                if atom_res is not None:
                    return atom_res
                last_error = "GitHub API 限流（403），可在本地 .env 配置 GITHUB_TOKEN 提额"
            elif e.code == 404:
                last_error = "仓库不存在或尚未发布任何 Release（404）"
            else:
                last_error = f"HTTP 接口异常（{e.code}）"
            break
        except (urllib.error.URLError, TimeoutError, OSError):
            last_error = "网络超时或无法访问 GitHub，已跳过"
            break
    return {"repo": repo, "ok": False, "error": last_error}


def render_markdown(results: list[dict]) -> str:
    """把各仓库最新版本拼成 Markdown 追踪简报。"""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ok_count = sum(1 for r in results if r["ok"])
    lines = [
        "# ai-radar 开源工具最新版本追踪",
        "",
        f"> 采集时间：`{now_str}` ｜ 配置来源：`release-radar.yaml` ｜ 成功 `{ok_count}/{len(results)}`",
        "",
        "| 仓库 | 最新版本 | 发布日期 | 来源 / 状态 |",
        "|---|---|---|---|",
    ]
    for r in results:
        if r["ok"]:
            lines.append(
                f"| `{r['repo']}` | [`{r['tag']}`]({r['url']}) | {r['published_at']} | {r['note']} |"
            )
        else:
            lines.append(f"| `{r['repo']}` | — | — | ⚠️ {r['error']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cfg = load_config(CONFIG_PATH)
    repos = cfg.get("repos") or []
    timeout = int(cfg.get("timeout_seconds", 10))
    out_dir = BASE_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / cfg.get("output_file", "release-radar.md")

    results = [fetch_latest_release(repo, timeout=timeout) for repo in repos]
    out_path.write_text(render_markdown(results), encoding="utf-8")
    ok_count = sum(1 for r in results if r["ok"])
    print(f"已生成开源版本追踪简报：{out_path.relative_to(BASE_DIR)}（成功 {ok_count}/{len(results)}）")


if __name__ == "__main__":
    main()
