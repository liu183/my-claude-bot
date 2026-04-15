# 网文章节分析器

## 项目简介

本项目用于深度分析都市神医、乡村神医类网文的前100章内容，通过多Agent协作系统提取关键创作素材，包括：
- 剧情主线和支线结构
- 后宫人物设计和关系网络
- 创作风格特征
- 创作模板和套路总结

## 项目结构

```
novel-analysis-chapter-analyzer/
├── agents/                 # AI代理配置
│   ├── plot-analyzer.md  # 剧情分析代理
│   ├── character-analyzer.md  # 人物分析代理
│   ├── style-analyzer.md # 风格分析代理
│   └── summarizer.md     # 汇总生成代理
├── src/                   # 源代码
│   ├── text-preprocessor.py  # 文本预处理
│   ├── chapter-splitter.py   # 章节分割
│   ├── multi-agent.py       # 多Agent协调器
│   └── template-generator.py # 模板生成器
├── analysis-results/       # 分析结果
│   ├── [小说名]/          # 各小说独立分析目录
└── docs/                  # 项目文档
    ├── setup.md           # 安装配置
    └── usage.md          # 使用说明
```

## 快速开始

1. 确保Python 3.9+环境已安装
2. 安装依赖：`pip install -r requirements.txt`
3. 运行分析：`python src/analyze-novel.py --path "D:\迅雷下载\筛检版\小说名.txt"`

## 分析流程

1. **文本预处理** - 清理文本、编码转换
2. **章节分割** - 按章节分割文本
3. **多Agent并行分析** - 每章分配给专门Agent分析
4. **全局结构化** - 整合所有章节数据
5. **模板生成** - 输出创作素材模板

## 输出格式

每部小说生成：
- `main_plot.md` - 剧情主线分析
- `sub_plots.md` - 支线剧情汇总
- `characters.md` - 后宫人物图谱
- `style_guide.md` - 创作风格指南
- `template.md` - 创作模板总结

---
*项目创建: 2026-04-15*
*作者: Claude Opus 4.6*