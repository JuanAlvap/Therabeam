import base64
import requests

class Client:

    def __init__(self):
        pass

    def upload(self, img):
        url = 'http://localhost:3455/newupload'

        headers = {'Content-Type': 'application/json'}

        with open(img, 'rb') as f:
            bfiles = base64.b64encode(f.read())
        print(bfiles)
        print("--------------------------")

        r = requests.post(url,headers=headers, json={"uploadedimage" : bfiles.decode("ascii")})

        if r.status_code == 200:
            print("IMAGE UPLOAD SUCCESSFULL")
        else:
            print("ERROR")


c = Client()
c.upload('Skin Contours.png')


    




