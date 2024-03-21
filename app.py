from dotenv import dotenv_values
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
import uvicorn

from api import health_check, ping, predict_api, predict_api_v2

config = dotenv_values(".env")

BASE_URL = "/api/"

routes = [
    Route(BASE_URL + "ping", ping, methods=["GET"]),
    Route(BASE_URL + "health-check", health_check, methods=["GET"]),
    Route(BASE_URL + "v1/predict", predict_api, methods=["POST"]),
    Route(BASE_URL + "v2/predict", predict_api_v2, methods=["POST"]),
]

middleware = [
    Middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
