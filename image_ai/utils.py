from django.conf import settings
from yolov5.detect import run
import cv2
from image_ai.apps import ImageAiConfig
import keras_ocr 

def crop_img(img_url):

    run(
        weights=settings.MODEL_PATH,
        save_crop = True,
        imgsz = (480, 480),
        conf_thres=0.6,
        source=img_url,
        exist_ok=True
    )
    dir_path = settings.YOLO_PATH + "/runs/detect/exp2/crops/monitor"
    img_name = img_url.split("/")[-1]
    img_path = dir_path + "/" + img_name
    img = cv2.imread(img_path)
    # getting 30% right side part of image
    col = (img.shape[1]*70)//100

    crop_img = img[:, col:]
    save_path = settings.YOLO_PATH + "/crop/crop.png"
    cv2.imwrite(save_path, crop_img)

    return save_path

def extract_data(cropped_image_path):
    
    pipeline = ImageAiConfig.pipeline
    images = [ keras_ocr.tools.read(path) for path in [
      cropped_image_path
    ]]

    prediction_groups = pipeline.recognize(images)

    data = {}
    headings = ["Blood Pressure", "Pulse Rate", "SpO2", "Respiratory Rate", "Temperature"]
    counter = 0
    for text, box in prediction_groups[0]:
        length = len(text)
        if(text.isnumeric() or "/" in text or "." in text):
            if((length == 2 or length == 3) and counter == 0):
                # print(f"{headings[0]}: {text}")
                data[headings[0]] = text
                counter+=1
            elif("/" in text or length == 6 or length == 7 and counter == 1):
                text_1 = text[0:3]
                text_2 = text[4:]
                # print(f"{headings[1]}: {text_1}/{text_2}")
                data[headings[1]] = f"{text_1}/{text_2}"
                counter+=1
            elif(text.isnumeric() and int(text) >= 0 and int(text) <=100 and counter == 2):
                # print(f"{headings[2]}: {text}")
                data[headings[2]] = text
                counter+=1
            elif(text.isnumeric() and length == 2 and counter == 3):
                # print(f"{headings[3]}: {text}")
                data[headings[3]] = text
                counter+=1
            elif("." in text or length == 3 and (counter == 3 or counter == 4)):
                text_1 = text[0:2]
                text_2 = text[2:]
                # print(f"{headings[4]}: {text_1}.{text_2}")
                data[headings[4]] = f"{text_1}.{text_2}"

    return data

def main(img_url):
    crop_img_path = crop_img(img_url)
    extract_data(crop_img_path)


    


