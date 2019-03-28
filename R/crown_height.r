## FITTING A MODEL FOR THE VARAIBLE WINDOW FILTER

library(car)
library(tidyverse)
library(fmsb)

setwd("C:/Users/nkolarik/Desktop/thesis")

data <- read.csv("./data/field_validation2018/total_insitu.csv", header = TRUE)

## data at the site level
grass <- data %>% filter(type == "grass", height1 > 0)
shrub <- data %>% filter(type == "shrub", height1 > 0)
tree <- data %>% filter(type == "tree", height1 > 0)

grass_tree <- data %>% filter(type != "shrub", height1 > 0)


all_ht <- data$mean_height
all_ht_sq <- data$mean_height^2; all_ht_sq

all_crowns <- data$crown_max_dia

all_model <- lm(formula = all_crowns ~ all_ht); all_model ## Rsq 0.7559
summary(all_model)

hist(rstandard(all_model)) ## normalish?
shapiro.test(rstandard(all_model)) ## p-value = 1.047e-11 VIOLATES ASSUMPTION OF NORMALITY

## plot of residuals
plot(all_model$fitted.values, rstandard(all_model)) # linearISH

plot(all_ht, all_crowns)
abline(all_model)

all_model2 <- lm(formula = all_crowns ~ poly(all_ht_sq), 2, raw = TRUE); all_model2 ##Rsq 0.6808 
summary(all_model2)


## grass sites only

grass_model <- lm(grass$crown_max_dia~grass$mean_height); grass_model ## Rsq 0.8125
summary(grass_model)
plot(grass$mean_height, grass$crown_max_dia)


## shrub sites only

shrub_model <- lm(shrub$crown_max_dia~shrub$mean_height); shrub_model ## Rsq 0.1358
summary(shrub_model)
plot(shrub$mean_height, shrub$crown_max_dia)


## tree sites only

tree_model <- lm(tree$crown_max_dia~tree$mean_height); tree_model ## Rsq 0.8979
summary(tree_model)
plot(tree$mean_height, tree$crown_max_dia)
abline(tree_model)


## non-shrub sites 
 
grass_tree_model <- lm(grass_tree$crown_max_dia~grass_tree$mean_height); grass_tree_model
summary(grass_tree_model)
plot(grass_tree$mean_height, grass_tree$crown_max_dia)#Adj Rsq 0.9141
abline(grass_tree_model)

## analysis of residuals
## normality test
hist(rstandard(grass_tree_model)) ## right skewed
shapiro.test(rstandard(grass_tree_model))##p = 0.0006844 - violates normality assumption

## transforming crown measurements squaring
crowns2 <- grass_tree$crown_max_dia**2
grass_tree_model2 <- lm(crowns2 ~ grass_tree$mean_height)
summary(grass_tree_model2)
plot(grass_tree$mean_height, crowns2)

##analysis of residuals
hist(rstandard(grass_tree_model2)) 
shapiro.test(rstandard(grass_tree_model2))  ##p-value = 5.537e-07

## try a sqrt transform
sqrt_crowns <- sqrt(grass_tree$crown_max_dia)
sqrt_grass_tree <- lm(sqrt_crowns ~ grass_tree$mean_height)
summary(sqrt_grass_tree)
plot(sqrt_grass_tree)
plot(grass_tree$mean_height,sqrt_crowns ) ## Adjusted R-squared:  0.937

##analysis of residuals
## normality
hist(rstandard(sqrt_grass_tree)) 
shapiro.test(rstandard(sqrt_grass_tree)) ##  p-value = 0.1141 NORMALish!

## crown = (0.925949 + 0.230284 * height)**2
## crown = 0.8573816 + 0.4264624 * height + 0.05303072 * height**2

## data for only trees - filter on woodys > 3
trees_only <- data %>% filter(mean_height > 3); trees_only

## " Shrubs
shrubs_only <- data%>% filter(mean_height <3); shrubs_only

## linear models
only_tree <- lm(trees_only$crown_max_dia ~ trees_only$mean_height); summary(only_tree) ##Rsq 0.6124
plot(trees_only$mean_height, trees_only$crown_max_dia)
abline(only_tree)


only_shrub <- lm(shrubs_only$crown_max_dia ~ shrubs_only$mean_height); summary(only_shrub) ##Rsq 0.2425
plot(shrubs_only$mean_height, shrubs_only$crown_max_dia)
abline(only_shrub)