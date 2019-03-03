import requests
import os
import shutil
import sys
from argparse import ArgumentParser

# TODO: modify code, to access and parse IIIF Manifest instead !

parser = ArgumentParser(description="Download Full Quality sets of pages from Gallica")
parser.add_argument("text", type=str,
                    help="either the ID of the text (in http://gallica.bnf.fr/ark:/12148/btv1b53084829z/, this would be btv1b53084829z), or the path to a .csv file containing relevant information")
parser.add_argument("--source", type=str, default='gallica',
                    help="Source from which to download (e.g., gallica, e-codices, bvmm)")
parser.add_argument("--start", type=int, default=1, help="Page to start from")
parser.add_argument("--end", type=int, default=None, help="Page to end at")


def dl_write(i, source, bookid):

    if source == 'gallica':
        uri = "http://gallica.bnf.fr/iiif/ark:/12148/{0}/f{1}/full/full/0/native.jpg".format(bookid, i)

    elif source == 'e-codices':
        bibl = bookid.split('-')[0]

        # https://www.e-codices.unifr.ch/loris/bbb/bbb-0113/bbb-0113_e002.jp2/full/full/0/default.jpg
        uri = "https://www.e-codices.unifr.ch/loris/{0}/{1}/{1}_{2}.jp2/full/full/0/default.jpg".format(bibl, bookid, i)

    elif source == 'bvmm':
        bibl = bookid.split('/')[0]
        trueid = bookid.split('/')[1]
        page = trueid[1:] + '_' + str(i).zfill(4)
        # https://iiif.irht.cnrs.fr/iiif/Boulogne-sur-Mer/B621606201_MS0192/jp2/621606201_MS0192_0010/full/full/0/default.jpg
        uri = "https://iiif.irht.cnrs.fr/iiif/{0}/{1}/jp2/{2}/full/full/0/default.jpg".format(bibl, trueid, page)

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


def ms_dl(bookid, source, start, end):
    try:
        os.makedirs(bookid)
    except Exception as E:
        pass

    if end is None:
        dl_write(i, bookid)
    else:

        if source == 'e-codices':
            pages = []
            for i in range(start, end + 1):
                pages.append(str(i).zfill(3)+'r')
                pages.append(str(i).zfill(3) + 'v')

        else:
            pages = range(start, end + 1)

        for i in pages:
            print("Downloading {current}/{end}".format(current=i, end=end))
            # Thanks to @seeksanusername for the native format URL as I was using highres before
            # https://medium.com/@seeksanusername/astuce1-r%C3%A9cup%C3%A9rer-de-la-hd-sur-gallica-bef0a6cc7f89
            dl_write(i, source, bookid)


if __name__ == "__main__":
    args = parser.parse_args()

    text = args.text

    if text.endswith(".csv"):
        mss = read_csv(text)
        for ms in mss:
            print("Now downloading: {}".format(ms[0]))
            ms_dl(ms[0], ms[1], int(ms[2]), int(ms[3]))

    else:
        source, start, end = args.source, args.start, args.end
        bookid = text
        ms_dl(bookid, source, start, end)
