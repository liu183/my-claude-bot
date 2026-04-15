#!/usr/bin/env python3
"""
文本预处理模块
处理小说文本的编码、格式等问题
"""

import re
import os
from typing import List, Dict, Tuple
import chardet


class TextPreprocessor:
    """文本预处理器"""

    def __init__(self):
        self.encoding = 'utf-8'

    def detect_encoding(self, file_path: str) -> str:
        """检测文件编码"""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding'] or 'utf-8'

    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符（保留中文、英文、数字）
        text = re.sub(r'[^\u4e00-\u9fff\u0041-\u005a\u0061-\u007a\u0030-\u0039\r\n\s.,，。！？？、""""''()（）]', '', text)
        # 修正常见的乱码字符
        text = self._fix_common_encoding_issues(text)
        return text

    def _fix_common_encoding_issues(self, text: str) -> str:
        """修复常见编码问题"""
        # 修正GBK编码的乱码
        replacements = {
            '��': '',
            'ï¿½': '',
            '\ufeff': '',
            '\r\n': '\n',
            '\r': '\n'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def extract_metadata(self, text: str) -> Dict[str, str]:
        """提取小说元信息"""
        metadata = {}

        # 提取书名
        title_match = re.search(r'书名[：:]\s*(.+?)\n', text)
        if title_match:
            metadata['title'] = title_match.group(1).strip()

        # 提取作者
        author_match = re.search(r'作者[：:]\s*(.+?)\n', text)
        if author_match:
            metadata['author'] = author_match.group(1).strip()

        # 提取状态
        status_match = re.search(r'状态[：:]\s*(.+?)\n', text)
        if status_match:
            metadata['status'] = status_match.group(1).strip()

        # 提取评分
        rating_match = re.search(r'评分[：:]\s*(.+?)\n', text)
        if rating_match:
            metadata['rating'] = rating_match.group(1).strip()

        # 提取字数
        word_count_match = re.search(r'字数[：:]\s*(.+?)\n', text)
        if word_count_match:
            metadata['word_count'] = word_count_match.group(1).strip()

        # 提取章节
        chapter_match = re.search(r'章节[：:]\s*(.+?)\n', text)
        if chapter_match:
            metadata['chapters'] = chapter_match.group(1).strip()

        # 提取分类和标签
        category_match = re.search(r'分类[：:]\s*(.+?)\n', text)
        if category_match:
            metadata['category'] = category_match.group(1).strip()

        tag_match = re.search(r'标签[：:]\s*(.+?)\n', text)
        if tag_match:
            metadata['tags'] = tag_match.group(1).strip()

        # 提取简介
        intro_start = text.find('简介：')
        if intro_start != -1:
            intro_end = text.find('\n========================================')
            if intro_end != -1:
                metadata['introduction'] = text[intro_start:intro_end].strip()

        return metadata

    def process_file(self, file_path: str) -> Tuple[str, Dict[str, str]]:
        """处理文件，返回清理后的文本和元信息"""
        # 检测编码
        self.encoding = self.detect_encoding(file_path)

        # 读取文件
        with open(file_path, 'r', encoding=self.encoding, errors='ignore') as f:
            text = f.read()

        # 清理文本
        cleaned_text = self.clean_text(text)

        # 提取元信息
        metadata = self.extract_metadata(text)

        return cleaned_text, metadata


if __name__ == '__main__':
    # 测试代码
    preprocessor = TextPreprocessor()
    test_path = r"D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt"
    cleaned_text, metadata = preprocessor.process_file(test_path)
    print("元信息:", metadata)
    print("前200字符:", cleaned_text[:200])