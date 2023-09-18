'''
Translate image files using Naver's Papago API
'''

import base64
import functools
import getpass
import json
import os
import pathlib
import shutil
import uuid


import requests
import requests_toolbelt
import PIL.Image as Image


@functools.lru_cache(maxsize=1)
def get_application_id() -> str:
  id = os.getenv('NAVER_APPLICATION_ID')
  if id is None:
     id = getpass.getpass('NAVER_APPLICATION_ID: ')
  return id


@functools.lru_cache(maxsize=1)
def get_secret() -> str:
  sec = os.getenv('NAVER_SECRET')
  if sec is None:
     sec = getpass.getpass('NAVER_SECRET: ')
  return sec


def save_sample_img(write_path:pathlib.Path=pathlib.Path('sample_en.png')):
    url = 'https://user-images.githubusercontent.com/17876446/268568007-59e0cd8b-4d66-49d3-897e-74909da3a7c6.png'
    response = requests.get(url)
    img = response.content

    write_path.write_bytes(img)


# %% [markdown]
# ## Translate image
# * ko : https://api.ncloud-docs.com/docs/ai-naver-imagetoimageapi
# * en : https://api.ncloud-docs.com/docs/en/ai-naver-imagetoimageapi
# 
# 


def rezize_img(img_path:pathlib.Path, tgt_size:int=1920):
    # https://stackoverflow.com/questions/9174338/programmatically-change-image-resolution
    img = Image.open(img_path)
    ratio = tgt_size / max(img.size)
    if ratio < 1.0:
        ratio *= 0.9 # to be on a safer side
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.ANTIALIAS)
        img.save(img_path)


def translate_img(image_path:pathlib.Path, src:str, tgt:str, tgt_folder:pathlib.Path, User_client_ID:str, User_client_secret:str):
    print(f'Processing {image_path.name}'.ljust(60, '='))
    data = {
    'source': src,
    'target': tgt,
    'image': (image_path.name, image_path.open('rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }
    print('Encoding Start '.ljust(40, '='))
    m = requests_toolbelt.MultipartEncoder(data, boundary=uuid.uuid4())
    print('Encoding Done '.ljust(40, '='))

    headers = {
    "Content-Type": m.content_type,
    "X-NCP-APIGW-API-KEY-ID": User_client_ID,
    "X-NCP-APIGW-API-KEY": User_client_secret
    }

    url = " https://naveropenapi.apigw.ntruss.com/image-to-image/v1/translate"
    print('Posting Start '.ljust(40, '='))
    res = requests.post(url, headers=headers, data=m.to_string())
    # print(res.text)
    print('Posting Done '.ljust(40, '='))

    tgt_path = tgt_folder / pathlib.Path(image_path).name

    try:
        assert not res.json().get('error'), res.json().get('error')
    except AssertionError as e:
        print(res.json().get('errorMessage'))
        err = res.json().get('error')
        if err['errorCode'] == '26007': # No text in image
            print(f'No text in image: {image_path.name}')
            shutil.copy(image_path, tgt_path)
        else:
            raise e
    else:
        # renderedImage -> Image output
        resObj = json.loads(res.text)
        imageStr = resObj.get("data").get("renderedImage")
        imgdata = base64.b64decode(imageStr)

        print('Writing Start '.ljust(40, '='))
        tgt_path.write_bytes(imgdata)
        print('Writing Done '.ljust(40, '='))
        print(f'Finished Processing {image_path.name}'.ljust(60, '='))


def main():
    input_folder = pathlib.Path('pdf2png')
    assert input_folder.exists(), f"'{input_folder}' does not exist"
    assert input_folder.is_dir(), f"'{input_folder}' is not a directory"
    assert input_folder.glob('*.png'), f"'{input_folder}' does not contain any png files"

    target_folder = pathlib.Path('target')
    target_folder.mkdir(exist_ok=True)

    assert target_folder.exists(), f"'{target_folder}' does not exist"
    assert target_folder.is_dir(), f"'{target_folder}' is not a directory"

    assert os.getenv('SRC', False), 'SRC is not set'
    assert os.getenv('TGT', False), 'TGT is not set'

    for input_png in input_folder.glob('*.png'):
        rezize_img(input_png)
        
        translate_img(
            input_png, os.environ['SRC'], os.environ['TGT'], target_folder,
            get_application_id(), get_secret()
        )


if "__main__" == __name__: 
    main()
