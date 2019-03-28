## CONVERTING FILED MEASUREMENTS TO POINT AND POLYGON SHAPEFILES

library(googlesheets)
library(sp)
library(rgdal)

path <- "C:/Users/nkolarik/Desktop/thesis/field_validation2018/crowns"


##	Load data from Google Sheet:
##		https://docs.google.com/spreadsheets/d/1r3B5FJ01KJuEZ-X1tt1m7b99PosFuQWBXqAPNIXMUaM/edit#gid=0
#gs_ls()
#tc <- gs_title("Tom Sawyer Trees")

#gs_ws_ls(tc)

##	Get data from the Data sheet:
#ws <- gs_read(ss=tc, ws = "Data", skip=0)
ws <- read.csv("C:/Users/nkolarik/Desktop/thesis/field_validation2018/grass/N1004/N1004_val.csv", header = TRUE)

# convert to data.frame
d <- as.data.frame(ws)


## Tree Measurement Data, Sample Processing:

##  Sample of four trees, with stem location X/Y and crown dimensions on 
##    cardinal directions:

##  https://goo.gl/maps/osR2LAQqkup
prj_str <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
#prj_str_utm <- "+proj=utm +zone=16 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"

## Appropriate UTM zone for data
prj_str_utm <- "+proj=utm +south +zone=34 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"

#plot(c(-3,3), c(-3,3))
#xspline(c(1,0,-1,0), c(0,1,0,-.5), -1, open=F, repEnds=T)
names(d)

##  Create spatial points data.frame of tree locations:
#stems <- SpatialPointsDataFrame(d[,c("lon","lat")], d, coords.nrs = numeric(0), proj4string = CRS(prj_str), match.ID=T)
stems <- SpatialPointsDataFrame(d[,c("POINT_X","POINT_Y")], d, coords.nrs = numeric(0), proj4string = CRS(prj_str), match.ID=T)

stems_prj <- spTransform(stems, CRS(prj_str_utm))
plot(stems_prj)


##  Create polygon objects using splines of crown dimensions:
pc <- list()
for (i in 1:nrow(stems_prj)) {
  tree <- stems_prj[i,]
  x <- tree@coords[1]
  y <- tree@coords[2]
	#crown <- xspline(c(x,x+tree$crownE,x,x-tree$crownW), c(y+tree$crownN,y,y-tree$crownS,y), -1, open=F, repEnds=T, draw=F)
  crown <- xspline(c(x,x+tree$crownE,x,x-tree$crownW), c(y+tree$crownN,y,y-tree$crownS,y), -1, open=F, repEnds=T, draw=F)
  pc[[i]] <- Polygons(list(Polygon(list(as.matrix(data.frame(crown$x, crown$y))), hole=F)), ID=i)
}
crowns_prj <- SpatialPolygonsDataFrame(
  SpatialPolygons(pc, proj4string = CRS(prj_str_utm)
  ),
  d, match.ID=T
)

plot(crowns_prj)
plot(stems_prj, add=T, col="red")


##	Save off data as shapefiles and KML:
writeOGR(spTransform(stems_prj, CRS(prj_str)), dsn=paste0(path, "output/", "stems.kml"), layer="stems", driver="KML")
writeOGR(stems_prj, dsn=paste0(path, "output"), layer="stems_prj", driver="ESRI Shapefile")
writeOGR(spTransform(crowns_prj, CRS(prj_str)), dsn=paste0(path, "output/", "crowns.kml"), layer="crowns", driver="KML")
writeOGR(crowns_prj, dsn=paste0(path, "output"), layer="crowns_prj", driver="ESRI Shapefile")
