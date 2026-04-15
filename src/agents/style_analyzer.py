#!/usr/bin/env python3
"""
风格分析代理
分析单个章节的写作风格特点
"""

import re
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """基础分析器抽象类"""

    @abstractmethod
    async def analyze(self, chapter_id: int, title: str, content: str) -> Dict[str, Any]:
        """分析章节内容"""
        pass


class StyleAnalyzer(BaseAnalyzer):
    """风格分析器"""

    def __init__(self):
        # 词汇难度等级
        self.vocabulary_levels = {
            'high': ['玄妙', '精妙', '造诣', '深邃', '精湛', '登峰造极', '炉火纯青'],
            'medium': ['厉害', '强大', '不错', '挺好', '可以', '还行'],
            'low': ['简单', '普通', '一般', '还行', '凑合']
        }

        # 句式复杂度模式
        self.sentence_patterns = {
            'complex': r'[^。！？]+[，；][^。！？]+[，；][^。！？]+',
            'standard': r'[^。！？]+[，][^。！？]+',
            'simple': r'[^。！？]+[。！？]'
        }

        # 情感类型关键词
        self.emotion_keywords = {
            '热血': ['热血', '沸腾', '燃烧', '激昂', '澎湃', '热血沸腾'],
            '暧昧': ['暧昧', '心跳', '脸红', '害羞', '亲密', '肌肤之亲'],
            '紧张': ['紧张', '焦急', '担忧', '害怕', '恐惧', '提心吊胆'],
            '温馨': ['温馨', '温暖', '舒适', '惬意', '安心', '幸福'],
            '幽默': ['搞笑', '滑稽', '可笑', '好笑', '有趣', '逗乐'],
            '严肃': ['严肃', '认真', '庄重', '正式', '严肃认真']
        }

        # 场景类型关键词
        self.scene_keywords = {
            'medical': ['治病', '医术', '治疗', '针灸', '把脉', '诊断', '手术', '药方'],
            'battle': ['战斗', '对决', '较量', '比试', '打斗', '冲突', '争斗'],
            'romantic': ['暧昧', '心跳', '脸红', '害羞', '亲密', '肌肤之亲', '逆推'],
            'daily': ['生活', '日常', '吃饭', '睡觉', '走路', '聊天', '工作']
        }

        # 金句模式
        self.quote_patterns = [
            r'(.{0,30}?)(感叹|感悟|金句|名言|道理)(.{0,30}?)',
            r'(.{0,30}?)(（.{0,30}?)）',  # 括号内的句子
            r'"([^"]+)"',  # 引号内的句子
            r'「([^"]+)」'  # 引号内的句子
        ]

    async def analyze(self, chapter_id: int, title: str, content: str) -> Dict[str, Any]:
        """分析章节风格"""
        content = self._clean_content(content)

        # 分析语言风格
        language_style = self._analyze_language_style(content)

        # 分析叙事节奏
        narrative_rhythm = self._analyze_narrative_rhythm(content)

        # 分析情感内容
        emotional_content = self._analyze_emotional_content(content)

        # 分析场景类型
        scene_types = self._analyze_scene_types(content)

        # 分析对话特色
        dialogue_features = self._analyze_dialogue_features(content)

        return {
            'chapter_id': chapter_id,
            'title': title,
            'language_style': language_style,
            'narrative_rhythm': narrative_rhythm,
            'emotional_content': emotional_content,
            'scene_types': scene_types,
            'dialogue_features': dialogue_features
        }

    def _clean_content(self, content: str) -> str:
        """清理内容"""
        # 移除章节标题
        content = re.sub(r'^第[一二三四五六七八九十百千万0-9]+章[^：:]*[：:]?.*$', '', content, flags=re.MULTILINE)
        # 合并多个空白字符
        content = re.sub(r'\s+', ' ', content)
        return content.strip()

    def _analyze_language_style(self, content: str) -> Dict[str, str]:
        """分析语言风格"""
        # 分析词汇难度
        vocab_score = 0
        for level, words in self.vocabulary_levels.items():
            for word in words:
                vocab_score += content.count(word) * (3 if level == 'high' else 2 if level == 'medium' else 1)

        # 确定词汇水平
        if vocab_score > 20:
            vocabulary_level = '高'
        elif vocab_score > 10:
            vocabulary_level = '中'
        else:
            vocabulary_level = '低'

        # 分析句式结构
        complex_count = len(re.findall(self.sentence_patterns['complex'], content))
        standard_count = len(re.findall(self.sentence_patterns['standard'], content))
        simple_count = len(re.findall(self.sentence_patterns['simple'], content))

        total_sentences = complex_count + standard_count + simple_count
        if total_sentences == 0:
            sentence_structure = '标准'
        else:
            if complex_count / total_sentences > 0.3:
                sentence_structure = '复杂'
            elif simple_count / total_sentences > 0.7:
                sentence_structure = '简单'
            else:
                sentence_structure = '标准'

        # 分析修辞手法
        rhetorical_devices = []
        if '比喻' in content or '如' in content:
            rhetorical_devices.append('比喻')
        if '拟人' in content or '似乎' in content:
            rhetorical_devices.append('拟人')
        if '夸张' in content or '极度' in content:
            rhetorical_devices.append('夸张')
        if '排比' in content or '一连串' in content:
            rhetorical_devices.append('排比')

        # 确定语调
        tone_keywords = ['幽默', '搞笑', '逗乐']
        if any(keyword in content for keyword in tone_keywords):
            tone = '幽默'
        else:
            tone = '严肃'

        return {
            'vocabulary_level': vocabulary_level,
            'sentence_structure': sentence_structure,
            'rhetorical_devices': rhetorical_devices,
            'tone': tone
        }

    def _analyze_narrative_rhythm(self, content: str) -> Dict[str, Any]:
        """分析叙事节奏"""
        # 计算句子长度
        sentences = re.split(r'[。！？]', content)
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0

        # 判断整体速度
        if avg_sentence_length > 50:
            overall_speed = '慢'
        elif avg_sentence_length > 20:
            overall_speed = '中'
        else:
            overall_speed = '快'

        # 查找节奏变化点
        pacing_changes = []
        sentences = re.split(r'[。！？]', content)

        for i, sentence in enumerate(sentences[:-1]):
            # 检查前后句子长度差异
            next_sentence = sentences[i + 1]
            if abs(len(sentence) - len(next_sentence)) > 30:
                pacing_changes.append(f"第{i+1}句：长度变化显著")

        # 分析场景转换
        scene_transitions = []
        transition_keywords = ['突然', '忽然', '紧接着', '随后', '然后', '']
        for keyword in transition_keywords:
            if keyword in content:
                scene_transitions.append(f"使用'{keyword}'进行场景转换")

        return {
            'overall_speed': overall_speed,
            'pacing_changes': pacing_changes[:5],  # 只取前5个
            'scene_transitions': scene_transitions[:3]  # 只取前3个
        }

    def _analyze_emotional_content(self, content: str) -> Dict[str, Any]:
        """分析情感内容"""
        # 分析情感类型和强度
        emotion_scores = {}
        for emotion_type, keywords in self.emotion_keywords.items():
            score = sum(content.count(keyword) for keyword in keywords)
            emotion_scores[emotion_type] = score

        # 选择主要情感
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            intensity = min(emotion_scores[primary_emotion] * 2, 10)
        else:
            primary_emotion = '平淡'
            intensity = 5

        # 分析情感递进
        emotional_progression = []
        if '开始' in content and '越来越' in content:
            emotional_progression.append('情感开始升温')
        if '高潮' in content or '顶点' in content:
            emotional_progression.append('情感达到高潮')
        if '平息' in content or '冷静' in content:
            emotional_progression.append('情感逐渐平息')

        return {
            'primary_emotion': primary_emotion,
            'intensity_level': str(intensity),
            'emotional_progression': emotional_progression
        }

    def _analyze_scene_types(self, content: str) -> Dict[str, List[str]]:
        """分析场景类型"""
        scene_types = {
            'medical': [],
            'battle': [],
            'romantic': [],
            'daily': []
        }

        # 分析医疗场景
        medical_matches = re.findall(f"({'|'.join(self.scene_keywords['medical'])})", content)
        if medical_matches:
            scene_types['medical'].append('包含医疗事件')
            # 评估专业度
            professional_terms = ['玄阴', '玄阳', '针灸', '把脉', '诊断', '手术']
            professional_score = sum(content.count(term) for term in professional_terms)
            scene_types['medical'].append(f'专业度: {min(professional_score * 2, 10)}/10')

        # 分析战斗场景
        battle_matches = re.findall(f"({'|'.join(self.scene_keywords['battle'])})", content)
        if battle_matches:
            scene_types['battle'].append('包含战斗事件')
            # 评估紧张度
            intensity_words = ['激烈', '狂暴', '凶猛', '惊险', '紧张']
            intensity_score = sum(content.count(word) for word in intensity_words)
            scene_types['battle'].append(f'紧张度: {min(intensity_score * 2, 10)}/10')

        # 分析感情场景
        romantic_matches = re.findall(f"({'|'.join(self.scene_keywords['romantic'])})", content)
        if romantic_matches:
            scene_types['romantic'].append('包含感情事件')
            # 评估浪漫度
            romantic_words = ['害羞', '脸红', '心跳', '暧昧', '甜蜜']
            romantic_score = sum(content.count(word) for word in romantic_words)
            scene_types['romantic'].append(f'浪漫度: {min(romantic_score * 3, 10)}/10')

        # 分析生活场景
        if '生活' in content or '日常' in content:
            scene_types['daily'].append('包含日常生活场景')

        return scene_types

    def _analyze_dialogue_features(self, content: str) -> Dict[str, List[str]]:
        """分析对话特色"""
        # 提取对话
        dialogues = re.findall(r'([^"「」\n]+)[："「」](.+?)[："」」]', content)

        # 分析主角对话风格
        main_character_style = []
        if dialogues:
            # 检查对话长度
            avg_dialogue_length = sum(len(d[1]) for d in dialogues) / len(dialogues)
            if avg_dialogue_length > 20:
                main_character_style.append('对话较长，善于表达')
            else:
                main_character_style.append('对话简洁，直击要点')

        # 查找标志性金句
        memorable_quotes = []
        for pattern in self.quote_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    for item in match:
                        if len(item) > 5 and len(item) < 50:
                            memorable_quotes.append(item)
                else:
                    if len(match) > 5 and len(match) < 50:
                        memorable_quotes.append(match)

        # 去重并限制数量
        memorable_quotes = list(set(memorable_quotes))[:5]

        return {
            'main_character_style': main_character_style,
            'supporting_character_styles': ['配角对话风格待分析'],
            'memorable_quotes': memorable_quotes
        }


if __name__ == '__main__':
    # 测试代码
    analyzer = StyleAnalyzer()
    content = """
    叶枫施展绝世医术，玄阴玄阳功法运转，精准治愈了绝色总裁唐酥酥的怪病。
    唐酥酥害羞地看着叶枫，心跳加速，脸颊泛红，对他产生浓浓爱意。
    反派赵总嘲讽叶枫是穷小子，结果被叶枫当场打脸，震惊全场。
    """
    result = analyzer.analyze(1, "第1章 玄阴玄阳", content)
    print(yaml.dump(result, default_flow_style=False))