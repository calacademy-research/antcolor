#Parses caste habitat data from Bradley et al. 2006 into dataframe castegenushab

parseGenusHabitatData <- function(path){
  
BradleyGenusHabitatData <- read.csv(path) 
#BradleyGenusHabitatData <- CasteHabitatData
castegenushab <- BradleyGenusHabitatData
castegenushab$Genus <- as.character(castegenushab$Genus)
castegenushab$Habitat <- as.character(castegenushab$Habitat)
castegenushab$isSoil <- NA
castegenushab$isSurface <- NA
castegenushab$isArboreal <- NA

for (i in 1:nrow(castegenushab))
{
  row <- castegenushab[i,]
  habcode <- row$Habitat
  print(habcode)
  castegenushab[i,3] <- (grepl('A', habcode, fixed=TRUE))
  castegenushab[i,4] <- (grepl('B', habcode, fixed=TRUE))
  castegenushab[i,5] <- (grepl('C', habcode, fixed=TRUE))
}
}

addGenusHabitatData2All <- function(){
#Iterate through big dataframe and add hab tags
colorspecimens$isSoil <- NA
colorspecimens$isSurface <- NA
colorspecimens$isArboreal <- NA
for (i in 1:nrow(colorspecimens))
{
  brow <- colorspecimens[i,]
  bgenus <- brow$genus
  for(k in 1:nrow(castehab))
  {
    srow <- castehab[k,]
    sgenus <- srow$Genus
    if(bgenus == sgenus)
    {
      colorspecimens[i,83] = castehab[k,3]
      colorspecimens[i,84] = castehab[k,4]
      colorspecimens[i,85] = castehab[k,5]
    }
  }
}
}

