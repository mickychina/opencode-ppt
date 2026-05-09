import uvicorn

from fastapi import FastAPI

from app.routes import router
from app.config import settings

app = FastAPI(title="PPT Generator Service", version="1.0.0")
app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=False)
