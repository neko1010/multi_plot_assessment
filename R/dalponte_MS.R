## DALPONTE2016 IMPLEMENTATION FOR MULTISPECTRAL DATA

library(lidR)
library(gdalUtils)
library(rgdal)
library(raster)

library(stringr)

setwd("C:/Users/nkolarik/Desktop/thesis/data/CHM")
#setwd("C:/Users/nkolarik/Desktop/IDW_tst/CHM")

for(cover in list.files(".")){
  print(cover)
  for (site in list.files(cover)){
    print(site)
    ##CHMs
    ## use paste for string (filepath) manipulation
    chm_dir <- paste(".", cover, site, "warped", sep = "/"); 
    print(chm_dir)
    #print(list.files(chm_dir))
    for (item in list.files(chm_dir)){
      if ((endsWith(item, "tif")) && (!str_detect(item, "rgb"))){
        print(item)
        ## creating raster obj
        data <- raster(paste(chm_dir, item, sep = "/"))
        ## moving window for maxima detection also filter?- setting mavic window (kernel) roughly equal to sequoia (3 to 1)
        ## also setting max crown in pixels based upon largest crown diameter measured - Gianormous Baobad A2100 ~ 30m
        kernel <- matrix(1,3,3)
        max_cr <- 300
        

        ## removing NaN vals and smoothing with window
        chm <- raster::focal(data, w = kernel, fun = mean, na.rm = TRUE)
        
        ## function for variablw window filter
        f <- function(x) {0.8573816 + 0.4264624 * x + 0.05303072 * x**2 } ## from data crown_dia ~ height >> see testing in crown_height.r
        
        ttops <- tree_detection(chm,lmf(f, hmin = 1))##  Units are map units in v2.0
        plot(ttops)
        
        ##  This is good, and fast (a few seconds, but highly dependent on ttops):
        ## itcSegment (refactored) segmentation >>> region growing

        #itc_trees <- lastrees_dalponte(las = las, chm = chm, treetops = ttops, th_tree = 1, max_cr=50, extra=TRUE)
        itc_trees <- dalponte2016( chm = chm, treetops = ttops, th_tree = 1, max_cr=max_cr, th_seed = 0.2, th_cr = 0.2)()
  
        plot(itc_trees)        
        base <- unlist(strsplit(item, "_")[1])[1]
        print(base)
        ## write to .tif
        writeRaster(itc_trees, paste("../..", "output/ITC", cover, site, paste( base, "ITC", "trees.tif", sep = "_" ), sep = "/"), overwrite = T)
        
        ## For IDW_tst
        #writeRaster(itc_trees, paste("../output/ITC", cover, site, paste( base, "ITC", "trees.tif", sep = "_" ), sep = "/"), overwrite = T)
      }
    }
    
  }
}

