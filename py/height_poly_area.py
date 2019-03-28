import arcpy
import os

from arcpy.sa import *

def get_max_to_poly(tree_dir, chm_dir):
    """
    Utilizing the ZonalStatistics tool in ArcGIS to extract the height of delineated
    crowns. Heights are assigned in 10**-4 units to minimize possibility of
    erroneously merging crowns with the same height, as the input to this tool
    requires the raster have integer values. The first argument is the directory
    where crown rasters are stored and the second is the directory for CHM rasters.
    """
    arcpy.CheckOutExtension("Spatial")
    ## Looping through covers
    for cover in os.listdir(tree_dir):
        ## Looping through referebce IDs
        for refID in os.listdir(os.path.join(tree_dir, cover)):

            ## looping through items in directory of products
            for item in os.listdir(os.path.join(tree_dir, cover, refID)):
                if item.endswith(".tif"):
                    if "rgb" in item:
                        chm = os.path.join(chm_dir, cover, refID, "warped",
                            item.split("_")[0] + "_chm_sbst2.tif")
                    else:
                        chm = os.path.join(chm_dir, cover, refID, "warped",
                            item.split("_")[0] + "_CHM_wrp.tif")

                    ## needs to be an int raster for input
                    tree_ras = Int(os.path.join(tree_dir, cover, refID, item))
                    outras = ZonalStatistics(tree_ras, "VALUE", chm, "MAXIMUM")
                    ## convert heights to 10**-4 m preparing for potential integer mixups
                    outras10000 = outras * 10000
                    ## make a directory for polys
                    poly_dir = (os.path.join(tree_dir, cover, refID, "polys"))
                    try:
                        os.mkdir(poly_dir)
                    except:
                        pass
                    ##convert to poly
                    out_poly = os.path.join(poly_dir, os.path.splitext(item)[0][:-5] + "poly.shp")
                    ## define coordinate sstem
                    out_crs = arcpy.SpatialReference("WGS 1984 UTM Zone 35S")
                    ##converting to int vals from float for polygon conversion
                    int_raster = Int(outras10000)
                    arcpy.RasterToPolygon_conversion(int_raster, out_poly, "SIMPLIFY")
                    arcpy.DefineProjection_management(out_poly, out_crs)
                    print(" {} converted to polyons and projected!".format(item))



def calc_area(tree_dir, geom, units):
    """
    Adding a field to crown polygons that calculates 2D crown area.

    First arg is the directory where products are stored assuming a
    "Cover/Reference Id/product for each band" structure. The second arg
    is a string representing the geometry being calculated, and the third
    a string for desired units (see arcgis docs).
    """

    #arcpy.CheckOutExtension("Spatial")
    ## Looping through covers
    for cover in os.listdir(tree_dir):
        ## Looping through reference IDs
        for refID in os.listdir(os.path.join(tree_dir, cover)):
            poly_dir = (os.path.join(tree_dir, cover, refID, "polys"))

            ## looping through polygon shapefiles
            for item in os.listdir(poly_dir):
                if item.endswith(".shp"):
                    poly = os.path.join(poly_dir, item)
                    arcpy.AddGeometryAttributes_management(poly, Geometry_Properties = geom,
                        Area_Unit = units)

                    print(" {} now includes a new {} field".format(item, geom))


def main():
    tree_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\H2O"
    chm_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\data\\CHM"
    get_max_to_poly(tree_dir, chm_dir)
    calc_area(tree_dir, geom = "AREA", units = "SQUARE_METERS")

if __name__ == '__main__':
    main()
