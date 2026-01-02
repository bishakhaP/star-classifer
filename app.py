import joblib
import numpy as np
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "stellar_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "stellar_scaler.pkl"))

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(data: dict):

    try:
        B_V  = float(data["B_V"])
        Amag = float(data["Amag"])
        Plx  = float(data["Plx"])
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid input values"}
        )

    VMAG_MEAN   = 7.921309
    EPLX_MEAN   = 1.109705
    SPTYPE_MEAN = 1462.485386

    X = np.array([[VMAG_MEAN, Plx, EPLX_MEAN, B_V, SPTYPE_MEAN, Amag]])
    X_scaled = scaler.transform(X)

    prediction = int(model.predict(X_scaled)[0])
    probability = model.predict_proba(X_scaled)[0].tolist()

    return {
        "class": prediction,
        "probability": probability
    }






