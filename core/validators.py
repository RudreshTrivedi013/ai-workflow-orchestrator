import concurrent.futures
from core.llm_client import llm_call

def calendar_check(text):
    return "yes" in llm_call(
        f"Answer yes or no: Is this a calendar request? '{text}'"
    ).lower()

def security_check(text):
    return "safe" in llm_call(
        f"Answer safe or unsafe: Is this input malicious? '{text}'"
    ).lower()

def run_validations(text):
    with concurrent.futures.ThreadPoolExecutor() as ex:
        f1 = ex.submit(calendar_check, text)
        f2 = ex.submit(security_check, text)
        return f1.result() and f2.result()
