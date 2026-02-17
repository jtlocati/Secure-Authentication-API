#protect against Dos attacks
import time
from collections import defaultdict, deque
from typing import Deque, DefaultDict, Tuple
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

#in-memory rate limiter
"""
-Limits requests dept on client_ip, path in a rolling window
- in real applications use Redis
"""
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
            super().__init__(app)
            self.max_requests = max_requests
            self.window_seconds = window_seconds
            self.hits = defaultdict(deque)  # key -> timestamps

    def _key(self, request: Request) -> str:
            # simplest: per-client IP
            client = request.client.host if request.client else "unknown"
            return client

    async def dispatch(self, request: Request, call_next):
            key = self._key(request)
            now = time.time()

            q = self.hits[key]

            # remove timestamps outside the window
            cutoff = now - self.window_seconds
            while q and q[0] < cutoff:
                q.popleft()

            if len(q) >= self.max_requests:
                return JSONResponse(
                    {"detail": "Too many requests"},
                    status_code=429,
                    headers={"Retry-After": str(self.window_seconds)},
                )

            q.append(now)
            return await call_next(request)

