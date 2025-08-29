from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    transcription: str = Field(..., description="Raw transcription text.")

class AnalyzeResponse(BaseModel):
    analysis: dict

class TranscribeResponse(BaseModel):
    transcription: str

class VoiceInputResponse(BaseModel):
    status: str
    file_path: str
