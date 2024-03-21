from starlette.responses import JSONResponse


async def ping(request):
    return JSONResponse({"status": 200, "message": "pong", "data": {}})
