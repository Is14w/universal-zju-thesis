# 浙江大学毕业设计论文模板 | Zhejiang University Bachelor Thesis Typst Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个优雅、易用的浙江大学本科毕业设计论文 Typst 模板，遵循学校官方格式要求。

> 本项目基于 [universal-jlu-thesis](https://github.com/Islatri/universal-jlu-thesis) 修改而来，将吉林大学毕业设计论文模板适配为浙江大学本科毕业论文（设计）格式。

> **警告：本模板为民间开源项目**，非官方出品，使用前请了解：
>
> - 模板可能不被学校认可
> - 正式提交时，请务必**提前验证格式是否符合要求**
> - 建议保持源文件备份，以便随时转换至 Word 或 LaTeX

**请务必注意：**封面、原创性声明（签名 + 日期）、授权书（作者签名 + 导师签名 + 日期）等内容模板无法自动生成，请自行用 Word 编辑后导出为 PDF，再使用 `tools/merge.py` 拼接到正文中。

我本人并不是ZJU的学生，因此也不会过分维护这个项目。欢迎Fork和PR来完善，或者如果你有更好的解决方案，也欢迎分享。

## 关于本项目

[Typst](https://typst.app/) 是使用 Rust 语言开发的全新文档排版系统，具有 Markdown 级别的简洁语法和 LaTeX 级别的专业排版能力。

**universal-zju-thesis** 是基于 [universal-jlu-thesis](https://github.com/Islatri/universal-jlu-thesis) 修改的浙江大学本科毕业论文（设计）Typst 模板，遵循浙江大学官方的格式要求。

## 快速开始

### 前置要求

安装 Typst 0.14.0 或更高版本：

- [Typst GitHub Releases](https://github.com/typst/typst/releases/)
- Scoop: `scoop install typst`
- Homebrew (macOS): `brew install typst`

### 克隆仓库

```bash
git clone https://github.com/Is14w/universal-zju-thesis.git
cd universal-zju-thesis
typst compile thesis.typ --root ./
```

### 实时预览

推荐使用 VS Code + [Tinymist Typst](https://marketplace.visualstudio.com/items?itemName=myriad-dreamin.tinymist) 插件：

```bash
typst watch thesis.typ --root ./
```

## 基本使用流程

1. 克隆仓库
2. 修改 `thesis.typ` 中的论文基本信息（标题、作者、指导教师等）
3. 按照示例格式编写各章节内容
4. 在 `works/refs.bib` 中添加参考文献
5. 运行编译命令生成 PDF

`tools` 目录下包含了一个 Python 脚本 `CalculateChineseCharacters.py`，用于统计论文中中文字符的数量。你可以通过以下命令运行该脚本：

```bash
./tools/Calculate.cmd

// 或者在 Linux/macOS 上
./tools/Calculate.sh
```

通常来说，毕业论文的中文字符要求为 20000 字以上（不包括空格和标点符号）。你可以使用这个工具来检查你的论文是否满足这一要求。

## 拼接封面 / 声明 / 授权页

模板不包含封面、原创性声明和授权书（这些需要手写签名），你需要：

1. 用 Word 编辑好封面、声明、授权书，分别导出为 PDF
2. 用 `tools/merge.py` 将它们拼接到 Typst 编译的正文 PDF 中

### 用法

```bash
pip install pypdf  # 一次性安装依赖
```

```bash
# 封面第 1 页插入到最前面 (after 0 表示最前面)
python tools/merge.py thesis.pdf --after 0 cover.pdf:1

# 完整拼接：封面 → 声明 → 授权书 → 正文
python tools/merge.py thesis.pdf \
  --after 0 cover.pdf:1 \
  --after 1 declaration.pdf \
  --after 2 authorization.pdf \
  -o thesis-final.pdf

# 同时删除正文第 3、7 页，正文只取 1-80 页
python tools/merge.py thesis.pdf \
  --after 0 cover.pdf:1 \
  --drop 3,7 \
  --body-pages 1-80 \
  -o final.pdf
```

`--after N FILE[:PAGES]` 中的 `PAGES` 指定取文件的哪几页（如 `3-5` 或 `3`），省略则取全部页。

也提供了脚本包装：

- **Windows**: `tools\merge.cmd`
- **macOS / Linux**: `bash tools/merge.sh`

## 文件结构

```
universal-zju-thesis/
├── core/                    # 核心模板文件
│   ├── template.typ         # 主模板定义
│   ├── fonts.typ            # 字体配置
│   ├── abstract.typ         # 摘要页
│   ├── toc.typ              # 目录
│   ├── bibliography.typ     # 参考文献
│   └── utils.typ            # 工具函数
├── works/                   # 资源文件
│   ├── assets/              # 图片资源
│   ├── refs.bib             # 参考文献数据库
│   └── gbt-7714-2015-numeric.csl  # 参考文献 CSL 样式
├── thesis.typ               # 论文主文件（模板实例）
├── lib.typ                  # 库入口文件
├── typst.toml               # Typst 包配置
├── thumbnail.png            # 缩略图
└── README.md
```

## 格式规范

### 字号对照

| 论文部分   | 字号   | 字体              | pt 值  | 格式       |
| ---------- | ------ | ----------------- | ------ | ---------- |
| 章标题     | 三号   | 仿宋加黑          | 16pt   | 左对齐     |
| 节标题     | 小三号 | 仿宋加黑          | 15pt   | 左对齐     |
| 条标题     | 四号   | 仿宋加黑          | 14pt   | 左对齐     |
| 正文       | 小四号 | 仿宋              | 12pt   | 1.5 倍行距 |
| 图/表标题  | 五号   | 宋体加黑          | 10.5pt | 居中       |
| 表格内容   | 五号   | 宋体              | 10.5pt | 单倍行距   |
| 页眉       | 小五号 | 宋体              | 9pt    |            |

### 三线表

- 顶线：1.5pt 粗
- 表头-数据分隔线：0.5pt 细
- 底线：1.5pt 粗
- 列间：0.5pt 细竖线
- 无左右外侧边线

## 依赖

- **Typst** 0.14.0 或更高版本

### 字体依赖

为获得最佳排版效果，建议安装以下字体：

- **FangSong**（仿宋）- 正文字体
- **SimSun**（宋体）- 图表标题/内容字体
- **SimHei**（黑体）- 目录标题字体
- **Times New Roman** - 英文字体

## 致谢

- 感谢 [universal-jlu-thesis](https://github.com/Islatri/universal-jlu-thesis) 为本模板提供基础框架，本项目系在其基础上修改而来
- 感谢 [universal-hit-thesis](https://github.com/hitszosa/universal-hit-thesis) 为原始模板的设计思路提供启发
- 感谢浙江大学提供的官方论文格式规范文档

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](./LICENSE) 文件。

---

**如果这个项目对你有帮助，请考虑给个 Star 来支持我们！**
