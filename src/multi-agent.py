#!/usr/bin/env python3
"""
多Agent协调器
管理多个AI代理并行分析小说章节
"""

import asyncio
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from src.agents.plot_analyzer import PlotAnalyzer
from src.agents.character_analyzer import CharacterAnalyzer
from src.agents.style_analyzer import StyleAnalyzer
from src.agents.summarizer import Summarizer


@dataclass
class ChapterAnalysisResult:
    """章节分析结果"""
    chapter_id: int
    title: str
    plot_analysis: Dict[str, Any]
    character_analysis: Dict[str, Any]
    style_analysis: Dict[str, Any]


class MultiAgentCoordinator:
    """多Agent协调器"""

    def __init__(self, num_agents: int = 4):
        self.num_agents = num_agents
        self.plot_analyzer = PlotAnalyzer()
        self.character_analyzer = CharacterAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        self.summarizer = Summarizer()
        self.executor = ThreadPoolExecutor(max_workers=num_agents)

    async def analyze_chapter(self, chapter_id: int, title: str, content: str) -> ChapterAnalysisResult:
        """分析单个章节"""
        # 并行运行三个分析器
        plot_task = self.plot_analyzer.analyze(chapter_id, title, content)
        character_task = self.character_analyzer.analyze(chapter_id, title, content)
        style_task = self.style_analyzer.analyze(chapter_id, title, content)

        # 等待所有分析完成
        plot_analysis, character_analysis, style_analysis = await asyncio.gather(
            plot_task,
            character_task,
            style_task
        )

        return ChapterAnalysisResult(
            chapter_id=chapter_id,
            title=title,
            plot_analysis=plot_analysis,
            character_analysis=character_analysis,
            style_analysis=style_analysis
        )

    async def analyze_all_chapters(self, chapters: List[Dict[str, Any]]) -> List[ChapterAnalysisResult]:
        """分析所有章节"""
        # 创建章节分析任务
        tasks = []
        for chapter in chapters:
            task = self.analyze_chapter(
                chapter['chapter_id'],
                chapter['title'],
                chapter['content']
            )
            tasks.append(task)

        # 并发执行所有任务
        results = await asyncio.gather(*tasks)

        return results

    async def consolidate_results(self, chapter_results: List[ChapterAnalysisResult]) -> Dict[str, Any]:
        """整合所有章节的分析结果"""
        # 按章节ID排序
        sorted_results = sorted(chapter_results, key=lambda x: x.chapter_id)

        # 整合数据
        consolidated = {
            'novel_info': {
                'total_chapters': len(chapter_results),
                'analyzed_chapters': len([r for r in sorted_results if r.chapter_id <= 100])
            },
            'plot_data': [],
            'character_data': [],
            'style_data': []
        }

        # 收集所有章节的数据
        for result in sorted_results:
            if result.chapter_id <= 100:  # 只收集前100章
                consolidated['plot_data'].append(result.plot_analysis)
                consolidated['character_data'].append(result.character_analysis)
                consolidated['style_data'].append(result.style_analysis)

        # 生成最终报告
        final_reports = await self.summarizer.generate_final_reports(
            consolidated['plot_data'],
            consolidated['character_data'],
            consolidated['style_data']
        )

        return {
            'consolidated_data': consolidated,
            'final_reports': final_reports
        }

    def save_results(self, results: Dict[str, Any], output_dir: str):
        """保存分析结果"""
        os.makedirs(output_dir, exist_ok=True)

        # 保存整合后的数据
        consolidated_file = os.path.join(output_dir, 'consolidated_data.json')
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(results['consolidated_data'], f, ensure_ascii=False, indent=2)

        # 保存各报告文件
        reports = results['final_reports']

        # 主线剧情报告
        with open(os.path.join(output_dir, 'main_plot.md'), 'w', encoding='utf-8') as f:
            f.write(reports['main_plot'])

        # 支线剧情报告
        with open(os.path.join(output_dir, 'sub_plots.md'), 'w', encoding='utf-8') as f:
            f.write(reports['sub_plots'])

        # 后宫人物报告
        with open(os.path.join(output_dir, 'characters.md'), 'w', encoding='utf-8') as f:
            f.write(reports['characters'])

        # 创作风格报告
        with open(os.path.join(output_dir, 'style_guide.md'), 'w', encoding='utf-8') as f:
            f.write(reports['style_guide'])

        # 创作模板报告
        with open(os.path.join(output_dir, 'template.md'), 'w', encoding='utf-8') as f:
            f.write(reports['template'])

        print(f"分析结果已保存到: {output_dir}")


# 示例使用
if __name__ == '__main__':
    async def main():
        # 创建协调器
        coordinator = MultiAgentCoordinator(num_agents=4)

        # 模拟章节数据
        mock_chapters = [
            {
                'chapter_id': 1,
                'title': '第1章 玄阴玄阳',
                'content': '清晨。晶宫大酒店606房间，一男一女的尖叫声，同时响起。'
            },
            {
                'chapter_id': 2,
                'title': '第2章 意外相遇',
                'content': '叶枫站在酒店门口，看着远处走来的唐酥酥。'
            }
        ]

        # 分析章节
        print("开始分析章节...")
        chapter_results = await coordinator.analyze_all_chapters(mock_chapters)
        print(f"分析了 {len(chapter_results)} 个章节")

        # 整合结果
        print("整合分析结果...")
        final_results = await coordinator.consolidate_results(chapter_results)

        # 保存结果
        coordinator.save_results(final_results, 'analysis-results/test-novel')

    asyncio.run(main())