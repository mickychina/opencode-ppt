import base64
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas import GenerateFromDescriptionRequest
from app.services.content_parser import parse_description_to_slides, parse_text_to_slides
from app.services.llm_generator import generate_slides_with_llm_debug
from app.services.ppt_builder import build_ppt

router = APIRouter(prefix="/api/ppt", tags=["ppt"])


@router.post("/from-description")
def generate_from_description(payload: GenerateFromDescriptionRequest):
    llm_debug = None
    if payload.use_llm:
        try:
            llm_debug = generate_slides_with_llm_debug(payload.description)
            slides = llm_debug["slides"]
        except Exception as exc:
            llm_debug = {"error": str(exc)}
            slides = parse_description_to_slides(payload.description, use_llm=False)
    else:
        slides = parse_description_to_slides(payload.description, use_llm=False)

    output_path = _create_output_path("description")
    build_ppt(slides=slides, style=payload.style, output_path=output_path, title=payload.title)
    return _json_with_ppt(output_path, slides, llm_debug)


@router.post("/from-file")
async def generate_from_file(
    file: UploadFile = File(...),
    style: str = Form("business"),
    title: str | None = Form(None),
    use_llm: bool = Form(True),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="文件必须是 UTF-8 文本") from exc

    llm_debug = None
    if use_llm:
        try:
            llm_debug = generate_slides_with_llm_debug(text)
            slides = llm_debug["slides"]
        except Exception as exc:
            llm_debug = {"error": str(exc)}
            slides = parse_text_to_slides(text, use_llm=False)
    else:
        slides = parse_text_to_slides(text, use_llm=False)

    output_path = _create_output_path("file")
    build_ppt(slides=slides, style=style, output_path=output_path, title=title)
    return _json_with_ppt(output_path, slides, llm_debug)


def _create_output_path(prefix: str) -> str:
    tmp_dir = tempfile.mkdtemp(prefix="pptgen_")
    return str(Path(tmp_dir) / f"{prefix}_generated.pptx")


def _json_with_ppt(output_path: str, slides: list[dict], llm_debug: dict | None) -> dict:
    file_bytes = Path(output_path).read_bytes()
    return {
        "filename": Path(output_path).name,
        "slides": slides,
        "llm_debug": llm_debug,
        "ppt_base64": base64.b64encode(file_bytes).decode("utf-8"),
    }
