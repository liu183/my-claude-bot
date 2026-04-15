#!/usr/bin/env python3
"""
人物分析代理
分析单个章节的人物相关信息
"""

import re
import yaml
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from plot_analyzer import BaseAnalyzer


@dataclass
class Character:
    """角色数据"""
    name: str
    type: str  # 主角/后宫/反派/配角
    identity: str
    appearance: str
    personality: List[str]
    abilities: List[str]
    relationships: Dict[str, Dict[str, str]]


class CharacterAnalyzer(BaseAnalyzer):
    """人物分析器"""

    def __init__(self):
        # 常见角色类型关键词
        self.character_type_keywords = {
            '主角': ['主角', '主人公', '男主', '叶枫', '主角名称'],
            '后宫': ['美女', '女神', '总裁', '千金', '护士', '学生', '老师', '绝色'],
            '反派': ['反派', '仇人', '敌人', '对手', '赵总', '反派名称'],
            '配角': ['朋友', '伙伴', '同学', '医生', '路人']
        }

        # 后宫成员常见特征
        self.harem_traits = {
            '温柔': ['温柔', '贤惠', '体贴', '善解人意'],
            '傲娇': ['傲娇', '高冷', '傲慢', '毒舌'],
            '冷艳': ['冷艳', '冰山', '高冷', '冷酷'],
            '活泼': ['活泼', '开朗', '阳光', '可爱'],
            '成熟': ['成熟', '稳重', '知性', '优雅'],
            '清纯': ['清纯', '纯真', '天真', '可爱']
        }

    async def analyze(self, chapter_id: int, title: str, content: str) -> Dict[str, Any]:
        """分析章节人物"""
        content = self._clean_content(content)

        # 提取新出现的人物
        new_characters = self._extract_new_characters(content)

        # 分析人物发展
        character_development = self._analyze_character_development(content)

        # 分析后宫互动
        harem_interaction = self._analyze_harem_interaction(content)

        return {
            'chapter_id': chapter_id,
            'title': title,
            'new_characters': new_characters,
            'character_development': character_development,
            'harem_interaction': harem_interaction
        }

    def _clean_content(self, content: str) -> str:
        """清理内容"""
        # 移除章节标题
        content = re.sub(r'^第[一二三四五六七八九十百千万0-9]+章[^：:]*[：:]?.*$', '', content, flags=re.MULTILINE)
        # 合并多个空白字符
        content = re.sub(r'\s+', ' ', content)
        return content.strip()

    def _extract_new_characters(self, content: str) -> Dict[str, Dict[str, str]]:
        """提取新出现的人物"""
        new_characters = {}

        # 查找人物描述
        character_patterns = [
            # 格式1：人物 + 是 + 身份描述
            (r'([^，。！？]+)\s*(?:是|叫做|名叫)\s*([^，。！？]+)', 1, 2),
            # 格式2：身份 + 人物
            (r'([^，。！？]+(?:总裁|千金|护士|医生|老师|学生))\s*([^，。！？]+)', 2, 1),
            # 格式3：直接出现人物名
            (r'([^，。！？]{2,4})(?:说|道|想|感觉)', 1, 1)
        ]

        # 已知人物集合（避免重复）
        known_characters = {'叶枫', '主角', '作者'}

        for pattern, name_idx, identity_idx in character_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= max(name_idx, identity_idx):
                    name = match[name_idx - 1].strip()
                    identity = match[identity_idx - 1].strip() if identity_idx > name_idx else name

                    # 过滤掉已知人物和无意义名称
                    if name not in known_characters and len(name) >= 2 and '的' not in name:
                        character_type = self._classify_character_type(name, content)
                        new_characters[name] = {
                            'type': character_type,
                            'role': '章节作用',
                            'first_appearance': True,
                            'identity': identity,
                            'appearance': '待补充',
                            'personality': self._extract_personality(name, content),
                            'abilities': self._extract_abilities(name, content),
                            'relationships': self._extract_relationships(name, content)
                        }

        return new_characters

    def _classify_character_type(self, name: str, content: str) -> str:
        """分类角色类型"""
        name_lower = name.lower()
        content_lower = content.lower()

        # 主角判断
        if '主角' in name_lower or '男主' in name_lower or name == '叶枫':
            return '主角'

        # 后宫成员判断
        harem_keywords = ['总裁', '千金', '美女', '女神', '护士', '学生', '老师']
        if any(keyword in content_lower for keyword in harem_keywords):
            # 检查是否是女性角色
            female_indicators = ['她', '美女', '女神', '小姐', '女士']
            if any(indicator in content_lower for indicator in female_indicators):
                return '后宫'

        # 反派判断
       反派_keywords = ['反派', '仇人', '敌人', '对手', '反派名称', '赵总']
        if any(keyword in content_lower for keyword in反派_keywords):
            return '反派'

        return '配角'

    def _extract_personality(self, name: str, content: str) -> List[str]:
        """提取人物性格"""
        personality = []
        name_lower = name.lower()

        # 查找性格描述
        personality_patterns = [
            (f'{name}(.{{0,20}}?)(温柔|体贴|贤惠|傲娇|高冷|活泼|开朗|冷漠|善良|邪恶)', '温柔体贴贤惠傲娇高冷活泼开朗冷漠善良邪恶'),
            (f'{name}(.{{0,20}}?)(坚定|果断|犹豫|勇敢|胆怯|聪明|愚蠢)', '坚定果断犹豫勇敢胆怯聪明愚蠢'),
            (f'{name}(.{{0,20}}?)(正义|邪恶|正直|狡猾|真诚|虚伪)', '正义邪恶正直狡猾真诚虚伪')
        ]

        for pattern, traits in personality_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if match[1] in traits:
                    personality.append(match[1])

        # 如果没有找到，使用默认性格
        if not personality:
            personality = ['普通']

        return list(set(personality))  # 去重

    def _extract_abilities(self, name: str, content: str) -> List[str]:
        """提取人物能力"""
        abilities = []
        name_lower = name.lower()

        # 查找能力描述
        ability_patterns = [
            (f'{name}(.{{0,20}}?)(医术|医术|治疗|治愈|针灸|手术)', '医术'),
            (f'{name}(.{{0,20}}?)(武功|实力|修为|功法)', '武功'),
            (f'{name}(.{{0,20}}?)(智慧|聪明|聪明才智)', '智慧'),
            (f'{name}(.{{0,20}}?)(经商|管理|经营)', '经商')
        ]

        for pattern, ability in ability_patterns:
            matches = re.findall(pattern, content)
            if matches:
                abilities.append(ability)

        if not abilities:
            abilities = ['普通']

        return list(set(abilities))

    def _extract_relationships(self, name: str, content: str) -> Dict[str, Dict[str, str]]:
        """提取人物关系"""
        relationships = {}

        # 查找与主角的关系
        if '主角' in content or '叶枫' in content:
            relationships['主角'] = {
                'type': '关系类型',
                'status': '关系状态',
                'reason': '原因'
            }

        return relationships

    def _analyze_character_development(self, content: str) -> Dict[str, Dict[str, str]]:
        """分析人物发展"""
        development = {}

        # 查找人物变化
        change_patterns = [
            (r'(\w+)\s*变得\s*([^。！？]+)', '变化'),
            (r'(\w+)\s*感觉\s*([^。！？]+)', '感受'),
            (r'(\w+)\s*决定\s*([^。！？]+)', '决心'),
            (r'(\w+)\s*开始\s*([^。！？]+)', '开始')
        ]

        for pattern, change_type in change_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                character = match[0]
                detail = match[1]

                if character not in development:
                    development[character] = {'changes': [], 'relationships': []}

                development[character]['changes'].append({
                    'type': change_type,
                    'detail': detail
                })

                # 同时分析关系变化
                if '喜欢' in detail or '爱慕' in detail:
                    development[character]['relationships'].append({
                        'target': '主角',
                        'change': '关系变好',
                        'reason': '产生好感'
                    })

        return development

    def _analyze_harem_interaction(self, content: str) -> Dict[str, Any]:
        """分析后宫互动"""
        interaction = {
            'active_members': [],
            'interaction_type': '待确定',
            'progression': 0,
            'new_elements': []
        }

        # 查找活跃的后宫成员
        harem_keywords = ['总裁', '千金', '美女', '女神', '护士', '学生', '老师', '她']
        active_members = set()

        for keyword in harem_keywords:
            if keyword in content:
                # 查找具体的人物
                characters = re.findall(r'([^。！？]{2,4})' + keyword, content)
                active_members.update(characters)

        interaction['active_members'] = list(active_members)

        # 分析互动类型
        interaction_types = {
            '感情': ['喜欢', '爱慕', '心动', '害羞', '脸红'],
            '医疗': ['治疗', '医术', '针灸', '把脉'],
            '战斗': ['战斗', '对决', '较量', '比试']
        }

        interaction_type_scores = {}
        for itype, keywords in interaction_types.items():
            score = sum(content.count(keyword) for keyword in keywords)
            interaction_type_scores[itype] = score

        # 选择得分最高的互动类型
        if interaction_type_scores:
            interaction['interaction_type'] = max(interaction_type_scores, key=interaction_type_scores.get)

        # 分析感情进展
        progression_keywords = ['心动', '喜欢', '爱慕', '亲密', '肌肤之亲', '逆推']
        progression = 0
        for keyword in progression_keywords:
            progression += content.count(keyword) * 2

        interaction['progression'] = min(progression, 10)  # 限制在0-10

        # 提取新的暧昧元素
        new_elements = []
       暧昧_patterns = [
            r'(.{0,20}?)(害羞|脸红|心跳|紧张|暧昧|亲密|肌肤之亲)',
            r'(.{0,20}?)(推倒|占便宜|逆推|非礼)'
        ]

        for pattern in暧昧_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if match[1] in ['害羞', '脸红', '心跳', '紧张', '暧昧', '亲密', '肌肤之亲', '推倒', '占便宜', '逆推', '非礼']:
                    new_elements.append(match[1])

        interaction['new_elements'] = list(set(new_elements))

        return interaction


if __name__ == '__main__':
    # 测试代码
    analyzer = CharacterAnalyzer()
    content = """
    叶枫施展绝世医术，治愈了绝色总裁唐酥酥的怪病。
    唐酥酥害羞地看着叶枫，心跳加速，对他产生好感。
    反派赵总嘲讽叶枫是穷小子，被叶枫当场打脸。
    """
    result = analyzer.analyze(1, "第1章 玄阴玄阳", content)
    print(yaml.dump(result, default_flow_style=False))