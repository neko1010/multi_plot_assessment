import arcpy
import os
import numpy as np

def get_point_lyrs(points):
    """
    A tool that utilizes arcpy tools to make layers from point shapefiles
    representing visually validated points for each vegetation cover of
    interest: Tree, Shrub, Other. Input argument is the directory where point
    shapefiles are stored.Layers are returned in lists for later use
    in SQL queries.
    """

    pt_lyrs = []
    for point in os.listdir(points):
        if point.endswith(".shp"):
            tree = arcpy.MakeFeatureLayer_management(os.path.join(points, point),
                 "tree_pts", where_clause = "Cover = 'tree'")
            pt_lyrs.append(tree)
            shrub = arcpy.MakeFeatureLayer_management(os.path.join(points, point),
                 "shrub_pts", where_clause = "Cover = 'shrub'" )
            pt_lyrs.append(shrub)
            other = arcpy.MakeFeatureLayer_management(os.path.join(points, point),
                 "other_pts", where_clause = "Cover = 'other'" )
            pt_lyrs.append(other)
    return pt_lyrs


def get_cover_lyrs(polys, band):
    """
    A tool that utilizes arcpy tools to make layers from polygon shapefiles
    representing estimates for each vegetation cover of
    interest: Tree and Shrub. The 'Other' class is assumed as not belonging
    to either tree or shrub. First argument is the directory where polygon
    estimates are stored and second is the band of data to use for analysis
    entered as a string. Layers are returned in lists for later use in
    SQL queries. Currently only uses the 'rgb' point cloud as baseline.
    """

    covers = []
    for poly in os.listdir(polys):
        ## can change band here ex. 'rgb', 'gre', 'red', 'reg', 'nir'
        if poly.endswith(".shp") and band in poly:
            if "ITC" in polys or "H2O" in polys:
                tree_est = arcpy.MakeFeatureLayer_management(os.path.join(polys, poly),
                    "tree_lyr", where_clause = "GRIDCODE > 30000")
                covers.append(tree_est)
                shrub_est = arcpy.MakeFeatureLayer_management(os.path.join(polys, poly),
                     "shrub_lyr", where_clause = "GRIDCODE < 30000 AND GRIDCODE > 10000" )
                covers.append(shrub_est)

            ## exception for height threshold maps
            else:
                tree_est = arcpy.MakeFeatureLayer_management(os.path.join(polys, poly),
                    "tree_lyr", where_clause = "GRIDCODE = 2")
                covers.append(tree_est)
                shrub_est = arcpy.MakeFeatureLayer_management(os.path.join(polys, poly),
                     "shrub_lyr", where_clause = "GRIDCODE = 1" )
                covers.append(shrub_est)
    return covers



def confusion_mat(pt_lyrs, cvr_lyrs, conf_mat):
    """
    Using the returned point layer list, cover layer list, and an empty matrix
    object as input arguments, this tool returns a populated confusion matrix
    to be used for disagreement analysis.
    """

    ## empty matrix values
    a1 = 0
    a2 = 0
    a3 = 0
    b1 = 0
    b2 = 0
    b3 = 0
    c1 = 0
    c2 = 0
    c3 = 0

    ## converting 'result' objects to count integers
    tree_res = arcpy.GetCount_management(pt_lyrs[0])
    tree_ct = int(tree_res.getOutput(0))
    shrub_res = arcpy.GetCount_management(pt_lyrs[1])
    shrub_ct = int(shrub_res.getOutput(0))
    other_res = arcpy.GetCount_management(pt_lyrs[2])
    other_ct = int(other_res.getOutput(0))

    print("{} tree, {} shrub, and {} grass".format(tree_ct, shrub_ct, other_ct))

    ## Selecting (tree) points based on spatial relationship to estimate layers
    tree_tree =arcpy.SelectLayerByLocation_management(pt_lyrs[0], "WITHIN", cvr_lyrs[0])
    ## counting selected points
    a1_res = arcpy.GetCount_management(tree_tree)
    a1_loc = int(a1_res.getOutput(0))

    ## tree observations estimated as shrub
    tree_shrub =arcpy.SelectLayerByLocation_management(pt_lyrs[0], "WITHIN", cvr_lyrs[1])
    a2_res = arcpy.GetCount_management(tree_shrub)
    a2_loc = int(a2_res.getOutput(0))

    ##tree observations estimated as other
    a3_loc = tree_ct - (a1_loc + a2_loc)

    ##shrubs
    ## shrub observations estimated as tree
    shrub_tree = arcpy.SelectLayerByLocation_management(pt_lyrs[1], "WITHIN", cvr_lyrs[0])
    b1_res = arcpy.GetCount_management(shrub_tree)
    b1_loc = int(b1_res.getOutput(0))

    ## shrub-shrub
    shrub_shrub = arcpy.SelectLayerByLocation_management(pt_lyrs[1], "WITHIN", cvr_lyrs[1])
    b2_res = arcpy.GetCount_management(shrub_shrub)
    b2_loc = int(b2_res.getOutput(0))

    ## shrub observations estimated as other
    b3_loc = shrub_ct - (b1_loc + b2_loc)

    ##non-woody
    other_tree = arcpy.SelectLayerByLocation_management(pt_lyrs[2], "WITHIN", cvr_lyrs[0])
    c1_res = arcpy.GetCount_management(other_tree)
    c1_loc = int(c1_res.getOutput(0))

    other_shrub = arcpy.SelectLayerByLocation_management(pt_lyrs[2], "WITHIN", cvr_lyrs[1])
    c2_res = arcpy.GetCount_management(other_shrub)
    c2_loc = int(c2_res.getOutput(0))

    ## other-other
    c3_loc = other_ct - (c1_loc + c2_loc)

    a1 += a1_loc
    a2 += a2_loc
    a3 += a3_loc
    b1 += b1_loc
    b2 += b2_loc
    b3 += b3_loc
    c1 += c1_loc
    c2 += c2_loc
    c3 += c3_loc


    conf_mat = np.asmatrix([[a1, a2, a3],
                           [b1, b2, b3],
                           [c1, c2, c3]])

    return(conf_mat)

def main():
    ## could refactor here to run this from command line?

    arcpy.env.overwriteOutput = True
    #rdm_pt_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\data\\random_pts"
    #alg_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\thresh"
    #alg_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\H2O"
    #alg_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\ITC"
    
    rdm_pt_dir = "E:\\thesis\\data\\random_pts"
    #alg_dir = "E:\\thesis\\output\\thresh"
    #alg_dir = "E:\\thesis\\output\\H2O"
    alg_dir = "E:\\thesis\\output\\ITC"


    mat = np.asarray([[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]])

## all covers
##    for cover in os.listdir(alg_dir):
##        ## Looping through referebce IDs
##        for refID in os.listdir(os.path.join(alg_dir, cover)):
##            points = os.path.join(os.path.join(rdm_pt_dir, cover, refID))
##            pt_lyrs = get_point_lyrs(points)
##            ## looping through items in directory of products
##            polys = os.path.join(alg_dir, cover, refID, "polys")
##            cvr_lyrs = get_cover_lyrs(polys)
##
##            mat += confusion_mat(pt_lyrs, cvr_lyrs, mat)
##            print(mat)
    ##INSERT COVER TYPE AS STRING FOR DESIRED COVER
    covers = ["grass", "shrub", "tree"]
    bands = ['rgb', 'gre', 'red', 'reg', 'nir']
    csv_dest = "C:\\Users\\nkolarik\\Desktop\\thesis\\docs\\qa_bands"
    for band in bands:
        for cover in covers:
        ## Looping through referebce IDs
            mat = np.asarray([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]])

            for refID in os.listdir(os.path.join(alg_dir, cover)):
                points = os.path.join(os.path.join(rdm_pt_dir, cover, refID))
                pt_lyrs = get_point_lyrs(points)
                ## looping through items in directory of products
                polys = os.path.join(alg_dir, cover, refID, "polys")
                cvr_lyrs = get_cover_lyrs(polys, band)
                ## matrix aggregating sites for covers
                #mat += confusion_mat(pt_lyrs, cvr_lyrs, mat)
                ## matrices for each band and each site!
                mat = confusion_mat(pt_lyrs, cvr_lyrs, mat)
                ## saving to csv
                #np.savetxt(os.path.join(csv_dest, "{}_{}.csv".format(band, cover)), mat, delimiter = ',')
                alg = alg_dir.split("\\")[-1]
                #np.savetxt(os.path.join(csv_dest, "{}_{}_{}_{}.csv".format(alg, refID, band, cover)), mat, delimiter = ',')
                np.savetxt(os.path.join(csv_dest, "{}_{}_{}_{}_update.csv".format(alg, refID, band, cover)), mat, delimiter = ',')

if __name__ == '__main__':
    main()
