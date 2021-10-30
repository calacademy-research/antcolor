#Some stats run for the presentation version of project
## that was presented at the California Academy of Sciences on August 9th, 2018

#Refresh all variables if starting fresh
rm(list=ls()) 

#Prepare new dataframes from each set
source("prepareElasticGISDataframes.R")
prepareElasticGISDataframes('allantshsv') #name of dataset in Elastic

locatedspecimens = cbind(locatedspecimens, solar) #Workaround for solar bug 


locatedspecimens1 <- locatedspecimens
colorlocated1 <- colorlocated
colorspecimens1 <- colorspecimens
colortempsolar1 <- colortempsolar

remove(locatedspecimens)
remove(colorlocated)
remove(colorspecimens)
remove(colortempsolar)

#Filter for value in field
colorlocated1 <- dplyr::filter(colorlocated1, grepl(FALSE, fossil)) #set to desired field and value
colorlocated1workers <- dplyr::filter(colorlocated1, grepl('worker', caste)) #set to desired field and value
colorlocated1males <- dplyr::filter(colorlocated1, grepl('male', caste)) #set to desired field and value

colorspecimens1 <- dplyr::filter(colorspecimens1, grepl(FALSE, fossil)) #set to desired field and value
colorspecimens1workers <- dplyr::filter(colorspecimens1, grepl('worker', caste)) #set to desired field and value


#Set to numeric
source("Helpers/makeNumeric.R")
makeNumeric(colorlocated1$solar)
makeNumeric(colorlocated$temperature)
makeNumeric(colorlocated$altitude)
colorlocatedtempsolar = colorlocated[complete.cases(colorlocated$temperature), ]
colorlocatedtempsolar = colorlocatedtempsolar[complete.cases(colorlocatedtempsolar$solar), ]

#Prep workers by genus subset
source("prepareSubsetDataframe.R")
colorspecimens1workersgenera <- prepareSubsetDataframe(df= colorspecimens1workers,subsetBy= 'genus')
View(colorspecimens1workersgenera)
View(colorspecimens1caste)

colorspecimens1workersgenera$meanbrownblackness = as.numeric(as.character(colorspecimens1workersgenera$meanbrownblackness))
#mean(colorspecimens2workers$brownnessHSV, na.rm=TRUE)

#Prep located males by genus subset
source("Helpers/prepareSubsetDataframe.R")
colorlocated1malesgenera <- prepareSubsetDataframe(df= colorlocated1males,subsetBy= 'genus')
View(colorlocated1malesgenera)

#Prep located workers by genus subset
source("prepareSubsetDataframe.R")
colorlocated1workersgenera <- prepareSubsetDataframe(df= colorlocated1workers,subsetBy= 'genus')
View(colorlocated1workersgenera)

#Prep located by genus subset
source("prepareSubsetDataframe.R")
colorlocated1genera <- prepareSubsetDataframe(df= colorlocated1,subsetBy= 'genus',threshold = 10)
View(colorlocated1genera)

#Prep microhabitat subset
source("prepareSubsetDataframe.R")
colorspecimens1microhab <- prepareSubsetDataframe(df= colorspecimens1,subsetBy= 'microhabitatInferred')
View(colorspecimens1workersmicrohab)

#Write files to Excel for plotting
source("write2Excel.R")
write2Excel(df= colorspecimens1microhab, path = "C:/Users/OWNER/Desktop/data.xlsx") 

colorspecimens1cara <- dplyr::filter(colorspecimens1, grepl('Carebara', genus)) #set to desired field and value

#Get some means and SDs
sd(colorspecimens1$red)
mean(colorspecimens1$red)
sd(colorspecimens1$green)
mean(colorspecimens1$green)
sd(colorspecimens1$blue)
mean(colorspecimens1$blue)
mean(colorspecimens1$purplenessHSV, na.rm = TRUE)

#Regression of lightness to temperature for all castes
forlinear = colorlocated1
#forlinear$brownness = scale(forlinear$brownness)
#forlinear$temperature = scale(forlinear$temperature)
plot(forlinear$solar, forlinear$lightness,log="")
reg1 <- lm(lightness ~ solar,data=forlinear) 
summary(reg1)
abline(reg1)

#Regression of lightness to temperature for males only
forlinear = colorlocated1males
plot(forlinear$solar, forlinear$lightness,log="")
reg1 <- lm(lightness ~ solar,data=forlinear) 
summary(reg1)
abline(reg1)

#Regressions of genus climate variance vs. lightness/pigmentation variance

#Prep located workers by genus subset
source("Helpers/prepareSubsetDataframe.R")
colorlocated1workersgenera <- prepareSubsetDataframe(df= colorlocated1workers,subsetBy= 'genus',threshold = 25)

forlinear = colorlocated1genera

forlinear$sdtemp = as.numeric(as.character(forlinear$sdtemp))
forlinear$sdsolar = as.numeric(as.character(forlinear$sdsolar))
forlinear$sdlightness = as.numeric(as.character(forlinear$sdlightness))
plot(forlinear$sdtemp, forlinear$sdlightness,log="")
reg <- lm(sdlightness ~ sdtemp,data=forlinear) 
summary(reg)
abline(reg)

plot(df$sdtemp, df$sdlightness,log="")
reg <- lm(sdlightness ~ sdtemp,data=forlinear) 
summary(reg)
abline(reg)

plot(df$sdsolar, df$sdbrownness,log="")
reg <- lm(sdbrownness ~ sdsolar,data=forlinear) 
summary(reg)
abline(reg)

forlinear = colorlocated1workersgenera
forlinear$sdtemp = as.numeric(as.character(forlinear$sdtemp))
forlinear$sdbrownness = as.numeric(as.character(forlinear$sdbrownness))
plot(forlinear$sdtemp, forlinear$sdbrownness,log="")
reg <- lm(sdbrownness ~ sdtemp,data=forlinear) 
summary(reg)
abline(reg)

forlinear = colorlocated1workersgenera
forlinear$meantemp = as.numeric(as.character(forlinear$meantemp))
forlinear$meanlightness = as.numeric(as.character(forlinear$meanlightness))
plot(forlinear$meantemp, forlinear$meanlightness,log="")
reg <- lm(meanlightness ~ meantemp,data=forlinear) 
summary(reg)
abline(reg)

forlinear = colorlocated1malesgenera
forlinear$meantemp = as.numeric(as.character(forlinear$meantemp))
forlinear$meanlightness = as.numeric(as.character(forlinear$meanlightness))
plot(forlinear$meantemp, forlinear$meanlightness,log="")
reg <- lm(meanlightness ~ meantemp,data=forlinear) 
summary(reg)
abline(reg)

forlinear = colorlocated1genera
forlinear$meantemp = as.numeric(as.character(forlinear$meantemp))
forlinear$meanlightness = as.numeric(as.character(forlinear$meanlightness))
plot(forlinear$meantemp, forlinear$meanlightness,log="")
reg <- lm(meanlightness ~ meantemp,data=forlinear) 
summary(reg)
abline(reg)

forlinear = colorlocated1workersgenera
forlinear$sdsolar = as.numeric(as.character(forlinear$sdsolar))
forlinear$sdlightness = as.numeric(as.character(forlinear$sdlightness))
forlinear$sdtemp = as.numeric(as.character(forlinear$sdtemp))
plot(forlinear$sdsolar, forlinear$sdlightness,log="")
reg <- lm(sdbrownness ~ sdtemp,data=forlinear) 
summary(reg)
abline(reg)

#Run some LMMs

#Run some PCAs 

#Genus level comparisons
colorlocated1cremat <- dplyr::filter(colorlocated1, grepl('Crematogaster', genus)) #set to desired field and value
colorlocated1tetraMG <- dplyr::filter(colorlocated1tetra, grepl('Malagasy', bioregion)) #set to desired field and value

forlinear = colorlocated1cremat
#forlinear$sdsolar = as.numeric(as.character(forlinear$sdsolar))
#forlinear$sdlightness = as.numeric(as.character(forlinear$sdlightness))
#forlinear$sdtemp = as.numeric(as.character(forlinear$sdtemp))
plot(forlinear$solar, forlinear$lightness,log="")
reg <- lm(lightness ~ solar,data=forlinear) 
summary(reg)
abline(reg)

plot(forlinear$temperature, forlinear$lightness,log="")
reg <- lm(lightness ~ temperature,data=forlinear) 
summary(reg)
abline(reg)