from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import os
from typing import Annotated
from config import UPLOAD_DIR
from transcription import transcribe_audio
from analysis import analyze_transcription
from schemas import (
    AnalyzeRequest, AnalyzeResponse, TranscribeResponse, VoiceInputResponse
)

app = FastAPI(title="AI Voice System", version="1.0.0")


origins = [
    "http://localhost:3000",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],            
)

async def _save_upload(file: UploadFile, destination_dir: str) -> str:
    os.makedirs(destination_dir, exist_ok=True)
    file_path = os.path.join(destination_dir, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as out:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await out.write(chunk)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")



@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/voice-input", response_model=VoiceInputResponse)
async def voice_input(file: Annotated[UploadFile, File(...)]):
    """
    Accepts audio file upload and stores it for later processing.
    """
    file_path = await _save_upload(file, UPLOAD_DIR)
    return VoiceInputResponse(status="Voice input received", file_path=file_path)

@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(file: Annotated[UploadFile, File(...)]):
    """
    Transcribes the uploaded audio file to text using Whisper (async wrapper).
    """
    file_path = await _save_upload(file, UPLOAD_DIR)
    text = await transcribe_audio(file_path)
    if text.startswith("Error during transcription:"):
        raise HTTPException(status_code=500, detail=text)
    return TranscribeResponse(transcription=text)

@app.post("/analyze-sentiment", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Runs the full call analysis pipeline (CrewAI + LangChain) on transcription text.
    """
    result = await analyze_transcription(request.transcription)
    return AnalyzeResponse(analysis=result)


