import arcpy
from arcpy.sa import *
import os

def height_thresh(chm_dir, thresh_dir):
    """
    Creating height threshold maps from the georeferenced CHMs for each site
    flown, for each band in the Parrot Sequoia sensor and the Mavic RGB camera.
    Pixelss >= 3m are assigned a value of 2 (trees), and pixels >= 1m AND
    < 3m are assigned a value of 1 (shrub), while all others are 0.

    First param is the directory where CHM are stored assuming a
    "Cover/Reference Id/CHM for each band" structure. Second is the directory
    where the output rasters are to be stored.
    """
    ## Checking out the Spatial Analyst extension for handling rasters
    arcpy.CheckOutExtension("Spatial")
        ## Looping through covers
    for cover in os.listdir(chm_dir):
        ## Looping through reference IDs
        for refID in os.listdir(os.path.join(chm_dir, cover)):
            for item in os.listdir(os.path.join(chm_dir, cover, refID, "warped")):
                infile = os.path.join(chm_dir, cover, refID, "warped", item)
                if "rgb" in item:
                    outfile = os.path.join(thresh_dir, cover, refID, os.path.splitext(item)[0][:-9] + "thresh.tif")
                else:
                    outfile = os.path.join(thresh_dir, cover, refID, os.path.splitext(item)[0][:-7] + "thresh.tif")
                ## assigning values based on height estimates
                if item.endswith(".tif"):
                    tree = Con(infile, 2, 0 , "VALUE >= 3")
                    shrub = Con(infile, 1, 0 , "VALUE < 3 AND VALUE >= 1")
                    woody = tree + shrub
                    woody.save(outfile)
                    print("{} trees and shrubs are combined here: {}".format(refID, outfile))


def main():
    chm_dir = "C:\\Users\\nkolarik\\Desktop\\IDW_tst\\CHM"
    #chm_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\data\\CHM"
    #thresh_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\thresh"
    thresh_dir = "C:\\Users\\nkolarik\\Desktop\\IDW_tst\\output\\thresh"


    height_thresh(chm_dir, thresh_dir)

if __name__ == '__main__':
    main()
