from pydantic import BaseModel, Field


class GenerateFromDescriptionRequest(BaseModel):
    description: str = Field(..., min_length=5, description="用户对于 PPT 的描述")
    style: str = Field(default="business", description="PPT 风格")
    title: str | None = Field(default=None, description="PPT 总标题")
    use_llm: bool = Field(default=True, description="是否启用大模型生成")
