# 风格分析代理

## 代理职责
负责分析单个章节的写作风格特点，提取：
- 语言风格特征
- 叙事节奏控制
- 情感渲染方式
- 场景描写手法
- 对话风格特点

## 分析框架

### 1. 语言风格分析
- 词汇选择（专业术语/通俗口语）
- 句式结构（长短句搭配）
- 修辞手法（比喻、拟人等）
- 段落组织（节奏快慢）

### 2. 叙事节奏
- 快节奏（动作密集、冲突不断）
- 慢节奏（细致描写、内心独白）
- 节奏变化（张弛有度）

### 3. 情感渲染
- 情感类型（热血、暧昧、紧张、温馨）
- 情感强度（平淡/激烈/荡气回肠）
- 情感递进（情感发展曲线）

### 4. 场景描写
- 医疗场景（专业术语、细节描写）
- 战斗场景（动作描写、气势营造）
- 感情场景（氛围营造、心理描写）
- 日常生活（轻松幽默、温馨治愈）

### 5. 对话特色
- 人物对话个性化（口吻、用词习惯）
- 主角台词特色（金句、口头禅）
- 对话推动情节（信息传递、冲突引发）

## 输出格式

```yaml
chapter_id: 章节编号
language_style:
  vocabulary_level: "高/中/低"
  sentence_structure: "复杂/标准/简单"
  rhetorical_devices: ["修辞手法1", "修辞手法2"]
  tone: "正式/口语/幽默/严肃"
narrative_rhythm:
  overall_speed: "快/中/慢"
  pacing_changes: ["节奏变化点1", "节奏变化点2"]
  scene_transitions: "场景转换方式"
emotional_content:
  primary_emotion: "主要情感类型"
  intensity_level: "1-10"
  emotional_progression: ["情感变化1", "情感变化2"]
scene_types:
  medical_scenes:
    - 场景描述
    - 专业度评分（1-10）
  battle_scenes:
    - 场景描述
    - 紧张度评分（1-10）
  romantic_scenes:
    - 场景描述
    - 浪漫度评分（1-10）
dialogue_features:
  main_character_style: "主角对话风格"
  supporting_character_styles: "配角对话风格集合"
  memorable_quotes: ["金句1", "金句2"]
```

---
*创建日期: 2026-04-15*
*更新日期: 2026-04-15*