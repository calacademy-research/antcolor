#Stats for analyzing caste-clade thresholded data and calculating caste representation by species, genus, or taxon in AntWeb,

#Prep caste-clade thresholded dataframes : contain all clades with enough specimens of each caste to meet the threshold
source("Helpers/casteCladeThreshold.R")
castespeciesthreshed1 <-  casteCladeThreshold(cladetype = 'scientificName', min_threshold = 1)
castespeciesthreshed2 <-  casteCladeThreshold(cladetype = 'scientificName', min_threshold = 2)
castespeciesthreshed3 <-  casteCladeThreshold(cladetype = 'scientificName', min_threshold = 3)
castespeciesthreshed5 <-  casteCladeThreshold(cladetype = 'scientificName', min_threshold = 5)

castegenusthreshed1 <-  casteCladeThreshold(cladetype = 'genus', min_threshold = 1,comparison_type = 1)
nrow(castegenusthreshed1)
castegenusthreshed2 <-  casteCladeThreshold(cladetype = 'genus', min_threshold = 2)
nrow(castegenusthreshed2)
castegenusthreshed3 <-  casteCladeThreshold(cladetype = 'genus', min_threshold = 3)
nrow(castegenusthreshed3)
castegenusthreshed5 <-  casteCladeThreshold(cladetype = 'genus', min_threshold = 5)
nrow(castegenusthreshed5)

castetaxonthreshed1 <- casteCladeThreshold(cladetype = 'antwebTaxonName', min_threshold = 1)
nrow(castetaxonthreshed1)

#Species and subspecies threshed
#Workers 
mean(castetaxonthreshed1$meanlightness.x)
mean(castetaxonthreshed1$sdlightness.x, na.rm = TRUE)
mean(castetaxonthreshed1$selightness.x, na.rm = TRUE)

#Queens
mean(castetaxonthreshed1$meanlightness)
mean(castetaxonthreshed1$sdlightness, na.rm = TRUE)
mean(castetaxonthreshed1$selightness, na.rm = TRUE)

#Males
mean(castetaxonthreshed1$meanlightness.y)
mean(castetaxonthreshed1$sdlightness.y, na.rm = TRUE)
mean(castetaxonthreshed1$selightness.y, na.rm = TRUE)

#Genera threshed
#Workers 
mean(castegenusthreshed1$meanlightness.x)
mean(castegenusthreshed1$sdlightness.x, na.rm = TRUE)
mean(castegenusthreshed1$selightness.x, na.rm = TRUE)

#Queens
mean(castegenusthreshed1$meanlightness)
mean(castegenusthreshed1$sdlightness, na.rm = TRUE)
mean(castegenusthreshed1$selightness, na.rm = TRUE)

#Males
mean(castegenusthreshed1$meanlightness.y)
mean(castegenusthreshed1$sdlightness.y, na.rm = TRUE)
mean(castegenusthreshed1$selightness.y, na.rm = TRUE)
View(castegenusthreshed1)

#Reformat taxon or species table to use in ANOVA
castetaxonthreshed1anovaformatted <- data.frame(matrix(ncol = 5, nrow = 645))
x <- c("taxon", "Caste", "meanlightness", "sdlightness", "selightness")
colnames(castetaxonthreshed1anovaformatted) <- x
View(castetaxonthreshed1anovaformatted)

i = 1
for (row in 1:nrow(castetaxonthreshed1)) {
  term <- as.character(castetaxonthreshed1[row,1])
  caste <- 'worker'
  lightness <- as.numeric(castetaxonthreshed1[row,3])
  SDlightness <- as.numeric(castetaxonthreshed1[row,4])
  SElightness <- as.numeric(castetaxonthreshed1[row,5])
  
  castetaxonthreshed1anovaformatted[i,] <- cbind(term, caste, lightness, SDlightness, SElightness)
  i <- i+1
  
  caste <- 'queen'
  lightness <- as.numeric(castetaxonthreshed1[row,109])
  SDlightness <- as.numeric(castetaxonthreshed1[row,110])

  SElightness <- as.numeric(castetaxonthreshed1[row,111])

  castetaxonthreshed1anovaformatted[i,] <- cbind(term, caste, lightness, SDlightness, SElightness)
  i <- i+1
  
  caste <- 'male'
  lightness <- as.numeric(castetaxonthreshed1[row,56])
  SDlightness <- as.numeric(castetaxonthreshed1[row,57])

  SElightness <- as.numeric(castetaxonthreshed1[row,58])

  castetaxonthreshed1anovaformatted[i,] <- cbind(term, caste, lightness, SDlightness, SElightness)
  i <- i+1
}


anova <- aov(meanlightness ~ Caste, data=castegenusthreshed1anovaformatted)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

anova <- aov(meanlightness ~ Caste, data=castetaxonthreshed1anovaformatted)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

mean(castetaxonthreshed1$sdlightness.x, na.rm = TRUE)

#Count number of valid taxa
sum(castegenusthreshed1$numvalidtaxa)
mean(castegenusthreshed1$meanlightness)
mean(castegenusthreshed1$meanlightness.x)
mean(castegenusthreshed1$meanlightness.y)

mean(castespeciesthreshed2$meanlightness)
mean(castespeciesthreshed2$meanlightness.x)
mean(castespeciesthreshed2$meanlightness.y)

mean(castespeciesthreshed3$meanlightness)
mean(castespeciesthreshed3$meanlightness.x)
mean(castespeciesthreshed3$meanlightness.y)

nrow(colorspecimensmalesgenera)
sum(colorspecimensmalesgenera$numvalidtaxa)
nrow(colorspecimensqueensgenera)
View(colorspecimensqueensgenera)
sum(colorspecimensqueensgenera$numvalidtaxa)
nrow(colorspecimensworkersgenera)
sum(colorspecimensworkersgenera$numvalidtaxa)

#used to write to Excel to later draw a 3D color scatter in Python
source("Helpers/write2Excel.R")
write2Excel(castespeciesthreshed1)

sum(castegenusthreshed1$numvalidtaxa)
sum(castegenusthreshed1$numvalidtaxa.x)
sum(castegenusthreshed1$numvalidtaxa.y)
View(castegenusthreshed1)
colorspecimensworkerstaxa <- prepareSubsetDataframe(df= colorspecimensworkers,subsetBy= 'antwebTaxonName',threshold = 1)

#MORE STUFF
mean(colorspecimensworkersgenera$meanred)
mean(colorspecimensworkersgenera$meanblue)
mean(colorspecimensworkersgenera$meangreen)

View(castegenusthreshed1)
castegenusthreshed1$meansaturation <- as.numeric(castegenusthreshed1$meansaturation)

mean(castegenusthreshed1$meanhue.x, na.rm = TRUE)
mean(castegenusthreshed1$meansaturation.x, na.rm = TRUE)
mean(castegenusthreshed1$meanlightness.x, na.rm = TRUE)

mean(castegenusthreshed1$meansaturation, na.rm = TRUE)
mean(castegenusthreshed1$meanlightness, na.rm = TRUE)
mean(castegenusthreshed1$meanhue, na.rm = TRUE)

mean(castegenusthreshed1$meanhue.y, na.rm = TRUE)
mean(castegenusthreshed1$meansaturation.y, na.rm = TRUE)
mean(castegenusthreshed1$meanlightness.y, na.rm = TRUE)