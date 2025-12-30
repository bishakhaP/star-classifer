import joblib
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

model = joblib.load("stellar_model.pkl")
scaler = joblib.load("stellar_scaler.pkl")
print("Model and scaler loaded successfully")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(data: dict):

    VMAG_MEAN   = 7.921309
    EPLX_MEAN   = 1.109705
    SPTYPE_MEAN = 1462.485386

    B_V  = data["B_V"]
    Amag = data["Amag"]
    Plx  = data["Plx"]

    X = np.array([[VMAG_MEAN, Plx, EPLX_MEAN, B_V, SPTYPE_MEAN, Amag]])
    X_scaled = scaler.transform(X)

    prediction = int(model.predict(X_scaled)[0])
    probability = model.predict_proba(X_scaled)[0].tolist()

    return JSONResponse({
        "class": prediction,
        "probability": probability
    })





