#!/usr/bin/env python3
"""
测试分析器功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 导入模块测试
def test_imports():
    """测试模块导入"""
    try:
        from text_preprocessor import TextPreprocessor
        print("✅ TextPreprocessor 导入成功")

        from chapter_splitter import ChapterSplitter
        print("✅ ChapterSplitter 导入成功")

        # 测试文本预处理
        preprocessor = TextPreprocessor()
        print(f"✅ TextPreprocessor 初始化成功，默认编码: {preprocessor.encoding}")

        # 测试章节分割器
        splitter = ChapterSplitter()
        print("✅ ChapterSplitter 初始化成功")

        # 测试小说文件
        test_file = r"D:\迅雷下载\筛检版\下山神医绝色总裁赖上我.txt"
        if os.path.exists(test_file):
            print(f"✅ 找到测试文件: {test_file}")

            # 测试文本预处理
            cleaned_text, metadata = preprocessor.process_file(test_file)
            print(f"✅ 文本预处理成功，元信息: {metadata.get('title', '未知')}")

            # 测试章节分割
            chapters = splitter.split_chapters(cleaned_text)
            first_100 = splitter.extract_chapter_range(chapters, 1, 100)
            summary = splitter.get_chapter_summary(first_100)
            print(f"✅ 章节分割成功，找到 {summary['total_chapters']} 章")

        else:
            print("❌ 未找到测试文件")

        return True

    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

if __name__ == '__main__':
    print("开始测试分析器...\n")
    success = test_imports()

    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 测试失败，请检查环境配置")