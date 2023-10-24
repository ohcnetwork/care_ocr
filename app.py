from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn
import io
from base import ROOT_DIR
from PIL import Image
import os

from utils import main
from base import reader
from routes import predict_v2

async def predict(request):
    form = await request.form()
    filename = form["image"].filename
    contents = await form["image"].read()
    contents = io.BytesIO(contents)
    # print(type(contents))
    save_path = str(ROOT_DIR) + "/image/" + filename
    Image.open(contents).save(save_path)
    
    data = main(save_path)
    os.remove(save_path)

    return JSONResponse(
        {
            "status": "success",
            "url": "file_url",
            "data": data,
        },
    )

async def get_ocr_data(request):
    form = await request.form()
    filename = form["image"].filename
    contents = await form["image"].read()
    contents = io.BytesIO(contents)
    save_path = str(ROOT_DIR) + "/image/" + filename
    Image.open(contents).save(save_path)

    data = reader.readtext(save_path)
    data = [{"bounding_box": d[0], "text": d[1], "confidence": d[2]} for d in data]
    for d in data:
        d["bounding_box"] = [[int(x), int(y)] for x, y in d["bounding_box"]]
    os.remove(save_path)

    return JSONResponse(
        {
            "status": "success",
            "data": data,
        },
    )



routes = [
    Route('/api/predict', predict, methods=['POST']),
    Route('/api/get-ocr-data', get_ocr_data, methods=['POST']),
    Route('/api/predict-v2', predict_v2, methods=['POST']),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)