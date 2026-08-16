#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaperJoy 单一信息源构建脚本
================================
SKILL.md 是唯一手工维护的文件（含 WorkBuddy 所需的 YAML frontmatter）。
本脚本剥离 frontmatter，拼上「通用提示词版」声明头，生成 PROMPT.md。

PROMPT.md 因此成为**派生产物**，不进版本跟踪（见 .gitignore），
仅在 Release 打包时由本脚本生成后随 zip 分发，彻底消除两份核心文件的重复维护。

用法：
    python tools/build_prompt.py
依赖：Python 3，无第三方依赖。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL = os.path.join(ROOT, "SKILL.md")
OUT = os.path.join(ROOT, "PROMPT.md")

HEADER = """# PaperJoy（学术文献深刻剖析系统）· 通用提示词版

> ⚠️ 本文件由 `SKILL.md` 经 `tools/build_prompt.py` **自动生成**，请勿手动编辑；
> 改 `SKILL.md` 后运行 `python tools/build_prompt.py` 重新生成即可。
> 把它设为任意 AI 助手（WorkBuddy、Claude、ChatGPT、Cursor、Gemini 等）的系统指令 / 自定义指令，
> AI 会严格按下方七模块流程剖析你贴入的文献。

---
"""


def extract_body(text: str) -> str:
    """剥离开头的 YAML frontmatter（--- ... ---），返回正文。"""
    if text.startswith("---"):
        # 找到第二个 '---' 行（frontmatter 结束符）
        m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
        if m:
            return text[m.end():]
    return text


def main():
    with open(SKILL, "r", encoding="utf-8") as f:
        src = f.read()
    body = extract_body(src).lstrip("\n")
    out = HEADER + body
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"generated: {os.path.relpath(OUT, ROOT)}  ({len(out)} chars)")


if __name__ == "__main__":
    main()
