#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      nkolarik
#
# Created:     13/09/2017
# Copyright:   (c) nkolarik 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import arcpy
from arcpy import env
from arcpy.sa import *

def photo2env(rootdir, bufferDist):
    """
    Creates a point layer from geotagged photos, buffers to set distance,
    creates polygon to encompass all buffered areas.

    Assumes directory structure of rootdir\refID\sensor\output...
    """
    for dir in os.listdir(rootdir):
        refID = rootdir + "\\" + dir
        for subdir in os.listdir(refID):
            inFolder = refID + "\\" + subdir
            outFeatures = refID + "\\points2"
            if subdir == "Sequoia":
                print(inFolder + " Processing")
                arcpy.GeoTaggedPhotosToPoints_management(inFolder, outFeatures)
                arcpy.Buffer_analysis(outFeatures + ".shp", outFeatures + "_buff2", bufferDist)
                arcpy.MinimumBoundingGeometry_management(outFeatures + "_buff2.shp", outFeatures + "_ENV2", "ENVELOPE", "ALL")


def main():
    rootdir = "C:\\Users\\nkolarik\\Desktop\\Kazava_Local\\temp"
    bufferDist = "31.8 meters"
    photo2env(rootdir, bufferDist)
if __name__ == '__main__':
    #main()




