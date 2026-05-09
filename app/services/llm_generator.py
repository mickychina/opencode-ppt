import json
from typing import Any

from openai import OpenAI

from app.config import settings


SYSTEM_PROMPT = (
    "你是一个专业的演示文稿策划助手。"
    "请根据用户输入生成结构化 JSON，格式为: "
    '{"slides":[{"title":"...","bullets":["...","..."]}]}'
    "只返回 JSON，不要包含 markdown 代码块。"
)


def generate_slides_with_llm(user_input: str, max_slides: int = 8) -> list[dict[str, Any]]:
    api_key = settings.openai_api_key
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 未配置")

    return generate_slides_with_llm_debug(user_input, max_slides)["slides"]


def generate_slides_with_llm_debug(user_input: str, max_slides: int = 8) -> dict[str, Any]:
    api_key = settings.openai_api_key
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 未配置")

    model = settings.openai_model
    base_url = settings.openai_base_url
    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = (
        f"请生成不超过 {max_slides} 页的 PPT 内容。"
        "每页 3-5 条要点，语句简洁。\n"
        f"用户输入：{user_input}"
    )

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    output_text = resp.output_text.strip()
    data = json.loads(output_text)
    slides = data.get("slides", [])
    if not slides:
        raise RuntimeError("大模型未返回有效 slides")

    return {
        "model": model,
        "base_url": base_url,
        "prompt": prompt,
        "output_text": output_text,
        "slides": slides,
    }
