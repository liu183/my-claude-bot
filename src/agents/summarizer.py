#!/usr/bin/env python3
"""
汇总生成代理
整合所有章节的分析结果，生成最终报告
"""

import json
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, Counter


@dataclass
class ConsolidatedData:
    """整合后的数据结构"""
    plot_data: List[Dict[str, Any]]
    character_data: List[Dict[str, Any]]
    style_data: List[Dict[str, Any]]


class Summarizer:
    """汇总生成器"""

    def __init__(self):
        self.novel_info = {}

    async def generate_final_reports(self, plot_data: List[Dict],
                                   character_data: List[Dict],
                                   style_data: List[Dict]) -> Dict[str, str]:
        """生成最终报告"""
        # 整合数据
        consolidated = ConsolidatedData(plot_data, character_data, style_data)

        # 生成各报告
        reports = {
            'main_plot': self._generate_main_plot_report(consolidated),
            'sub_plots': self._generate_sub_plots_report(consolidated),
            'characters': self._generate_characters_report(consolidated),
            'style_guide': self._generate_style_guide_report(consolidated),
            'template': self._generate_template_report(consolidated)
        }

        return reports

    def _generate_main_plot_report(self, consolidated: ConsolidatedData) -> str:
        """生成主线剧情报告"""
        report = f"""# 都市神医小说 - 主线剧情分析

## 故事阶段划分
"""

        # 分析剧情阶段
        plot_progression = self._analyze_plot_progression(consolidated.plot_data)

        for i, (stage_name, chapters) in enumerate(plot_progression.items(), 1):
            report += f"""
### 第{i}阶段：{stage_name}
- 时间跨度：第{chapters['start']}章 - 第{chapters['end']}章
- 核心事件：
"""
            for event in chapters['core_events']:
                report += f"  - {event}\n"

            report += "- 人物发展：\n"
            for char_dev in chapters['character_development']:
                report += f"  - {char_dev}\n"

        # 主线核心矛盾
        report += """
## 主线核心矛盾
"""
        core_conflict = self._identify_core_conflict(consolidated.plot_data)
        report += f"- 核心冲突：{core_conflict['description']}\n"
        report += f"- 发展过程：{core_conflict['development']}\n"
        report += f"- 最终解决：{core_conflict['resolution']}\n"

        # 关键转折点
        report += """
## 关键转折点
"""
        turning_points = self._find_turning_points(consolidated.plot_data)
        for i, point in enumerate(turning_points[:5], 1):
            report += f"{i}. 第{point['chapter']}章：{point['description']}\n"

        return report

    def _generate_sub_plots_report(self, consolidated: ConsolidatedData) -> str:
        """生成支线剧情报告"""
        report = f"""# 都市神医小说 - 支线剧情汇总

## 按类型分类的支线
"""

        # 按类型分析支线
        sub_plots_by_type = self._categorize_sub_plots(consolidated.plot_data)

        for plot_type, plots in sub_plots_by_type.items():
            report += f"""
### {plot_type}支线
"""
            for i, plot in enumerate(plots[:10], 1):  # 只显示前10条
                report += f"- 支线{i}：{plot['description']}\n"
                report += f"  - 起始章节：{plot['start_chapter']}\n"
                report += f"  - 相关人物：{', '.join(plot['characters'])}\n"
                report += f"  - 发展过程：{plot['development']}\n"

        return report

    def _generate_characters_report(self, consolidated: ConsolidatedData) -> str:
        """生成后宫人物报告"""
        report = f"""# 都市神医小说 - 后宫人物图谱

## 后宫成员列表
"""

        # 整理后宫人物信息
        harem_members = self._extract_harem_members(consolidated.character_data)

        for i, (name, info) in enumerate(harem_members.items(), 1):
            report += f"""
### {i}. {name}
- 出场章节：第{info['first_chapter']}章
- 身份地位：{info['identity']}
- 性格特征：{', '.join(info['personality'])}
- 外貌特征：{info['appearance']}
- 与主角关系发展：
"""
            for rel in info['relationship_progress']:
                report += f"  - {rel['stage']}: {rel['description']}\n"

            report += "- 标志性事件：\n"
            for event in info['key_events']:
                report += f"  - {event}\n"

        # 后宫关系网络
        report += """
## 后宫关系网络
"""
        relationship_network = self._analyze_harem_relationships(consolidated.character_data)
        for rel in relationship_network:
            report += f"- {rel['character1']} ↔ {rel['character2']}：{rel['relation_description']}\n"

        return report

    def _generate_style_guide_report(self, consolidated: ConsolidatedData) -> str:
        """生成创作风格报告"""
        report = f"""# 都市神医小说 - 创作风格分析

## 语言风格特征
"""
        # 分析语言风格
        style_features = self._analyze_language_style(consolidated.style_data)

        report += f"- 词汇特点：{style_features['vocabulary']}\n"
        report += f"- 句式偏好：{style_features['sentence_structure']}\n"
        report += f"- 修辞特色：{', '.join(style_features['rhetorical_devices'])}\n"

        report += """
## 叙事模式
"""
        narrative_patterns = self._analyze_narrative_patterns(consolidated.style_data)

        report += f"- 开场方式：{narrative_patterns['opening']}\n"
        report += f"- 冲突设置：{narrative_patterns['conflict']}\n"
        report += f"- 高潮营造：{narrative_patterns['climax']}\n"
        report += f"- 收尾习惯：{narrative_patterns['ending']}\n"

        report += """
## 场景描写风格
"""
        scene_styles = self._analyze_scene_styles(consolidated.style_data)

        for scene_type, style in scene_styles.items():
            report += f"- {scene_type}场景：{style}\n"

        return report

    def _generate_template_report(self, consolidated: ConsolidatedData) -> str:
        """生成创作模板报告"""
        report = f"""# 都市神医小说 - 创作模板总结

## 标准剧情模板
"""
        # 生成剧情模板
        plot_templates = self._generate_plot_templates(consolidated.plot_data)

        for template_name, template_content in plot_templates.items():
            report += f"""
### {template_name}
{template_content}
"""

        report += """
## 人物设定模板
"""
        # 生成人物模板
        character_templates = self._generate_character_templates(consolidated.character_data)

        report += "### 主角模板\n"
        report += character_templates['main_character'] + "\n"

        report += "### 后宫成员模板\n"
        for template in character_templates['harem_members']:
            report += f"- {template}\n"

        report += """
## 对话模式模板
"""
        # 生成对话模板
        dialogue_templates = self._generate_dialogue_templates(consolidated.style_data)

        report += "### 主角金句模板\n"
        for template in dialogue_templates['main_character_quotes']:
            report += f"- {template}\n"

        report += "### 反派挑衅模板\n"
        for template in dialogue_templates['villain_taunts']:
            report += f"- {template}\n"

        report += "### 女主羞涩模板\n"
        for template in dialogue_templates['female_shyness']:
            report += f"- {template}\n"

        return report

    # 辅助分析方法

    def _analyze_plot_progression(self, plot_data: List[Dict]) -> Dict:
        """分析剧情进展"""
        stages = {
            '初入都市': {'start': 1, 'end': 20, 'core_events': [], 'character_development': []},
            '医术扬名': {'start': 21, 'end': 50, 'core_events': [], 'character_development': []},
            '感情纠葛': {'start': 51, 'end': 80, 'core_events': [], 'character_development': []},
            '最终决战': {'start': 81, 'end': 100, 'core_events': [], 'character_development': []}
        }

        # 根据实际数据填充
        for chapter_data in plot_data:
            chapter_id = chapter_data['chapter_id']
            plot_function = chapter_data['plot_function']

            if chapter_id <= 20:
                stages['初入都市']['core_events'].extend([
                    event['event'] for event in chapter_data['main_events'][:2]
                ])
            elif chapter_id <= 50:
                stages['医术扬名']['core_events'].extend([
                    event['event'] for event in chapter_data['main_events'][:2]
                ])
            elif chapter_id <= 80:
                stages['感情纠葛']['core_events'].extend([
                    event['event'] for event in chapter_data['main_events'][:2]
                ])
            else:
                stages['最终决战']['core_events'].extend([
                    event['event'] for event in chapter_data['main_events'][:2]
                ])

        return stages

    def _identify_core_conflict(self, plot_data: List[Dict]) -> Dict:
        """识别核心冲突"""
        # 统计冲突类型
        conflict_types = Counter()
        for chapter_data in plot_data:
            for conflict in chapter_data['conflicts']:
                conflict_types[conflict['type']] += 1

        # 返回最主要的冲突
        if conflict_types:
            main_conflict = conflict_types.most_common(1)[0][0]
            return {
                'description': f'主角通过医术和实力解决各种{main_conflict}冲突',
                'development': '从弱小到强大，逐步建立势力',
                'resolution': '最终成为医术界和商界的巅峰人物'
            }
        else:
            return {
                'description': '医术成长和感情发展的双重主线',
                'development': '逐步提升医术，收获多位美女青睐',
                'resolution': '成为医神级人物，拥有美满后宫'
            }

    def _find_turning_points(self, plot_data: List[Dict]) -> List[Dict]:
        """找到关键转折点"""
        turning_points = []

        for chapter_data in plot_data:
            chapter_id = chapter_data['chapter_id']

            # 标记可能的转折点
            if any(event['importance'] >= 8 for event in chapter_data['main_events']):
                turning_points.append({
                    'chapter': chapter_id,
                    'description': f'重要事件：{chapter_data["main_events"][0]["event"][:30]}...'
                })

            if chapter_data['plot_function'] == '转折':
                turning_points.append({
                    'chapter': chapter_id,
                    'description': '剧情转折点'
                })

        return turning_points[:5]

    def _categorize_sub_plots(self, plot_data: List[Dict]) -> Dict:
        """分类支线剧情"""
        sub_plots = defaultdict(list)

        for chapter_data in plot_data:
            for event in chapter_data['main_events']:
                if event['importance'] < 7:  # 不算主线的重要事件
                    if event['type'] in ['医疗', '打脸', '感情', '成长']:
                        sub_plots[event['type']].append({
                            'description': event['event'][:50],
                            'start_chapter': chapter_data['chapter_id'],
                            'characters': ['相关角色'],
                            'development': '继续发展'
                        })

        return dict(sub_plots)

    def _extract_harem_members(self, character_data: List[Dict]) -> Dict:
        """提取后宫成员信息"""
        harem_members = {}

        # 统计所有出现的人物
        all_characters = Counter()
        for chapter_data in character_data:
            for name, char_info in chapter_data['new_characters'].items():
                if char_info['type'] == '后宫':
                    all_characters[name] += 1

        # 构建后宫成员信息
        for name, count in all_characters.most_common():
            # 这里需要根据实际数据填充详细信息
            harem_members[name] = {
                'first_chapter': 1,  # 需要根据实际数据计算
                'identity': '身份设定',
                'personality': ['性格特征'],
                'appearance': '外貌描述',
                'relationship_progress': [
                    {'stage': '初遇', 'description': '初次相遇'},
                    {'stage': '熟悉', 'description': '逐渐熟悉'}
                ],
                'key_events': ['标志性事件1', '标志性事件2']
            }

        return harem_members

    def _analyze_harem_relationships(self, character_data: List[Dict]) -> List[Dict]:
        """分析后宫关系网络"""
        relationships = []

        # 简化的关系分析
        possible_pairs = [
            ('唐酥酥', '林小雪'),
            ('苏媚儿', '赵薇薇'),
            ('林小雪', '苏媚儿')
        ]

        for char1, char2 in possible_pairs:
            relationships.append({
                'character1': char1,
                'character2': char2,
                'relation_description': '竞争关系/姐妹情谊'
            })

        return relationships

    def _analyze_language_style(self, style_data: List[Dict]) -> Dict:
        """分析语言风格"""
        # 统计语言特征
        vocab_levels = Counter()
        sentence_structures = Counter()
        rhetorical_devices = Counter()

        for chapter_data in style_data:
            vocab_levels[chapter_data['language_style']['vocabulary_level']] += 1
            sentence_structures[chapter_data['language_style']['sentence_structure']] += 1
            for device in chapter_data['language_style']['rhetorical_devices']:
                rhetorical_devices[device] += 1

        return {
            'vocabulary': f"以{vocab_levels.most_common(1)[0][0]}词汇为主",
            'sentence_structure': f"偏好{sentence_structures.most_common(1)[0][0]}句式",
            'rhetorical_devices': list(rhetorical_devices.keys())
        }

    def _analyze_narrative_patterns(self, style_data: List[Dict]) -> Dict:
        """分析叙事模式"""
        # 根据风格数据推断叙事模式
        return {
            'opening': '直接从场景开始，快速进入剧情',
            'conflict': '通过打脸事件制造冲突',
            'climax': '医术展示或战斗高潮',
            'ending': '留下悬念或伏笔，引出下章'
        }

    def _analyze_scene_styles(self, style_data: List[Dict]) -> Dict:
        """分析场景风格"""
        scene_styles = {}

        # 统计场景类型
        for chapter_data in style_data:
            for scene_type, descriptions in chapter_data['scene_types'].items():
                if scene_type not in scene_styles:
                    scene_styles[scene_type] = []
                scene_styles[scene_type].extend(descriptions)

        return scene_styles

    def _generate_plot_templates(self, plot_data: List[Dict]) -> Dict:
        """生成剧情模板"""
        return {
            '开场模板': """主角低调出场，展示特殊能力
遇到美女角色，产生初步交集
反派出现，制造第一个冲突
主角化解冲突，留下悬念""",
            '发展模板': """医术展示治病救人
美女角色好感度提升
反派势力不断挑衅
主角实力逐步提升
后宫成员陆续加入""",
            '高潮模板': """重大危机出现
主角展现真正实力
反派彻底被打脸
美女角色倾心
收尾进入新阶段""",
            '收尾模板': """总结本章收获
为下章埋下伏笔
感情线有所进展
实力得到提升
留下期待"""
        }

    def _generate_character_templates(self, character_data: List[Dict]) -> Dict:
        """生成人物模板"""
        return {
            'main_character': """主角：
- 姓名：常见霸总风格姓名（如：叶辰、林轩、萧寒）
- 身份：低调的隐藏高手（神医、隐世高手）
- 性格：表面冷漠，内心温柔
- 能力：医术超群、武功高强
- 特征：从不主动惹事，但被惹必反击""",
            'harem_members': [
                "绝色总裁：高冷、傲娇、身世神秘",
                "护士妹妹：温柔、体贴、善解人意",
                "校花女神：清纯、美丽、学霸",
                "警花队长：英姿飒爽、正义感强",
                "商业女强人：成熟、独立、有魅力"
            ]
        }

    def _generate_dialogue_templates(self, style_data: List[Dict]) -> Dict:
        """生成对话模板"""
        return {
            'main_character_quotes': [
                "我只要一针！",
                "还有谁？！",
                "在我面前，你不够格",
                "医者仁心，但医术无涯",
                "小病小灾，不足挂齿"
            ],
            'villain_taunts': [
                "就凭你？",
                "你算什么东西",
                "不自量力",
                "乡巴佬进城",
                "癞蛤蟆想吃天鹅肉"
            ],
            'female_shyness': [
                "你...你流氓！",
                "讨厌啦~",
                "人家才不要",
                "你好坏哦",
                "脸都红了呢"
            ]
        }


if __name__ == '__main__':
    # 测试代码
    summarizer = Summarizer()

    # 模拟数据
    mock_plot_data = [
        {
            'chapter_id': 1,
            'title': '第1章',
            'main_events': [
                {'event': '叶枫施展医术', 'type': '医疗', 'importance': 8},
                {'event': '治疗唐酥酥', 'type': '医疗', 'importance': 7}
            ],
            'plot_function': '开端',
            'conflicts': []
        }
    ]

    mock_character_data = [
        {
            'chapter_id': 1,
            'new_characters': {
                '唐酥酥': {
                    'type': '后宫',
                    'identity': '总裁',
                    'personality': ['傲娇', '高冷'],
                    'abilities': ['管理']
                }
            }
        }
    ]

    mock_style_data = [
        {
            'chapter_id': 1,
            'language_style': {
                'vocabulary_level': '中',
                'sentence_structure': '标准',
                'rhetorical_devices': ['比喻'],
                'tone': '严肃'
            }
        }
    ]

    import asyncio

    async def test():
        reports = await summarizer.generate_final_reports(
            mock_plot_data,
            mock_character_data,
            mock_style_data
        )
        print(reports['main_plot'])

    asyncio.run(test())