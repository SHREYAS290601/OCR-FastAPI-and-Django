from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
template = Jinja2Templates(directory=str(BASE_DIR / "template"))


@app.get("/")
async def base_land(request: Request):
    return template.TemplateResponse("base.html", {"request": request})


@app.post("/")
def get_file():
    return {"file": "file"}
