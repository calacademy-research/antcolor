

colorspecimensponerines <- dplyr::filter(colorspecimens, grepl('Ponerinae', subfamily)) #set to desired field and value
mean(colorspecimensponerines$lightness)
mean(colorspecimensponerines$pixSD, na.rm =  TRUE)
mean(colorspecimensponerines$pixUsed, na.rm = TRUE)

colorspecimensformicines <- dplyr::filter(colorspecimens, grepl('Formicinae', subfamily)) #set to desired field and value
mean(colorspecimensformicines$lightness)
mean(colorspecimensformicines$pixSD, na.rm =  TRUE)
mean(colorspecimensformicines$pixUsed, na.rm = TRUE)

colorspecimensformicines <- dplyr::filter(colorspecimens, grepl('Formicinae', subfamily)) #set to desired field and value
mean(colorspecimensformicines$lightness)
mean(colorspecimensformicines$pixSD, na.rm =  TRUE)
mean(colorspecimensformicines$pixUsed, na.rm = TRUE)

source("Helpers/prepareSubsetDataframe.R")
colorspecimensworkersgenera <- prepareSubsetDataframe(df= colorspecimensworkers,subsetBy= 'genus',threshold = 3)

View(colorspecimensworkersgenera)
mean(colorspecimensworkersgenera$meanpixUsed, na.rm= TRUE)

colorspecimensworkersgeneramin5 <- prepareSubsetDataframe(df= colorspecimensworkers,subsetBy= 'genus',threshold = 5)
View(colorspecimensworkersgeneramin5)

### GET QUANTILE
#Get rows below or above the quantile
source("Helpers/getQuantile.R")
generapixSDpercentile10 = getQuantile(df = colorspecimensworkersgeneramin5, column= colorspecimensworkersgeneramin5$meanpixSD, qval= 0.9, under= FALSE)
View(generapixSDpercentile10)

mean(generapixSDpercentile10$meanlightness, na.rm = TRUE)
mean(generapixSDpercentile90$meanlightness, na.rm = TRUE)

#pixused
generapixUsedpercentile10 = getQuantile(df = colorspecimensworkersgeneramin5, column= colorspecimensworkersgeneramin5$meanpixUsed, qval= 0.9, under= FALSE)
View(generapixUsedpercentile10)

mean(generapixSDpercentile10$meanlightness, na.rm = TRUE)
mean(generapixSDpercentile90$meanlightness, na.rm = TRUE)
