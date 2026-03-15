# Claude Code Project Configuration

> **📋 这是一个标准项目结构模板**
>
> 此文件是项目配置模板，创建新项目时请复制此结构并根据具体需求更新内容。
>
> **模板说明**：
> - 此目录（`Project/`）是标准项目结构模板
> - 不要在此目录下进行实际开发
> - 创建新项目时复制此结构到新目录
> - 详细说明请参考 `README.md`

## Project Overview

**⚠️ 模板项目 - 需要填写实际项目信息**

**项目名称**: [待填写 - 创建新项目时填写]
**项目描述**: [待填写 - 创建新项目时填写]
**创建日期**: [待填写 - 使用模板的日期]
**模板版本**: v1.0.0
**模板来源**: `D:\workspace\happy-claude-code\Project`

## Project Structure

### 标准项目结构模板

```
📦 Project-Template/                    # ← 标准项目结构模板（当前目录）
├── 📄 README.md                        # 模板说明文档
├── 📄 CLAUDE.md                        # ← 本文件 - 项目配置模板
├── 📁 .claude/
│   ├── 📁 rules/
│   │   ├── 📄 core.md                 # 核心规则（优先级最高）
│   │   ├── 📄 config.md               # 配置管理规则
│   │   └── 📄 release.md              # 发布流程规则
│   ├── 📁 skills/
│   │   ├── 📁 runtime-diagnosis/      # 运行时诊断 - 统一收集日志、状态和依赖
│   │   ├── 📁 config-migration/       # 配置迁移 - 配置迁移回滚防污
│   │   ├── 📁 release-check/          # 发布检查 - 发布前校验、smoke test
│   │   └── 📁 incident-triage/        # 故障分诊 - 线上故障分诊
│   ├── 📁 agents/
│   │   ├── 📄 reviewer.md             # 代码审查代理
│   │   └── 📄 explorer.md             # 代码探索代理
│   └── 📄 settings.json               # Claude Code 配置
└── 📁 docs/
    └── 📁 ai/
        ├── 📄 architecture.md         # 系统架构文档
        └── 📄 release-runbook.md      # 发布操作手册
```

### 使用说明

**创建新项目时**：
1. 复制整个 `Project/` 目录到新的项目位置
2. 重命名项目目录
3. 更新 `CLAUDE.md` 中的项目信息
4. 根据项目需求调整配置
5. 初始化 Git 仓库

## Development Workflow

### 1. 新功能开发
- 使用 `brainstorming` skill 进行需求分析
- 创建分支进行开发
- 使用 `TDD` skill 进行测试驱动开发
- 提交前使用 `code-review` skill 进行代码审查

### 2. 配置变更
- 使用 `config-migration` skill 进行配置迁移
- 确保配置变更可回滚
- 避免配置污染

### 3. 发布流程
- 使用 `release-check` skill 进行发布前检查
- 执行 smoke test
- 更新 `release-runbook.md`

### 4. 故障处理
- 使用 `runtime-diagnosis` skill 收集诊断信息
- 使用 `incident-triage` skill 进行故障分诊
- 记录故障处理过程

## Rules Priority

1. **core.md** - 核心规则，优先级最高
2. **config.md** - 配置相关规则
3. **release.md** - 发布相关规则

## Skills Usage

所有技能按照 .claude/skills/ 目录结构组织，根据任务类型调用相应技能。

---
*此文件由标准项目结构模板生成 - 请根据具体项目更新内容*
