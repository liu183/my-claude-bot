# Novel Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a multi-agent system to analyze novels and extract creative writing templates, focusing on urban medical-themed web novels.

**Architecture:** Multi-agent architecture with specialized analyzers for plot, characters, style, and summarization. Agents process chapters in parallel and consolidate results into comprehensive reports.

**Tech Stack:** Python 3.9+, asyncio, concurrent.futures, regex-based text analysis, YAML output

---

## Task 1: Install Dependencies and Setup Environment

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Install required dependencies**

```python
# requirements.txt content:
chardet>=4.0.0
PyYAML>=5.4.0
```

- [ ] **Step 2: Verify Python environment**

Run: `python --version`
Expected: Python 3.9+ version displayed

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All dependencies installed successfully

- [ ] **Step 4: Test imports**

```python
# Test script
from text_preprocessor import TextPreprocessor
from chapter_splitter import ChapterSplitter
print("All imports successful")
```

Run: `python test-imports.py`
Expected: "All imports successful"

- [ ] **Step 5: Commit**

```bash
git add requirements.txt
git commit -m "feat: add project dependencies"
```

---

## Task 2: Test Text Preprocessing

**Files:**
- Test: `src/test_text_preprocessor.py`

- [ ] **Step 1: Write failing test for text preprocessing**

```python
# src/test_text_preprocessor.py
import unittest
from text_preprocessor import TextPreprocessor

class TestTextPreprocessor(unittest.TestCase):
    def test_detect_encoding(self):
        preprocessor = TextPreprocessor()
        # Mock file with known encoding
        encoding = preprocessor.detect_encoding("test.txt")
        self.assertIn(encoding, ['utf-8', 'gbk'])
    
    def test_clean_text(self):
        preprocessor = TextPreprocessor()
        dirty_text = "This  has   extra  spaces\n\nand\nnewlines"
        clean_text = preprocessor.clean_text(dirty_text)
        self.assertEqual(clean_text, "This has extra spaces and newlines")
```

- [ ] **Step 2: Run test to verify failure**

Run: `python -m pytest src/test_text_preprocessor.py::TestTextPreprocessor::test_detect_encoding -v`
Expected: FAIL with "test.txt not found" or similar

- [ ] **Step 3: Update text_preprocessor.py with encoding detection**

```python
# src/text_preprocessor.py
import chardet

def detect_encoding(self, file_path: str) -> str:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))  # Read first 10KB
    return result['encoding'] or 'utf-8'
```

- [ ] **Step 4: Add test file and run tests**

Create: `test_utf8.txt` with content: "测试文本"
Run: `python -m pytest src/test_text_preprocessor.py -v`
Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add src/text_preprocessor.py src/test_text_preprocessor.py
git commit -m "feat: implement text preprocessing with encoding detection"
```

---

## Task 3: Test Chapter Splitting

**Files:**
- Test: `src/test_chapter_splitter.py`
- Modify: `src/chapter-splitter.py`

- [ ] **Step 1: Write failing test for chapter detection**

```python
# src/test_chapter_splitter.py
import unittest
from chapter_splitter import ChapterSplitter

class TestChapterSplitter(unittest.TestCase):
    def test_chapter_detection(self):
        splitter = ChapterSplitter()
        test_text = """第一章 开始
这是第一章内容。
第二章 继续
这是第二章内容。"""
        chapters = splitter.split_chapters(test_text)
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0].title, "第一章 开始")
```

- [ ] **Step 2: Run test to verify failure**

Run: `python -m pytest src/test_chapter_splitter.py::TestChapterSplitter::test_chapter_detection -v`
Expected: FAIL or incorrect chapter count

- [ ] **Step 3: Fix chapter detection logic**

```python
# src/chapter-splitter.py
def _is_chapter_title(self, line: str) -> bool:
    if not line:
        return False
    
    # Check various chapter formats
    patterns = [
        r'第[一二三四五六七八九十百千万]+章\s+[^第]',
        r'第[0-9]+章\s+[^第]',
        r'第[一二三四五六七八九十百千万]+卷\s+[^第]',
    ]
    
    for pattern in patterns:
        if re.search(pattern, line):
            return True
    
    return False
```

- [ ] **Step 4: Add more test cases and verify**

```python
def test_chapter_extraction(self):
    splitter = ChapterSplitter()
    test_text = """第1章 玄阴玄阳
内容。
第2章 意外相遇
更多内容。"""
    chapters = splitter.extract_chapter_range(splitter.split_chapters(test_text), 1, 2)
    self.assertEqual(len(chapters), 2)
```

Run: `python -m pytest src/test_chapter_splitter.py -v`
Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add src/chapter-splitter.py src/test_chapter_splitter.py
git commit -m "feat: implement chapter splitting with multiple format support"
```

---

## Task 4: Implement Plot Analyzer

**Files:**
- Test: `src/test_plot_analyzer.py`
- Modify: `src/agents/plot_analyzer.py`

- [ ] **Step 1: Write failing test for plot analysis**

```python
# src/test_plot_analyzer.py
import unittest
from plot_analyzer import PlotAnalyzer

class TestPlotAnalyzer(unittest.TestCase):
    def test_event_classification(self):
        analyzer = PlotAnalyzer()
        content = "叶枫施展医术，治愈了总裁的怪病。"
        events = analyzer._extract_main_events(content)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['type'], 'medical')
```

- [ ] **Step 2: Run test and verify failure**

Run: `python -m pytest src/test_plot_analyzer.py::TestPlotAnalyzer::test_event_classification -v`
Expected: FAIL with method not found or incorrect classification

- [ ] **Step 3: Implement event classification**

```python
# src/agents/plot_analyzer.py
def _classify_event_type(self, text: str) -> str:
    scores = {}
    for event_type, patterns in self.event_patterns.items():
        scores[event_type] = 0
        for pattern in patterns:
            matches = re.findall(pattern, text)
            scores[event_type] += len(matches)
    
    return max(scores, key=scores.get)

def _extract_main_events(self, content: str) -> List[Dict[str, str]]:
    events = []
    paragraphs = content.split('。')
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        event_type = self._classify_event_type(para)
        importance = self._calculate_importance(para)
        
        if importance >= 5:
            events.append({
                'event': para,
                'type': event_type,
                'importance': importance
            })
    
    return events
```

- [ ] **Step 4: Test with actual novel content**

Create: `sample_chapter.txt` with real novel text
Run test with actual content
Expected: Events classified correctly

- [ ] **Step 5: Commit**

```bash
git add src/agents/plot_analyzer.py src/test_plot_analyzer.py
git commit -m "feat: implement plot analyzer with event classification"
```

---

## Task 5: Implement Character Analyzer

**Files:**
- Test: `src/test_character_analyzer.py`
- Modify: `src/agents/character_analyzer.py`

- [ ] **Step 1: Write test for character extraction**

```python
# src/test_character_analyzer.py
import unittest
from character_analyzer import CharacterAnalyzer

class TestCharacterAnalyzer(unittest.TestCase):
    def test_harem_member_detection(self):
        analyzer = CharacterAnalyzer()
        content = "绝色总裁唐酥酥害羞地看着叶枫。"
        result = analyzer.analyze(1, "测试", content)
        self.assertIn('唐酥酥', result['new_characters'])
        self.assertEqual(result['new_characters']['唐酥酥']['type'], '后宫')
```

- [ ] **Step 2: Run and verify failure**

Run: `python -m pytest src/test_character_analyzer.py::TestCharacterAnalyzer::test_harem_member_detection -v`
Expected: FAIL with character not found or wrong type

- [ ] **Step 3: Implement character extraction logic**

```python
# src/agents/character_analyzer.py
def extract_new_characters(self, content: str) -> Dict[str, Dict[str, str]]:
    new_characters = {}
    
    # Look for character patterns
    character_patterns = [
        (r'([^，。！？]+)\s*(?:是|叫做|名叫)\s*([^，。！？]+)', 1, 2),
        (r'([^，。！？]+(?:总裁|千金|护士|医生|老师|学生))\s*([^，。！？]+)', 2, 1),
    ]
    
    for pattern, name_idx, identity_idx in character_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if len(match) >= max(name_idx, identity_idx):
                name = match[name_idx - 1].strip()
                identity = match[identity_idx - 1].strip() if identity_idx > name_idx else name
                
                if len(name) >= 2 and '的' not in name:
                    character_type = self._classify_character_type(name, content)
                    new_characters[name] = {
                        'type': character_type,
                        'role': '章节作用',
                        'first_appearance': True,
                        'identity': identity,
                        'appearance': '待补充',
                        'personality': self._extract_personality(name, content),
                        'abilities': self._extract_abilities(name, content),
                        'relationships': {}
                    }
    
    return new_characters
```

- [ ] **Step 4: Add harem interaction analysis**

```python
def _analyze_harem_interaction(self, content: str) -> Dict[str, Any]:
    interaction = {
        'active_members': [],
        'interaction_type': '待确定',
        'progression': 0,
        'new_elements': []
    }
    
    # Find active harem members
    harem_keywords = ['总裁', '千金', '美女', '女神', '护士']
    for keyword in harem_keywords:
        if keyword in content:
            characters = re.findall(r'([^。！？]{2,4})' + keyword, content)
            interaction['active_members'].extend(characters)
    
    # Analyze interaction type
    if any(word in content for word in ['喜欢', '爱慕', '心动']):
        interaction['interaction_type'] = '感情'
    elif any(word in content for word in ['治疗', '医术']):
        interaction['interaction_type'] = '医疗'
    
    return interaction
```

- [ ] **Step 5: Commit**

```bash
git add src/agents/character_analyzer.py src/test_character_analyzer.py
git commit -m "feat: implement character analyzer with harem detection"
```

---

## Task 6: Implement Style Analyzer

**Files:**
- Test: `src/test_style_analyzer.py`
- Modify: `src/agents/style_analyzer.py`

- [ ] **Step 1: Write test for style analysis**

```python
# src/test_style_analyzer.py
import unittest
from style_analyzer import StyleAnalyzer

class TestStyleAnalyzer(unittest.TestCase):
    def test_vocabulary_level(self):
        analyzer = StyleAnalyzer()
        content = "叶枫施展绝世医术，玄阴玄阳功法运转。"
        result = analyzer.analyze(1, "测试", content)
        self.assertIn('vocabulary_level', result['language_style'])
```

- [ ] **Step 2: Run and verify failure**

Run: `python -m pytest src/test_style_analyzer.py::TestStyleAnalyzer::test_vocabulary_level -v`
Expected: FAIL with style not analyzed

- [ ] **Step 3: Implement language style analysis**

```python
# src/agents/style_analyzer.py
def _analyze_language_style(self, content: str) -> Dict[str, str]:
    # Analyze vocabulary level
    vocab_score = 0
    for level, words in self.vocabulary_levels.items():
        for word in words:
            vocab_score += content.count(word) * (3 if level == 'high' else 2 if level == 'medium' else 1)
    
    if vocab_score > 20:
        vocabulary_level = '高'
    elif vocab_score > 10:
        vocabulary_level = '中'
    else:
        vocabulary_level = '低'
    
    # Analyze sentence structure
    sentences = re.split(r'[。！？]', content)
    avg_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    
    sentence_structure = '复杂' if avg_length > 50 else '简单' if avg_length < 20 else '标准'
    
    return {
        'vocabulary_level': vocabulary_level,
        'sentence_structure': sentence_structure,
        'rhetorical_devices': self._find_rhetorical_devices(content),
        'tone': self._determine_tone(content)
    }
```

- [ ] **Step 4: Add scene type analysis**

```python
def _analyze_scene_types(self, content: str) -> Dict[str, List[str]]:
    scene_types = {
        'medical': [],
        'battle': [],
        'romantic': [],
        'daily': []
    }
    
    # Analyze medical scenes
    if any(keyword in content for keyword in ['治病', '医术', '治疗']):
        scene_types['medical'].append('包含医疗事件')
    
    # Analyze romantic scenes
    if any(keyword in content for keyword in ['害羞', '脸红', '心跳']):
        scene_types['romantic'].append('包含感情事件')
    
    return scene_types
```

- [ ] **Step 5: Commit**

```bash
git add src/agents/style_analyzer.py src/test_style_analyzer.py
git commit -m "feat: implement style analyzer with scene detection"
```

---

## Task 7: Implement Summarizer

**Files:**
- Test: `src/test_summarizer.py`
- Modify: `src/agents/summarizer.py`

- [ ] **Step 1: Write test for summarization**

```python
# src/test_summarizer.py
import unittest
from summarizer import Summarizer

class TestSummarizer(unittest.TestCase):
    def test_main_plot_generation(self):
        summarizer = Summarizer()
        plot_data = [{
            'chapter_id': 1,
            'main_events': [{'event': '医术展示', 'type': 'medical', 'importance': 8}]
        }]
        result = summarizer._generate_main_plot_report_from_data(plot_data)
        self.assertIn('核心事件', result)
```

- [ ] **Step 2: Run and verify failure**

Run: `python -m pytest src/test_summarizer.py::TestSummarizer::test_main_plot_generation -v`
Expected: FAIL with method not found

- [ ] **Step 3: Implement plot summarization**

```python
# src/agents/summarizer.py
def _generate_main_plot_report_from_data(self, plot_data: List[Dict]) -> str:
    report = "# 都市神医小说 - 主线剧情分析\n\n## 故事阶段划分\n"
    
    # Group chapters by stages
    stages = self._analyze_plot_progression(plot_data)
    
    for i, (stage_name, chapters) in enumerate(stages.items(), 1):
        report += f"""
### 第{i}阶段：{stage_name}
- 时间跨度：第{chapters['start']}章 - 第{chapters['end']}章
- 核心事件：
"""
        for event in chapters['core_events']:
            report += f"  - {event}\n"
    
    return report
```

- [ ] **Step 4: Add template generation**

```python
def _generate_character_templates(self, character_data: List[Dict]) -> Dict:
    return {
        'main_character': """主角：
- 姓名：霸总风格姓名（如：叶辰、林轩）
- 身份：低调隐藏高手
- 性格：表面冷漠，内心温柔
- 能力：医术超群、武功高强""",
        'harem_members': [
            "绝色总裁：高冷傲娇",
            "护士妹妹：温柔体贴",
            "校花女神：清纯美丽"
        ]
    }
```

- [ ] **Step 5: Commit**

```bash
git add src/agents/summarizer.py src/test_summarizer.py
git commit -m "feat: implement summarizer with report generation"
```

---

## Task 8: Integrate Multi-Agent System

**Files:**
- Test: `src/test_multi_agent.py`
- Modify: `src/multi-agent.py`

- [ ] **Step 1: Write integration test**

```python
# src/test_multi_agent.py
import asyncio
from multi_agent import MultiAgentCoordinator

async def test_integration():
    coordinator = MultiAgentCoordinator(num_agents=2)
    chapters = [{
        'chapter_id': 1,
        'title': '测试章节',
        'content': '叶枫施展医术，治愈了总裁。'
    }]
    results = await coordinator.analyze_all_chapters(chapters)
    assert len(results) == 1

# Run: asyncio.run(test_integration())
```

- [ ] **Step 2: Verify test failure**

Run: `python src/test_multi_agent.py`
Expected: FAIL with import or async errors

- [ ] **Step 3: Fix agent coordination**

```python
# src/multi-agent.py
async def analyze_all_chapters(self, chapters: List[Dict[str, Any]]) -> List[ChapterAnalysisResult]:
    # Create analysis tasks
    tasks = []
    for chapter in chapters:
        task = self.analyze_chapter(
            chapter['chapter_id'],
            chapter['title'],
            chapter['content']
        )
        tasks.append(task)
    
    # Concurrent execution
    results = await asyncio.gather(*tasks)
    return results

async def analyze_chapter(self, chapter_id: int, title: str, content: str) -> ChapterAnalysisResult:
    # Parallel execution of three analyzers
    plot_task = self.plot_analyzer.analyze(chapter_id, title, content)
    character_task = self.character_analyzer.analyze(chapter_id, title, content)
    style_task = self.style_analyzer.analyze(chapter_id, title, content)
    
    plot_analysis, character_analysis, style_analysis = await asyncio.gather(
        plot_task, character_task, style_task
    )
    
    return ChapterAnalysisResult(
        chapter_id=chapter_id,
        title=title,
        plot_analysis=plot_analysis,
        character_analysis=character_analysis,
        style_analysis=style_analysis
    )
```

- [ ] **Step 4: Test with real novel data**

Use actual chapter text from sample novel
Run integration test
Expected: All agents produce consistent results

- [ ] **Step 5: Commit**

```bash
git add src/multi-agent.py src/test_multi_agent.py
git commit -m "feat: implement multi-agent coordination system"
```

---

## Task 9: Create Main Analysis Script

**Files:**
- Modify: `src/analyze-novel.py`

- [ ] **Step 1: Implement main analysis flow**

```python
# src/analyze-novel.py
def analyze_novel(self, file_path: str, output_dir: str = None) -> Dict[str, Any]:
    print(f"开始分析小说: {file_path}")
    
    # 1. Text preprocessing
    cleaned_text, metadata = self.preprocessor.process_file(file_path)
    
    # 2. Chapter splitting
    all_chapters = self.splitter.split_chapters(cleaned_text)
    first_100_chapters = self.splitter.extract_chapter_range(all_chapters, 1, 100)
    
    # 3. Prepare chapter data
    chapters_data = [{
        'chapter_id': ch.chapter_id,
        'title': ch.title,
        'content': ch.content
    } for ch in first_100_chapters]
    
    # 4. Multi-agent analysis
    chapter_results = loop.run_until_complete(
        self.coordinator.analyze_all_chapters(chapters_data)
    )
    
    # 5. Consolidate results
    consolidated_results = loop.run_until_complete(
        self.coordinator.consolidiate_results(chapter_results)
    )
    
    # 6. Save results
    self.coordinator.save_results(consolidated_results, output_dir)
    
    return consolidated_results
```

- [ ] **Step 2: Add command-line interface**

```python
def main():
    parser = argparse.ArgumentParser(description='网文章节分析器')
    parser.add_argument('path', help='小说文件路径')
    parser.add_argument('--output', '-o', help='输出目录', default='analysis-results')
    parser.add_argument('--agents', '-a', type=int, default=4, help='Agent数量')
    args = parser.parse_args()
    
    analyzer = NovelAnalyzer(num_agents=args.agents)
    analyzer.analyze_novel(args.path, args.output)
```

- [ ] **Step 3: Test with sample novel**

```bash
python src/analyze-novel.py "sample_chapter.txt" --test
```

Expected: Successful analysis with all reports generated

- [ ] **Step 4: Commit**

```bash
git add src/analyze-novel.py
git commit -m "feat: implement main analysis script with CLI"
```

---

## Task 10: Create Batch Processing and Final Testing

**Files:**
- Modify: `src/analyze-novel.py`
- Create: `batch_test.py`

- [ ] **Step 1: Add batch processing capability**

```python
def analyze_multiple_novels(self, novel_dir: str, output_dir: str = None) -> Dict[str, Any]:
    txt_files = []
    for file in os.listdir(novel_dir):
        if file.endswith('.txt'):
            txt_files.append(os.path.join(novel_dir, file))
    
    results = {}
    for file_path in txt_files:
        novel_name = Path(file_path).stem
        result = self.analyze_novel(file_path, os.path.join(output_dir, novel_name))
        results[novel_name] = result
    
    return results
```

- [ ] **Step 2: Create comprehensive test suite**

```python
# batch_test.py
import os
from analyze_novel import NovelAnalyzer

def run_batch_test():
    analyzer = NovelAnalyzer(num_agents=4)
    
    # Test with real novel directory
    results = analyzer.analyze_multiple_novels(
        "D:\\迅雷下载\\筛检版",
        "test_output"
    )
    
    # Verify all reports generated
    for novel_name, result in results.items():
        assert 'main_plot' in result['final_reports']
        assert 'characters' in result['final_reports']
    
    print("Batch test completed successfully!")

if __name__ == '__main__':
    run_batch_test()
```

- [ ] **Step 3: Run end-to-end test**

Run: `python batch_test.py`
Expected: Successful analysis of multiple novels with all reports generated

- [ ] **Step 4: Update documentation**

```markdown
# Update README.md with usage examples
## Quick Start
```bash
# Analyze single novel
python src/analyze-novel.py "path/to/novel.txt"

# Batch analyze directory
python src/analyze-novel.py "path/to/novels" --batch
```
```

- [ ] **Step 5: Final commit**

```bash
git add src/analyze-novel.py batch_test.py README.md
git commit -m "feat: add batch processing and complete implementation"
git push origin novel-analyzer
```

---

**Plan complete and saved to `docs/superpowers/plans/2026-04-15-novel-analysis-implementation.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**