#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      nkolarik
#
# Created:     12/10/2018
# Copyright:   (c) nkolarik 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import arcpy
from arcpy import env
from arcpy.sa import *

import os
import arcpy

def create_chm(rootdir):
    """
    Resamples the DTM to the resolution of the DSM and then subtracts the
    resampled DTM from the DSM to create a Canopy Height Model (CHM)

    Assumes directory structure of rootdir\refID\sensor\output...
    """
    arcpy.CheckOutExtension("3d")
    ## Needed ffor the Minus_3d tool
    refIDs = os.listdir(rootdir)
    for refID in refIDs:
        if "Products" in refIDs:
            refIDs.remove("Products")
        if "ENV" in refIDs:
            refIDs.remove("ENV")
        #sensors =  ["Mavic", "Sequoia"]
        sensors = ["Sequoia"]
        for sensor in sensors:
            if sensor == "Mavic":
                bands = ["Output"]
            if sensor == "Sequoia":
                bands = ['gre', 'red', 'reg', 'nir']
            for band in bands:
                for root, dirs, files in os.walk(os.path.join(rootdir, refID, sensor, band)):
                    for dir in dirs:
                        ##excludes directories containing only tiles
                        if "tiles" in dirs:
                            dirs.remove("tiles")
                    for f in files:
                        if f.endswith("dsm.tif"):
                            DSM = os.path.join(root,f)
                        if f.endswith("dtm.tif"):
                            DTM = os.path.join(root,f)
                            CellSize = arcpy.GetRasterProperties_management(DSM, property_type = "CELLSIZEX")
                            ## Defining cell size to resample the DTM to that of the DSM- known
                            ##bug for doing so in the Resample_management tool.
                            ##BUG!!! https://community.esri.com/thread/162982
                            DTMrsmpl = os.path.join(rootdir, refID,  sensor, band, "DTMrsmpl.tif")
                            arcpy.Resample_management(DTM, DTMrsmpl, CellSize )
                            ## Subtract DTM (resampled) from DSM to create CHM
                            if sensor == "Mavic":
                                arcpy.Minus_3d(DSM, DTMrsmpl, os.path.join(rootdir, refID, sensor, band, "{}_{}_CHM.tif".format(refID, sensor)))
                                print (refID,  sensor, " CHM Created")
                            if sensor == "Sequoia":
                                ## have to use the old formatting style (Python 2.7)
                                arcpy.Minus_3d(DSM, DTMrsmpl, os.path.join(rootdir, refID, sensor, band, "%s_%s_CHM.tif"%(refID, band))) #"{}_{}_CHM.tif".format(refID, sensor)))
                                print (refID,  band, " CHM Created")


def raster_mask(rootdir):
    """
    Subsetting SfM/MVS products to isolate "non-distorted" portion
    of imagery.

    Assumes directory structure of rootdir\refID\sensor\output...
    """

    arcpy.CheckOutExtension("Spatial")
    refIDs = os.listdir(rootdir)
    #print refID
    for refID in refIDs:
        if "Products" in refIDs:
            refIDs.remove("Products")
        if "ENV" in refIDs:
            refIDs.remove("ENV")

        mask = os.path.join(rootdir, refID, "points2_ENV2.shp")
        #sensors =  ["Mavic", "Sequoia"]
        sensors = ["Sequoia"]

        for sensor in sensors:
            if sensor == "Mavic":
                bands = ["Output"]
            if sensor =="Sequoia":
                bands = ['gre', 'red', 'reg', 'nir']
            for band in bands:
                for f in os.listdir(os.path.join(rootdir, refID, sensor, band)):
                    if f.endswith("CHM.tif"):
                        #print file
                        outExtractByMask = ExtractByMask(os.path.join(rootdir, refID, sensor, band, f), mask)
                        time.sleep(2)
                        outExtractByMask.save(os.path.splitext(os.path.join(rootdir, refID, sensor, band, f))[0] + "_sbst2.tif" )
                        time.sleep(2)
                        outExtractByMask = None
                        ##clears background workspace?
                        print (refID + " FINISHED")


def main():
    #rootdir = "A:/drone_data/Drone_data_Africa2017_processed/tmp"
    #create_chm(rootdir)
    raster_mask(rootdir)

if __name__ == '__main__':
    main()
