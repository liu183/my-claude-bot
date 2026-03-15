# Release Rules

## Release Process Rules

### 1. 发布前检查
- 所有测试必须通过
- 代码审查必须完成
- 文档必须更新
- 使用 `release-check` skill 进行检查

### 2. 版本管理
- 遵循语义化版本规范
- 维护 CHANGELOG.md
- 打 Git tag

### 3. 发布流程
1. 创建 release 分支
2. 更新版本号
3. 执行完整测试
4. 生成 release notes
5. 合并到 main
6. 部署到生产环境
7. 执行 smoke test

### 4. 回滚准备
- 每次发布前准备回滚方案
- 保留前一版本备份
- 记录回滚步骤

---
*发布流程规则*
