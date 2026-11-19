"""生成「青禾文具」虚构练习数据。

所有公司、客户、人名均为虚构。运行方式：
    python practice/scripts/make_data.py
会在 practice/data/ 下生成三个月的销售 Excel。
"""

import random
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook

random.seed(20261119)  # 固定随机种子，保证每次生成的数据一样

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "sales"

PRODUCTS = {
    "中性笔（黑，12支装）": 18.0,
    "A4 复印纸（500张）": 26.5,
    "订书机（中号）": 35.0,
    "文件夹（10个装）": 22.0,
    "便利贴（6本装）": 15.5,
    "白板笔（4色）": 19.9,
}

CUSTOMERS = [
    "城南第三小学",
    "星澜广告有限公司",
    "启明会计师事务所",
    "绿洲物业管理处",
    "远航外贸有限公司",
    "晨曦培训中心",
]

SALES_REPS = ["小林", "阿杰", "王姐"]


def month_rows(year: int, month: int, n: int):
    first = date(year, month, 1)
    rows = []
    for i in range(n):
        day = first + timedelta(days=random.randint(0, 27))
        product, price = random.choice(list(PRODUCTS.items()))
        qty = random.choice([5, 10, 10, 20, 30, 50])
        rows.append(
            [
                day.isoformat(),
                f"QH{year}{month:02d}{i + 1:03d}",
                random.choice(CUSTOMERS),
                product,
                qty,
                price,
                round(qty * price, 2),
                random.choice(SALES_REPS),
            ]
        )
    rows.sort(key=lambda r: r[0])
    return rows


def write_month(year: int, month: int, n: int, amount_header: str = "金额"):
    wb = Workbook()
    ws = wb.active
    ws.title = "销售明细"
    ws.append(["日期", "订单号", "客户", "产品", "数量", "单价", amount_header, "销售员"])
    for row in month_rows(year, month, n):
        ws.append(row)
    for col, width in zip("ABCDEFGH", [12, 14, 18, 22, 8, 8, 10, 8]):
        ws.column_dimensions[col].width = width
    path = DATA_DIR / f"{year}-{month:02d}-销售明细.xlsx"
    wb.save(path)
    return path


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(write_month(2026, 8, 24))
    print(write_month(2026, 9, 27))
    # 10 月的表由另一位同事整理，金额列叫「销售额」——后面的课会用到这个差异
    print(write_month(2026, 10, 31, amount_header="销售额"))
