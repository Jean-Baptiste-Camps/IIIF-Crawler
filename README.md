# IIIF-Crawler

Tool to interrogate IIIF servers and get images of manuscripts.

Forked from PonteIneptique's bnfcrawler, [https://gist.github.com/PonteIneptique/adbb7472b9ced07ca9287fbf2e1584ce](https://gist.github.com/PonteIneptique/adbb7472b9ced07ca9287fbf2e1584ce) !

Currently implemented:

- gallica;
- e-codices (beta);
- bvmm
- … (more to come).

## Usage

```bash
python3 iiifcrawler.py ID --source SOURCE --start 1 --end 2
```
where ID is the identifier of the manuscript, e.g. the ark `btv1b9059486c` or the code `bbb-0113`, or `Boulogne-sur-Mer/B621606201_MS0192`, SOURCE, the source from which to download (currently, only `gallica` and `e-codices`, and 1 and 2 are the beginning and end folios you want to download (N.B.: page number are different on Gallica, and E-Codices, so, on E-Codices, `15` to `16` will send back four pages, 15r to 16v).

Alternatively, you can pass a csv file with the relevant informations (see `example.csv`).

```bash
python3 iiifcrawler.py example.csv
```

