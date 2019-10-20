import requests
import DataModels
import json

RANDOM_IMAGE_URL = "https://xtima6ctq9.execute-api.us-east-1.amazonaws.com/dev/"
CLARIFAI_MODEL_URL = "https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs"
CLARIFAI_AUTH_HEADER = "Key 5387ffaf015e40f6a12d782172f88fa9"

def getCaptchaImages(count, previousImages):
    images = []
    urls = []
    x = 1
    while x <= count:
        r = requests.get(url = RANDOM_IMAGE_URL)
        data = r.json()
        url = data['imageUrl']
        if url not in urls and url not in previousImages:
            img = DataModels.CaptchaImage(len(images) + 1,data['imageUrl'])
            urls.append(url)
            images.append(img)
            x = x + 1
    return images

def validteCaptchaSelection(images):
    valid = True
    apiReq = DataModels.ClarifaiRequest()
    apiReqImages = []
    for img in images:
        apiReq.inputs.append({"data": {"image": {"url": img['url']}}})
    resp = DataModels.AppResponse()
    data = apiReq.serialize()
    headers = {'Authorization': CLARIFAI_AUTH_HEADER, 'content-type':'application/json'}
    r = requests.post(url = CLARIFAI_MODEL_URL, json = data, headers = headers)
    jsonResp = r.json()
    if jsonResp['status']['code'] == 10000:
        for img in images:
            isPie = False
            for output in jsonResp['outputs']:    
                if output['input']['data']['image']['url'] == img['url']:
                    for c in output['data']['concepts']:
                        if c['name'] == 'pie' and c['value'] > 0.5:
                            isPie = True
                            break
                    break
            if not isPie == img['selected']:
                valid = False
                break
    if valid:
        resp = DataModels.AppResponse(True, 'OK','OK')
    else:
        resp = DataModels.AppResponse(False,'FAIL','Invalid Submission')
    return resp
