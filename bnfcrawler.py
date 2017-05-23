import requests
import os
import shutil

start, end = 215, 350
bookid = "btv1b8447879g"

try:
    os.makedirs(bookid)
except Exception as E:
    print(E)

for i in range(start, end+1):
    print("Downloading {current}/{end}".format(current=i, end=end))
    uri ="http://gallica.bnf.fr/ark:/12148/{0}/f{1}.highres".format(bookid, i)
    response = requests.get(uri, stream=True)
    with open("{0}/{0}.p{1}.jpg".format(bookid, i), "wb") as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)