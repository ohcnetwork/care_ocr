from django.conf import settings
from yolov5.detect import run
import cv2
from image_ai.apps import ImageAiConfig


def crop_img(img_url):

    run(
        weights=settings.MODEL_PATH,
        save_crop = True,
        imgsz = (480, 480),
        conf_thres=0.6,
        source=img_url,
        exist_ok=True
    )
    dir_path = settings.YOLO_PATH + "/runs/detect/exp/crops/monitor"
    img_name = img_url.split("/")[-1].split(".")[0]
    img_name = img_name + ".jpg"
    img_path = dir_path + "/" + img_name
    img = cv2.imread(img_path)
    # getting 30% right side part of image
    col = (img.shape[1]*70)//100

    crop_img = img[:, col:]
    save_path = settings.YOLO_PATH + "/crop/crop.png"
    cv2.imwrite(save_path, crop_img)

    return save_path
    # return crop_img

def extract_data(cropped_image_path):
    data_dict = {}
    txt = ImageAiConfig.reader.readtext(cropped_image_path, detail=0)
    print("-"*20)
    print(txt)
    print("-"*20)
    data_dict = {}
    headings = ["Blood Pressure", "Pulse Rate", "SpO2", "Respiratory Rate", "Temperature"]
    counter = 0
    for text in txt:
        length = len(text)
        if('.' in text and counter == 0):
            continue
        if(text.isnumeric() or "/" in text or "." in text):
            if(((length == 2 or length == 3 ) and ("." not in text)) and counter == 0 and headings[0] not in data_dict.keys()):
                print(f"{headings[0]}: {text}")
                data_dict[headings[0]] = text

                
            elif(("/" in text or length == 6 or length == 7 )and counter == 1 and headings[1] not in data_dict.keys()):
                text_1 = text[0:3]
                text_2 = text[4:]
                print(f"{headings[1]}: {text_1}/{text_2}")
                data_dict[headings[1]] = f"{text_1}/{text_2}"
                
            elif(text.isnumeric() and int(text) >= 0 and int(text) <=100 and headings[2] not in data_dict.keys()):
                print(f"{headings[2]}: {text}")
                data_dict[headings[2]] = text
                
            elif(text.isnumeric() and length == 2 and headings[3] not in data_dict.keys()):
                print(f"{headings[3]}: {text}")
                data_dict[headings[3]] = text
                
            elif("." in text or length == 3 and headings[4] not in data_dict.keys()):
                text_1, text_2 = text.split(".")
                print(f"{headings[4]}: {text_1}.{text_2}")
                data_dict[headings[4]] = f"{text_1}.{text_2}"
            counter+=1


    return data_dict

def main(img_url):
    crop_img_path = crop_img(img_url)
    return extract_data(crop_img_path)


    


