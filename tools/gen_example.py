"""YTP VocaBuddy - Lab 3：例句生成 CLI（v2：JSON 輸出＋驗證＋降階）

用法：
    python tools/gen_example.py algorithm
    python tools/gen_example.py            # 不給單字就用 interval

金鑰請放環境變數 ANTHROPIC_API_KEY，不要寫進程式碼、不要 commit。
"""
import json
import os
import re
import sys

import anthropic

# 模型名稱會更新；可用環境變數 ANTHROPIC_MODEL 覆寫，不必改程式碼
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

# Prompt 是程式碼：寫成常數、進 Git
SYSTEM = "你是高中英語老師。只輸出 JSON，不要 markdown 圍欄，不要其他文字。"
PROMPT = (
    "為英文單字「{word}」產生學習卡內容。只回傳 JSON，不要其他文字，"
    '格式：{{"word": "...", "sentence": "...", "zh": "...", "tip": "..."}}。'
    "sentence 用 CEFR B1 難度，且必須包含該單字。"
)

# 罐頭內容：AI 掛了、網路斷了，使用者也永遠看得到東西
FALLBACK = {
    "sentence": "Practice makes perfect.",
    "zh": "熟能生巧。",
    "tip": "（預設內容：AI 暫時不可用）",
}


def ask(client, word):
    """呼叫 Claude，回傳原始文字。"""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM,
        messages=[{"role": "user", "content": PROMPT.format(word=word)}],
    )
    return msg.content[0].text


def parse(text):
    """解析 JSON；模型偶爾會多包一層 ```json 圍欄，先剝掉。"""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    return json.loads(text)


def generate(word):
    """信任但要驗證：解析得了、欄位齊全、例句真的含目標單字才放行。"""
    for _ in range(2):  # 失敗最多重試一次
        try:
            client = anthropic.Anthropic()  # 自動讀環境變數的 key
            data = parse(ask(client, word))
            if word.lower() in data["sentence"].lower() and data["zh"] and data["tip"]:
                return data
        except Exception:  # JSON 壞掉、欄位缺漏、網路/API 錯誤…全部接住
            pass
    return {"word": word, **FALLBACK}  # 降階：永遠有東西可給


def main():
    word = sys.argv[1] if len(sys.argv) > 1 else "interval"
    print(json.dumps(generate(word), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
