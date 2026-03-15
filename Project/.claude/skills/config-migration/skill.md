# Config Migration Skill

## Description

处理配置迁移，确保配置变更可回滚，避免配置污染。

## When to Use

当需要以下操作时使用此技能：
- 配置文件结构变更
- 配置项新增/修改/删除
- 环境配置迁移
- 配置版本升级

## Migration Principles

### 1. 可回滚性
- 保留旧配置备份
- 记录迁移历史
- 提供回滚脚本

### 2. 防污原则
- 不污染现有配置
- 使用独立的配置空间
- 清晰的版本隔离

### 3. 验证优先
- 迁移前验证
- 迁移后验证
- 提供验证脚本

## Migration Process

### Step 1: 备份现有配置
```bash
# 创建备份
cp config.json config.json.backup.$(date +%Y%m%d_%H%M%S)
```

### Step 2: 分析配置差异
```bash
# 比较配置
diff old_config.json new_config.json
```

### Step 3: 执行迁移
```bash
# 执行迁移脚本
./scripts/migrate-config.sh --from=v1 --to=v2
```

### Step 4: 验证配置
```bash
# 验证配置语法
./scripts/validate-config.sh config.json

# 验证配置加载
app --validate-config
```

### Step 5: 记录迁移
```bash
# 记录到迁移日志
echo "$(date): Migrated config from v1 to v2" >> migration.log
```

## Rollback Process

```bash
# 回滚到之前版本
./scripts/rollback-config.sh --to=v1

# 恢复备份
cp config.json.backup.20250315_102030 config.json
```

## Migration Script Template

```bash
#!/bin/bash
# migrate-config.sh

VERSION_FROM=$1
VERSION_TO=$2
BACKUP_DIR="/backups/config"

# 创建备份
backup_config() {
    timestamp=$(date +%Y%m%d_%H%M%S)
    cp config.json "$BACKUP_DIR/config.json.$timestamp"
}

# 执行迁移
migrate() {
    echo "Migrating from $VERSION_FROM to $VERSION_TO"
    # 迁移逻辑
}

# 验证
validate() {
    # 验证逻辑
}

# 主流程
backup_config
migrate
validate
```

## Checklist

- [ ] 配置已备份
- [ ] 迁移脚本已准备
- [ ] 验证脚本已准备
- [ ] 回滚方案已准备
- [ ] 测试环境已验证
- [ ] 迁移已记录

---
*配置迁移技能*
