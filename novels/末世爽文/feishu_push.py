#!/usr/bin/env python3
"""
番茄小说每日飞书推送脚本
每天发送4章小说到飞书群
"""

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 配置
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/cb1bb02c-3952-4d8f-8c6d-871bc4650882"
CHAPTERS_DIR = Path(__file__).parent / "初稿"
STATE_FILE = Path(__file__).parent / "push_state.json"
CHAPTERS_PER_DAY = 4
NOVEL_NAME = "末世，从征服四个校花开始"


def get_chapter_files():
    """获取所有章节文件，按章节数字排序"""
    files = list(CHAPTERS_DIR.glob("第*.md"))

    def chapter_num(f):
        match = re.search(r'第(\w+)章', f.stem)
        if match:
            num_str = match.group(1)
            cn_to_arab = {
                '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
                '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
                '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
                '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
                '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
                '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
                '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39, '四十': 40,
                '四十一': 41, '四十二': 42, '四十三': 43, '四十四': 44, '四十五': 45,
                '四十六': 46, '四十七': 47, '四十八': 48, '四十九': 49, '五十': 50,
                '五十一': 51, '五十二': 52, '五十三': 53, '五十四': 54, '五十五': 55,
                '五十六': 56, '五十七': 57, '五十八': 58, '五十九': 59, '六十': 60,
                '六十一': 61, '六十二': 62, '六十三': 63, '六十四': 64, '六十五': 65,
                '六十六': 66, '六十七': 67, '六十八': 68, '六十九': 69, '七十': 70,
                '七十一': 71, '七十二': 72, '七十三': 73, '七十四': 74, '七十五': 75,
                '七十六': 76, '七十七': 77, '七十八': 78, '七十九': 79, '八十': 80,
                '八十一': 81, '八十二': 82, '八十三': 83, '八十四': 84, '八十五': 85,
                '八十六': 86, '八十七': 87, '八十八': 88, '八十九': 89, '九十': 90,
                '九十一': 91, '九十二': 92, '九十三': 93, '九十四': 94, '九十五': 95,
                '九十六': 96, '九十七': 97, '九十八': 98, '九十九': 99, '一百': 100,
            }
            return cn_to_arab.get(num_str, 0)
        return 0

    files.sort(key=chapter_num)
    return files


def load_state():
    """加载推送状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_sent_index": -1, "sent_dates": []}


def save_state(state):
    """保存推送状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def read_chapter(filepath):
    """读取章节内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()


def format_chapter_for_feishu(title, content):
    """将章节格式化为飞书富文本段落"""
    # 飞书 post 消息的 content 是嵌套列表
    # 每个段落是一个列表，包含文本元素
    lines = content.split('\n')
    paragraphs = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            text = line.lstrip('#').strip()
            paragraphs.append([{"tag": "text", "text": f"【{text}】"}])
        elif line == '---':
            paragraphs.append([{"tag": "text", "text": "————————————"}])
        else:
            paragraphs.append([{"tag": "text", "text": line}])

    return paragraphs


def send_single_to_feishu(title, content):
    """发送单章到飞书"""
    content_lines = format_chapter_for_feishu(title, content)

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"📖 {NOVEL_NAME} - {title}",
                    "content": content_lines
                }
            }
        }
    }

    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        FEISHU_WEBHOOK,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('code') == 0 or result.get('StatusCode') == 0:
                return True
            else:
                print(f"    ❌ 发送失败: {result}")
                return False
    except Exception as e:
        print(f"    ❌ 发送异常: {e}")
        return False


def send_header_to_feishu(count):
    """发送今日更新预告"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"📖 {NOVEL_NAME}\n今日更新 {count} 章，请查收！"
        }
    }

    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        FEISHU_WEBHOOK,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('code') == 0 or result.get('StatusCode') == 0
    except:
        return False


def main():
    chapters = get_chapter_files()
    total = len(chapters)
    print(f"📚 共发现 {total} 章")

    state = load_state()
    start_index = state["last_sent_index"] + 1

    if start_index >= total:
        print("🎉 所有章节已发送完毕！")
        return

    end_index = min(start_index + CHAPTERS_PER_DAY, total)
    print(f"📤 本次发送: 第{start_index+1}章 ~ 第{end_index}章 (共{end_index - start_index}章)")

    chapters_data = []
    for i in range(start_index, end_index):
        filepath = chapters[i]
        title = filepath.stem  # 如 "第一章"
        content = read_chapter(filepath)
        chapters_data.append((title, content))
        print(f"  📖 已读取: {title}")

    print(f"\n🚀 正在发送到飞书...")

    # 先发送预告
    send_header_to_feishu(len(chapters_data))
    time.sleep(1)

    # 逐章发送
    all_success = True
    for title, content in chapters_data:
        print(f"  📤 发送: {title}...")
        ok = send_single_to_feishu(title, content)
        if ok:
            print(f"    ✅ {title} 发送成功")
        else:
            all_success = False
            print(f"    ❌ {title} 发送失败")
        time.sleep(2)  # 避免频率限制

    if all_success:
        state["last_sent_index"] = end_index - 1
        from datetime import datetime
        state["sent_dates"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "chapters": f"{start_index+1}-{end_index}",
            "count": end_index - start_index
        })
        save_state(state)
        remaining = total - end_index
        print(f"\n✅ 完成！还剩 {remaining} 章待发送")
    else:
        print(f"\n⚠️ 部分章节发送失败，状态未更新，下次将重试")


if __name__ == "__main__":
    main()
