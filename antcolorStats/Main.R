library("elastic", lib.loc="~/R/win-library/3.5")
library("jsonlite", lib.loc="~/R/win-library/3.5")
library("raster", lib.loc="~/R/win-library/3.5")
library("rgdal", lib.loc="~/R/win-library/3.5")
library("dplyr", lib.loc="~/R/win-library/3.5")

#A playground of ant data! Run other functions from here to handle data. 

source("prepareSpecimenDataframes.R")
prepareSpecimenDataframes('allants6')
df <- dplyr::filter(df, grepl('Madagascar', country)) #set to desired field and value
df = colorlocated
plot(df$solar, df$lightness,log="")
reg <- lm(lightness ~ temperature + solar,data=colorlocated) 
summary(reg)
abline(reg)

mean(over$lightness)
mean(over$red)
mean(over$green)
mean(over$blue)

t.test(under$lightness,over$lightness)
### PREPARE DATAFRAMES FROM ELASTIC
#specimens has all specimens
#colorspecimens has all with colors
#locatedspecimens has all with geolocations
#colorlocated has all with colors and geolocations
source("prepareSpecimenDataframes.R")
  df = prepareSpecimenDataframes('allants6')
  View(colorlocated)

### FILTER A DATAFRAME
#Get a dataframe filtered for a value 
#source("filterSpecimens.R")
#df <- filterSpecimens(df= colorspecimens, field= 'genus', value= 'Pheidole')
#View(df)
  df <- dplyr::filter(df, grepl('worker', caste)) #set to desired field and value

### PREPARE SUBSET DATAFRAMES
#Subset a dataframe, averaging values at the given level ie. species or genus
  source("prepareSubsetDataframe.R")
  df <- prepareSubsetDataframe(df= colorspecimens,subsetBy= 'caste')
  View(df)

### REMOVE IQR OUTLIERS
#Removes outliers by IQR
  source("removeIQRoutliers.R")
  df <- colorspecimens
  df <- removeIQRoutliers(df, 'lightness')

  df$lightness = scale(df$lightness)

### REMOVE IQR OUTLIERS BY GENUS
#Removes IQR outliers by genus
  source("outliersbyGenus.R")
  df <- outliersbyGenus(df= colorspecimens, field= 'lightness')
  View(df)
  
### SCALE & RANGE
#Scale and range the given column from 0-1 
  source("scale&Range.R")
  View(scaleRange(column = colorlocated$solar))

  
### REMOVE WHERE EQUALS
#Remove rows which match the column value
  source("removeWhereEquals.R") 
  removeWhereEquals(column = colorspecimens$fossil, value = TRUE)
  
### GET QUANTILE
#Get rows below or above the quantile
  source("getQuantile.R")
  over = getQuantile(column= df$temperature, qval= 0.9, under= FALSE)
  View(over)
  
### GET MEAN
  mean(df$lightness) 
  
### WRITE TO EXCEL
#Write a dataframe to an Excel file
  source("write2Excel.R")
  write2Excel(df= subset, path = "C:/Users/OWNER/Desktop/data.xlsx") 
  
### RUN A LINEAR/MULTIPLE REGRESSION
  
### RUN A CHI2 TEST
chisq.test(filtered$genus,filtered$lightness)
  
  