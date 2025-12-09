from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from pathlib import Path
from ..data_loader import CSV_PATH

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    contents = await file.read()
    p = CSV_PATH
    p.write_bytes(contents)
    df = pd.read_csv(p)
    required = {"year","sector","industry","region","emissions_tCO2e"}
    if not required.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"CSV missing cols. required: {required}")
    return {"status":"ok", "rows": len(df)}
