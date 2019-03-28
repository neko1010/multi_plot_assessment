import arcpy
import os
import shutil

from arcpy.sa import *

def raster_to_poly(tree_dir):
    """
    Coverting output rasters to polys and defining projection.

    First param is the directory where products are stored assuming a
    "Cover/Reference Id/product for each band" structure.
    """

    arcpy.CheckOutExtension("Spatial")
    ## Looping through covers
    for cover in os.listdir(tree_dir):
        ## Looping through referebce IDs
        for refID in os.listdir(os.path.join(tree_dir, cover)):
            poly_dir = (os.path.join(tree_dir, cover, refID, "polys"))
            ## making directory for polygons
            try:
                os.mkdir(poly_dir)
            except:
                pass

            ## looping through items in directory of products
            for item in os.listdir(os.path.join(tree_dir, cover, refID)):
                if item.endswith(".tif"):
                    raster = os.path.join(tree_dir, cover, refID, item)
                    out_poly = os.path.join( poly_dir, os.path.splitext(item)[0][:-5] + "poly.shp")
                    out_crs = arcpy.SpatialReference("WGS 1984 UTM Zone 35S")
                    ##converting to int vals from float for polygon conversion
                    int_raster = Int(raster)
                    arcpy.RasterToPolygon_conversion(int_raster, out_poly, "SIMPLIFY")
                    arcpy.DefineProjection_management(out_poly, out_crs)

                    print(" {} converted to polyons and projected!".format(raster))
def main():

    #tree_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\ITC"
    raster_to_poly(tree_dir)

if __name__ == '__main__':
    main()
