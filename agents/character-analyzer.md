# 人物分析代理

## 代理职责
负责分析单个章节的人物相关信息，提取：
- 新人物出现
- 人物关系变化
- 后宫成员互动
- 人物性格展示
- 人物技能/能力展示

## 分析框架

### 1. 人物类型分类
- 主角
- 后宫成员
- 反派角色
- 配角/工具人
- 重要NPC

### 2. 人物关系网
- 感情关系（好感度变化）
- 师承关系
- 敌对关系
- 合作关系
- 社交关系（朋友、同门等）

### 3. 人物特征提取
- 外貌特征
- 性格特点
- 能力技能
- 背景故事
- 成长变化
- 口头禅/习惯动作

### 4. 后宫分析维度
- 出场顺序
- 性格类型（温柔、傲娇、冷艳、活泼等）
- 身份地位（总裁、医生、学生、老师等）
- 与主角的互动方式
- 对剧情的影响程度

## 输出格式

```yaml
chapter_id: 章节编号
new_characters:
  character_name: 
    type: "主角/后宫/反派/配角"
    role: "章节作用"
    first_appearance: true/false
    identity: "身份描述"
    appearance: "外貌描述"
    personality: ["性格特征1", "性格特征2"]
    abilities: ["能力1", "能力2"]
    relationships:
      target: "目标角色"
      type: "关系类型"
      status: "关系状态（好感度1-10）"
character_development:
  character_name:
    changes: ["变化描述"]
    relationships:
      - target: "角色名"
        change: "关系变化"
        reason: "变化原因"
harem_interaction:
  active_members: ["活跃后宫成员"]
  interaction_type: "互动类型（感情/医疗/战斗）"
  progression: "感情进展程度（1-10）"
  new_elements: ["新加入的暧昧/亲密元素"]
```

---
*创建日期: 2026-04-15*
*更新日期: 2026-04-15*