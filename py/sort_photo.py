import os
import shutil
import sys

## makes directories for each band of sequoia data and
## moves photos into appropriate directories

veg = sys.argv[1]

sites = os.listdir(veg)
sites.remove('Products')
for site in sites:

    photos = os.path.join(veg, site, "Sequoia")
    file_list = os.listdir(photos)

    nir = [photo for photo in file_list if "NIR" in photo]
    gre = [photo for photo in file_list if "GRE" in photo]
    red = [photo for photo in file_list if "RED" in photo]
    reg = [photo for photo in file_list if "REG" in photo]

    for band in ['nir', 'gre', 'red', 'reg']:
        os.mkdir(os.path.join(photos, band))

    for band in [nir, gre, red, reg]:
        for photo in band:
            if band == nir:
                shutil.move(os.path.join(photos, photo), os.path.join(photos, "nir"))
            if band == gre:
                shutil.move(os.path.join(photos, photo), os.path.join(photos, "gre"))
            if band == red:
                shutil.move(os.path.join(photos, photo), os.path.join(photos, "red"))
            if band == reg:
                shutil.move(os.path.join(photos, photo), os.path.join(photos, "reg"))


