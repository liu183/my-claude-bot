#!/usr/bin/env python3
"""
剧情分析代理
分析单个章节的剧情内容
"""

import re
import yaml
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class PlotEvent:
    """剧情事件"""
    description: str
    importance: int  # 1-10
    event_type: str  # 医疗/打脸/感情/成长
    characters_involved: List[str]


class BaseAnalyzer(ABC):
    """基础分析器抽象类"""

    @abstractmethod
    async def analyze(self, chapter_id: int, title: str, content: str) -> Dict[str, Any]:
        """分析章节内容"""
        pass


class PlotAnalyzer(BaseAnalyzer):
    """剧情分析器"""

    def __init__(self):
        self.event_patterns = {
            'medical': [
                r'治病|医术|开药|针灸|把脉|诊断',
                r'治疗|治愈|手术|药方|偏方',
                r'神医|圣手|国手|专家'
            ],
            'face_slap': [
                r'打脸|打脸|啪啪',
                r'嘲讽|轻视|鄙视',
                r'震惊|震惊|不敢相信',
                r'认输|求饶|道歉'
            ],
            'romantic': [
                r'害羞|脸红|心跳',
                r'心动|喜欢|爱慕',
                r'暧昧|亲密|肌肤之亲',
                r'逆推|推倒|占便宜'
            ],
            'growth': [
                r'突破|晋级|提升',
                r'领悟|顿悟|觉醒',
                r'修炼|功法|秘籍',
                r'实力|修为|境界'
            ]
        }

    async def analyze(self, chapter_id: int, title: str, content: str) -> Dict[str, Any]:
        """分析章节剧情"""
        # 清理文本
        content = self._clean_content(content)

        # 提取主要事件
        main_events = self._extract_main_events(content)

        # 分析情节功能
        plot_function = self._analyze_plot_function(title, content)

        # 分析人物发展
        character_development = self._analyze_character_development(content)

        # 分析冲突
        conflicts = self._analyze_conflicts(content)

        # 分析伏笔
        foreshadowing = self._analyze_foreshadowing(content)

        return {
            'chapter_id': chapter_id,
            'title': title,
            'main_events': main_events,
            'plot_function': plot_function,
            'character_development': character_development,
            'conflicts': conflicts,
            'foreshadowing': foreshadowing
        }

    def _clean_content(self, content: str) -> str:
        """清理内容"""
        # 移除章节标题
        content = re.sub(r'^第[一二三四五六七八九十百千万0-9]+章[^：:]*[：:]?.*$', '', content, flags=re.MULTILINE)
        # 合并多个空白字符
        content = re.sub(r'\s+', ' ', content)
        return content.strip()

    def _extract_main_events(self, content: str) -> List[Dict[str, str]]:
        """提取主要事件"""
        events = []

        # 按段落分割
        paragraphs = content.split('。')

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 分析事件类型和重要性
            event_type = self._classify_event_type(para)
            importance = self._calculate_importance(para)

            if importance >= 5:  # 只保留重要事件
                events.append({
                    'event': para,
                    'type': event_type,
                    'importance': importance
                })

        return events

    def _classify_event_type(self, text: str) -> str:
        """分类事件类型"""
        scores = {}

        for event_type, patterns in self.event_patterns.items():
            scores[event_type] = 0
            for pattern in patterns:
                matches = re.findall(pattern, text)
                scores[event_type] += len(matches)

        # 返回得分最高的事件类型
        return max(scores, key=scores.get)

    def _calculate_importance(self, text: str) -> int:
        """计算事件重要性"""
        importance = 5  # 基础分

        # 关键词加分
        importance_keywords = [
            (r'震惊|轰动|引爆', 3),
            (r'突破|晋级|蜕变', 2),
            (r'重要|关键|决定', 2),
            (r'首次|第一次|初次', 1),
            (r'高潮|顶点|巅峰', 3),
            (r'转折|变化|改变', 2)
        ]

        for pattern, score in importance_keywords:
            matches = re.findall(pattern, text)
            importance += len(matches) * score

        # 限制分数范围
        return min(importance, 10)

    def _analyze_plot_function(self, title: str, content: str) -> str:
        """分析情节功能"""
        title_lower = title.lower()
        content_lower = content.lower()

        # 根据标题判断
        if '开始' in title_lower or '之初' in title_lower:
            return '开端'
        elif '结局' in title_lower or '终章' in title_lower:
            return '结局'
        elif '转折' in title_lower or '变故' in title_lower:
            return '转折'
        elif '高潮' in title_lower or '决战' in title_lower:
            return '高潮'
        elif '回忆' in title_lower or '往事' in title_lower:
            return '回忆'

        # 根据内容判断
        if '新角色' in content_lower or '第一次' in content_lower:
            return '引入'
        elif '矛盾' in content_lower or '冲突' in content_lower:
            return '冲突'
        elif '解决' in content_lower or '平息' in content_lower:
            return '解决'
        elif '铺垫' in content_lower or '伏笔' in content_lower:
            return '铺垫'

        return '发展'

    def _analyze_character_development(self, content: str) -> List[Dict[str, str]]:
        """分析人物发展"""
        developments = []

        # 查找人物变化
        character_patterns = [
            (r'(\w+)\s*变得', '变化'),
            (r'(\w+)\s*感觉', '感受'),
            (r'(\w+)\s*认为', '认知'),
            (r'(\w+)\s*决定', '决心')
        ]

        for pattern, dev_type in character_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) > 1:  # 确保找到完整匹配
                    developments.append({
                        'character': match[0],
                        'type': dev_type,
                        'detail': match[1]
                    })

        return developments

    def _analyze_conflicts(self, content: str) -> List[Dict[str, str]]:
        """分析冲突"""
        conflicts = []

        # 冲突关键词
        conflict_keywords = [
            ('医术', '医疗冲突'),
            ('实力', '武力冲突'),
            ('地位', '地位冲突'),
            ('感情', '感情冲突'),
            ('名誉', '名誉冲突'),
            ('利益', '利益冲突')
        ]

        for keyword, conflict_type in conflict_keywords:
            if keyword in content:
                # 找出冲突参与者
                participants = re.findall(r'(\w+)\s*(?:和|vs|VS)\s*(\w+)', content)
                if participants:
                    conflicts.append({
                        'type': conflict_type,
                        'participants': [p for pair in participants for p in pair],
                        'resolution': 'pending'  # 暂时标记为待解决
                    })

        return conflicts

    def _analyze_foreshadowing(self, content: str) -> List[str]:
        """分析伏笔"""
        foreshadowing = []

        # 伏笔关键词
        foreshadowing_patterns = [
            r'预示|暗示|预示着',
            r'将来|以后|未来',
            r'将会|将要|可能',
            r'未知|神秘|谜团'
        ]

        for pattern in foreshadowing_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # 获取包含伏笔的句子
                sentences = re.split(r'[。！？]', content)
                for sentence in sentences:
                    if re.search(pattern, sentence):
                        foreshadowing.append(sentence.strip())

        return foreshadowing[:5]  # 返回前5个伏笔


if __name__ == '__main__':
    # 测试代码
    analyzer = PlotAnalyzer()
    content = """
    叶枫施展医术，治愈了绝色总裁唐酥酥的怪病。
    唐酥酥震惊于叶枫的医术，开始对他产生好感。
    反派赵总嘲笑叶枫是穷小子，结果被叶枫打脸。
    """
    result = analyzer.analyze(1, "第1章 玄阴玄阳", content)
    print(yaml.dump(result, default_flow_style=False))