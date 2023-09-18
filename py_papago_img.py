import requests
from requests_toolbelt import MultipartEncoder
import uuid
import json
import base64


def translate_img(image_path, src, tgt, tgt_folder, User_client_ID, User_client_secret):
    data = {
    'source': src,
    'target': tgt,
    'image': (image_path, open(image_path, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }
    m = MultipartEncoder(data, boundary=uuid.uuid4())

    headers = {
    "Content-Type": m.content_type,
    "X-NCP-APIGW-API-KEY-ID": User_client_ID,
    "X-NCP-APIGW-API-KEY": User_client_secret
    }

    url = " https://naveropenapi.apigw.ntruss.com/image-to-image/v1/translate"
    res = requests.post(url, headers=headers, data=m.to_string())
    print(res.text)

    # renderedImage -> Image output
    resObj = json.loads(res.text)
    imageStr = resObj.get("data").get("renderedImage")
    imgdata = base64.b64decode(imageStr)

    tgt_path = tgt_folder / image_path.name
    tgt_path.wrtie_bytes(imgdata)
