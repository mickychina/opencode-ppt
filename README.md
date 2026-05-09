# PPT 生成服务

一个基于 FastAPI 的 PPT 生成服务，支持：

1. 根据用户文本描述生成 PPT。
2. 根据用户上传文件内容生成 PPT。
3. 设置 PPT 风格（商务、极简、创意、教育）。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问：`http://127.0.0.1:8000/docs`

## API

### 1) 文本描述生成 PPT
- `POST /api/ppt/from-description`
- Body:
```json
{
  "description": "做一份关于人工智能发展趋势的 6 页演示",
  "style": "business",
  "title": "AI 趋势"
}
```

### 2) 文件生成 PPT
- `POST /api/ppt/from-file`
- form-data:
  - `file`: txt/md 文件
  - `style`: business | minimal | creative | education
  - `title`: 可选

## 说明

当前版本使用启发式规则把文本拆分为多页。你可以在 `app/services/content_parser.py` 中替换为 LLM 生成逻辑。


## 大模型配置

默认开启大模型生成（失败自动回退到规则生成）。

### 方式一：使用 `.env` 配置文件（推荐）

1. 复制配置模板：

```bash
cp .env.example .env
```

2. 编辑 `.env`：

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 方式二：使用环境变量

```bash
export OPENAI_API_KEY="your_key"
export OPENAI_MODEL="gpt-4.1-mini"
# 可选：兼容网关
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

请求中可设置 `use_llm=false` 关闭大模型。
