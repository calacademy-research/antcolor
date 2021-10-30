#Genus stuff

#Read in all species microhabs if haven't already
allgenusmicrohabs <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/speciesmicrohabs.csv')

#Split taxa into genus
allgenusmicrohabs$Species <- as.character(allgenusmicrohabs$Species)
split_taxa <- as.matrix(strsplit(allgenusmicrohabs$Species," "))
values <- c()
for(i in 1:nrow(split_taxa))
{
  values <- c(values,split_taxa[[i]][1])
}
allgenusmicrohabs$Genus <- values

library(dplyr)
#Sum num microhabitats for each genus
allgenusmicrohabs <- allgenusmicrohabs %>% #I use df for all temporary dataframes
  group_by(Genus) %>% #Group by genus
  summarize(sumArboreal = sum(numArboreal),sumLitterSoil= sum(numLitter + numSoil),sumGround = sum(numGround))


#Create genus color averages for workers (add colorPC1 if you haven't yet)
library(dplyr)
df <- colorspecimensworkers

#Split taxa into genus
df$antwebTaxonName <- as.character(df$antwebTaxonName)

split_taxa <- as.matrix(strsplit(df$antwebTaxonName," "))
values <- c()
for(i in 1:nrow(split_taxa))
{
  values <- c(values,split_taxa[[i]][1])
}
df$Genus <- values

df <- df %>% #I use df for all temporary dataframes
  group_by(Genus) %>% #Group by genus
  summarize(colorPC1_mean = mean(PC1, na.nm = TRUE), nColor = n())

#Prep both dataframes
df$Genus <- as.character(df$Genus)
df$colorPC1_mean <- as.numeric(df$colorPC1_mean)
allgenusmicrohabs$Genus <- as.character(allgenusmicrohabs$Genus)

#Merge both dataframes into final
colorgenusmicrohabs <- merge.data.frame(allgenusmicrohabs, df, by ="Genus", all = TRUE)
View(colorgenusmicrohabs)

#Count number of microhab-classified species and total species
print("Total species")
nrow(colorgenusmicrohabs)

filtered <- dplyr::filter(colorgenusmicrohabs, numLitter >= 1)
filtered <- rbind(filtered,dplyr::filter(colorspeciesmicrohabs, numArboreal >= 1))
filtered <- rbind(filtered,dplyr::filter(colorspeciesmicrohabs, numElse >= 1))
nrow(filtered)
