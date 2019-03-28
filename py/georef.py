import arcpy
import os
import shutil

def georef(chm_dir, link_dir):
        """
        Georeferencing CHM output from each band of the Parrot Sequoia
        to the Mavic rgb data.

        First param is the directory where CHM are stored assuming a
        "Cover/Reference Id/CHM for each band" structure. Second is where the
        .txt files; products of georeferencing (in GUI) a Sequoia orthophoto to the
        Mavic ortho in ArcGIS.
        """
        ## Looping through covers
        for cover in os.listdir(chm_dir):
            ## Looping through referebce IDs
            for refID in os.listdir(os.path.join(chm_dir, cover)):
                warp_dir = (os.path.join(chm_dir, cover, refID, "warped"))
                try:
                    os.mkdir(warp_dir)
                except:
                    pass
                for item in os.listdir(os.path.join(chm_dir, cover, refID)):
                    infile = os.path.join(chm_dir, cover, refID, item)
                    outfile = os.path.join(warp_dir, os.path.splitext(item)[0][:-5] + "wrp.tif")
                    link_file = os.path.join(link_dir, cover, refID + ".txt")

                    if "rgb" in item:
                        shutil.copy(infile, warp_dir)
                        print(item)
                    ## Georectification
                    elif item.endswith(".tif"):
                        arcpy.WarpFromFile_management(infile, outfile, link_file, "POLYORDER1")
                        print(infile, outfile, link_file)

def main():
    chm_dir = "C:\\Users\\nkolarik\\Desktop\\IDW_tst\\CHM"
    #chm_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\data\\CHM"
    link_dir = "C:\\Users\\nkolarik\\Desktop\\thesis\\output\\transformations"
    georef(chm_dir, link_dir)
if __name__ == '__main__':
    main()
