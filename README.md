# 证明有据：Lean 与 Rocq 图解入门

一本以 Lean 4 与 Rocq 为核心的中文图解入门书。通过共同的问题，理解命题、证明状态、等式、归纳、程序规格及证明工程。面向会读少量代码、对正确性与数学推理感兴趣的读者。

[下载 EPUB 阅读版](downloads/Lean-Rocq.epub) · [检查状态](VERIFICATION.md)

## 阅读顺序

1. [为什么还要证明](chapters/01-why-proof.md)
2. [命题、类型与证据](chapters/02-propositions-types.md)
3. [看懂证明状态](chapters/03-proof-state.md)
4. [建立工作环境](chapters/04-environment.md)
5. [第一个双语言证明](chapters/05-first-proofs.md)
6. [等式与重写](chapters/06-equality.md)
7. [自然数与归纳](chapters/07-induction.md)
8. [列表与程序性质](chapters/08-lists.md)
9. [从函数到规格](chapters/09-specification.md)
10. [搜索、自动化与库](chapters/10-libraries-automation.md)
11. [真实项目与信任](chapters/11-real-projects.md)
12. [证明工程与学习路线](chapters/12-proof-engineering.md)

附录：[阅读路线与小项目](appendices/a-reading-guide.md) · [术语与符号](appendices/b-glossary.md)

## 构建

依赖 Python 3 与 Pandoc 3；重绘图解还需要 Python 3（仅标准库）。

```bash
python3 scripts/draw_figures.py
python3 scripts/build.py
```

生成 `build/Lean-Rocq-Complete.md` 与 `build/Lean-Rocq.epub`，不会生成网站。EPUB 包含目录、全部正文与内嵌图解。分章 Markdown 引用的 SVG 在 `assets/images/`；图是原创教学示意，不是工具界面截图。

`book.json` 维护章节顺序、路径和稳定标识，后续主页可直接复用；`site/` 存放阅读站样式与搜索脚本；在线站由同一份分章 Markdown 生成。

## 检查状态

见 [VERIFICATION.md](VERIFICATION.md)。书中附有证明源码；当前交付不宣称完成 Lean 或 Rocq 编译。使用前请在自己的版本固定环境中运行对应命令。

## 工程与来源

各章在知识点附近列出来源，来源总索引见 [references/README.md](references/README.md)。Git 根提交仅含空 README，后续逐步提交规划、正文与交付工程；远端仓库：[YZYExp/Learn-Proof-Assistant](https://github.com/YZYExp/Learn-Proof-Assistant)。

## 在线阅读与 Pages CI

阅读站部署目标：https://yzyexp.github.io/Learn-Proof-Assistant/

```bash
python3 -m venv .venv
.venv/bin/pip install -r site/requirements.txt
.venv/bin/python scripts/build_site.py --base-path /Learn-Proof-Assistant/
```

输出为 `build/site`，含主页、12章、附录、资料索引、检查记录及已有 EPUB 下载。构建会校验本地链接、图片和章节锚点。支持手机目录与全文搜索。

`.github/workflows/pages.yml` 在 main 相关内容更新时自动构建并部署；PR 仅构建检查；也可手动触发。Pages 的 Source 需设为 **GitHub Actions**。网页只依赖 Python 与 Markdown，不运行 Pandoc、字体安装或 Lean/Rocq 编译；EPUB 使用已提交的阅读版，更新正文后请另外运行整书构建并更新 `downloads/Lean-Rocq.epub`。
