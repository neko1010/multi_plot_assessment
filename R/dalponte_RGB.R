## DALPONTE2016 IMPLEMENTATION FOR RGB DATA; PROCESSES INPUT CHM AS MOSAICS TO INCREASE PROCESSING TIME

library(lidR)
library(gdalUtils)
library(rgdal)
library(raster)

library(stringr)

setwd("C:/Users/nkolarik/Desktop/thesis/data/CHM")

#setwd("C:/Users/nkolarik/Desktop/IDW_tst/CHM")

kernel <- matrix(1,9,9)
max_cr <- 900

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
      if ((endsWith(item, "tif")) && (str_detect(item, "rgb"))){ 

        d <- raster(paste(chm_dir, item, sep = "/"))
        ## removing NaN vals and smoothing with window
        chm <- raster::focal(d, w = kernel, fun = mean, na.rm = TRUE)
        
        ## create an extent class object
        extent_obj <- extent(chm)
        
        
        ## FROM FRS
        ##  Imagine pulling these from your extent_obj@xmin/xmax, etc.
        x_min <- extent_obj@xmin
        x_max <- extent_obj@xmax
        y_min <- extent_obj@ymin  
        y_max <- extent_obj@ymax
        
        ##  Must be square:
        #N_tiles <- 9
        N_tiles <- 16
        
        ##  Dynamic code below to calculate boundaries for N tiles
        ##    arranged in a square:
        x_range <- x_max - x_min
        y_range <- y_max - y_min
        
        tile_width <- floor(x_range / sqrt(N_tiles))
        half_tile_width <- floor(tile_width / 2)
        
        
        coord_list <- data.frame("x1"=numeric(),"x2"=numeric(), "y1"=numeric(), "y2"=numeric())
        for (i in seq(0, sqrt(N_tiles)-1)) {
          for (j in seq(0, sqrt(N_tiles)-1)) {
            tile_center_x <- x_min + i * tile_width + half_tile_width
            tile_center_y <- y_min + j * tile_width + half_tile_width
            
            ##  Add and subtract a whole tile width to ensure 100% overlap:
            x1 <- tile_center_x - tile_width
            x2 <- tile_center_x + tile_width
            y1 <- tile_center_y - tile_width
            y2 <- tile_center_y + tile_width
            
            ##  Check for sanity in case of rounding errors or for the edge tiles:
            if (x1 < x_min) x1 <- x_min
            if (y1 < y_min) y1 <- y_min
            if (x2 > x_max || (x_max - x2) < half_tile_width) x2 <- x_max
            if (y2 > y_max || (y_max - y2) < half_tile_width) y2 <- y_max
            
            ##  From tile center location set x1 to tile center minus 1/2 a tile:
            coord_list[i*sqrt(N_tiles) + j + 1, ] <- c(x1, x2, y1, y2)
          }
        }
        
        ## dir for tiles
        tiles_dir <- paste("../..", "output/ITC", cover, site,"tiles/",sep = "/")
        dir.create(tiles_dir)
        
        ## vwf function
        f <- function(x) { 0.8573816 + 0.4264624 * x + 0.05303072 * x**2 } ## from data crown_dia ~ height >> see testing in crown_height.r
        
        
        for(i in 1:nrow(coord_list)) {
          #row <- coord_list[i,]
          row <- as.numeric(as.vector(coord_list[i,]))
          #print(extent(row))
          tile <- crop(chm, row)
          ttops <- tree_detection(tile, lmf(f, hmin = 1))
        
          #writeOGR(ttops, "./tst/tiles", paste(i, "_ttops", sep = ""), driver = "ESRI Shapefile")
          woodys <- dalponte2016( chm = tile, treetops = ttops, th_tree = 1, th_seed = 0.2, th_cr = 0.2, max_cr=max_cr)()
          writeRaster(woodys, paste(tiles_dir, paste0(i, "_crowns.tif"), sep = "/"), overwrite = T)

        }
          
        
        ##  Choose buffer zone in m to identify edge polygons:
        buffer_dist <- 5
        
        ##  Calculate buffer dist in pixels:
        buffer_pix <- round(buffer_dist/xres(d))
        
          
        for (i in 1:N_tiles) {
        	d <- raster(paste0(tiles_dir, i,"_crowns.tif"))
        	
        	##  Extract buffer region pixel values:
        	r1 <- d[1:buffer_pix,]
        	r2 <- d[(dim(d)[1]-buffer_pix):dim(d)[1],]
        	r2 <- d[(dim(d)[1]-buffer_pix):dim(d)[1],]
        	c1 <- d[,1:buffer_pix]
        	c2 <- d[,(dim(d)[2]-buffer_pix):dim(d)[2]]
        	
        	##  Extract unique IDs from all buffer pixels:
        	ids <- unique(c(r1,r2,c1,c2))
        	
        	##  Duplicate raster:  
        	d2 <- d
        	
        	##  Loop over crown IDs in buffer and remove them:
        	for (id in ids) { 
        		d2[d2==id] <- NA 
        	}
        	writeRaster(d2, file=paste0(tiles_dir, i,"_crowns_buff.tif"), overwrite = T)
        }
        
        
        ##  Calculate values for merging:
        for (i in 1:16) {
        	d <- raster(paste0(tiles_dir, i,"_crowns_buff.tif"))  ## Change to path
        	
        	## Counting pixels for each value:
        	counts <- freq(d)
        	## Converting to df
        	count_df <- as.data.frame(counts)
        	## Removing the NA column in the count df
        	no_na_df <- count_df[-nrow(count_df),]
        	## Reassigning raster vals to counts (other than NA)
        	d2 <- reclassify(d, no_na_df)
        	
        	##  Encode tile, ID, and area in cells:
        	##    - Assumes never having more than 999 trees
        	##    - Assumes never having more than 999999 cells per crown
        	d3 <- i*1000000000 + d*1000000 + d2
        	
        	writeRaster(d3, file=paste0(tiles_dir, i, "_crowns_buff_encoded.tif"), overwrite = T)
        }
        
        
        ##  Mosaic them together:)
        ds <- list()

        for (i in 1:N_tiles) {
        	ds[i] <- brick(paste0(tiles_dir, i,"_crowns_buff_encoded.tif"))
        }
        names(ds[1:2]) <- c('x','y') ##args necessary for do.call()
        ds$fun <- max
        ds$na.rm <- TRUE
        out <- do.call(raster::mosaic, ds)
        
        base <- unlist(strsplit(item, "_")[1])[1]
        
        writeRaster(out, file=paste("../..", "output/ITC", cover, site,
                                    paste( base, "ITC", "mosaicked_trees.tif", sep = "_" ), sep = "/"), overwrite=T)

        plot(out)
        
        
        ##  Create ID raster and area in cells raster:
        #format(max(out[],na.rm=T),scientific=F)
        
        ID_raster <- floor(out/1000000)
        plot(ID_raster)
        writeRaster(ID_raster, file= paste0(tiles_dir, base, "_crowns_mosaicked_IDs.tif"), overwrite = T)#, datatype="INT2U"))
        
        area_raster <- floor(out - ID_raster*1000000)
        plot(area_raster)
        writeRaster(area_raster, file=paste0(tiles_dir, base, "_crowns_mosaicked_areas.tif"), overwrite = T)
       
      }
    }
  }
}


## do.call similar to map
#mos <- do.call(raster::mosaic, c(tiles_to_write, fun<- max ))
#plot(mos)
#writeRaster(mos, "./tst/FRS2max_mos_A2100.tif")
