import time

def retry(fn, retries=3):
    for _ in range(retries):
        try:
            return fn()
        except:
            time.sleep(1)
    return None
