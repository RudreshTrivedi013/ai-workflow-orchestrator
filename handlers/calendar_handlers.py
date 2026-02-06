import json
from core.llm_client import call_llm
from core.prompts import CALENDAR_PROMPT
from retrieval.calendar_store import save_event

def create_event(text: str):
    prompt = CALENDAR_PROMPT.format(text=text)
    response = call_llm(prompt)

    try:
        event = json.loads(response)
        save_event(event)
        return event
    except Exception:
        return {"error": "Invalid LLM response"}
