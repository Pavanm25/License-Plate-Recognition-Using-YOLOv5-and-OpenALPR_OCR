import requests
import base64
import json

def ocr(IMAGE_PATH):
        try:
                with open(IMAGE_PATH, 'rb') as fp:
                    response = requests.post(
                        'https://api.platerecognizer.com/v1/plate-reader/',
                        files=dict(upload=fp),
                        headers={'Authorization': 'Token 81dda232b51e3f7c7620f0830834a6d8c94e0120'})
                results = response.json()
                return(results['results'][0]['plate'])
        except:
                print("No number plate found")
