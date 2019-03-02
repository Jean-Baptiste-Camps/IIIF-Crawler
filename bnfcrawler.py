import requests
import os
import shutil
import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="Download Full Quality sets of pages from Gallica")
parser.add_argument("text", type=str, help="either the ID of the text (in http://gallica.bnf.fr/ark:/12148/btv1b53084829z/, this would be btv1b53084829z), or the path to a .csv file containing relevant information")
parser.add_argument("--start", type=int, default=1, help="Page to start from")
parser.add_argument("--end", type=int, default=None, help="Page to end at")


def dl_write(i, bookid):
    uri = "http://gallica.bnf.fr/iiif/ark:/12148/{0}/f{1}/full/full/0/native.jpg".format(bookid, i)
    response = requests.get(uri, stream=True)
    with open("{0}/p{1}.jpg".format(bookid, i), "wb") as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)


def read_csv(file):
    with open(file, 'r') as f:

        if not f.readline().split('\t') == ['ID', 'source', 'start', 'end\n']:
            sys.stderr.write("Error: csv file must have headings 'ID', 'source', 'start', 'end'\n")
            sys.exit(1)

        mss = []
        for line in f.readlines():
            mss.append(line.rstrip().split('\t'))

    return mss


def ms_dl(bookid, start, end):
    try:
        os.makedirs(bookid)
    except Exception as E:
        pass

    if end is None:
        dl_write(i, bookid)
    else:
        for i in range(start, end + 1):
            print("Downloading {current}/{end}".format(current=i, end=end))
            # Thanks to @seeksanusername for the native format URL as I was using highres before
            # https://medium.com/@seeksanusername/astuce1-r%C3%A9cup%C3%A9rer-de-la-hd-sur-gallica-bef0a6cc7f89
            dl_write(i, bookid)


if __name__ == "__main__":
    args = parser.parse_args()

    text = args.text

    if text.endswith(".csv"):
        mss = read_csv(text)
        for ms in mss:
            print("Now downloading: {}".format(ms[0]) )
            ms_dl(ms[0], int(ms[2]), int(ms[3]))


    else:
        start, end = args.start, args.end
        bookid = text
        ms_dl(bookid, start, end)

