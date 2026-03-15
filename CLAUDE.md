# Claude Code Project Configuration

## Project Overview

**项目名称**: Novel Creation Studio（网文小说创作工作室）
**项目描述**: 专业的网文小说创作与优化工作空间，提供从构思、大纲、创作到审核的完整流程支持
**创建日期**: 2025-03-15
**项目类型**: 创作工具与工作流管理
**目标用户**: 网文作者、小说创作者

## 项目定位

这是一个专业的网文小说创作工作空间，整合了：
- 📚 **创作资料管理** - 世界观、角色设定、大纲等
- 🛠️ **创作工具集** - 17+ 专业创作技能
- 📖 **参考资料库** - 平台规则、写作知识、案例研究
- 🔍 **质量保障** - 自动化审核、一致性检查、毒点检测
- 📊 **数据分析** - 留存率优化、节奏分析

## Project Structure

```
novel-creation-studio/
├── 📄 CLAUDE.md                      # 本文件 - 项目配置
├── 📄 README.md                      # 项目说明
├── 📁 novels/                        # 小说创作目录
│   ├── 📁 [小说名]/                  # 单个小说项目
│   │   ├── 📄 outline.md            # 大纲
│   │   ├── 📄 characters.md         # 角色设定
│   │   ├── 📄 worldview.md          # 世界观
│   │   ├── 📄 chapters/             # 章节内容
│   │   └── 📁 analysis/             # 分析报告
├── 📁 reference/                     # 参考资料
│   ├── 📁 docs/                      # 创作文档
│   ├── 📁 settings/                  # 设定资料
│   └── 📁 skills/                    # 创作技能
├── 📁 .claude/
│   ├── 📁 rules/                     # 创作规则
│   │   ├── 📄 core.md                # 核心创作规则
│   │   ├── 📄 consistency.md         # 一致性规则
│   │   └── 📄 quality.md             # 质量标准
│   ├── 📁 skills/                    # 技能集
│   │   ├── 📁 novel-review/          # 小说审核技能
│   │   ├── 📁 character-consistency/ # 角色一致性检查
│   │   ├── 📁 plot-analysis/         # 剧情分析
│   │   ├── 📁 pace-analysis/         # 节奏分析
│   │   ├── 📁 toxin-detector/        # 毒点检测
│   │   └── 📁 optimization/          # 优化技能
│   ├── 📁 agents/                    # AI 代理
│   │   ├── 📄 editor.md              # 编辑代理
│   │   ├── 📄 reviewer.md            # 审核代理
│   │   └── 📄 analyzer.md            # 分析代理
│   └── 📄 settings.json              # 配置文件
└── 📁 docs/
    ├── 📁 guides/                    # 使用指南
    └── 📁 templates/                 # 模板文件
```

## 创作工作流

### 1. 新小说创作流程
```
构思 → 设定 → 大纲 → 创作 → 审核 → 优化 → 发布
```

#### 阶段一：构思与设定
- 使用 `brainstorming` skill 进行创意发散
- 创建世界观设定（worldview.md）
- 设计角色档案（characters.md）
- 确定战力体系（power-system.md）

#### 阶段二：大纲规划
- 使用 `novel-outline-generator` 生成大纲
- 设计故事节奏和情节发展
- 规划章节结构
- 创建时间线（timeline.md）

#### 阶段三：内容创作
- 按大纲进行章节创作
- 使用 `novel-opening-optimizer` 优化开头
- 使用 `novel-hook-detector` 检查钩子
- 实时一致性检查

#### 阶段四：质量审核
- 使用 `novel-reviewer` 进行全面审核
- 使用 `novel-toxin-detector` 检测毒点
- 使用 `novel-pace-analyzer` 分析节奏
- 使用 `character-consistency` 检查一致性

#### 阶段五：优化发布
- 根据审核结果优化内容
- 使用 `retention-rate-optimizer` 优化留存
- 准备发布材料
- 更新连载状态

### 2. 已有小说优化流程
```
分析 → 诊断 → 方案 → 修复 → 验证 → 总结
```

#### 步骤详情
1. **完整分析** - 使用 `novel-reviewer` 全面分析
2. **问题诊断** - 识别核心问题（P0/P1/P2）
3. **制定方案** - 生成详细修复方案
4. **执行修复** - 按优先级修复问题
5. **验证效果** - 检查修复效果
6. **总结经验** - 记录到知识库

## 核心技能集

### 审核类技能
- `apocalyptic-novel-reviewer.md` - 末世小说专项审核
- `novel-character-consistency.md` - 角色一致性检查
- `novel-toxin-detector.md` - 毒点检测
- `novel-pace-analyzer.md` - 节奏分析

### 创作类技能
- `novel-outline-generator.md` - 大纲生成
- `novel-opening-optimizer.md` - 开头优化
- `novel-hook-detector.md` - 钩子检测
- `novel-title-generator.md` - 标题生成

### 优化类技能
- `retention-rate-optimizer.md` - 留存率优化
- `genre-innovator.md` - 类型创新
- `author-growth-planner.md` - 作者成长规划

### 商业类技能
- `ip-adaptation-evaluator.md` - IP改编评估
- `copyright-protection-advisor.md` - 版权保护顾问

## 质量标准

### P0 级问题（必须修复）
- 世界观严重冲突
- 角色设定前后矛盾
- 战力体系崩溃
- 重大逻辑漏洞

### P1 级问题（应该修复）
- 节奏拖沓或混乱
- 角色行为不符合人设
- 情节逻辑不够严谨
- 毒点影响阅读体验

### P2 级问题（建议优化）
- 文笔可以提升
- 描写可以更生动
- 对话可以更自然
- 情节可以更精彩

## 平台适配

### 番茄小说平台
- 免费阅读模式
- 算法推荐机制
- 完读率重要性
- 更新频率要求

### 平台规则
- 内容审核规范
- 禁止内容类型
- 推荐机制说明
- 收益分成模式

## 参考资料

### 核心文档
- `番茄小说平台规则与写作知识总结.md` - 平台规则详解
- `末世小说战力体系参考.md` - 战力体系参考
- `末世小说完整优化总结报告.md` - 优化案例

### 设定模板
- `characters.md` - 角色设定模板
- `worldview.md` - 世界观设定模板
- `style.md` - 写作风格参考
- `cheatsheet.md` - 快速参考表

## Git 工作流

### 分支策略
- `main` - 稳定版本
- `feature/[小说名]` - 单个小说开发
- `optimization/[小说名]` - 优化工作
- `docs` - 文档更新

### 提交规范
```
feat: 新增小说《[小说名]》大纲
fix: 修复《[小说名]》角色一致性问题
docs: 更新《[小说名]》角色设定
review: 完成《[小说名]》第1-10章审核
optimize: 优化《[小说名]》开篇节奏
```

## 项目里程碑

### Phase 1: 基础建设 ✅
- [x] 项目结构搭建
- [x] 参考资料整合
- [x] 技能集导入
- [x] Git 仓库初始化

### Phase 2: 功能完善
- [ ] 完善所有技能配置
- [ ] 创建小说模板
- [ ] 建立质量标准
- [ ] 编写使用文档

### Phase 3: 实战应用
- [ ] 新小说创作
- [ ] 已有小说优化
- [ ] 工作流优化
- [ ] 知识库积累

---

**💡 使用提示**：
- 新小说创作：告诉 Claude "开始创作新小说"
- 小说优化：告诉 Claude "优化《小说名》"
- 质量审核：告诉 Claude "审核《小说名》第X-Y章"
- 问题诊断：告诉 Claude "诊断《小说名》的问题"

---
*网文小说创作工作室 - 让创作更专业*
