# Runtime Diagnosis Skill

## Description

统一收集运行时日志、系统状态和依赖信息，用于问题诊断和故障排查。

## When to Use

当出现以下情况时使用此技能：
- 应用运行异常
- 性能问题分析
- 功能行为不符合预期
- 需要收集诊断信息

## Diagnosis Steps

### 1. 系统状态收集
```bash
# 检查进程状态
ps aux | grep app-name

# 检查端口占用
netstat -tlnp | grep port

# 检查磁盘使用
df -h

# 检查内存使用
free -h
```

### 2. 日志收集
```bash
# 应用日志
tail -f /path/to/app.log

# 错误日志
grep "ERROR" /path/to/app.log

# 系统日志
journalctl -u app-name -n 100
```

### 3. 依赖检查
```bash
# 检查依赖服务
ping database-host
curl api-endpoint/health

# 检查依赖版本
npm list  # 或 pip list, mvn dependency:tree
```

### 4. 性能分析
```bash
# CPU 使用
top -p <pid>

# 内存分析
pmap <pid>

# 网络连接
lsof -p <pid>
```

## Output Format

诊断报告应包含：
1. **系统状态摘要**
   - 进程状态
   - 资源使用情况
   - 网络连接状态

2. **日志分析**
   - 错误日志摘要
   - 警告信息
   - 异常模式

3. **依赖状态**
   - 数据库连接
   - 外部服务可用性
   - 依赖版本信息

4. **问题分析**
   - 可能的问题根因
   - 建议的解决方案
   - 预防措施

## Example Usage

```bash
# 完整诊断
runtime-diagnosis --app=my-app --since="1 hour ago"
```

---
*运行时诊断技能*
