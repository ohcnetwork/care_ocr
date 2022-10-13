from tkinter import Image
from django.db import DatabaseError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
import cloudinary.uploader
from image_ai.utils import main
import cv2
from django.conf import settings
import numpy
from PIL import Image

class UploadPredictView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get("image")
        save_path = str(settings.ROOT_DIR) + "/image/" + file.name
        # img = cv2.imdecode(numpy.frombuffer(file.read() , numpy.uint64), cv2.IMREAD_UNCHANGED)
        # img = Image.fromarray(img)
        # img.save(save_path)

        # data = main(save_path)
        # upload_data = cloudinary.uploader.upload(file)
        # # print(upload_data)
        # img = upload_data["url"]
        img = Image.open(file).save(save_path)
       
        data = main(save_path)
        return Response(
            {
                "status": "success",
                "url": "file_url",
                "data": data,
            },
            status=201,
        )


# Create your views here.
