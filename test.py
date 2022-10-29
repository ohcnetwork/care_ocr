from urllib import response
import requests

url="http://127.0.0.1:8000/api/predict"
files={"image":open("./data/image.png", "rb")}

response = requests.post(url=url, files=files)

print(response.json())