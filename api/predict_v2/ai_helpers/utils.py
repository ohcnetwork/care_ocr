import base64


def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")


def prediction_parser(prediction):
    json_start = prediction.find("{")
    json_end = prediction.rfind("}") + 1

    return prediction[json_start:json_end]
