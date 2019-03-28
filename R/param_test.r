## TESTING PARAMETERS OF THE DALPONTE2016 ALG ITERATIVELY 

library(lidR)
library(gdalUtils)
library(rgdal)
library(raster)

library(stringr)

setwd("C:/Users/nkolarik/Desktop/thesis/data/CHM")

#data <- raster(paste(chm_dir, item, sep = "/"))
data <- raster("./tree/A2100/A2100rgb_chm_sbst2.tif")


## moving window for maxima detection also filter?- setting mavic window (kernel) roughly equal to sequoia (3 to 1)
## also setting max crown in pixels based upon largest crown diameter measured - Gianormous Baobab A2100 ~ 30m
#if (str_detect(item, "rgb")){
#  kernel <- matrix(1,9,9)
#  max_cr <- 900
#  
#}else{
#  kernel <- matrix(1,3,3)
#  max_cr <- 300
#}

kernel <- matrix(1,9,9)
max_cr <- 900

## removing NaN vals and smoothing with window
chm <- raster::focal(data, w = kernel, fun = mean, na.rm = TRUE)

## create an extent class object
extent_obj <- extent(chm)
## determining x and y distances
x <- extent_obj@xmax - extent_obj@xmin; x
y <- extent_obj@ymax - extent_obj@ymin; y

## vectors for 3x3 subsets
#a1 <- c(extent_obj@xmin, extent_obj@xmin + x/3, extent_obj@ymin, extent_obj@ymin + y/3); a1
#a2 <- c(extent_obj@xmin, extent_obj@xmin + x/3, extent_obj@ymin + y/3, extent_obj@ymax - y/3); a2
#a3 <- c(extent_obj@xmin, extent_obj@xmin + x/3, extent_obj@ymax - y/3, extent_obj@ymax); a3
#
#b1 <- c(extent_obj@xmin + x/3, extent_obj@xmax - x/3, extent_obj@ymin, extent_obj@ymin + y/3); b1
#b2 <- c(extent_obj@xmin + x/3, extent_obj@xmax - x/3, extent_obj@ymin + y/3, extent_obj@ymax - y/3); b2
#b3 <- c(extent_obj@xmin + x/3, extent_obj@xmax - x/3, extent_obj@ymax - y/3, extent_obj@ymax); b3

c1 <- c(extent_obj@xmax - x/3, extent_obj@xmax, extent_obj@ymin, extent_obj@ymin + y/3); c1
#c2 <- c(extent_obj@xmax - x/3, extent_obj@xmax, extent_obj@ymin + y/3, extent_obj@ymax - y/3); c2
#c3 <- c(extent_obj@xmax - x/3, extent_obj@xmax, extent_obj@ymax - y/3, extent_obj@ymax); c3
#
## reassigning subsets to cropped rasters
#a1 <- crop(chm, a1); a1
#a2 <- crop(chm, a2)
#a3 <- crop(chm, a3)#

#b1 <- crop(chm, b1); b1
#b2 <- crop(chm, b2)
#b3 <- crop(chm, b3)#

c1 <- crop(chm, c1); c1
#c2 <- crop(chm, c2)
#c3 <- crop(chm, c3)

#ttops <- tree_detection(chm, ws=9, hmin=3) ##  Units are pixels for ws IF RASTER, m otherwise; m for hmin on raster
#ttops <- tree_detection(chm, ws=5, hmin=1) ##  Units are m for point cloud
#ttops <- tree_detection(chm,lmf(ws = 2, hmin = 1))#, ws=9, hmin=1) ##  Units are map units in v2.0

#ttops <- tree_detection(a1, lmf(ws = 2, hmin = 1))
#plot(ttops)

##variable window filter
#f <- function(x) {x * 0.07 + 3}
#f <- function(x) {x * 0.2 + 2}
#f <- function(x) {0.00895 * x^2 + 3.09632} ## Popescu and Wynne 2004
f <- function(x) {0.8573816 + 0.4264624 * x + 0.05303072 * x**2 } ## from data crown_dia ~ height >> see testing in crown_height.r

##  This is good, and fast (a few seconds, but highly dependent on ttops):
## itcSegment (refactored) segmentation >>> region growing

## range of params to test
seed_th<- seq(0.2, 0.8, 0.2)
cr_th <- seq(0.2, 0.8, 0.2)

## treetops
ttops <- tree_detection(c1, lmf(f, hmin = 1))

for (seed in seed_th){
  for (cr in cr_th){
    woodys <- dalponte2016( chm = c1, treetops = ttops, th_seed = seed, th_cr = cr, th_tree = 1, max_cr=900)()
    writeRaster(woodys, paste("../tst/param_test2", paste(seed, "_", cr, ".tif", sep = ""), sep = "/"))
  }
}

