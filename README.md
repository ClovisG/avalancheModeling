# avalancheModeling


Irstea shares online a big dataset of avalanche events. The format is in PDF and can be downloded from ftp://avalanchesftp.grenoble.cemagref.fr/epaclpa/EPA_listes_evenements/

In the scripts/ folder, one can find draft for parsing this data to tabular form.

## Parsing of EPA data

### Requirements

Needed
* Python3
* pdftotext (can be found at *https://gitlab.freedesktop.org/poppler/poppler/commits/master*)

### Parsing the data

Edit the path in the scripts and run:
```
sh parse.sh
```
To transform the PDFs to txt files.

Then you can parse the txt files to create a Python a list of dictionnaries for each event:
```
python3 txtToDict.py epaParsed/*
```
It will create a pickle file *events.dict* containing the data, ready to be used in Python.



If you want to load your data in R, transform the python dictionnaries to TSV files:
```
python3 dictToTsv.py
```

There is still some bugs in the parsing of the data, feel free to improve the scripts!

### Notes on the CampToCamp.org API

Can query outings through:
```
https://api.camptocamp.org/outings?bbox=-549043%2C4306073%2C1466449%2C6933061&act=skitouring&date=2016-11-20%2C2016-11-26&pl=fr
```

Converting WGS84 GPS coordinate system to Web Mercator Bbox in Python:
```
from pyproj import Proj, transform
print(transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), -0.1285907, 51.50809))  # longitude first, latitude second.
```

### Notes for reading the Shapefiles for EPA data

One can use the Python lib at https://github.com/GeospatialPython/pyshp
