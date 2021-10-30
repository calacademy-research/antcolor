#Prep the ant color dataset from Elastic

#Prep starter dataframes
#Creates: locatedspecimens (all with geocoords), colorlocated (all with valid color + geo), 
##        colorspecimens (all with valid color), and colortempsolar

library(dplyr)
source("Helpers/prepareElasticGISDataframes.R")

prepareElasticGISDataframes('allantshsv') #name of dataset in Elastic

#Prep caste dataframes : contain all specimens in each caste 
colorspecimens <- filter(colorspecimens, grepl(FALSE, fossil)) #no fossils, for example
colorspecimensworkers <- filter(colorspecimens, grepl('worker', caste))
colorspecimensqueens <- filter(colorspecimens, grepl('queen', caste)) 
colorspecimensmales <- filter(colorspecimens, grepl('male', caste)) 

source("Helpers/casteCladeThreshold.R")
source("Helpers/oldSubset.R")
#Prep caste-clade thresholded dataframes 
castegenusthreshed1_wqm <- casteCladeThreshold('genus', 1, 1)
castegenusthreshed1_wm <- casteCladeThreshold('genus', 1, 2)
castegenusthreshed1_wq <- casteCladeThreshold('genus', 1, 3)
