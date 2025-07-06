from fastapi import Request, HTTPException
from time import time
from collections import defaultdict
from config import RATE_LIMIT

rate_limit_store = defaultdict(list)

def rate_limiter(request: Request):
    ip = request.client.host
    now = time()
    window = 3600
    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < window]
    if len(rate_limit_store[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    rate_limit_store[ip].append(now)
