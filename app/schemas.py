from typing import Literal

from pydantic import BaseModel, Field


SUPPORTED_STYLES = ("business", "minimal", "creative", "education")
StyleType = Literal["business", "minimal", "creative", "education"]


class GenerateFromDescriptionRequest(BaseModel):
    description: str = Field(..., min_length=5, description="用户对于 PPT 的描述")
    style: StyleType = Field(default="business", description="PPT 风格")
    title: str | None = Field(default=None, description="PPT 总标题")
    use_llm: bool = Field(default=True, description="是否启用大模型生成")
    max_slides: int = Field(default=8, ge=1, le=30, description="最多生成页数")
