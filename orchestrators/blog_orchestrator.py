from core.llm_client import llm_call
from core.schemas import BLOG_PLAN_SCHEMA
from core.utils import safe_json_parse

def blog_orchestrator(topic):
    plan_prompt = f"""
    Create blog plan.
    JSON: {BLOG_PLAN_SCHEMA}
    Topic: {topic}
    """
    plan = safe_json_parse(llm_call(plan_prompt))

    content = ""
    for sec, wc in zip(plan["sections"], plan["word_count_per_section"]):
        content += f"\n### {sec}\n"
        content += llm_call(f"Write {wc} words on {sec}")

    return llm_call(f"Polish this blog:\n{content}", max_tokens=4000)
