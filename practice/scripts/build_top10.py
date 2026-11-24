"""《给 AI 当监工》M2 参考脚本：从 OpenRouter 公开快照筛选「商用实时付费多模态 Top 10」。

读取：practice/data/openrouter-models-2026-11-24.json（原始快照，只读不改）
输出：practice/output/模型比价Top10.xlsx

运行方式：
    python3 practice/scripts/build_top10.py
"""

import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# 1. 顶部配置变量（监工最常核对、改动的一块）
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "openrouter-models-2026-11-24.json"
OUTPUT_PATH = BASE_DIR / "output" / "模型比价Top10.xlsx"
EXCHANGE_RATE = 7.2
TOP_N = 10


def load_models(json_path: Path) -> list[dict]:
    """读取 JSON 快照，返回模型字典列表。"""
    with json_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return raw_data.get("data", [])


def is_valid_chat_vision_model(model: dict) -> bool:
    """判断单个模型是否符合「支持看图 + 纯文字对话 + 商用实时付费」口径。"""
    model_id = model.get("id", "")

    # 规则 1：排除 ~ 动态别名、:free 免费版、:batch 离线批处理版
    if model_id.startswith("~"):
        return False
    if ":free" in model_id or ":batch" in model_id:
        return False

    # 规则 2：输入必须支持图片
    arch = model.get("architecture") or {}
    inputs = arch.get("input_modalities") or []
    outputs = arch.get("output_modalities") or []
    modality = arch.get("modality") or ""
    if ("image" not in inputs) and ("image->" not in modality):
        return False

    # 规则 3：输出必须是纯文字（排除输出含 audio 的音乐生成模型，如 lyria-3）
    if outputs != ["text"]:
        return False

    # 规则 4：输入价和输出价都必须大于 0（排除 -1 动态路由和 0 免费项）
    pricing = model.get("pricing") or {}
    try:
        prompt_usd = float(pricing.get("prompt") or 0)
        completion_usd = float(pricing.get("completion") or 0)
    except (ValueError, TypeError):
        return False

    if prompt_usd <= 0 or completion_usd <= 0:
        return False

    return True


def calc_cny_pricing(model: dict, exchange_rate: float) -> dict:
    """把每 Token 美元字符串折算为每百万 Token 的人民币单价与综合均价。"""
    pricing = model.get("pricing") or {}
    arch = model.get("architecture") or {}

    prompt_usd_m = float(pricing["prompt"]) * 1_000_000
    completion_usd_m = float(pricing["completion"]) * 1_000_000
    prompt_cny_m = prompt_usd_m * exchange_rate
    completion_cny_m = completion_usd_m * exchange_rate
    avg_cny_m = (prompt_cny_m + completion_cny_m) / 2.0

    return {
        "id": model["id"],
        "name": model.get("name") or model["id"],
        "context_length": model.get("context_length") or 0,
        "prompt_usd": prompt_usd_m,
        "completion_usd": completion_usd_m,
        "prompt_cny": prompt_cny_m,
        "completion_cny": completion_cny_m,
        "avg_cny": avg_cny_m,
        "input_modalities": ", ".join(arch.get("input_modalities") or []),
    }


def select_top_models(
    models: list[dict],
    exchange_rate: float = EXCHANGE_RATE,
    top_n: int = TOP_N,
) -> list[dict]:
    """批量筛选、算价并按综合均价从低到高取前 N 名。"""
    qualified = []
    for model in models:
        if not is_valid_chat_vision_model(model):
            continue
        qualified.append(calc_cny_pricing(model, exchange_rate))

    qualified.sort(key=lambda item: (item["avg_cny"], item["prompt_cny"], item["completion_cny"]))
    return qualified[:top_n]


def save_excel(top_models: list[dict], output_path: Path, exchange_rate: float = EXCHANGE_RATE) -> None:
    """把筛选结果写成带基础样式的 Excel 比价表。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "商用实时付费Top10"

    header_font = Font(name="Microsoft YaHei", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    ws.merge_cells("A1:J1")
    ws["A1"] = f"OpenRouter 支持图片输入大模型比价表 - 商用实时付费 Top {len(top_models)} (汇率 1 USD = {exchange_rate} RMB)"
    ws["A1"].font = Font(name="Microsoft YaHei", size=13, bold=True, color="1F4E79")
    ws.row_dimensions[1].height = 30

    headers = [
        "排名", "模型 ID", "模型名称", "上下文窗口",
        "输入价 ($/M)", "输出价 ($/M)",
        "输入价 (¥/M)", "输出价 (¥/M)", "综合均价 (¥/M)",
        "支持输入模态",
    ]
    ws.row_dimensions[2].height = 24
    for col_idx, text in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_idx, value=text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    for rank, item in enumerate(top_models, start=1):
        row_num = rank + 2
        values = [
            rank,
            item["id"],
            item["name"],
            item["context_length"],
            item["prompt_usd"],
            item["completion_usd"],
            item["prompt_cny"],
            item["completion_cny"],
            item["avg_cny"],
            item["input_modalities"],
        ]
        for col_idx, val in enumerate(values, start=1):
            cell = ws.cell(row=row_num, column=col_idx, value=val)
            cell.border = thin_border
            if col_idx == 4:
                cell.number_format = "#,##0"
            elif col_idx in (5, 6):
                cell.number_format = "$#,##0.0000"
            elif col_idx in (7, 8, 9):
                cell.number_format = "¥#,##0.0000"

    col_widths = {"A": 8, "B": 38, "C": 32, "D": 14, "E": 15, "F": 15, "G": 15, "H": 15, "I": 16, "J": 22}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    wb.save(output_path)


def main() -> None:
    models = load_models(DATA_PATH)
    top_models = select_top_models(models, exchange_rate=EXCHANGE_RATE, top_n=TOP_N)
    save_excel(top_models, OUTPUT_PATH, exchange_rate=EXCHANGE_RATE)

    print(f"已读取 {len(models)} 个模型，筛出前 {len(top_models)} 名，保存至 {OUTPUT_PATH.relative_to(BASE_DIR)}")
    for rank, item in enumerate(top_models[:5], start=1):
        print(
            f"Top {rank}: {item['id']} | "
            f"综合均价 ¥{item['avg_cny']:.4f}/M "
            f"(输入 ¥{item['prompt_cny']:.4f} / 输出 ¥{item['completion_cny']:.4f})"
        )


if __name__ == "__main__":
    main()
