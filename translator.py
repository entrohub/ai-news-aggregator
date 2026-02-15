import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))


def translate_to_zh(text):
    """Translate text to Chinese using GPT-4o-mini."""
    if not text or not text.strip():
        return text
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个翻译助手。将用户输入的英文翻译成简体中文，只输出翻译结果，不要解释。如果输入已经是中文，直接原样返回。"},
                {"role": "user", "content": text[:500]},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Translation Error]: {e}")
        return text
