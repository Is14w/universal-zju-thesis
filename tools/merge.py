"""拼接 ZJU 毕业论文 PDF —— 将指定 PDF 的指定页插入到正文的指定位置。"""

import argparse
from pathlib import Path

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("需要安装 pypdf: pip install pypdf")
    raise


def parse_range(s: str) -> tuple[int, int | None]:
    """解析页码范围 '3-5' / '3-' / '3'。页码从 1 开始。"""
    s = s.strip()
    if "-" in s:
        parts = s.split("-", 1)
        start = int(parts[0]) if parts[0] else 1
        end = int(parts[1]) if parts[1] else None
        return start, end
    else:
        p = int(s)
        return p, p


def parse_page_set(s: str) -> set[int]:
    """解析 '1,3,5-7' 形式的页码集合。"""
    pages: set[int] = set()
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        else:
            pages.add(int(part))
    return pages


def parse_insert_spec(s: str) -> tuple[Path, tuple[int, int | None]]:
    """解析 'file.pdf:3-5' 或 'file.pdf:3' 或 'file.pdf'。"""
    if ":" in s:
        path_str, range_str = s.rsplit(":", 1)
        rng = parse_range(range_str)
    else:
        path_str = s
        rng = (1, None)  # 默认全部页
    return Path(path_str), rng


def add_pages_from_range(writer: PdfWriter, path: Path, start: int, end: int | None) -> int:
    """将 PDF [start, end] 页加入 writer，返回实际添加页数。"""
    reader = PdfReader(str(path))
    total = len(reader.pages)
    end = end or total
    count = 0
    for i in range(start, end + 1):
        if 1 <= i <= total:
            writer.add_page(reader.pages[i - 1])
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="拼接 PDF —— 从 A 取第 X-Y 页，插入到正文第 N 页之后",
    )
    parser.add_argument(
        "body",
        type=Path,
        help="正文 PDF（Typst 编译输出）",
    )
    parser.add_argument(
        "--after",
        type=str,
        nargs=2,
        action="append",
        default=[],
        metavar=("N", "FILE[:PAGES]"),
        help="将 FILE 的指定页插入到正文第 N 页之后 (N=0 表示最前面)。"
             " PAGES 如 '3-5' 或 '3'，省略则取全部。"
             " 可多次使用。",
    )
    parser.add_argument(
        "--drop",
        type=str,
        metavar="PAGES",
        help="从正文中删除的页，如 '1,3,5-7'",
    )
    parser.add_argument(
        "--body-pages",
        type=str,
        metavar="RANGE",
        help="正文保留的页码范围，如 '1-50'",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("thesis-final.pdf"),
        help="输出文件路径 (默认: thesis-final.pdf)",
    )

    args = parser.parse_args()

    if not args.body.exists():
        parser.error(f"正文 PDF 不存在: {args.body}")

    # ---- 收集插入操作，按 after 位置排序 ----
    inserts: list[tuple[int, Path, tuple[int, int | None]]] = []
    for n_str, spec in args.after:
        n = int(n_str)
        fpath, rng = parse_insert_spec(spec)
        if not fpath.exists():
            parser.error(f"文件不存在: {fpath}")
        inserts.append((n, fpath, rng))
    inserts.sort(key=lambda x: x[0])  # 按插入位置排序

    # ---- 构建最终 PDF ----
    writer = PdfWriter()

    # 确定正文要保留的页
    body_reader = PdfReader(str(args.body))
    body_total = len(body_reader.pages)

    if args.body_pages:
        body_start, body_end = parse_range(args.body_pages)
        body_end = body_end or body_total
    else:
        body_start, body_end = 1, body_total

    # 要删除的页
    drop_set: set[int] = set()
    if args.drop:
        drop_set = parse_page_set(args.drop)

    # 按顺序处理：正文页 → 到达 after 位置时插入
    insert_idx = 0
    page_num = 0  # 当前已写入的页数（用于定位 after）

    for i in range(body_start, body_end + 1):
        if i < 1 or i > body_total:
            continue
        if i in drop_set:
            print(f"  跳过正文第 {i} 页")
            continue

        # 在当前正文页之前，先处理所有 after < 当前页号的插入
        while insert_idx < len(inserts) and inserts[insert_idx][0] < i:
            n, fpath, rng = inserts[insert_idx]
            start, end = rng
            print(f"插入: {fpath.name} 第 {start}-{end or '末'} 页 → 正文第 {n} 页之后")
            cnt = add_pages_from_range(writer, fpath, start, end)
            page_num += cnt
            insert_idx += 1

        writer.add_page(body_reader.pages[i - 1])
        page_num += 1

        # 处理 after == 当前页号的插入
        while insert_idx < len(inserts) and inserts[insert_idx][0] == i:
            n, fpath, rng = inserts[insert_idx]
            start, end = rng
            print(f"插入: {fpath.name} 第 {start}-{end or '末'} 页 → 正文第 {n} 页之后")
            cnt = add_pages_from_range(writer, fpath, start, end)
            page_num += cnt
            insert_idx += 1

    # 处理 remaining inserts（after 可能在最后一页之后）
    while insert_idx < len(inserts):
        n, fpath, rng = inserts[insert_idx]
        start, end = rng
        print(f"插入: {fpath.name} 第 {start}-{end or '末'} 页 → 正文第 {n} 页之后")
        cnt = add_pages_from_range(writer, fpath, start, end)
        page_num += cnt
        insert_idx += 1

    writer.write(str(args.output))
    print(f"\n已生成: {args.output}  ({len(writer.pages)} 页)")


if __name__ == "__main__":
    main()
