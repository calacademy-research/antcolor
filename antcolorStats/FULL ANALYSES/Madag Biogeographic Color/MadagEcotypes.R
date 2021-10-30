library(rgdal)
library(raster)

#Creates pts, a dataframe of all specimens that lie within the ecotypes with the ecotypes assigned 
pts <- data.frame(colorlocatedworkers$decimalLongitude, colorlocatedworkers$decimalLatitude,colorlocatedworkers$lightness,colorlocatedworkers$genus,colorlocatedworkers$scientificName, colorlocatedworkers$minimumElevationInMeters,
                  colorlocatedworkers$isArboreal)
names(pts) <- c('x','y','lightness','genus','species','altitude')

ecos <- shapefile('S:/QGIS_stuff/QGIS_workshop/QGIS_files/vector/Madagascar/wwf_mad.shp')
plot(ecos)
e <- extract(ecos, pts[, c('x', 'y')])
pts$ecotype <-e$ECO_NAME
pts <- pts[complete.cases(pts),]


#Filter however you want, or not at all 
df <- dplyr::filter(df, grepl('Camponotus', genus))
mean(df$lightness)
sd(df$lightness)
nrow(df)

df <- dplyr::filter(pts, grepl('Madagascar spiny thickets', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar dry deciduous forests', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar lowland forests', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar succulent woodlands', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar subhumid forests', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar ericoid thickets', ecotype))

df <- dplyr::filter(pts, grepl('Madagascar mangroves', ecotype))

#Check lightness vs. altitude in a filtered ecotype
cor.test(df$lightness, df$altitude, use = "complete.obs")
anova <- aov(lightness ~ altitude, data=pts)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

#Subset species after filtering for ecotype
library(dplyr)
colnames(pts)[7] = "test"; #Temp bugfix
ecotypeSpecies <- group_by(df, species) %>% summarize(lightness = mean(lightness))
mean(ecotypeSpecies$lightness)
summary(ecotypeSpecies)
