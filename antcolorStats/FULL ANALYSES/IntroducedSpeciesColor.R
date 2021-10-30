#Examine introduced species and lightness
introducedspeciesdata <- read.delim('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/speciesListDownload.txt')
View(introducedspeciesdata)
g <- introducedspeciesdata$Genus
g <- sapply(g, tolower)

introducedspeciesdata$scientificName <- paste(g, introducedspeciesdata$Species)
introducedspeciesdata$term <- introducedspeciesdata$scientificName

df <- merge(introducedspeciesdata, colorspecimensworkersspecies, by='term')
mean(colorspecimensworkersspecies$meanlightness)
mean(df$meanlightness)
nrow(df)