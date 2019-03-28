## QUANTITY AND ALLOCATION DISAGREEMENT

library(xtable)

setwd("C:\\Users\\nkolarik\\Desktop\\thesis\\docs\\qa_bands")



files <- list.files(".")
bands <- c("rgb", "gre", "red", "reg","nir")
covers <- c("grass", "shrub", "tree")


df <- data.frame()
for(cover in covers){
  for(band in bands){
    
    data<- read.csv(paste0(band, "_", cover, ".csv"), header = FALSE)
    ##counts
    tree_ct <- sum(data$V1)
    shrub_ct <- sum(data$V2)
    other_ct <- sum(data$V3)
    
    d <- data/sum(data)
    
    ### assumes a 3x3 conufusion matrix tree, shrub, other
    
    ## quantity disagreements 
    treeQ <- abs(sum(d$V1) - sum(d$V1[1], d$V2[1], d$V3[1]))
    shrubQ <- abs(sum(d$V2) - sum(d$V1[2], d$V2[2], d$V3[2]))
    otherQ <- abs(sum(d$V3) - sum(d$V1[3], d$V2[3], d$V3[3]))
    
    ##allocation disagreements
    treeA <- 2 * min(sum(d$V2[1], d$V3[1]), sum(d$V1[2], d$V1[3]))
    shrubA <- 2 * min(sum(d$V1[2], d$V3[2]), sum(d$V2[1], d$V2[3]))
    otherA <- 2 * min(sum(d$V1[3], d$V2[3]), sum(d$V3[1], d$V3[2]))
    
    ## totals
    totalQ <- sum(treeQ, shrubQ, otherQ)/2
    totalA <- sum(treeA, shrubA, otherA)/2
    totalD <- sum(totalA, totalQ)
    
    tree_row <- c(cover, band, tree_ct, round(treeQ, 3), round(treeA, 3), round(sum(treeQ, treeA),3));
    shrub_row <- c(cover, band, shrub_ct, round(shrubQ, 3), round(shrubA,3), round(sum(shrubQ, shrubA),3))
    other_row<- c(cover, band, other_ct, round(otherQ,3), round(otherA,3), round(sum(otherQ, otherA), 3))
    assign(paste0(band,"_",cover), list(tree_row, shrub_row, other_row))
  }
}

grass_df <-data.frame(rbind(rgb_grass[1], gre_grass[1], red_grass[1], reg_grass[1], nir_grass[1],
                  rgb_grass[2], gre_grass[2], red_grass[2], reg_grass[2], nir_grass[2],
                  rgb_grass[3], gre_grass[3], red_grass[3], reg_grass[3], nir_grass[3])); grass_df

shrub_df <- data.frame(rbind(rgb_shrub[1], gre_shrub[1], red_shrub[1], reg_shrub[1], nir_shrub[1],
                  rgb_shrub[2], gre_shrub[2], red_shrub[2], reg_shrub[2], nir_shrub[2],
                  rgb_shrub[3], gre_shrub[3], red_shrub[3], reg_shrub[3], nir_shrub[3])); shrub_df

tree_df <- data.frame(rbind(rgb_tree[1], gre_tree[1], red_tree[1], reg_tree[1], nir_tree[1],
                 rgb_tree[2], gre_tree[2], red_tree[2], reg_tree[2], nir_tree[2],
                 rgb_tree[3], gre_tree[3], red_tree[3], reg_tree[3], nir_tree[3])); tree_df

summmary <- cbind(grass_df, shrub_df, tree_df)
xsum <- xtable(summary)


#data<- read.csv(f, header = FALSE)
#
###counts
#tree_ct <- sum(data$V1)
#shrub_ct <- sum(data$V2)
#other_ct <- sum(data$V3)
#
#d <- data/sum(data)
#
#### assumes a 3x3 conufusion matrix tree, shrub, other
#
### quantity disagreements 
#treeQ <- abs(sum(d$V1) - sum(d$V1[1], d$V2[1], d$V3[1]))
#shrubQ <- abs(sum(d$V2) - sum(d$V1[2], d$V2[2], d$V3[2]))
#otherQ <- abs(sum(d$V3) - sum(d$V1[3], d$V2[3], d$V3[3]))
#
###allocation disagreements
#treeA <- 2 * min(sum(d$V2[1], d$V3[1]), sum(d$V1[2], d$V1[3]))
#shrubA <- 2 * min(sum(d$V1[2], d$V3[2]), sum(d$V2[1], d$V2[3]))
#otherA <- 2 * min(sum(d$V1[3], d$V2[3]), sum(d$V3[1], d$V3[2]))
#
### totals
#totalQ <- sum(treeQ, shrubQ, otherQ)/2
#totalA <- sum(treeA, shrubA, otherA)/2
#totalD <- sum(totalA, totalQ)
#
#tree_row <- c(band, tree_ct, round(treeQ, 3), round(treeA, 3), round(sum(treeQ, treeA),3))
#shrub_row <- c(band, shrub_ct, round(shrubQ, 3), round(shrubA,3), round(sum(shrubQ, shrubA),3))
#other_row<- c(band, other_ct, round(otherQ,3), round(otherA,3), round(sum(otherQ, otherA), 3))
#
### need to figure out how to make this more flexible - otherwise I will have to repeat the above code block 15 times!
#assign(paste(band, cover, "rows", sep = "_"),list(tree_row, shrub_row, other_row)) ## Error in as.vector(x, "character") : cannot coerce type 'closure' to vector of type 'character'


