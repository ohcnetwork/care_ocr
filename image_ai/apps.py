from django.apps import AppConfig
import keras_ocr 

class ImageAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_ai'
    pipeline = keras_ocr.pipeline.Pipeline()
