#-------------------------------------------------------------------------------
# Name:        module1
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

def create_chm(rootdir):
    """
    Resamples the DTM to the resolution of the DSM and then subtracts the
    resampled DTM from the DSM to create a Canopy Height Model (CHM)

    Assumes directory structure of rootdir\refID\sensor\output...
    """
    arcpy.CheckOutExtension("3d")
    ## Needed ffor the Minus_3d tool
    refIDs = []
    for subdir in os.listdir (rootdir):
        refIDs.append(rootdir + "\\" + subdir)
    for refID in refIDs:
        sensors =  ["\\Mavic", "\\Sequoia"]
        for sensor in sensors:
            layers = ""
            for root, dirs, files in os.walk(refID + sensor + "\\Output"):
                for dir in dirs:
                    ##excludes directories containing only tiles
                    if "tiles" in dirs:
                        dirs.remove("tiles")
                for file in files:
                    if file.endswith("dsm.tif"):
                        DSM = os.path.join(root,file)
                    if file.endswith("dtm.tif"):
                        DTM = os.path.join(root,file)
                        CellSize = arcpy.GetRasterProperties_management(DSM, property_type = "CELLSIZEX")
                        ## Defining cell size to resample the DTM to that of the DSM- known
                        ##bug for doing so in the Resample_management tool.
                        ##BUG!!! https://community.esri.com/thread/162982
                        DTMrsmpl = refID + sensor + "\\Output" + "\\DTMrsmpl.tif"
                        arcpy.Resample_management(DTM, DTMrsmpl, CellSize )
                        ## Subtract DTM (resampled) from DSM to create CHM
                        arcpy.Minus_3d(DSM, DTMrsmpl, refID + sensor + "\\Output" + sensor +"CHM.tif")
                        print (refID + sensor + " CHM Created")


def stack(rootdir):
    """
    Grabs desired layers to stack, creates a .txt file to document which layers
    are represented by correspoinding band list.

    Assumes directory structure of rootdir\refID\sensor\output...
    """
    refIDs = []
    for subdir in os.listdir (rootdir):
        refIDs.append(rootdir + "\\" + subdir)
    for refID in refIDs:
        sensors =  ["\\Mavic", "\\Sequoia"]
        for sensor in sensors:
            ## Creating an open string to serve as the string of files to use
            ## for the first argument in the CompositeBands_management tool
            layers = ""
            ## Creating a .txt file that lists bands for reference
            with open(refID + sensor + "\\Output" + sensor + "_lyrs.txt", "w+") as lyrfile:
                for root, dirs, files in os.walk(refID + sensor + "\\Output"):
                    for dir in dirs:
                        ## Directory exclusion
                        if "tiles"in dirs:
                            dirs.remove("tiles")
                        if "reflectance" in dirs:
                            dirs.remove("reflectance")
                        if "dtm" in dirs:
                            dirs.remove("dtm")
                        if sensor == "\\Sequoia" and "2_mosaic" in dirs:
                            dirs.remove("2_mosaic")
                    for file in files:
                        ## 'and not file.endswith("view.tif")' added 20180504 due to a dsm_preview.tif in new p4d version
                        if file.endswith(".tif") and not file.endswith("view.tif"):
                            ## Writing band to the file containing list of layers
                            lyrfile.write(file + "\n")
                            ## Writing band to the string of layers
                            layers += (os.path.join(root, file + "; "))
            #lyrfile.close()
            arcpy.CompositeBands_management(str(layers), str(refID + sensor + "\\Output\\Stack.tif"))
            print (refID + sensor + " Stacked")
def main():
    rootdir = "C:\\Users\\nkolarik\\Desktop\\Kazava_Local"
    create_chm(rootdir)
    stack(rootdir)
if __name__ == '__main__':
    #main()
