from django.apps import AppConfig
import easyocr

class ImageAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_ai'
    reader = easyocr.Reader(['en'])
