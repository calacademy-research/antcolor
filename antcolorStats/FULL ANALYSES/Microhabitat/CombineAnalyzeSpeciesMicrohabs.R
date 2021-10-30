#Combines the species microhabitat csv generated using Python & Elastic with the species color averages
#That table looks like [1]Species, [2]numSoil, [3]numLitter, [4]numGround, [5]numArboreal
#Read in all species microhabs
allspeciesmicrohabs <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/speciesmicrohabs.csv')

#Create species color averages for workers (add colorPC1 if you haven't yet)
library(dplyr)
df <- colorspecimensmales %>% #I use df for all temporary dataframes
  group_by(antwebTaxonName) %>% #Group by taxon name
  summarize(colorPC1_mean = mean(PC1, na.nm = TRUE), nColor = n())

#Prep both dataframes
df$Species <- as.character(df$antwebTaxonName)
df$colorPC1_mean <- as.numeric(df$colorPC1_mean)
allspeciesmicrohabs$Species <- as.character(allspeciesmicrohabs$Species)

#Merge both dataframes into final
colorspeciesmicrohabs <- merge.data.frame(allspeciesmicrohabs, df, by = "Species", all = TRUE)
#Drop columns
drops <- c("X","antwebTaxonName")
colorspeciesmicrohabs <- colorspeciesmicrohabs[ , !(names(colorspeciesmicrohabs) %in% drops)]

#Count number of microhab-classified species and total species

print("Total species")
nrow(colorspeciesmicrohabs) #25k 
#6k ground, 6k soil, 6k litter, 3k arboreal 
View(colorspeciesmicrohabs)
filtered <- dplyr::filter(colorspeciesmicrohabs, numLitter >= 1)
nrow(filtered) 
filtered <- dplyr::filter(colorspeciesmicrohabs, numArboreal >= 1)
nrow(filtered)
filtered <- rbind(filtered,dplyr::filter(colorspeciesmicrohabs, numGround>= 1))
nrow(filtered)
filtered <- rbind(filtered,dplyr::filter(colorspeciesmicrohabs, numSoil>= 1))
nrow(filtered)

filtered <- dplyr::filter(colorspeciesmicrohabs, numSoil>= 1 | numGround>= 1 | numArboreal >=1 | numLitter >=1)
nrow(filtered) #9k have at least 1 microhab

filtered <- dplyr::filter(colorspeciesmicrohabs, numSoil>= 1 | numLitter >=1)
nrow(filtered) #9k have at least 1 microhab

#Add the total number of microhab-recorded specimens
colorspeciesmicrohabs$nMicrohab <- colorspeciesmicrohabs$numLitter + 
                                      colorspeciesmicrohabs$numGround +
                                      colorspeciesmicrohabs$numSoil +
                                      colorspeciesmicrohabs$numArboreal

colorspeciesmicrohabs$numSoilLitter <- colorspeciesmicrohabs$numLitter + colorspeciesmicrohabs$numSoil
#Add percentages using nMicrohab
colorspeciesmicrohabs$pSoil <- (colorspeciesmicrohabs$numSoil / colorspeciesmicrohabs$nMicrohab)
colorspeciesmicrohabs$pLitter <- (colorspeciesmicrohabs$numLitter / colorspeciesmicrohabs$nMicrohab)
colorspeciesmicrohabs$pSoilLitter <- (colorspeciesmicrohabs$numSoilLitter / colorspeciesmicrohabs$nMicrohab)
colorspeciesmicrohabs$pGround <- (colorspeciesmicrohabs$numGround / colorspeciesmicrohabs$nMicrohab)
colorspeciesmicrohabs$pArboreal <- (colorspeciesmicrohabs$numArboreal / colorspeciesmicrohabs$nMicrohab)

#Idea - single linear variable across microhabs
#EXAMPLE 10% soil, 20% litter, 30$ ground, 40% arboreal 
#100% arboreal = 1 
#100% soil = 0 
#THERE IS A WAY TO DO THIS SURELY!!!

#For now, add categorical bools based on percentage thresholds
#Threshold for being solely in one:
thresh1 = 0.80
#Threshold for being in two - greater than 30% in each and greater than 80% total i.e. 40 and 40, 31 and 49
thresh2each = 0.30
thresh2both = 0.80

colorspeciesmicrohabs$boolSoilLitter <- (colorspeciesmicrohabs$numSoilLitter > thresh1)
colorspeciesmicrohabs$boolSoilLitterGround <- (colorspeciesmicrohabs$pGround > thresh2each & 
                                           colorspeciesmicrohabs$pSoilLitter > thresh2each & 
                                           (colorspeciesmicrohabs$pSoilLitter + colorspeciesmicrohabs$pGround > thresh2both))
colorspeciesmicrohabs$boolGround <- (colorspeciesmicrohabs$pGround > thresh1)
colorspeciesmicrohabs$boolGroundArboreal <- (colorspeciesmicrohabs$pGround > thresh2each & 
                                               colorspeciesmicrohabs$pArboreal > thresh2each & 
                                               (colorspeciesmicrohabs$pArboreal + colorspeciesmicrohabs$pGround > thresh2both))
colorspeciesmicrohabs$boolArboreal <- (colorspeciesmicrohabs$pArboreal > thresh1)

#Temp
colorspeciesmicrohabs$boolGround <- (colorspeciesmicrohabs$pElse > thresh1)
colorspeciesmicrohabs$boolLitterGround <- (colorspeciesmicrohabs$pElse > thresh2each & 
                                             colorspeciesmicrohabs$pLitter > thresh2each & 
                                             (colorspeciesmicrohabs$pLitter + colorspeciesmicrohabs$pElse > thresh2both))
colorspeciesmicrohabs$boolArboreal <- (colorspeciesmicrohabs$pArboreal > thresh1)
colorspeciesmicrohabs$boolGroundArboreal <- (colorspeciesmicrohabs$pElse > thresh2each & 
                                               colorspeciesmicrohabs$pArboreal > thresh2each & 
                                               (colorspeciesmicrohabs$pArboreal + colorspeciesmicrohabs$pElse > thresh2both))
#Done
View(colorspeciesmicrohabs)

filtered <- dplyr::filter(colorspeciesmicrohabs, boolArboreal == TRUE)
mean(filtered$colorPC1_mean, na.rm = TRUE)
nrow(filtered)


View(filtered)
mean(filtered$PC1,na.rm = TRUE)

View(filtered)
#SLOPPY MATH BELOW
#Quick maths
filtered <- dplyr::filter(colorspeciesmicrohabs, numLitter >= 1)
filtered <- dplyr::filter(filtered, numLitter >= (numArboreal * 3))
filtered <- dplyr::filter(colorspeciesmicrohabs, numArboreal >= 1)
filtered <- dplyr::filter(filtered, numArboreal >= (numLitter * 3))
filtered <- dplyr::filter(colorspeciesmicrohabs, numElse >= 1)
nrow(filtered)
mean(filtered$pc1_mean,na.rm = TRUE)
View(filtered)

library(dplyr)
library(data.table)

rawmicrohabs <- unique(colorspecimens$microhabitat)
rawmicrohabs[rawmicrohabs %like% "trunk"]
rawmicrohabs

#OR combine with caste species colors
castetaxonthreshed1$Species <- castetaxonthreshed1$term
colorspeciesmicrohabs <- merge.data.frame(allspeciesmicrohabs, speciescoloraverages, by = "Species", all = TRUE)

#Quick maths
filtered <- dplyr::filter(colorspeciesmicrohabs, numLitter>= 2)
nrow(filtered)
mean(filtered$meanlightness.x,na.rm = TRUE)
mean(filtered$meanlightness,na.rm = TRUE)
mean(filtered$meanlightness.y,na.rm = TRUE)

filtered <- dplyr::filter(colorspeciesmicrohabs, numArboreal>= 2)
nrow(filtered)
mean(filtered$meanlightness.x,na.rm = TRUE)
mean(filtered$meanlightness,na.rm = TRUE)
mean(filtered$meanlightness.y,na.rm = TRUE)

filtered <- dplyr::filter(colorspeciesmicrohabs, numElse>= 30)
nrow(filtered)
mean(filtered$meanlightness.x,na.rm = TRUE)
mean(filtered$meanlightness,na.rm = TRUE)
mean(filtered$meanlightness.y,na.rm = TRUE)

#OPTIONAL - filter for num with both
filtered <- dplyr::filter(filtered, numLitter<= 3)
nrow(filtered)
mean(filtered$meanlightness.x,na.rm = TRUE)
mean(filtered$meanlightness,na.rm = TRUE)
mean(filtered$meanlightness.y,na.rm = TRUE)

#POSSIBLY - weed out bad reads using genus data 

#OPTIONAL - adjust colorspeciesmicrohabs to have only 1 microhab per species

#Again
filtered <- dplyr::filter(colorspeciesmicrohabs, numLitter > 0)
filtered <- dplyr::filter(filtered, numLitter >= (numArboreal * 3))

filtered <- dplyr::filter(colorspeciesmicrohabs, numArboreal > 0)
filtered <- dplyr::filter(filtered, numArboreal >= (numLitter * 3))
View(filtered)
nrow(filtered)
mean(filtered$meanlightness.x,na.rm = TRUE)
mean(filtered$meanlightness,na.rm = TRUE)
mean(filtered$meanlightness.y,na.rm = TRUE)

#do with pc1 

#To find additional categoricals
library(stringr)
#Read in all uncat microhabs
uncatmicrohabs <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/microhabUncat.csv')
uncatmicrohabs$mhstring <- as.character(uncatmicrohabs$mhstring)
View(uncatmicrohabs)

df <- data.frame(word=character(0))

#Split strings and add all words to df 
for(i in rownames(uncatmicrohabs))
{
  str <- uncatmicrohabs[1,"mhstring"]
  split <- str_split(str," ")
  for(string in split)
  {
    df[nrow(df) + 1,] = c(string)
  }
}

words <- df %>% 
  group_by(word) %>%
  summarize(n = n())
  
View(words)