#!/usr/bin/env python3
"""
章节分割模块
将小说文本分割为独立的章节
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from text_preprocessor import TextPreprocessor


@dataclass
class Chapter:
    """章节数据结构"""
    chapter_id: int
    title: str
    content: str
    start_line: int
    end_line: int


class ChapterSplitter:
    """章节分割器"""

    def __init__(self):
        self.text_preprocessor = TextPreprocessor()
        # 章节标题正则表达式模式
        self.chapter_patterns = [
            r'第[一二三四五六七八九十百千万]+章\s+[^第]',  # 第X章格式
            r'第[0-9]+章\s+[^第]',  # 第X章（数字）
            r'第[一二三四五六七八九十百千万]+卷\s+[^第]',  # 第X卷格式
            r'第[0-9]+卷\s+[^第]',  # 第X卷（数字）
            r'第[一二三四五六七八九十百千万]+部\s+[^第]',  # 第X部格式
            r'第[0-9]+部\s+[^第]',  # 第X部（数字）
        ]

    def split_chapters(self, text: str) -> List[Chapter]:
        """分割文本为章节"""
        # 将文本按行分割
        lines = text.split('\n')
        chapters = []
        current_chapter = None
        chapter_count = 0

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # 检查是否是章节标题
            if self._is_chapter_title(line):
                # 保存上一章节
                if current_chapter:
                    chapters.append(current_chapter)

                # 创建新章节
                chapter_count += 1
                title = line
                content_lines = []

                # 收集章节内容（直到下一个章节标题之前）
                for i in range(line_num, len(lines)):
                    next_line = lines[i].strip()
                    if i > line_num and self._is_chapter_title(next_line):
                        break
                    content_lines.append(lines[i])

                current_chapter = Chapter(
                    chapter_id=chapter_count,
                    title=title,
                    content='\n'.join(content_lines),
                    start_line=line_num,
                    end_line=i - 1 if i < len(lines) else len(lines)
                )

        # 添加最后一章
        if current_chapter:
            chapters.append(current_chapter)

        return chapters

    def _is_chapter_title(self, line: str) -> bool:
        """判断是否是章节标题"""
        if not line:
            return False

        # 检查各种章节格式
        for pattern in self.chapter_patterns:
            if re.search(pattern, line):
                return True

        # 检查其他可能的格式
        # 【卷名】格式
        if re.search(r'【[^】]+】', line):
            return True

        # XX第X章格式
        if re.search(r'[^第]*第[一二三四五六七八九十百千万0-9]+章[^第]*', line):
            return True

        return False

    def extract_chapter_range(self, chapters: List[Chapter], start_chapter: int = 1, end_chapter: int = 100) -> List[Chapter]:
        """提取指定章节范围"""
        return [ch for ch in chapters if start_chapter <= ch.chapter_id <= end_chapter]

    def get_chapter_summary(self, chapters: List[Chapter]) -> Dict[str, int]:
        """获取章节数据概览"""
        total_chapters = len(chapters)
        total_lines = sum(ch.end_line - ch.start_line + 1 for ch in chapters)
        avg_lines_per_chapter = total_lines / total_chapters if total_chapters > 0 else 0

        return {
            'total_chapters': total_chapters,
            'total_lines': total_lines,
            'avg_lines_per_chapter': avg_lines_per_chapter
        }


if __name__ == '__main__':
    # 测试代码
    splitter = ChapterSplitter()

    # 读取测试文件
    preprocessor = TextPreprocessor()
    text, metadata = preprocessor.process_file(r"D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt")

    # 分割章节
    chapters = splitter.split_chapters(text)

    # 提取前100章
    first_100_chapters = splitter.extract_chapter_range(chapters, 1, 100)

    # 输出统计信息
    summary = splitter.get_chapter_summary(first_100_chapters)
    print(f"总章节数: {summary['total_chapters']}")
    print(f"总行数: {summary['total_lines']}")
    print(f"平均每章行数: {summary['avg_lines_per_chapter']:.1f}")
    print("\n前5章标题:")
    for i, chapter in enumerate(first_100_chapters[:5]):
        print(f"{chapter.chapter_id}. {chapter.title}")