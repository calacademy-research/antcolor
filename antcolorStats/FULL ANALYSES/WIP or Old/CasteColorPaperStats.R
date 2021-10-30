#Some stats run for the Summer 2018 presentation version of project
# presented at the California Academy of Sciences

#Refresh all variables
rm(list=ls()) 

#Prepare new dataframes from each set
source("prepareSpecimenDataframes.R")
prepareSpecimenDataframes('allantshsv')


#Look at means, SDs, SEs
se <- function(x) sqrt(var(x)/length(x))

nrow(colorspecimensworkers)

mean(colorspecimensworkers$lightness)
sd(colorspecimensworkers$lightness)
se(colorspecimensworkers$lightness)

mean(colorspecimensworkers$saturation)
sd(colorspecimensworkers$saturation)
se(colorspecimensworkers$saturation)

nrow(colorspecimensmales)
mean(colorspecimensmales$lightness)
sd(colorspecimensmales$lightness)
se(colorspecimensmales$lightness)

mean(colorspecimensmales$saturation)
sd(colorspecimensmales$saturation)
se(colorspecimensmales$saturation)

nrow(colorspecimensqueens)

mean(colorspecimensqueens$lightness)
sd(colorspecimensqueens$lightness)
se(colorspecimensqueens$lightness)

mean(colorspecimensqueens$saturation)
sd(colorspecimensqueens$saturation)
se(colorspecimensqueens$saturation)

#anovas
anova <- aov(saturation ~ caste, data=colorspecimens)
summary(anova)
TukeyHSD(anova)

cor(colorspecimens$lightness,colorspecimens$saturation)
#Filter for value in field
colorlocated <- dplyr::filter(colorlocated, grepl(FALSE, fossil)) #set to desired field and value
colorlocatedworkers <- dplyr::filter(colorlocated, grepl('worker', caste)) #set to desired field and value

#Prep caste subset
source("Helpers/prepareSubsetDataframe.R")
colorspecimenscaste <- prepareSubsetDataframe(df= colorspecimens,subsetBy= 'caste')
View(colorspecimenscaste)

#Check means for groups with regard to image analysis
colorspecimensqueens <- dplyr::filter(colorspecimens, grepl("queen", caste)) #set to desired field and value
colorspecimensqueens$pixUsed = as.numeric(as.character(colorspecimensqueens$pixUsed))
mean(colorspecimensqueens$pixUsed, na.rm=TRUE)
sd(colorspecimensqueens$pixUsed, na.rm=TRUE)

mean(colorspecimensqueens$pixSD, na.rm=TRUE)

colorspecimensmales <- dplyr::filter(colorspecimens, grepl("male", caste)) #set to desired field and value
colorspecimensmales$pixUsed = as.numeric(as.character(colorspecimensmales$pixUsed))
mean(colorspecimensmales$pixUsed, na.rm=TRUE)
sd(colorspecimensmales$pixUsed, na.rm=TRUE)

mean(colorspecimensmales$pixSD, na.rm=TRUE)

colorspecimensworkers <- dplyr::filter(colorspecimens, grepl("worker", caste)) #set to desired field and value
colorspecimensworkers$pixUsed = as.numeric(as.character(colorspecimensworkers$pixUsed))
mean(colorspecimensworkers$pixUsed, na.rm=TRUE)
sd(colorspecimensworkers$pixUsed, na.rm=TRUE)

mean(colorspecimensworkers$pixSD, na.rm=TRUE)

#Prep light genera subset
colorspecimensStrumigenys <- dplyr::filter(colorspecimens, grepl("Strumigenys", genus)) #set to desired field and value
colorspecimensSolenopsis <- dplyr::filter(colorspecimens, grepl("Solenopsis", genus)) #set to desired field and value
colorspecimensCarebara <- dplyr::filter(colorspecimens, grepl("Carebara", genus)) #set to desired field and value

source("Helpers/prepareSubsetDataframe.R")
colorspecimensStrumigenyscaste <- prepareSubsetDataframe(df= colorspecimensStrumigenys,subsetBy= 'caste')
colorspecimensSolenopsiscaste <- prepareSubsetDataframe(df= colorspecimensSolenopsis,subsetBy= 'caste')
colorspecimensCarebaracaste <- prepareSubsetDataframe(df= colorspecimensCarebara,subsetBy= 'caste')

View(colorspecimensCarebaracaste)

#last minute poster stuff
mean(colorspecimensworkers$red)
mean(colorspecimensworkers$red) - sd(colorspecimensworkers$red)
mean(colorspecimensworkers$red) + sd(colorspecimensworkers$red)
mean(colorspecimensworkers$green) + sd(colorspecimensworkers$green)
mean(colorspecimensworkers$green) - sd(colorspecimensworkers$green)
mean(colorspecimensworkers$blue) + sd(colorspecimensworkers$blue)
mean(colorspecimensworkers$blue) - sd(colorspecimensworkers$blue)
length(colorspecimensworkers$blue)

