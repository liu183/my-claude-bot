# Incident Triage Skill

## Description

线上故障分诊，快速定位问题、评估影响、制定处理方案。

## When to Use

当发生以下情况时使用此技能：
- 线上服务异常
- 性能严重下降
- 数据错误或丢失
- 安全事件发生

## Incident Response Process

### Phase 1: 检测和确认 (Detection & Confirmation)

#### 1.1 确认故障
```bash
# 检查服务状态
systemctl status app-name

# 检查监控指标
# - CPU 使用率
# - 内存使用率
# - 请求成功率
# - 响应时间
```

#### 1.2 评估影响
- [ ] 受影响用户数
- [ ] 受影响功能范围
- [ ] 业务影响程度
- [ ] 数据是否受损

#### 1.2 确定严重级别
- **P0 - 严重**：核心功能不可用，影响所有用户
- **P1 - 高**：重要功能受影响，影响部分用户
- **P2 - 中**：功能降级，影响有限
- **P3 - 低**：轻微问题，不影响核心功能

### Phase 2: 诊断分析 (Diagnosis)

#### 2.1 收集信息
```bash
# 使用 runtime-diagnosis skill
runtime-diagnosis --app=my-app --since="15 minutes ago"

# 检查最近变更
git log --since="1 hour ago"

# 检查部署记录
kubectl rollout history deployment/app-name
```

#### 2.2 定位根因
- [ ] 代码变更引起
- [ ] 配置变更引起
- [ ] 依赖服务故障
- [ ] 资源不足
- [ ] 外部因素

#### 2.3 复现问题
- [ ] 本地复现
- [ ] 测试环境复现
- [ ] 查看日志复现场景

### Phase 3: 处理方案 (Mitigation)

#### 3.1 紧急处理
```bash
# 立即回滚
./scripts/rollback.sh

# 或临时修复
./scripts/hotfix.sh
```

#### 3.2 选择处理策略
- **立即回滚**：影响严重且无法快速修复
- **热修复**：有快速修复方案
- **降级服务**：部分功能暂时关闭
- **扩容**：资源不足时

#### 3.3 执行修复
```bash
# 应用修复
kubectl apply -f fix.yaml

# 验证修复
curl http://app/health
```

### Phase 4: 恢复验证 (Recovery)

#### 4.1 验证修复
```bash
# 功能验证
./scripts/smoke-test.sh

# 监控指标
# - 错误率下降
# - 响应时间恢复
# - 服务可用
```

#### 4.2 持续监控
- [ ] 监控关键指标
- [ ] 检查错误日志
- [ ] 验证数据完整性

### Phase 5: 事后总结 (Postmortem)

#### 5.1 事故报告
```markdown
# Incident Report

## 概述
- 发生时间：
- 持续时长：
- 影响范围：
- 严重级别：

## 时间线
- XX:XX - 故障发生
- XX:XX - 故障检测
- XX:XX - 开始处理
- XX:XX - 问题解决

## 根本原因
- 问题描述
- 原因分析

## 处理过程
- 采取的措施
- 遇到的问题

## 改进措施
- 短期措施
- 长期措施
```

#### 5.2 改进措施
- [ ] 防止再次发生
- [ ] 改进检测能力
- [ ] 优化响应流程
- [ ] 更新文档

## Communication Protocol

### 内部沟通
- 技术团队：立即通知
- 产品团队：影响评估后通知
- 管理层：P0/P1 立即通知

### 外部沟通
- 用户：根据影响级别决定
- 公告：提供预计恢复时间

## Triage Commands

```bash
# 快速诊断
incident-triage --quick

# 完整诊断
incident-triage --full

# 生成报告
incident-triage --report
```

## On-Call Rotation

- 主值班人：[姓名]
- 备用值班人：[姓名]
- 升级路径：值班人 → 技术负责人 → CTO

---
*故障分诊技能*
