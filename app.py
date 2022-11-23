from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
import uvicorn
import io
from base import ROOT_DIR
from PIL import Image
import os
from utils import main


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


routes = [
    Route('/api/predict', predict, methods=['POST'])
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)