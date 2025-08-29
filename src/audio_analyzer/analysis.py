from typing import Any, Dict
from crewai import Crew
from langchain_openai import ChatOpenAI
import anyio
from agents import MyAgents
from tasks import MyTasks
from config import LLM_MODEL, LLM_TEMPERATURE

import json
import re
from typing import Dict, Any

async def analyze_transcription(transcription: str) -> Dict[str, Any]:
    def _run():
        llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
        agents = MyAgents()
        analysis_agent = agents.call_analysis_agent(llm)

        tasks = MyTasks()
        analysis_task = tasks.call_analysis_task(transcription, analysis_agent)

        crew = Crew(
            agents=[analysis_agent],
            tasks=[analysis_task],
            verbose=True,
        )
        return crew.kickoff()

    result = await anyio.to_thread.run_sync(_run)

    if hasattr(result, "raw"):
        raw_output = result.raw
    elif isinstance(result, dict) and "result" in result and "raw" in result["result"]:
        raw_output = result["result"]["raw"]
    else:
        raise ValueError("Unexpected result format from crew.kickoff")

    cleaned = re.sub(r"^```json|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

    try:
        parsed_json = json.loads(cleaned)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from LLM output: {e}")

