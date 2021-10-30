#Pull in csvs
df1 <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/specimenmicrohabsfinal1.csv')
df2 <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/specimenmicrohabsfinal2.csv')
df3 <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/specimenmicrohabsfinal3.csv')

#Merge them
merged <- rbind(df1,df2)
merged <- rbind(merged,df3)

rm('df1','df2','df3')

#OR just start with one
merged <- read.csv('C:/Users/OWNER/OneDrive - Hendrix College/Desktop/specimenmicrohabs400k.csv')
  
#Prep color data
library(dplyr)
temp <- colorspecimens
temp <- select(temp, specimenCode, hue, saturation, lightness, antwebTaxonName)
colnames(temp)[1] <- "SpecimenCode"

#Merge with taxon names - quick fix

#Merge with color data by shared specimenCode 
specimenmicrohabsmerged <- merge(merged, temp, by= "SpecimenCode",all = TRUE)

specimenmicrohabsmerged <- filter(specimenmicrohabsmerged, isSoil == 'True' | isGround== 'True' | isArboreal == 'True')
#Or
specimenmicrohabsmerged <- filter(specimenmicrohabsmerged, MicrohabString != 'None')

specimenmicrohabsmerged <- select(specimenmicrohabsmerged, -'X', -'antwebTaxonName',-'sortingID')

#DONE
View(specimenmicrohabsmerged)
nrow(specimenmicrohabsmerged)


write.csv(specimenmicrohabsmerged,"C:/Users/OWNER/OneDrive - Hendrix College/Desktop/allspecimenmicrohabs9-30.csv", row.names = FALSE)

#Also prep species microhabs for shits 
colorspeciesmicrohabsprepped <- select(colorspeciesmicrohabs, -'X',-'term',)
View(colorspeciesmicrohabs)

nrow(filter(specimenmicrohabsmerged, isGround== 'True'))
