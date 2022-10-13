from tkinter import Image
from django.db import DatabaseError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from image_ai.utils import main
from django.conf import settings
from PIL import Image
import os

class UploadPredictView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get("image")
        save_path = str(settings.ROOT_DIR) + "/image/" + file.name
        Image.open(file).save(save_path)
       
        data = main(save_path)
        os.remove(save_path)
        return Response(
            {
                "status": "success",
                "url": "file_url",
                "data": data,
            },
            status=201,
        )


# Create your views here.
