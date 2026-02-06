from core.llm_client import call_llm
from core.prompts import EMAIL_PROMPT

def run_email_flow(purpose, recipient, context):
    prompt = EMAIL_PROMPT.format(
        purpose=purpose,
        recipient=recipient,
        context=context
    )
    return call_llm(prompt)
