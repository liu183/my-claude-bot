#!/usr/bin/env python3
"""
网文章节分析主程序
"""

import os
import sys
import argparse
import asyncio
from pathlib import Path
from typing import List, Dict, Any

# 导入自定义模块
from text_preprocessor import TextPreprocessor
from chapter_splitter import ChapterSplitter, Chapter
from multi_agent import MultiAgentCoordinator, ChapterAnalysisResult
from agents.summarizer import Summarizer


class NovelAnalyzer:
    """小说分析器主类"""

    def __init__(self, num_agents: int = 4):
        self.num_agents = num_agents
        self.preprocessor = TextPreprocessor()
        self.splitter = ChapterSplitter()
        self.coordinator = MultiAgentCoordinator(num_agents)
        self.summarizer = Summarizer()

    def analyze_novel(self, file_path: str, output_dir: str = None) -> Dict[str, Any]:
        """分析单本小说"""
        print(f"开始分析小说: {file_path}")

        # 1. 文本预处理
        print("步骤1: 文本预处理...")
        cleaned_text, metadata = self.preprocessor.process_file(file_path)
        print(f"小说元信息: {metadata.get('title', '未知')}")

        # 2. 章节分割
        print("\n步骤2: 章节分割...")
        all_chapters = self.splitter.split_chapters(cleaned_text)
        first_100_chapters = self.splitter.extract_chapter_range(all_chapters, 1, 100)

        summary = self.splitter.get_chapter_summary(first_100_chapters)
        print(f"前100章统计: {summary['total_chapters']}章, {summary['total_lines']}行")

        # 3. 准备章节数据
        chapters_data = []
        for chapter in first_100_chapters:
            chapters_data.append({
                'chapter_id': chapter.chapter_id,
                'title': chapter.title,
                'content': chapter.content
            })

        if not chapters_data:
            print("错误: 未找到有效章节")
            return {}

        # 4. 多Agent并行分析
        print("\n步骤3: 多Agent并行分析...")
        print(f"使用 {self.num_agents} 个Agent并行分析...")

        # 运行分析
        loop = asyncio.get_event_loop()
        chapter_results = loop.run_until_complete(
            self.coordinator.analyze_all_chapters(chapters_data)
        )

        print(f"已完成 {len(chapter_results)} 章节分析")

        # 5. 整合结果
        print("\n步骤4: 整合分析结果...")
        consolidated_results = loop.run_until_complete(
            self.coordinator.consolidiate_results(chapter_results)
        )

        # 6. 保存结果
        if output_dir is None:
            novel_name = metadata.get('title', '未知小说')
            output_dir = os.path.join('analysis-results', novel_name)

        print(f"\n步骤5: 保存分析结果到 {output_dir}...")
        self.coordinator.save_results(consolidated_results, output_dir)

        # 7. 生成汇总报告
        print("\n步骤6: 生成汇总报告...")
        self._generate_summary_report(output_dir, metadata, summary)

        print(f"\n✅ 分析完成! 结果已保存到: {output_dir}")
        return consolidated_results

    def analyze_multiple_novels(self, novel_dir: str, output_dir: str = None) -> Dict[str, Any]:
        """批量分析目录下的所有小说"""
        print(f"批量分析小说目录: {novel_dir}")

        # 获取所有txt文件
        txt_files = []
        for file in os.listdir(novel_dir):
            if file.endswith('.txt'):
                txt_files.append(os.path.join(novel_dir, file))

        if not txt_files:
            print("错误: 目录下没有找到.txt文件")
            return {}

        print(f"找到 {len(txt_files)} 本小说")

        results = {}

        for i, file_path in enumerate(txt_files, 1):
            print(f"\n[{i}/{len(txt_files)}] 分析: {os.path.basename(file_path)}")

            novel_name = Path(file_path).stem
            if output_dir:
                novel_output_dir = os.path.join(output_dir, novel_name)
            else:
                novel_output_dir = os.path.join('analysis-results', novel_name)

            try:
                result = self.analyze_novel(file_path, novel_output_dir)
                results[novel_name] = result
            except Exception as e:
                print(f"分析失败: {e}")
                results[novel_name] = {'error': str(e)}

        # 生成批量分析报告
        if output_dir:
            batch_report_path = os.path.join(output_dir, 'batch_analysis_summary.md')
            self._generate_batch_report(batch_report_path, results)

        return results

    def _generate_summary_report(self, output_dir: str, metadata: Dict[str, str], summary: Dict[str, int]):
        """生成汇总报告"""
        report_path = os.path.join(output_dir, 'analysis_summary.md')

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"""# {metadata.get('title', '未知小说')} - 分析汇总报告

## 基本信息
- 书名: {metadata.get('title', '未知')}
- 作者: {metadata.get('author', '未知')}
- 状态: {metadata.get('status', '未知')}
- 评分: {metadata.get('rating', '未知')}
- 字数: {metadata.get('word_count', '未知')}
- 分类: {metadata.get('category', '未知')}
- 标签: {metadata.get('tags', '未知')}

## 分析统计
- 分析章节数: {summary['total_chapters']}
- 总行数: {summary['total_lines']}
- 平均每章行数: {summary['avg_lines_per_chapter']:.1f}

## 章节列表
""")

            # 读取主文件并添加前100章列表
            main_plot_file = os.path.join(output_dir, 'main_plot.md')
            if os.path.exists(main_plot_file):
                with open(main_plot_file, 'r', encoding='utf-8') as mf:
                    content = mf.read()
                    f.write("\n## 详细分析\n")
                    f.write(content)

    def _generate_batch_report(self, report_path: str, results: Dict[str, Any]):
        """生成批量分析报告"""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("""# 批量小说分析报告

## 分析概览

本次分析共分析了以下小说：

| 序号 | 小说名称 | 状态 | 章节数 |
|------|---------|------|--------|
""")

            for i, (novel_name, result) in enumerate(results.items(), 1):
                if 'error' in result:
                    status = "❌ 失败"
                    chapters = "-"
                else:
                    status = "✅ 成功"
                    if result and 'consolidated_data' in result:
                        chapters = result['consolidated_data']['novel_info']['analyzed_chapters']
                    else:
                        chapters = "100"

                f.write(f"| {i} | {novel_name} | {status} | {chapters} |\n")

            f.write("\n## 分析详情\n\n")

            # 添加各小说的简要分析
            for novel_name, result in results.items():
                if 'error' not in result:
                    f.write(f"### {novel_name}\n")
                    # 可以添加更多汇总信息
                    f.write("\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='网文章节分析器')
    parser.add_argument('path', help='小说文件路径或目录路径')
    parser.add_argument('--output', '-o', help='输出目录', default='analysis-results')
    parser.add_argument('--agents', '-a', type=int, default=4, help='Agent数量')
    parser.add_argument('--start', type=int, default=1, help='起始章节')
    parser.add_argument('--end', type=int, default=100, help='结束章节')
    parser.add_argument('--batch', action='store_true', help='批量分析目录下的所有小说')

    args = parser.parse_args()

    # 创建分析器
    analyzer = NovelAnalyzer(num_agents=args.agents)

    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)

    if args.batch:
        # 批量分析
        if not os.path.isdir(args.path):
            print("错误: 批量分析需要指定目录路径")
            sys.exit(1)

        analyzer.analyze_multiple_novels(args.path, args.output)
    else:
        # 单本分析
        if not os.path.isfile(args.path):
            print("错误: 请提供有效的小说文件路径")
            sys.exit(1)

        analyzer.analyze_novel(args.path, args.output)


if __name__ == '__main__':
    main()