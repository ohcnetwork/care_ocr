import base64
import json
from datetime import datetime


def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")


def prediction_parser(prediction):
    json_start = prediction.find("{")
    json_end = prediction.rfind("}") + 1

    json_prediction = json.loads(prediction[json_start:json_end])
    json_prediction["time_stamp"] = datetime.fromisoformat(
        json_prediction["time_stamp"]
    ).isoformat()

    return json_prediction
