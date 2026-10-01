#!/usr/bin/env python3
"""Summarize CSV columns without printing cell values."""

import argparse
import csv
import io
import math
from pathlib import Path
import sys


MAX_COLUMNS = 1_000
MAX_DISPLAY_COLUMNS = 200
TYPE_ORDER = ("boolean", "number", "text")


def terminal_safe(value):
    return "".join(
        char if char.isprintable() else char.encode("unicode_escape").decode("ascii")
        for char in value
    )


def value_type(value):
    token = value.strip()
    if token.casefold() in ("true", "false"):
        return "boolean"
    try:
        number = float(token)
    except ValueError:
        return "text"
    return "number" if math.isfinite(number) else "text"


def summarize(reader):
    try:
        header = next(reader)
    except StopIteration:
        raise ValueError("文件为空，缺少标题行。")
    if not header:
        raise ValueError("标题行为空。")
    if len(header) > MAX_COLUMNS:
        raise ValueError(f"列数超过 {MAX_COLUMNS} 列上限。")

    columns = [{"blank": 0, "types": {kind: 0 for kind in TYPE_ORDER}} for _ in header]
    rows = 0
    mismatched_rows = 0
    for row in reader:
        rows += 1
        if len(row) != len(header):
            mismatched_rows += 1
        for index, column in enumerate(columns):
            value = row[index] if index < len(row) else ""
            if not value.strip():
                column["blank"] += 1
            else:
                column["types"][value_type(value)] += 1

    print(f"数据行：{rows} · 列：{len(header)} · 列数不符的行：{mismatched_rows}")
    for index, (name, column) in enumerate(zip(header, columns[:MAX_DISPLAY_COLUMNS]), 1):
        label = terminal_safe(name[:120]) or "（无名列）"
        if len(name) > 120:
            label += "…"
        detail = " · ".join(
            f"{kind} {count}"
            for kind, count in column["types"].items()
            if count
        ) or "无非空值"
        print(f"{index}. {label} · 空值 {column['blank']} · {detail}")
    if len(header) > MAX_DISPLAY_COLUMNS:
        print(f"…另有 {len(header) - MAX_DISPLAY_COLUMNS} 列未显示。")


def main(argv=None):
    parser = argparse.ArgumentParser(description="查看 CSV 列结构，不输出单元格内容。")
    parser.add_argument("source", nargs="?", default="-", help="逗号分隔 CSV 文件；省略时从标准输入读取")
    args = parser.parse_args(argv)

    stream = None
    close_stream = False
    try:
        if args.source == "-":
            stream = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8-sig", newline="")
        else:
            stream = Path(args.source).open("r", encoding="utf-8-sig", newline="")
            close_stream = True
        summarize(csv.reader(stream, strict=True))
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"csv-shape: {terminal_safe(str(error))}", file=sys.stderr)
        return 2
    finally:
        if close_stream:
            stream.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
