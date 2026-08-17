#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaperJoy · 文献图表自动裁剪工具 (extract_figures.py)
====================================================
给定一篇 PDF，自动检测并裁剪其中的 Figure / Table 区域，
保存为 fig<N>.png / tbl<N>.png（与 PaperJoy 报告中的嵌入命名一致），
并打印「编号 -> 文件」清单，供 PaperJoy 在 markdown 中内联嵌入。

依赖: pymupdf  安装: pip install pymupdf
用法:
    python tools/extract_figures.py <论文.pdf> [--out .] [--dpi 200]

说明:
    - 图(Figure): 用 PDF 内嵌栅格图(page.get_image_info)定位，依邻近的
      "Figure N" 标题命名；矢量图无内嵌位图时回退到「标题上方区域」启发式。
    - 表(Table): 用版面表格检测(page.find_tables)定位，依上方 "Table N" 标题命名。
    - 自动裁剪基于版面检测，边界可能不精准，交付前请人工校对；
      未被识别或裁错时，请手动补截该图放入同目录并以 fig<N>.png / tbl<N>.png 命名。
"""
import os
import re
import sys
import json
import argparse

import pymupdf

CAP_RE = re.compile(r'^(Figure|Fig\.?|Table|Tab\.?)\s*[:.]?\s*(\d+)', re.IGNORECASE)
PAD = 4.0                # 裁剪留白 (pt)
MIN_AREA_RATIO = 0.01    # 忽略小于页面面积 1% 的图/表


def collect_captions(page):
    """返回 [(kind, num, rect), ...]  kind in {'figure','table'}"""
    caps = []
    try:
        data = page.get_text("dict")
    except Exception:
        return caps
    for block in data.get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            txt = "".join(s.get("text", "") for s in spans).strip()
            m = CAP_RE.match(txt)
            if not m:
                continue
            label = m.group(1).lower()
            kind = "figure" if label.startswith("fig") else "table"
            rect = pymupdf.Rect(line["bbox"])
            caps.append((kind, int(m.group(2)), rect))
    return caps


def nearest_caption(caps, region, kind):
    """为区域 region 找同类型、位置正确的最近标题。
    figure 标题通常在图下方；table 标题通常在表上方。"""
    best = None
    best_dist = None
    for ck, num, crect in caps:
        if ck != kind:
            continue
        if kind == "figure":
            if crect.y0 < region.y1 - 5:   # 标题应在区域下方
                continue
            dist = crect.y0 - region.y1
        else:
            if crect.y1 > region.y0 + 5:   # 标题应在区域上方
                continue
            dist = region.y0 - crect.y1
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best = (num, crect)
    return best


def crop_save(page, rect, path, scale):
    rect = pymupdf.Rect(
        rect.x0 - PAD, rect.y0 - PAD, rect.x1 + PAD, rect.y1 + PAD
    ) & page.rect
    if rect.is_empty or rect.width < 5 or rect.height < 5:
        return False
    pix = page.get_pixmap(clip=rect, matrix=pymupdf.Matrix(scale, scale))
    pix.save(path)
    return True


def unique_name(base, used):
    name = base
    i = 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    return name


def main():
    ap = argparse.ArgumentParser(description="PaperJoy 文献图表自动裁剪工具")
    ap.add_argument("pdf", help="输入 PDF 路径")
    ap.add_argument("--out", default=".", help="图表输出目录 (默认当前目录)")
    ap.add_argument("--dpi", type=int, default=200, help="裁剪图分辨率 (默认 200)")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        print(f"错误: 找不到 PDF: {args.pdf}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.out, exist_ok=True)
    scale = args.dpi / 72.0
    doc = pymupdf.open(args.pdf)

    manifest = {"figures": {}, "tables": {}, "notes": []}
    used = set()
    fig_unk = 0
    tbl_unk = 0

    for pno, page in enumerate(doc, start=1):
        parea = page.rect.width * page.rect.height
        caps = collect_captions(page)

        # ---- Figures: 内嵌栅格图 ----
        try:
            imgs = page.get_image_info()
        except Exception:
            imgs = []
        for info in imgs:
            bbox = pymupdf.Rect(info.get("bbox", (0, 0, 0, 0)))
            if bbox.is_empty:
                continue
            if (bbox.width * bbox.height) < MIN_AREA_RATIO * parea:
                continue  # 跳过图标/小装饰
            cap = nearest_caption(caps, bbox, "figure")
            if cap:
                num = cap[0]
                base = f"fig{num}"
            else:
                fig_unk += 1
                base = f"fig_unk{fig_unk}"
            name = unique_name(base, used)
            path = os.path.join(args.out, name + ".png")
            if crop_save(page, bbox, path, scale):
                manifest["figures"][name] = name + ".png"

        # ---- Figures 回退: 矢量图无内嵌位图 -> 标题上方启发式 ----
        for ck, num, crect in caps:
            if ck != "figure":
                continue
            base = f"fig{num}"
            if base in used:
                continue
            est_h = min(crect.y0, 0.45 * page.rect.height)
            region = pymupdf.Rect(crect.x0, crect.y0 - est_h, crect.x1, crect.y0)
            name = unique_name(base, used)
            path = os.path.join(args.out, name + ".png")
            if crop_save(page, region, path, scale):
                manifest["figures"][name] = name + ".png"
                manifest["notes"].append(f"{name}: 矢量图启发式裁剪(请校对编号与边界)")

        # ---- Tables ----
        try:
            tables = page.find_tables().tables
        except Exception:
            tables = []
        for t in tables:
            bbox = pymupdf.Rect(t.bbox)
            if (bbox.width * bbox.height) < MIN_AREA_RATIO * parea:
                continue
            if getattr(t, "row_count", 1) < 2:
                continue
            cap = nearest_caption(caps, bbox, "table")
            if cap:
                num = cap[0]
                base = f"tbl{num}"
            else:
                tbl_unk += 1
                base = f"tbl_unk{tbl_unk}"
            name = unique_name(base, used)
            path = os.path.join(args.out, name + ".png")
            if crop_save(page, bbox, path, scale):
                manifest["tables"][name] = name + ".png"

    # 写出 manifest
    manifest_path = os.path.join(args.out, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 人类/AI 可读摘要
    print("PaperJoy 图表自动裁剪完成:")
    for name in sorted(manifest["figures"]):
        print(f"  Figure -> {name}.png")
    for name in sorted(manifest["tables"]):
        print(f"  Table  -> {name}.png")
    if manifest["notes"]:
        print("需校对:")
        for n in manifest["notes"]:
            print(f"  - {n}")
    print(f"\nmanifest: {manifest_path}")
    print("MANIFEST_JSON:" + json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
