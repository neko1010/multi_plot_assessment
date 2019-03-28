import os
import arcpy
import csv

def in_situ_analysis(insitu, product):
    """
    Establishes the polygon estimate for each in situ measurement using union,
    selection queries, and join arcpy tools. The result is written to a csv,
    but beware! This csv must be further analyzed to remove instances
    where an in situ measurement was not recorded (not within 5m of transect point).
    The first argument is the directory where in situ measurements are stored and
    the second is where the output products to be matched are stored.
    """

    for cover in ["tree", "shrub", "grass"]:
        for refID in os.listdir(os.path.join(product, cover)):
            ## SPECIFICALLY CHANGING FOR K101
            if refID == "K101":
                poly_dir = os.path.join(product, cover, refID, "polys")
                crowns = os.path.join(insitu, cover, refID, "{}_crowns_UTM35S.shp".format(refID))
                stems = os.path.join(insitu, cover, refID, "{}_stems_UTM35S.shp".format(refID))
                anlys_dir = os.path.join(poly_dir, "analysis")
                try:
                    os.mkdir(anlys_dir)
                except:
                    continue
                sbsts = os.path.join(anlys_dir, "sbsts")
                try:
                    os.mkdir(sbsts)
                except:
                    continue
                for f in os.listdir(poly_dir):
                    if f.endswith(".shp"):
                        ## Union
                        union = os.path.join(anlys_dir, "{}_union.shp".format(f.split("_")[0]))
                        arcpy.Union_analysis([crowns, os.path.join(poly_dir, f)], union)
                        print("{} created!".format(union))
                        ## layer for selection
                        lyr = arcpy.MakeFeatureLayer_management(union)
                        ##selection FOR K101 ONLY DUE TO SHORTER REFID! IMPORTANCE OF NAMING CONVENTION!!!!
                        where_clause = "FID_{}_c >= 0 AND FID_{} >=0".format(refID, f.split("_")[0][:6])
                        selection = arcpy.SelectLayerByAttribute_management(lyr, where_clause = where_clause)
                        ##save subsetted layer
                        sbst = os.path.join(sbsts, "{}_union_sbst.shp".format(f.split("_")[0]))
                        arcpy.CopyFeatures_management(selection, sbst)
                        print("Selection of {} saved as {}!".format(union, sbst))
                        ##join
                        join = os.path.join(sbsts, "{}_join.shp".format(f.split("_")[0]))
                        arcpy.SpatialJoin_analysis(stems, sbst, join, join_operation =  "JOIN_ONE_TO_MANY",
                              match_option = "CLOSEST" )
                        print("{} joined to {} and saved as {} ".format(sbst, stems, join))
                        ## write to csv
                        arcpy.CopyRows_management(join, os.path.join(sbsts, "{}_join.csv").format(f.split("_")[0]))


            else:
                poly_dir = os.path.join(product, cover, refID, "polys")
                crowns = os.path.join(insitu, cover, refID, "{}_crowns_UTM35S.shp".format(refID))
                stems = os.path.join(insitu, cover, refID, "{}_stems_UTM35S.shp".format(refID))
                anlys_dir = os.path.join(poly_dir, "analysis")
                try:
                    os.mkdir(anlys_dir)
                except:
                    continue
                sbsts = os.path.join(anlys_dir, "sbsts")
                try:
                    os.mkdir(sbsts)
                except:
                    continue
                for f in os.listdir(poly_dir):
                    if f.endswith(".shp"):
                        ## Union
                        union = os.path.join(anlys_dir, "{}_union.shp".format(f.split("_")[0]))
                        arcpy.Union_analysis([crowns, os.path.join(poly_dir, f)], union)
                        print("{} created!".format(union))
                        ## layer for selection
                        lyr = arcpy.MakeFeatureLayer_management(union)
                        ##selection
                        where_clause = "FID_{}_ >= 0 AND FID_{} >=0".format(refID, f.split("_")[0][:6])
                        selection = arcpy.SelectLayerByAttribute_management(lyr, where_clause = where_clause)
                        ##save subsetted layer
                        sbst = os.path.join(sbsts, "{}_union_sbst.shp".format(f.split("_")[0]))
                        arcpy.CopyFeatures_management(selection, sbst)
                        print("Selection of {} saved as {}!".format(union, sbst))
                        ##join
                        join = os.path.join(sbsts, "{}_join.shp".format(f.split("_")[0]))
                        arcpy.SpatialJoin_analysis(stems, sbst, join, join_operation =  "JOIN_ONE_TO_MANY",
                              match_option = "CLOSEST" )
                        print("{} joined to {} and saved as {} ".format(sbst, stems, join))
                        ## write to csv
                        arcpy.CopyRows_management(join, os.path.join(sbsts, "{}_join.csv").format(f.split("_")[0]))


def reduce_insitu_csv(insitu_file):
    """
    Reduces the analyzed crown output to only estimates that correlate
    with in situ measurements to be plotted- based on stem/crown FID matches.
    Only required argument is the file to be reduced, returns the header and
    subset of rows to be written by subsequent function.
    """

    with open(insitu_file) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        header = header[4:14] + header[37:41]
        ## subsetting based on matching stem and crown IDs
        rowstowrite = [row[4:14] + row[37:41] for row in reader if row[4] == row[20]]
        return header, rowstowrite

def write_sbst_csv(header, rowstowrite, dest):
    """
    Writes the output of reduce_insitu_csv() to a new file to be compiled.
    Args are the header, rows of data, and the destination filename.
    """

    with open(dest, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rowstowrite:
            writer.writerow(row)




def main():
    #insitu = "C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018"
    #product = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\ITC"
    #product = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\H2O"
    #in_situ_analysis(insitu, product)

    for cover in ["tree", "shrub", "grass"]:
        for refID in os.listdir(os.path.join(product, cover)):
            anlys_sbst = os.path.join(product, cover, refID, "polys", "analysis", "sbsts")
            for f in os.listdir(anlys_sbst):
                if f.endswith(".csv"):
                    #print(f)
                    insitu_file = os.path.join(anlys_sbst, f)
                    ## didn't take the time to make this dynamic. change accordingly
                    dest = os.path.join(insitu, cover, refID, f.split("_")[0] +"_H2O_insitu_sbst.csv")
                    #dest = os.path.join(insitu, cover, refID, f.split("_")[0] +"_ITC_insitu_sbst.csv")
                    header, rowstowrite = reduce_insitu_csv(insitu_file)
                    write_sbst_csv(header, rowstowrite, dest)
                    print("{} in situ analysis results saved here: {}".format(refID, dest))
    #pass

if __name__ == '__main__':
    main()
