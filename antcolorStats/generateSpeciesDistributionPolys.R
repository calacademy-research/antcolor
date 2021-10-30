#Generate species distributions using raw AntWeb data
install.packages("devtools")
devtools::install_github("marlonecobos/rangemap")
library(rangemap)

unimagedspecimens <- as.data.frame(allspecimens)
View(summary(unimagedspecimens$antwebTaxonName))
unimagedset <- dplyr::filter(unimagedspecimens, grepl('formicinaecamponotus reaumuri', antwebTaxonName))


unimagedset <- cbind(as.character(unimagedset$genus), as.numeric(as.character(unimagedset$decimalLongitude)), as.numeric(as.character(unimagedset$decimalLatitude)))
unimagedset <- unimagedset[complete.cases(unimagedset),]
colnames(unimagedset) <- c('Species','Longitude', 'Latitude')
unimagedset <- as.data.frame(unimagedset)
unimagedset$Longitude <- as.numeric(as.character(unimagedset$Longitude))
unimagedset$Latitude <- as.numeric(as.character(unimagedset$Latitude))

#View occurrences on map
rangemap_explore(occurrences = unimagedset)

#Make buffered rangemap
buff_range <- rangemap_buff(occurrences = unimagedset, buffer_distance = 75000,
                            save_shp = FALSE, name = 'test')
rangemap_fig(buff_range, zoom = 1)

#Make non-disjunct hull rangemap
hull_range <- rangemap_hull(occurrences = unimagedset, hull_type = 'concave', buffer_distance = 10000,
                            split = FALSE, save_shp = FALSE, name = 'test1')

hull_range2 <- rangemap_hull(occurrences = unimagedset, hull_type = 'convex', buffer_distance = 10000,
                             split = TRUE, cluster_method = 'hierarchical', split_distance = 500000, save_shp = FALSE, name = 'test1')

hull_range3 <- rangemap_hull(occurrences = unimagedset, hull_type = 'convex', buffer_distance = 10000,
                             split = TRUE, cluster_method = 'k-means', n_k_means =  5, save_shp = FALSE, name = 'test1')

rangemap_fig(hull_range2, zoom = 1, add_occurrences = TRUE)

#generate from imaged species of Camponotus and save as shape files to /distributiondata

allspecimens <- as.data.frame(allspecimens)
df <- filter(allspecimens, genus == "Camponotus", bioregion == "Malagasy")
df <- group_by(df, antwebTaxonName)
df <- summarize(df, n())
colnames(df) <- c('taxon', 'n')
threshedtaxa <- filter(df, n >= 5)

filter(allspecimens, antwebTaxonName %in% df$taxon)
num <- function(vector)
{
  return(as.numeric(as.character(vector)))
}
root <- getwd()
setwd('Data/distributionSHPs')

test <- threshedtaxa[1:10,]
for(taxon in test$taxon) #nrow(threshedtaxa)threshedtaxa$taxon
{
  specimens <- filter(allspecimens, antwebTaxonName == taxon)
  specimens <- cbind(as.character(specimens$antwebTaxonName), num(specimens$decimalLongitude), num(specimens$decimalLatitude))
  specimens <- specimens[complete.cases(specimens),]
  colnames(specimens) <- c('Species','Longitude', 'Latitude')
  specimens <- as.data.frame(specimens)
  specimens$Longitude <- num(specimens$Longitude)
  specimens$Latitude <- num(specimens$Latitude)
  
  rangemap_hull(occurrences = specimens, hull_type = 'convex', buffer_distance = 10000,
                               split = TRUE, cluster_method = 'hierarchical', split_distance = 500000, save_shp = TRUE, name = taxon)
}

View(df)
source("Helpers/oldSubset.R")
colorspecimensCladeMadagtaxa <- prepareSubsetDataframe(df= colorspecimensCladeMadag,subsetBy= 'antwebTaxonName', threshold = 5)
