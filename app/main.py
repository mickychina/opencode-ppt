import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router

app = FastAPI(title="PPT Generator Service", version="1.0.0")
app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
