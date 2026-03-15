# 标准项目结构模板说明

## ⚠️ 重要提示

**这是一个项目模板目录，不要在此目录下进行实际开发！**

## 目录说明

此 `.claude/` 目录包含标准项目结构模板的配置文件：

```
.claude/
├── TEMPLATE_INFO.md        # 本文件 - 模板说明
├── rules/                  # 开发规则模板
│   ├── core.md            # 核心规则
│   ├── config.md          # 配置管理规则
│   └── release.md         # 发布流程规则
├── skills/                # 技能集模板
│   ├── runtime-diagnosis/ # 运行时诊断技能
│   ├── config-migration/  # 配置迁移技能
│   ├── release-check/     # 发布检查技能
│   └── incident-triage/   # 故障分诊技能
├── agents/                # AI 代理配置模板
│   ├── reviewer.md        # 代码审查代理
│   └── explorer.md        # 代码探索代理
└── settings.json          # Claude Code 配置
```

## 使用方式

### 创建新项目时

1. **复制模板目录**：
   ```bash
   cp -r Project/.claude /path/to/new-project/
   ```

2. **根据项目需求调整**：
   - 修改 `settings.json` 中的项目名称和配置
   - 根据需要调整 `rules/` 中的规则
   - 根据项目需求定制 `skills/` 和 `agents/`

3. **初始化 Git 仓库**：
   ```bash
   cd /path/to/new-project
   git init
   ```

## 模板特性

### 预配置的规则系统
- **core.md**: 代码质量、安全、Git 工作流等核心规则
- **config.md**: 配置管理和迁移规则
- **release.md**: 发布流程和质量控制规则

### 集成的技能系统
- **runtime-diagnosis**: 统一的运行时诊断能力
- **config-migration**: 安全的配置迁移流程
- **release-check**: 全面的发布前检查
- **incident-triage**: 系统的故障处理流程

### AI 代理配置
- **reviewer.md**: 自动化代码审查
- **explorer.md**: 智能代码探索

## 版本信息

- **模板版本**: v1.0.0
- **创建日期**: 2025-03-15
- **维护位置**: `D:\workspace\happy-claude-code\Project`

## 更新日志

### v1.0.0 (2025-03-15)
- 初始版本
- 完整的项目结构
- 四个核心技能
- 两个 AI 代理
- 标准规则系统

---

**📌 记住**：这是一个模板，创建新项目时请复制此结构，不要直接在此目录下开发！
