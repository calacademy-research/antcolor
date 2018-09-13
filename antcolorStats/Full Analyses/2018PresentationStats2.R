#Some stats run for the Summer 2018 presentation version of project
# presented at the California Academy of Sciences

#Refresh all variables
rm(list=ls()) 

#Prepare new dataframes from each set
source("prepareSpecimenDataframes.R")
prepareSpecimenDataframes('allants')

locatedspecimens1 <- locatedspecimens
colorlocated1 <- colorlocated
colorspecimens1 <- colorspecimens
colortempsolar1 <- colortempsolar

View(colorspecimens1)
View(colorspecimens2)

source("prepareSpecimenDataframes.R")
prepareSpecimenDataframes('allants6')

locatedspecimens2 <- locatedspecimens
colorlocated2 <- colorlocated
colorspecimens2 <- colorspecimens
colortempsolar2 <- colortempsolar

remove(locatedspecimens)
remove(colorlocated)
remove(colorspecimens)
remove(colortempsolar)

#Filter for value in field
colorlocated1 <- dplyr::filter(colorlocated1, grepl(FALSE, fossil)) #set to desired field and value
colorlocated1workers <- dplyr::filter(colorlocated1, grepl('worker', caste)) #set to desired field and value

colorlocated2 <- dplyr::filter(colorlocated2, grepl(FALSE, fossil)) #set to desired field and value
colorlocated2workers <- dplyr::filter(colorlocated2, grepl('worker', caste)) #set to desired field and value

colorspecimens1 <- dplyr::filter(colorspecimens1, grepl(FALSE, fossil)) #set to desired field and value
colorspecimens1workers <- dplyr::filter(colorspecimens1, grepl('worker', caste)) #set to desired field and value

colorspecimens2 <- dplyr::filter(colorspecimens2, grepl(FALSE, fossil)) #set to desired field and value
colorspecimens2workers <- dplyr::filter(colorspecimens2, grepl('worker', caste)) #set to desired field and value

colorlocated2 <- dplyr::filter(colorlocated2, grepl(FALSE, fossil)) #set to desired field and value
colorlocated2workers <- dplyr::filter(colorlocated2, grepl('worker', caste)) #set to desired field and value

#Prep workers by genus subset
source("prepareSubsetDataframe.R")
colorspecimens1workersgenera <- prepareSubsetDataframe(df= colorspecimens1workers,subsetBy= 'genus')
View(colorspecimens1workersgenera)
View(colorspecimens1caste)

colorspecimens1workersgenera$meanbrownblackness = as.numeric(as.character(colorspecimens1workersgenera$meanbrownblackness))
#mean(colorspecimens2workers$brownnessHSV, na.rm=TRUE)

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

#Run some regressions
forlinear = colorspecimens1workersgenera
reg1 <- lm(sdlightness ~ sdtemp,data=forlinear) 
summary(reg1)
abline(reg1)

#Run some LMMs

#Run some PCAs 