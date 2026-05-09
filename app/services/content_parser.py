from typing import Any, List

from app.services.llm_generator import generate_slides_with_llm


Slide = dict[str, str | list[str]]




def _normalize_slides(raw_slides: list[dict[str, Any]], fallback_text: str) -> List[Slide]:
    slides: List[Slide] = []
    for idx, item in enumerate(raw_slides, start=1):
        title = str(item.get("title") or item.get("heading") or f"第 {idx} 页").strip()

        bullets_raw = item.get("bullets")
        if bullets_raw is None:
            bullets_raw = item.get("points") or item.get("content") or item.get("items") or []

        if isinstance(bullets_raw, str):
            bullets = [bullets_raw.strip()] if bullets_raw.strip() else []
        elif isinstance(bullets_raw, list):
            bullets = [str(x).strip() for x in bullets_raw if str(x).strip()]
        else:
            bullets = []

        if not bullets:
            bullets = [f"{title}：待补充要点"]

        slides.append({"title": title, "bullets": bullets[:6]})

    if not slides:
        return [{"title": "项目概览", "bullets": [fallback_text[:120] or "待补充内容"]}]
    return slides

SECTION_HINTS = [
    "背景",
    "现状",
    "问题",
    "方案",
    "实施计划",
    "总结",
]


def parse_description_to_slides(description: str, use_llm: bool = True) -> List[Slide]:
    """根据描述生成基础页面结构（可替换为 LLM 调用）。"""
    desc = description.strip()

    if use_llm:
        try:
            return _normalize_slides(generate_slides_with_llm(desc), desc)
        except Exception:
            pass

    slides: List[Slide] = [
        {"title": "项目概览", "bullets": [desc]},
    ]
    for hint in SECTION_HINTS:
        slides.append(
            {
                "title": hint,
                "bullets": [
                    f"{hint}要点 1",
                    f"{hint}要点 2",
                    f"{hint}要点 3",
                ],
            }
        )
    return slides


def parse_text_to_slides(text: str, use_llm: bool = True) -> List[Slide]:
    """把文本按段落切分成多页。"""
    if use_llm:
        try:
            return _normalize_slides(generate_slides_with_llm(text), text)
        except Exception:
            pass

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return [{"title": "内容", "bullets": ["未识别到有效文本内容"]}]

    slides: List[Slide] = []
    for idx, para in enumerate(paragraphs, start=1):
        lines = [x.strip("-• \t") for x in para.split("\n") if x.strip()]
        title = lines[0][:30] if lines else f"第 {idx} 部分"
        bullets = lines[1:6] if len(lines) > 1 else [para[:120]]
        slides.append({"title": title, "bullets": bullets})
    return slides
