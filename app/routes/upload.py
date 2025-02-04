from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pathlib import Path

UPLOAD_DIR = Path("storage/app/medalists")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files allowed.")
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully!", "filename": file.filename}
