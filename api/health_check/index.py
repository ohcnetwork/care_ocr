from starlette.responses import JSONResponse


async def health_check(request):
    return JSONResponse({"status": 200, "message": "success", "data": {}})
