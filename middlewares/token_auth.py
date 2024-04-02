from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from config import API_AUTH_TOKEN


class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                {"error": "Authorization token is missing"}, status_code=401
            )

        token_value = token.split(" ")[-1]

        if token_value != API_AUTH_TOKEN:
            return JSONResponse(
                {"error": "Invalid Authorization token"}, status_code=401
            )

        return await call_next(request)
