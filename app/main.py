from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path


app = FastAPI(title="CheckStock")
STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
