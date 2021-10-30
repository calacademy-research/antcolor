#Pull in unimaged specimen information from AntWeb for extraction of various data and the mapping of species distributions
library(jsonlite)

#for file in directory
allspecimens <- matrix(nrow = 0, ncol = 51)
newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens10k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens20k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens30k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens40k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens50k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens60k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens70k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens80k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens100k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

newspecimens <- fromJSON('S:/Databases/madag_specimens/specimens106k.json')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)

nrow(allspecimens)

#OR just grab data from the url

newspecimens <- fromJSON('http://api.antweb.org/v3.1/specimens?geolocaleName=Madagascar&offset=40000&limit=10000&up=1')
newspecimens <- as.matrix(newspecimens$specimens)
allspecimens <- rbind(allspecimens,newspecimens)
