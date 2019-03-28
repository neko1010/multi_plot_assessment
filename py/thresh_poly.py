import os
import arcpy

from arcpy.sa import *


## CONVERTING HEIGHT THRESHOLD RASTER TO POLYS

arcpy.CheckOutExtension("Spatial")

#tree_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\thresh"

for cover in os.listdir(tree_dir):
    ## Looping through referebce IDs
    for refID in os.listdir(os.path.join(tree_dir, cover)):
        poly_dir = (os.path.join(tree_dir, cover, refID, "polys"))
        try:
            os.mkdir(os.path.join(tree_dir, cover,refID, "polys"))
        except:
            pass
        ## looping through items in directory of products
        for item in os.listdir(os.path.join(tree_dir, cover, refID)):
            if item.endswith(".tif"):
                ## needs to be an int raster for input :-P
                tree_ras = Int(os.path.join(tree_dir, cover, refID, item))
                ##convert to poly
                out_poly = os.path.join(poly_dir, os.path.splitext(item)[0][:-5] + "poly.shp")
                ## define coordinate sstem
                out_crs = arcpy.SpatialReference("WGS 1984 UTM Zone 35S")
                ##converting to int vals from float for polygon conversion
                arcpy.RasterToPolygon_conversion(tree_ras, out_poly, "SIMPLIFY")
                arcpy.DefineProjection_management(out_poly, out_crs)
                print(" {} converted to polyons and projected!".format(item))
def main():
    pass

if __name__ == '__main__':
    main()
