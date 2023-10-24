import traceback

from starlette.responses import JSONResponse

from routes.predict_v2.ai_helpers.chain import ChatChain


async def predict_v2(request):
    
    try:
      data = await request.json()

      if "ocr_data" not in data:
          return JSONResponse(status_code= 400, content={"error": "ocr_data not found"})
      
      ocr_data = data["ocr_data"]

      chat_chain = ChatChain(ocr_data)
      response = await chat_chain.async_predict()

      return JSONResponse({"data": response})
    
    except Exception as e:
      traceback.print_exc()
      return JSONResponse(status_code=500, content={"error": "Something went wrong"})
