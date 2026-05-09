from typing import List

from app.services.llm_generator import generate_slides_with_llm


Slide = dict[str, str | list[str]]


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
            return generate_slides_with_llm(desc)
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
            return generate_slides_with_llm(text)
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
