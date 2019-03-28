## CREATES A SUMMARY DATAFRAME WITH FACTORS FOR SITE TYPE, SITE, AND BANDS
## INCLUDES ALL INFO THAT WOULD BE INCLUDED IN A CONFUSION MATRIX

setwd("C:\\Users\\nkolarik\\Desktop\\thesis\\docs\\qa_bands")

## listing files in location
files <- list.files(".")

## empty lists for factors
algs <-c()
sites <- c()
bands <- c()
covers <- c()

## estimate_observation empties
tree_tree <- c()
tree_shrub<- c()
tree_other<- c()

shrub_tree <- c() 
shrub_shrub<- c() 
shrub_other<- c() 

other_tree<- c()
other_shrub<- c()
other_other<- c()

#tree_est <- c()
#shrub_est <- c()
#other_est <- c()
  
for(f in files){
  ##list of file string to manipulate
  fstr <- unlist(strsplit(f, "_"))
  
  ##read the csv
  d <- read.csv(f, header = FALSE)
  
  ##constructing the df
  algs <- c(algs, fstr[1])
  sites <- c(sites, fstr[2])
  bands <- c(bands, fstr[3])
  covers <- c(covers, unlist(strsplit(fstr[4], "\\."))[1])
  
  
  tree_tree <- c(tree_tree, d$V1[1])
  tree_shrub <- c(tree_shrub, d$V2[1])
  tree_other <- c(tree_other, d$V3[1])
  
  shrub_tree<- c(shrub_tree, d$V1[2]) 
  shrub_shrub<- c(shrub_shrub, d$V2[2]) 
  shrub_other<- c(shrub_other, d$V3[2]) 
  
  other_tree<- c(shrub_tree, d$V1[3]) 
  other_shrub<- c(shrub_shrub, d$V2[3]) 
  other_other<- c(shrub_other, d$V3[3])
  
  
}

## data frame to return 
df <- cbind(factor(algs), factor(sites), factor(bands), factor(covers), 
            tree_tree, tree_shrub, tree_other, shrub_tree, shrub_shrub, 
            shrub_other, other_tree, other_shrub, other_other)



