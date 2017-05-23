import requests
import os
import shutil
from argparse import ArgumentParser

parser = ArgumentParser(description="Download Full Quality sets of pages from the BNF")
parser.add_argument("text", type=str, help="ID of the text. In http://gallica.bnf.fr/ark:/12148/btv1b53084829z/, this would be btv1b53084829z")
parser.add_argument("--start", type=int, default=1, help="Page to start from")
parser.add_argument("--end", type=int, default=None, help="Page to end at")

def dl_write(i, bookid):
    uri = "http://gallica.bnf.fr/iiif/ark:/12148/{0}/f{1}/full/full/0/native.jpg".format(bookid, i)
    response = requests.get(uri, stream=True)
    with open("{0}/p{1}.jpg".format(bookid, i), "wb") as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)

if __name__ == "__main__":
    args = parser.parse_args()

    start, end = args.start, args.end
    bookid = args.text

    try:
        os.makedirs(bookid)
    except Exception as E:
        pass

    if end is None:
        dl_write(i, bookid)
    else:
        for i in range(start, end+1):
            print("Downloading {current}/{end}".format(current=i, end=end))
            # Thanks to @seeksanusername for the native format URL as I was using highres before
            # https://medium.com/@seeksanusername/astuce1-r%C3%A9cup%C3%A9rer-de-la-hd-sur-gallica-bef0a6cc7f89
            dl_write(i, bookid)
