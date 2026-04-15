# 安装配置指南

## 环境要求

- Python 3.9 或更高版本
- Windows/Linux/macOS 操作系统
- 至少 4GB 可用内存（建议 8GB 以上）

## 安装步骤

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd novel-analysis-chapter-analyzer
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

运行测试脚本验证安装是否成功：

```bash
python src/analyze-novel.py --help
```

## 配置说明

### Agent 数量配置

项目使用多 Agent 并行分析，可以通过以下方式配置 Agent 数量：

1. **命令行参数**（推荐）
   ```bash
   python src/analyze-novel.py <小说路径> --agents 8
   ```

2. **代码中修改**
   ```python
   # 在 src/analyze-novel.py 中修改
   analyzer = NovelAnalyzer(num_agents=8)
   ```

### 内存配置

如果遇到内存不足的问题，可以：

1. 减少 Agent 数量
2. 分批处理小说
3. 增加虚拟内存

## 故障排除

### 常见问题

1. **编码错误**
   - 确保小说文件使用 UTF-8 或 GBK 编码
   - 项目会自动检测文件编码

2. **内存不足**
   - 减少 Agent 数量
   - 使用单个文件模式而不是批量模式

3. **章节识别错误**
   - 确保小说使用标准的章节格式
   - 目前支持："第X章"、"第X卷"、"第X部"等格式

## 文件权限

确保对以下目录有读写权限：
- `analysis-results/`（输出目录）
- 各小说文件所在的目录

## 性能优化

1. **SSD 存储**：提高文件读取速度
2. **多核 CPU**：提高并行处理能力
3. **足够内存**：避免频繁的磁盘交换

---

*文档更新时间: 2026-04-15*