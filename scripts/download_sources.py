from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Print source acquisition commands for real datasets.")
    parser.add_argument("--kaggle-slug", default="elahehgolrokh/data-science-job-postings-with-salaries-2025")
    args = parser.parse_args()

    print("真实数据接入建议：")
    print()
    print("1. Kaggle职位数据")
    print("   需要先配置 Kaggle API token。")
    print(f"   kaggle datasets download -d {args.kaggle_slug} -p data/raw/kaggle --unzip")
    print()
    print("2. O*NET 30.3")
    print("   官方下载页：https://www.onetcenter.org/database.html")
    print("   建议下载 Text 或 Excel 格式，将 Software Skills、Essential Skills、Occupation Data 合并到 data/reference/")
    print()
    print("3. LinkedIn / Indeed")
    print("   使用官方/合作API、平台导出、数据供应商或学校合规数据源；不要把未授权爬虫作为默认项目路径。")
    print()
    print(f"当前项目根目录：{ROOT}")


if __name__ == "__main__":
    main()

