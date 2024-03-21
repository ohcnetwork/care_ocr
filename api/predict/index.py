import traceback

from starlette.responses import JSONResponse

from api.predict.ai_helpers.parse_chain import ParseChain
from api.predict.ai_helpers.ocr_helper import get_ocr_data


async def predict_api(request):

    try:
        form = await request.form()

        if "image" not in form:
            return JSONResponse(status_code=400, content={"error": "Image not found"})

        filename = form["image"].filename
        image_content = await form["image"].read()
        ocr_data = get_ocr_data(image_content, filename)

        parse_chain = ParseChain(ocr_data)
        response = await parse_chain.async_predict()

        return JSONResponse({"status": 200, "message": "success", "data": response})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})
