import tempfile
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.schemas import GenerateFromDescriptionRequest, StyleType
from app.services.content_parser import parse_description_to_slides, parse_text_to_slides
from app.services.ppt_builder import build_ppt

router = APIRouter(prefix="/api/ppt", tags=["ppt"])
@router.post("/from-description")
def generate_from_description(payload: GenerateFromDescriptionRequest):
    slides = parse_description_to_slides(
        payload.description,
        use_llm=payload.use_llm,
        max_slides=payload.max_slides,
    )
    output_path = _create_output_path("description")
    build_ppt(slides=slides, style=payload.style, output_path=output_path, title=payload.title)
    return _ppt_file_response(output_path)


@router.post("/from-file")
async def generate_from_file(
    file: UploadFile = File(...),
    style: StyleType = Form("business"),
    title: str | None = Form(None),
    use_llm: bool = Form(True),
    max_slides: int = Form(8),
):
    if max_slides < 1 or max_slides > 30:
        raise HTTPException(status_code=422, detail="max_slides 必须在 1~30 之间")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="文件必须是 UTF-8 文本") from exc

    slides = parse_text_to_slides(text, use_llm=use_llm, max_slides=max_slides)
    output_path = _create_output_path("file")
    build_ppt(slides=slides, style=style, output_path=output_path, title=title)
    return _ppt_file_response(output_path)


def _create_output_path(prefix: str) -> str:
    tmp_dir = tempfile.mkdtemp(prefix="pptgen_")
    return str(Path(tmp_dir) / f"{prefix}_generated.pptx")


def _ppt_file_response(output_path: str) -> FileResponse:
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=Path(output_path).name,
    )
