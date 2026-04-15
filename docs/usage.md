# 使用说明

## 快速开始

### 分析单本小说

```bash
# 基础用法
python src/analyze-novel.py "D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt"

# 指定输出目录
python src/analyze-novel.py "D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt" --output my_results

# 使用8个Agent并行分析
python src/analyze-novel.py "D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt" --agents 8
```

### 批量分析多本小说

```bash
# 批量分析目录下所有小说
python src/analyze-novel.py "D:\迅雷下载\筛检版" --batch

# 批量分析并指定输出目录
python src/analyze-novel.py "D:\迅雷下载\筛检版" --batch --output batch_results
```

## 分析结果说明

### 输出目录结构

每本小说的分析结果会保存在 `analysis-results/[小说名]/` 目录下：

```
analysis-results/
├── 下山神医绝色总裁赖上我/
│   ├── main_plot.md          # 主线剧情分析
│   ├── sub_plots.md         # 支线剧情汇总
│   ├── characters.md        # 后宫人物图谱
│   ├── style_guide.md       # 创作风格指南
│   ├── template.md          # 创作模板总结
│   ├── consolidated_data.json # 详细数据
│   └── analysis_summary.md   # 汇总报告
└── batch_analysis_summary.md  # 批量分析汇总
```

### 分析报告详解

#### 1. 主线剧情分析 (main_plot.md)
- 故事阶段划分
- 核心矛盾发展
- 关键转折点
- 剧情推进逻辑

#### 2. 支线剧情汇总 (sub_plots.md)
- 按类型分类的支线
- 医术支线
- 感情支线
- 其他支线

#### 3. 后宫人物图谱 (characters.md)
- 后宫成员详细信息
- 出场顺序
- 性格特征
- 感情进度
- 标志性事件

#### 4. 创作风格指南 (style_guide.md)
- 语言风格特征
- 叙事模式
- 场景描写风格
- 对话特色

#### 5. 创作模板总结 (template.md)
- 标准剧情模板
- 人物设定模板
- 对话模式模板
- 可直接使用的创作套路

## 高级用法

### 自定义分析范围

```bash
# 分析第10-50章
python src/analyze-novel.py "小说路径" --start 10 --end 50

# 分析前200章
python src/analyze-novel.py "小说路径" --end 200
```

### 调试模式

查看详细的处理过程：

```bash
# Windows
set PYTHONPATH=src
python -c "from analyze_novel import NovelAnalyzer; analyzer = NovelAnalyzer(); print('测试通过')"

# Linux/macOS
export PYTHONPATH=src
python -c "from analyze_novel import NovelAnalyzer; analyzer = NovelAnalyzer(); print('测试通过')"
```

### 错误处理

如果分析过程中遇到错误，系统会：

1. 记录错误信息到控制台
2. 在输出目录中创建 error.log 文件
3. 继续处理其他章节（如果可能）

## 性能优化建议

### 1. 并行度调整

根据硬件配置调整 Agent 数量：

- 低配机器（4GB 内存）：2-4 个 Agent
- 中配机器（8GB 内存）：4-8 个 Agent
- 高配机器（16GB+ 内存）：8-16 个 Agent

### 2. 分批处理

对于大量小说，建议分批处理：

```bash
# 第一批处理前10本
ls *.txt | head -10 | xargs -I {} python src/analyze-novel.py {}

# 第二批处理接下来的10本
ls *.txt | tail -10 | xargs -I {} python src/analyze-novel.py {}
```

### 3. 输出管理

定期清理旧的分析结果：

```bash
# 删除超过30天的分析结果
find analysis-results -type d -mtime +30 -exec rm -rf {} \;
```

## 常见问题解答

### Q: 分析速度很慢怎么办？
A: 尝试以下方法：
1. 增加 Agent 数量
2. 使用 SSD 存储
3. 关闭其他占用内存的程序

### Q: 如何处理编码错误？
A: 系统会自动检测文件编码，如果仍有问题：
1. 将小说文件转换为 UTF-8 编码
2. 使用 Notepad++ 等工具转换编码

### Q: 章节识别不准确怎么办？
A: 目前支持的标准格式：
- 第X章
- 第X卷
- 第X部
如果格式特殊，可以：
1. 手动修改章节标记
2. 联系开发者添加新的识别模式

### Q: 分析结果如何用于创作？
A: 生成的创作模板可以直接：
1. 作为写作框架使用
2. 参考人物设定
3. 借鉴情节套路
4. 学习对话风格

## 示例工作流

### 1. 收集素材

```bash
# 分析目标小说目录
python src/analyze-novel.py "D:\novels\target" --batch --output target_analysis
```

### 2. 对比分析

```bash
# 分析参考小说
python src/analyze-novel.py "D:\novels\reference" --batch --output reference_analysis
```

### 3. 生成报告

阅读生成的 `template.md` 文件，获取具体的创作套路和模板。

### 4. 应用创作

根据模板进行新的创作，保持相似的风格和结构。

---

*文档更新时间: 2026-04-15*