from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    status,
    File,
    UploadFile,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
import io
import uuid
from PIL import Image
from .ocr import OCR
from .ocr import get_information

BASE_DIR = pathlib.Path(__file__).parent
OUTPUTDIR = BASE_DIR / "output"
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
template = Jinja2Templates(directory=str(BASE_DIR / "template"))


@app.get("/")
async def base_land(request: Request):
    SESSION_ID = uuid.uuid4()
    return template.TemplateResponse(
        "base.html", {"request": request, "session_id": SESSION_ID}
    )


@app.post("/img-ocr")
async def get_file(
    session_id=Form(...),
    file: UploadFile = File(..., alias="file", validation_alias="file"),
):
    file_bytes = io.BytesIO(await file.read())
    SESSION_ID = session_id
    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty")
    fname = pathlib.Path(file.filename)
    fextention = fname.suffix
    try:
        img = Image.open(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file.Error {e}")
    dest = OUTPUTDIR / f"{SESSION_ID}{fextention}"
    img.save(dest)
    return RedirectResponse(
        f"/img-ocr/{dest.name}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/img-ocr/{filename}")
async def get_file(filename: str, request: Request):
    print(filename)
    SESSION_ID, fextension = filename.split(".")[0], filename.split(".")[-1]
    text = await OCR(SESSION_ID, fextension)
    try:
        information = await get_information(text)
    except Exception as e:
        print(f"error: {e}")

    return template.TemplateResponse(
        "home.html",
        {
            "request": request,
            "filename": filename,
            "text": text,
            "information": information,
        },
    )
