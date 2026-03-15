# Release Check Skill

## Description

发布前全面检查，确保发布的质量和安全性。

## When to Use

在以下情况下使用此技能：
- 准备发布新版本
- 部署到生产环境前
- 紧急 hotfix 发布

## Pre-Release Checklist

### 1. 代码质量
- [ ] 所有 PR 已合并
- [ ] 代码审查通过
- [ ] 无TODO或FIXME未处理
- [ ] 代码风格符合规范

### 2. 测试覆盖
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 测试覆盖率达标
- [ ] 关键路径已测试

### 3. 安全检查
- [ ] 无硬编码密钥
- [ ] 依赖无已知漏洞
- [ ] 权限配置正确
- [ ] 安全扫描通过

### 4. 文档更新
- [ ] CHANGELOG.md 更新
- [ ] API 文档更新
- [ ] 用户文档更新
- [ ] Release Notes 准备

### 5. 性能验证
- [ ] 性能测试通过
- [ ] 资源使用正常
- [ ] 响应时间可接受
- [ ] 无内存泄漏

### 6. 环境准备
- [ ] 测试环境验证
- [ ] 生产环境检查
- [ ] 监控配置就绪
- [ ] 回滚方案准备

## Smoke Test

### 基础功能
```bash
# 健康检查
curl http://app/health

# 版本检查
curl http://app/version

# 关键接口
curl http://app/api/endpoint
```

### 数据验证
```bash
# 数据库连接
db-cli --execute "SELECT 1"

# 缓存连接
redis-cli ping
```

### 日志验证
```bash
# 检查错误日志
tail -f logs/app.log | grep ERROR

# 检查启动日志
journalctl -u app -n 50
```

## Release Validation Script

```bash
#!/bin/bash
# release-check.sh

echo "=== Running Release Checks ==="

# 代码检查
echo "Checking code quality..."
npm run lint
npm run test

# 安全检查
echo "Running security scan..."
npm audit
safety check

# 文档检查
echo "Validating documentation..."
npm run docs:build

# 性能检查
echo "Running performance tests..."
npm run perf:test

echo "=== Release Checks Complete ==="
```

## Blocking Criteria

以下任一条件不满足时，**禁止发布**：
1. 任何测试失败
2. 关键 bug 未修复
3. 安全漏洞未处理
4. 文档未更新
5. 无回滚方案

## Release Notes Template

```markdown
# Release v1.0.0

## Features
- 新功能 1
- 新功能 2

## Bug Fixes
- 修复 bug 1
- 修复 bug 2

## Breaking Changes
- 破坏性变更说明

## Migration Guide
- 迁移步骤

## Known Issues
- 已知问题
```

---
*发布检查技能*
