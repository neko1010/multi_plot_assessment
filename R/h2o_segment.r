## IMPLEMENTATION OF WATERSHED SEGMENTATION

library(lidR)
library(gdalUtils)
library(rgdal)
library(raster)

library(stringr)

#setwd("C:/Users/nkolarik/Desktop/thesis/data/CHM")
setwd("C:/Users/nkolarik/Desktop/IDW_tst/CHM")


for (cover in list.files(".")){
  for (site in list.files(cover)){
    ##CHMs
    ## use paste for string (filepath) manipulation
    chm_dir <- paste(".", cover, site, "warped", sep = "/"); 
    print(chm_dir)
    #print(list.files(chm_dir))
    for (item in list.files(chm_dir)){
      if (endsWith(item, "tif")){
        ## creating raster obj
        data <- raster(paste(chm_dir, item, sep = "/"))
        ## moving window for maxima detection also filter?- setting mavic window roughly equal to sequoia (3 to 1)
        if (str_detect(item, "rgb")){
          kernel <- matrix(1,9,9)
        }else{
          kernel <- matrix(1,3,3)
        }
        ## removing NaN vals and smoothing with window 
        chm <- raster::focal(data, w = kernel, fun = mean, na.rm = TRUE)
        #print(summary(chm))
        ## watershed segmentation- smallest 'trees' detected are 1m (th_tree arg)
        #h2o_trees <- lastrees_watershed(chm = chm, th_tree = 1) ## v 1.6.1
        h2o_trees <- watershed(chm = chm, th = 1)() ## v 2.0
        plot(h2o_trees)
        

        ## extracting base for file name from chm
        base <- unlist(strsplit(item, "_")[1])[1]
        ## write to .tif
        writeRaster(h2o_trees, paste("../..", "output/H2O", cover, site, paste( base, "H2O", "trees.tif", sep = "_" ), sep = "/"))
        
        ## for IDW_tst
        #writeRaster(h2o_trees, paste("..", "output/H2O", cover, site, paste( base, "H2O", "trees.tif", sep = "_" ), sep = "/"), overwrite = TRUE)
  
        
      }
    }

  }
}
