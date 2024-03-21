import traceback
import io

from starlette.responses import JSONResponse

from api.predict_v2.ai_helpers.parse_chain_v2 import ParseChainV2


async def predict_api_v2(request):

    try:
        form = await request.form()

        if "image" not in form:
            return JSONResponse(status_code=400, content={"error": "Image not found"})

        filename = form["image"].filename
        image_content = await form["image"].read()
        image_content = io.BytesIO(image_content)

        parse_chain = ParseChainV2(image_content)
        response = await parse_chain.async_predict()

        return JSONResponse({"status": 200, "message": "success", "data": response})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})
