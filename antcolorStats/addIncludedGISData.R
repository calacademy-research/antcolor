#Add GIS data from included databases to allspecimens dataframe 
#Also adds mean, SD etc. from this data to a frame of color-identified taxa

library(raster)

alllocated <- allspecimens[!(is.na(allspecimens$decimalLatitude)), ]
alllocated$decimalLatitude <- num(alllocated$decimalLatitude)
alllocated$decimalLongitude <- num(alllocated$decimalLongitude)

ralt <- raster('Included_Databases/raster_mad/alt.asc')
rmeantemp <- raster('Included_Databases/raster_mad/bio1.asc')
rsolar <- raster('Included_Databases/raster_mad/solar.asc')
rforestcover <- raster('Included_Databases/raster_mad/percfor2010.asc')
prevcoords <- cbind(0,0)

for(rownum in 1:nrow(alllocated))
{
  if(rownum %% 100 == 0)
  {
    print(rownum)
  }
  row <- alllocated[rownum,]
  lat <- as.numeric(as.character(row[13]))
  lon <- as.numeric(as.character(row[14]))
  coords <- cbind(lon, lat)
  
  #if coords match previous, dont bother spending time extracting
  if(coords[1] != prevcoords[1] || coords[2] != prevcoords[2])
  {
    points <- SpatialPoints(coords, proj4string = r@crs)
    alt <- extract(ralt,points)
    meantemp <- extract(rmeantemp,points)
    solar <- extract(rsolar,points)
    forestcover <- extract(rforestcover,points)
  }
  
  alllocated[rownum,52] <- alt
  alllocated[rownum,53] <- meantemp
  alllocated[rownum,54] <- solar
  alllocated[rownum,55] <- forestcover
  prevcoords <- coords
  print(rownum)
}

View(alllocated)

#lapply is being a bitch so above for now
addGIS <- function(row)
{
  lat <- as.numeric(as.character(row[13]))
  lon <- as.numeric(as.character(row[14]))
  coords <- cbind(lat, lon)
  points <- SpatialPoints(coords, proj4string = r@crs)
  alt <- extract(ralt,points)
  meantemp <- extract(rmeantemp,points)
  solar <- extract(rsolar,points)
  forestcover <- extract(rforestcover,points)
  row[52] <- alt
  row[53] <- meantemp
  row[54] <- solar
  row[55] <- forestcover
}

alllocated <- by(alllocated, 1:nrow(alllocated), addGIS)

library(dplyr)
alllocatedtaxa <- alllocated
alllocatedtaxa <- cbind(alllocatedtaxa[,2],alllocatedtaxa[,52:55])
names(alllocatedtaxa) <- c("antwebTaxonName","altitude","temp","solar","forestcover")
alllocatedtaxa <- alllocatedtaxa[complete.cases(alllocatedtaxa),]
alllocatedtaxa <- group_by(alllocatedtaxa, antwebTaxonName)
#Summarize by taxon
alllocatedtaxa <- summarize(alllocatedtaxa, n(), solar_mean = mean(solar,na.rm = TRUE), solar_SD = sd(solar,na.rm = TRUE), solar_max = max(solar,na.rm = TRUE), solar_min = min(solar,na.rm = TRUE),
                  temp_mean = mean(temp,na.rm = TRUE), temp_SD = sd(temp,na.rm = TRUE), temp_max = max(temp,na.rm = TRUE), temp_min = min(temp,na.rm = TRUE),
                  altitude_mean = mean(altitude,na.rm = TRUE), altitude_SD = sd(altitude,na.rm = TRUE), altitude_max = max(altitude,na.rm = TRUE), altitude_min = min(altitude,na.rm = TRUE),
                  forestcover_mean = mean(forestcover,na.rm = TRUE), forestcover_SD = sd(forestcover,na.rm = TRUE), forestcover_max = max(forestcover,na.rm = TRUE), forestcover_min = min(forestcover,na.rm = TRUE))
nrow(alllocatedtaxa)

#Create color taxa dataframe and merge the two 
colormadagtaxa <- filter(colorspecimens, bioregion == "Malagasy")
colormadagtaxa <- group_by(colormadagtaxa,antwebTaxonName)
colormadagtaxa <- summarize(colormadagtaxa,n(),lightness_mean = mean(lightness,na.rm = TRUE), saturation_mean = mean(saturation,na.rm=TRUE))

colormerged <- merge(alllocatedtaxa,colormadagtaxa,by="antwebTaxonName") 
nrow(colormerged)

cor.test(colormerged$temp_mean,colormerged$altitude_mean)
cor.test(colormerged$solar_mean,colormerged$lightness_mean)
