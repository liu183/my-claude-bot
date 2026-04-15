#!/usr/bin/env python3
"""
演示分析器 - 展示如何分析网文章节
"""

import re
from typing import Dict, List, Any

class DemoNovelAnalyzer:
    """演示小说分析器"""

    def __init__(self):
        self.novel_dir = "D:\\迅雷下载\\筛检版"

    def get_novel_list(self) -> List[str]:
        """获取小说列表"""
        import os
        novels = []
        for file in os.listdir(self.novel_dir):
            if file.endswith('.txt'):
                novels.append(file)
        return novels

    def analyze_chapter_demo(self, chapter_text: str) -> Dict[str, Any]:
        """演示章节分析"""

        # 1. 剧情分析
        plot_events = []
        medical_count = len(re.findall(r'治病|医术|治疗|针灸|把脉', chapter_text))
        romance_count = len(re.findall(r'害羞|脸红|心跳|暧昧|爱慕', chapter_text))
        slap_count = len(re.findall(r'打脸|嘲讽|鄙视|震惊', chapter_text))

        if medical_count > 0:
            plot_events.append({
                'event': '医疗事件',
                'type': 'medical',
                'importance': medical_count * 3
            })
        if romance_count > 0:
            plot_events.append({
                'event': '感情事件',
                'type': 'romantic',
                'importance': romance_count * 2
            })
        if slap_count > 0:
            plot_events.append({
                'event': '打脸事件',
                'type': 'slap',
                'importance': slap_count * 3
            })

        # 2. 人物分析
        characters = {}

        # 提取角色
        character_names = re.findall(r'([^，。！？]{2,4})(?:是|叫|作为|这位)', chapter_text)
        for name in character_names:
            if len(name) >= 2:
                characters[name] = {
                    'type': '后宫' if any(kw in chapter_text for kw in ['总裁', '美女', '女神']) else '配角',
                    'identity': '身份待定',
                    'appearance': '外貌待定',
                    'personality': ['性格待定'],
                    'abilities': ['能力待定']
                }

        # 3. 风格分析
        word_count = len(chapter_text)
        sentence_count = len(re.split(r'[。！？]', chapter_text))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        style = {
            'vocabulary_level': '高' if avg_sentence_length > 40 else '中' if avg_sentence_length > 20 else '低',
            'sentence_structure': '复杂' if avg_sentence_length > 40 else '标准' if avg_sentence_length > 20 else '简单',
            'tone': '暧昧' if '脸红' in chapter_text or '心跳' in chapter_text else '热血' if '打脸' in chapter_text else '严肃'
        }

        return {
            'chapter_id': 1,
            'title': '演示章节',
            'plot_analysis': {
                'main_events': plot_events,
                'plot_function': '开端' if len(plot_events) == 1 else '发展',
                'character_development': [],
                'conflicts': [],
                'foreshadowing': []
            },
            'character_analysis': {
                'new_characters': characters,
                'character_development': {},
                'harem_interaction': {
                    'active_members': list(characters.keys()),
                    'interaction_type': '感情' if romance_count > 0 else '医疗' if medical_count > 0 else '待确定',
                    'progression': min(romance_count * 2, 10),
                    'new_elements': []
                }
            },
            'style_analysis': {
                'language_style': style,
                'narrative_rhythm': {
                    'overall_speed': '慢' if avg_sentence_length > 40 else '中' if avg_sentence_length > 20 else '快',
                    'pacing_changes': [],
                    'scene_transitions': []
                },
                'emotional_content': {
                    'primary_emotion': style['tone'],
                    'intensity_level': str(min(len(plot_events) * 2, 10)),
                    'emotional_progression': []
                },
                'scene_types': {
                    'medical': ['包含医疗事件'] if medical_count > 0 else [],
                    'battle': [],
                    'romantic': ['包含感情事件'] if romance_count > 0 else [],
                    'daily': []
                },
                'dialogue_features': {
                    'main_character_style': ['主角对话风格待分析'],
                    'supporting_character_styles': ['配角对话风格待分析'],
                    'memorable_quotes': ['"我只要一针！"', '"在我面前，你不够格"']
                }
            }
        }

def main():
    print("=== 网文章节分析器演示 ===\n")

    analyzer = DemoNovelAnalyzer()

    # 获取小说列表
    novels = analyzer.get_novel_list()
    print(f"找到 {len(novels)} 本小说：")
    for i, novel in enumerate(novels[:5], 1):  # 只显示前5本
        print(f"{i}. {novel}")
    if len(novels) > 5:
        print(f"... 还有 {len(novels) - 5} 本小说")

    print("\n=== 示例分析 ===")

    # 读取第一个小说的前几章
    first_novel = novels[0]
    print(f"\n分析小说: {first_novel}")

    # 读取文件内容
    try:
        with open(f"{analyzer.novel_dir}/{first_novel}", 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        print(f"\n文件大小: {len(content)} 字符")

        # 提取前几章
        chapter_pattern = r'第[一二三四五六七八九十百千万0-9]+章[^第]*'
        chapters = re.split(chapter_pattern, content)

        if len(chapters) > 1:
            # 分析第一章
            first_chapter = chapters[1][:2000]  # 取前2000字符作为示例
            result = analyzer.analyze_chapter_demo(first_chapter)

            print("\n=== 分析结果 ===")
            print(f"章节标题: {result['title']}")
            print(f"\n主要事件:")
            for event in result['plot_analysis']['main_events']:
                print(f"  - {event['event']} (重要性: {event['importance']})")

            print(f"\n人物数量: {len(result['character_analysis']['new_characters'])}")
            for name, info in result['character_analysis']['new_characters'].items():
                print(f"  - {name}: {info['type']}")

            print(f"\n风格: {result['style_analysis']['language_style']['vocabulary_level']}级词汇")
            print(f"语调: {result['style_analysis']['language_style']['tone']}")

        else:
            print("未找到章节标记")

    except Exception as e:
        print(f"读取文件时出错: {e}")

    print("\n=== 完整分析功能 ===")
    print("实际实现将包括:")
    print("1. 完整的章节分割和编号")
    print("2. 多Agent并行分析")
    print("3. 详细的人物关系网络")
    print("4. 全局的剧情结构梳理")
    print("5. 创作模板生成")
    print("6. 批量处理多本小说")

if __name__ == '__main__':
    main()