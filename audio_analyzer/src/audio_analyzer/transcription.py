from typing import Optional
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
from langchain_core.documents.base import Blob
import anyio

_parser = OpenAIWhisperParser()

async def transcribe_audio(audio_path: str) -> str:

    def _do_transcribe(path: str) -> str:
        transcription = ""

        for doc in _parser.lazy_parse(blob=Blob(path=path)):
            transcription += doc.page_content or ""
        return transcription

    try:
        return await anyio.to_thread.run_sync(_do_transcribe, audio_path)
    except Exception as e:

        return f"Error during transcription: {e}"
