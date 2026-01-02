import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

request_counts = defaultdict(list)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        current_time = time.time()
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < RATE_LIMIT_WINDOW
        ]
        
        if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas requisições. Tente novamente em alguns instantes.",
                headers={"Retry-After": str(RATE_LIMIT_WINDOW)}
            )
        
        request_counts[client_ip].append(current_time)
        
        response = await call_next(request)
        return response

