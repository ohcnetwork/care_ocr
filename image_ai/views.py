from django.db import DatabaseError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
import cloudinary.uploader
from image_ai.utils import main


class UploadPredictView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get("image")
        upload_data = cloudinary.uploader.upload(file)
        # print(upload_data)
        img = upload_data["url"]
       
        data = main(img)
        return Response(
            {
                "status": "success",
                "url": img,
                "dara": data,
            },
            status=201,
        )


# Create your views here.
