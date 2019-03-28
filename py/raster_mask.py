#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      nkolarik
#
# Created:     24/10/2017
# Copyright:   (c) nkolarik 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import arcpy
from arcpy import env
from arcpy.sa import *

def raster_mask(rootdir):
    """
    Subsetting SfM/MVS products to isolate "non-distorted" portion
    of imagery.

    Assumes directory structure of rootdir\refID\sensor\output...
    """

    arcpy.CheckOutExtension("Spatial")
    refIDs = []
    for subdir in os.listdir (rootdir):
        refIDs.append(rootdir + "\\" + subdir)
    #print refID
    for refID in refIDs:
        mask = refID + "\\points2_ENV2.shp"
        sensors =  ["\\Mavic", "\\Sequoia"]

        for sensor in sensors:
            for file in os.listdir(refID + sensor + "\\Output"):
                if file == "Stack.tif":
                    #print file
                    outExtractByMask = ExtractByMask(os.path.join(refID + sensor + "\\Output", file), mask)
                    time.sleep(2)
                    outExtractByMask.save(os.path.splitext(refID + sensor + "\\Output\\" + file)[0] + "_sbst2.tif" )
                    time.sleep(2)
                    outExtractByMask = None
                    ##clears background workspace?
                    print (refID + " FINISHED")


def main():
    rootdir = "C:\\Users\\nkolarik\\Desktop\\Kazava_Local"
    raster_mask(rootdir)

if __name__ == '__main__':
    #main()
