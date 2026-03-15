# 标准项目结构模板

> **⚠️ 这是一个项目模板，不要在此目录下进行实际开发**

## 用途说明

这是一个标准的项目结构模板，用于创建新项目时的参考和基础。

## 使用方式

### 创建新项目

当需要创建新项目时，按照以下步骤操作：

```bash
# 1. 在工作空间创建新项目目录
mkdir -p D:\workspace\happy-claude-code\my-new-project

# 2. 复制模板结构到新项目
cp -r D:\workspace\happy-claude-code\Project\.claude D:\workspace\happy-claude-code\my-new-project/
cp D:\workspace\happy-claude-code\Project\CLAUDE.md D:\workspace\happy-claude-code\my-new-project/
cp -r D:\workspace\happy-claude-code\Project\docs D:\workspace\happy-claude-code\my-new-project/

# 3. 进入新项目目录
cd D:\workspace\happy-claude-code\my-new-project

# 4. 更新 CLAUDE.md 中的项目信息
# 5. 根据项目需求调整配置
# 6. 初始化 Git 仓库
git init
```

### 通过 Claude Code 创建

直接告诉 Claude Code：
- "创建一个新项目，使用标准项目结构"
- "基于模板创建一个 [项目名称] 项目"

Claude Code 会自动：
1. 复制标准项目结构
2. 更新项目配置
3. 初始化 Git 仓库
4. 配置开发环境

## 项目结构说明

```
Project/                           # ← 标准项目结构模板
├── README.md                      # 本文件 - 模板说明
├── CLAUDE.md                      # 项目配置和开发工作流
├── .claude/
│   ├── rules/                     # 开发规则
│   │   ├── core.md                # 核心规则（优先级最高）
│   │   ├── config.md              # 配置管理规则
│   │   └── release.md             # 发布流程规则
│   ├── skills/                    # 技能集
│   │   ├── runtime-diagnosis/     # 运行时诊断技能
│   │   ├── config-migration/      # 配置迁移技能
│   │   ├── release-check/         # 发布检查技能
│   │   └── incident-triage/       # 故障分诊技能
│   ├── agents/                    # AI 代理配置
│   │   ├── reviewer.md            # 代码审查代理
│   │   └── explorer.md            # 代码探索代理
│   └── settings.json              # Claude Code 配置
└── docs/                          # 项目文档
    └── ai/
        ├── architecture.md        # 系统架构文档
        └── release-runbook.md     # 发布操作手册
```

## 模板特性

### ✅ 开箱即用
- 完整的项目结构
- 预配置的开发规则
- 集成的技能和代理
- 标准化的文档模板

### 🎯 最佳实践
- 符合 Claude Code 规范
- Git 工作流集成
- 完整的发布流程
- 故障处理机制

### 🔄 持续更新
此模板会根据实际使用情况进行优化和更新。

## 版本历史

- **v1.0.0** (2025-03-15) - 初始版本
  - 基础项目结构
  - 核心规则集
  - 四个核心技能
  - 两个 AI 代理
  - 标准文档模板

## 维护信息

- **模板位置**: `D:\workspace\happy-claude-code\Project`
- **远程仓库**: https://github.com/liu183/my-claude-bot.git
- **更新策略**: 根据项目需求持续优化

---

**⚠️ 重要提示**：
1. **不要直接在此目录下开发**
2. **创建新项目时复制此结构**
3. **根据项目需求调整配置**
4. **保持模板的标准化和更新**

---
*标准项目结构模板 - 2025-03-15*
