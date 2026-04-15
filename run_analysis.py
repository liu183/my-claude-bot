#!/usr/bin/env python3
"""
完整运行分析器 - 不需要外部依赖
"""

import re
import os
import json
from typing import Dict, List, Any
from datetime import datetime

class SimpleNovelAnalyzer:
    """简化的小说分析器 - 不依赖外部库"""

    def __init__(self, novel_dir: str):
        self.novel_dir = novel_dir
        self.supported_novels = []
        self.analysis_results = {}

    def find_novels(self) -> List[str]:
        """查找所有txt小说文件"""
        novels = []
        for file in os.listdir(self.novel_dir):
            if file.endswith('.txt'):
                novels.append(file)
        self.supported_novels = sorted(novels)
        return novels

    def read_novel(self, novel_name: str, max_chars: int = 50000) -> str:
        """读取小说内容（限制字符数以避免内存问题）"""
        try:
            with open(os.path.join(self.novel_dir, novel_name), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 如果内容太长，只取前50KB
                if len(content) > max_chars:
                    content = content[:max_chars]
                    print(f"警告: {novel_name} 内容过长，只分析前{max_chars}字符")
                return content
        except Exception as e:
            print(f"读取小说 {novel_name} 时出错: {e}")
            return ""

    def extract_chapters(self, content: str) -> List[Dict]:
        """提取章节"""
        chapters = []
        chapter_pattern = r'第[一二三四五六七八九十百千万0-9]+[章卷部][^第]*'
        matches = list(re.finditer(chapter_pattern, content))

        if not matches:
            # 如果没有找到章节标记，按段落分割
            paragraphs = content.split('\n')
            chapters.append({
                'chapter_id': 1,
                'title': '全文',
                'content': content,
                'start_pos': 0,
                'end_pos': len(content)
            })
        else:
            for i, match in enumerate(matches[:100]):  # 只取前100章
                start_pos = match.start()
                end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)

                chapter_content = content[start_pos:end_pos]

                chapters.append({
                    'chapter_id': i + 1,
                    'title': match.group(),
                    'content': chapter_content,
                    'start_pos': start_pos,
                    'end_pos': end_pos
                })

        return chapters

    def analyze_chapter(self, chapter: Dict) -> Dict:
        """分析单个章节"""
        content = chapter['content']
        result = {
            'chapter_id': chapter['chapter_id'],
            'title': chapter['title'],
            'analysis': {}
        }

        # 1. 剧情分析
        plot_analysis = self.analyze_plot(content)
        result['analysis']['plot'] = plot_analysis

        # 2. 人物分析
        character_analysis = self.analyze_characters(content)
        result['analysis']['characters'] = character_analysis

        # 3. 风格分析
        style_analysis = self.analyze_style(content)
        result['analysis']['style'] = style_analysis

        return result

    def analyze_plot(self, content: str) -> Dict:
        """剧情分析"""
        events = []

        # 医疗事件
        medical_keywords = ['治病', '医术', '治疗', '针灸', '把脉', '诊断', '手术', '药方']
        medical_count = sum(content.count(kw) for kw in medical_keywords)
        if medical_count > 0:
            events.append({
                'type': '医疗',
                'count': medical_count,
                'importance': min(medical_count * 3, 10)
            })

        # 感情事件
        romance_keywords = ['害羞', '脸红', '心跳', '暧昧', '爱慕', '喜欢', '心动']
        romance_count = sum(content.count(kw) for kw in romance_keywords)
        if romance_count > 0:
            events.append({
                'type': '感情',
                'count': romance_count,
                'importance': min(romance_count * 2, 10)
            })

        # 打脸事件
        slap_keywords = ['打脸', '嘲讽', '鄙视', '震惊', '不敢相信', '认输']
        slap_count = sum(content.count(kw) for kw in slap_keywords)
        if slap_count > 0:
            events.append({
                'type': '打脸',
                'count': slap_count,
                'importance': min(slap_count * 3, 10)
            })

        # 成长事件
        growth_keywords = ['突破', '晋级', '提升', '领悟', '功法', '实力']
        growth_count = sum(content.count(kw) for kw in growth_keywords)
        if growth_count > 0:
            events.append({
                'type': '成长',
                'count': growth_count,
                'importance': min(growth_count * 2, 10)
            })

        return {
            'total_events': len(events),
            'events': events,
            'main_plot': '医疗' if medical_count > 0 else '感情' if romance_count > 0 else '成长',
            'intensity': sum(e['importance'] for e in events)
        }

    def analyze_characters(self, content: str) -> Dict:
        """人物分析"""
        characters = {}
        harem_members = []

        # 提取角色名
        name_patterns = [
            r'([^，。！？]{2,4})(?:是|叫|作为|这位)',
            r'([^，。！？]{2,4})(?:总裁|千金|美女|女神|护士|医生|学生|老师)',
        ]

        for pattern in name_patterns:
            names = re.findall(pattern, content)
            for name in names:
                if len(name) >= 2 and name not in ['叶枫', '主角']:
                    if any(kw in content for kw in ['总裁', '千金', '美女', '女神', '护士']):
                        harem_members.append(name)
                        characters[name] = {
                            'type': '后宫',
                            'identity': '身份待定',
                            'interaction_count': content.count(name)
                        }
                    else:
                        characters[name] = {
                            'type': '配角',
                            'identity': '身份待定',
                            'interaction_count': content.count(name)
                        }

        return {
            'total_characters': len(characters),
            'harem_members': harem_members,
            'main_characters': list(characters.keys())[:10],  # 前10个主要角色
            'harem_count': len(harem_members)
        }

    def analyze_style(self, content: str) -> Dict:
        """风格分析"""
        # 词汇复杂度
        word_count = len(content.split())
        sentence_count = len(re.split(r'[。！？]', content))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # 词汇等级
        high_level_words = ['玄妙', '精湛', '造诣', '深邃', '绝世', '惊天']
        high_count = sum(content.count(word) for word in high_level_words)

        if high_count > 5:
            vocab_level = '高'
        elif high_count > 2:
            vocab_level = '中'
        else:
            vocab_level = '低'

        # 句式结构
        if avg_sentence_length > 40:
            sentence_structure = '复杂'
        elif avg_sentence_length > 20:
            sentence_structure = '标准'
        else:
            sentence_structure = '简单'

        # 语调
        if any(kw in content for kw in ['害羞', '脸红', '心跳']):
            tone = '暧昧'
        elif any(kw in content for kw in ['打脸', '震惊']):
            tone = '热血'
        elif any(kw in content for kw in ['治病', '医术']):
            tone = '专业'
        else:
            tone = '严肃'

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'vocabulary_level': vocab_level,
            'sentence_structure': sentence_structure,
            'tone': tone
        }

    def analyze_novel(self, novel_name: str, max_chapters: int = 10) -> Dict:
        """分析整本小说"""
        print(f"\n正在分析: {novel_name}")

        # 读取内容
        content = self.read_novel(novel_name)
        if not content:
            return {'error': '无法读取小说内容'}

        # 提取章节
        chapters = self.extract_chapters(content)
        chapters_to_analyze = chapters[:max_chapters]

        # 分析所有章节
        chapter_results = []
        total_plot_intensity = 0
        total_harem_members = set()
        all_styles = []

        for chapter in chapters_to_analyze:
            result = self.analyze_chapter(chapter)
            chapter_results.append(result)

            # 累计统计数据
            total_plot_intensity += result['analysis']['plot']['intensity']
            if 'characters' in result['analysis']:
                total_harem_members.update(result['analysis']['characters']['harem_members'])
            all_styles.append(result['analysis']['style'])

        # 生成最终报告
        novel_result = {
            'novel_name': novel_name,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chapters_analyzed': len(chapter_results),
            'total_chapters_found': len(chapters),
            'summary': {
                'avg_plot_intensity': round(total_plot_intensity / len(chapter_results), 1) if chapter_results else 0,
                'unique_harem_members': len(total_harem_members),
                'main_style': self.get_dominant_style(all_styles),
                'genre': '都市神医'
            },
            'chapters': chapter_results
        }

        return novel_result

    def get_dominant_style(self, styles: List[Dict]) -> str:
        """获取主要风格"""
        tone_counts = {}
        for style in styles:
            tone = style.get('tone', 'unknown')
            tone_counts[tone] = tone_counts.get(tone, 0) + 1

        return max(tone_counts, key=tone_counts.get) if tone_counts else 'unknown'

    def save_results(self, results: Dict, output_dir: str):
        """保存分析结果"""
        os.makedirs(output_dir, exist_ok=True)

        # 保存详细结果
        detailed_file = os.path.join(output_dir, 'detailed_results.json')
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # 生成汇总报告
        summary_file = os.path.join(output_dir, 'summary_report.md')
        self.generate_summary_report(results, summary_file)

        print(f"\n分析结果已保存到: {output_dir}")
        print(f"- 详细数据: {detailed_file}")
        print(f"- 汇总报告: {summary_file}")

    def generate_summary_report(self, results: Dict, output_file: str):
        """生成Markdown汇总报告"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"""# 网文小说分析报告

## 基本信息
- 分析时间: {results['analysis_date']}
- 分析小说数: {len(results.get('novels', []))}
- 分析章节数: {results.get('total_chapters_analyzed', 0)}

## 整体统计

### 小说分布
| 小说名 | 分析章节数 | 主要风格 | 后宫成员数 |
|-------|-----------|---------|-----------|""")

            for novel_name, data in results.get('novels', {}).items():
                if 'error' not in data:
                    summary = data.get('summary', {})
                    f.write(f"\n| {novel_name} | {data.get('chapters_analyzed', 0)} | {summary.get('main_style', 'unknown')} | {summary.get('unique_harem_members', 0)} |")

            f.write(f"""

## 创作模式总结

### 常见套路
1. **开场模式**: 主角低调出场，意外相遇美女
2. **发展模式**: 医术治病 → 打脸反派 → 美女倾心
3. **高潮模式**: 关键时刻，主角展现实力
4. **收尾模式**: 为下章埋下伏笔

### 人物模板
- **主角**: 低调高手，医术超群，从不主动惹事
- **后宫类型**:
  - 绝色总裁：高冷傲娇
  - 护士妹妹：温柔体贴
  - 校花女神：清纯美丽
  - 警花队长：英姿飒爽

### 对话模式
- 主角金句: "我只要一针！"、"在我面前，你不够格"
- 反派挑衅: "就凭你？"、"乡巴佬进城"
- 女主羞涩: "你...你流氓！"、"讨厌啦~"

## 创作建议

1. **章节安排**: 每章保持1000-2000字，避免过长
2. **节奏控制**: 快节奏为主，适当加入慢节奏调节
3. **感情线**: 逐步升温，避免突兀
4. **打脸节奏**: 每3-5章安排一次打脸情节
5. **医术展示**: 结合专业术语和通俗易懂的解释

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
""")

def main():
    """主函数"""
    print("=== 网文小说批量分析器 ===\n")

    # 设置小说目录
    novel_dir = "D:\\迅雷下载\\筛检版"
    if not os.path.exists(novel_dir):
        print(f"错误: 找不到小说目录 {novel_dir}")
        return

    # 创建分析器
    analyzer = SimpleNovelAnalyzer(novel_dir)

    # 查找所有小说
    novels = analyzer.find_novels()
    if not novels:
        print("错误: 目录下没有找到.txt文件")
        return

    print(f"找到 {len(novels)} 本小说")

    # 分析所有小说
    all_results = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'novels': {}
    }

    # 限制分析的小说数量以避免时间过长
    novels_to_analyze = novels[:3]  # 只分析前3本作为示例
    print(f"\n将分析前 {len(novels_to_analyze)} 本小说")

    for novel_name in novels_to_analyze:
        try:
            result = analyzer.analyze_novel(novel_name, max_chapters=5)  # 每本只分析前5章
            all_results['novels'][novel_name] = result

            # 打印简要结果
            if 'error' not in result:
                summary = result.get('summary', {})
                print(f"✅ {novel_name}: 分析了{result['chapters_analyzed']}章, "
                      f"风格:{summary.get('main_style', 'unknown')}, "
                      f"后宫:{summary.get('unique_harem_members', 0)}人")
            else:
                print(f"❌ {novel_name}: {result['error']}")

        except Exception as e:
            print(f"❌ 分析 {novel_name} 时出错: {e}")
            all_results['novels'][novel_name] = {'error': str(e)}

    # 保存结果
    output_dir = os.path.join(os.path.dirname(__file__), 'analysis_results')
    analyzer.save_results(all_results, output_dir)

    # 显示分析摘要
    print("\n=== 分析完成 ===")
    successful = sum(1 for r in all_results['novels'].values() if 'error' not in r)
    print(f"成功分析: {successful}/{len(novels_to_analyze)} 本小说")

    if successful > 0:
        print(f"\n详细结果请查看: {output_dir}/summary_report.md")

if __name__ == '__main__':
    main()