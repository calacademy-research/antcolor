library("elastic", lib.loc="~/R/win-library/3.5")
library("jsonlite", lib.loc="~/R/win-library/3.5")
library("raster", lib.loc="~/R/win-library/3.5")
library("rgdal", lib.loc="~/R/win-library/3.5")

#Big function to pull AntWeb specimens from Elasticsearch, also adding new GIS data 
#Avg. annual fields added: temp, altitude, solar radiation, rainfall (all WorldClim), UV (glUV), SOON soil type (HWSD)
prepareElasticGISDataframes <- function(index) { 
  
#connect to elasticsearch, pull specimens and convert to a dataframe
connect() # connect to elasticsearch
specimens <- Search(index= index, size = 50000, raw = TRUE) #get specimens from index
specimens = fromJSON(specimens)
specimens = specimens$hits$hits$'_source' #format properly
specimens$geolat = specimens$geo$coordinates$lat
specimens$geolon = specimens$geo$coordinates$lon
specimens = subset(specimens, select = -c(geo))

#filter for specimens with coords and format coords
locatedspecimens = specimens
locatedspecimens = locatedspecimens[!(is.na(locatedspecimens$decimalLatitude) | locatedspecimens$decimalLatitude==""), ]
specimenlats = locatedspecimens$decimalLatitude
specimenlons = locatedspecimens$decimalLongitude
coords = data.frame(x=specimenlons,y=specimenlats)
coords$x = as.numeric(as.character(coords$x))
coords$y = as.numeric(as.character(coords$y))

#pull temp data from WorldClim
r = getData("worldclim",var="bio",res=10) 
r = r[[c(1)]]
#extract temp data
points = SpatialPoints(coords, proj4string = r@crs)
temperature = extract(r,points)

#pull rainfall data from WorldClim
r = getData("worldclim",var="bio",res=10) 
r = r[[c(12)]]
#extract rainfall data
points = SpatialPoints(coords, proj4string = r@crs)
rainfall = extract(r,points)

#pull altitude data from WorldClim
r = getData("worldclim",var="alt",res=10) 
r = r[[c(1)]]
#extract altitude data
points = SpatialPoints(coords, proj4string = r@crs)
altitude = extract(r,points)

#attempt to pull soil data (WIP)

#hwsd <- raster("Included_Databases/hwsd.bil")
#proj4string(hwsd) <- "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"
#soil = hwsd[[c(1)]]
#points = SpatialPoints(coords)
#soiltype = extract(soil,points)
#View(soiltype)

#m <- dbDriver("SQLite")
#con <- dbConnect(m, dbname="HWSD.sqlite")
#dbListTables(con)
#p1 = dbGetQuery(con,'select * from D_SYMBOL' )

locatedspecimens <- cbind.data.frame(locatedspecimens,temperature)
locatedspecimens[56] = (locatedspecimens[56] / 10) #temp / 10
locatedspecimens <- cbind.data.frame(locatedspecimens,rainfall)
locatedspecimens <- cbind.data.frame(locatedspecimens,altitude)

points = SpatialPoints(coords, proj4string = r@crs)

#pull solar radiation data from WorldClim files and avg for year
mean1 = raster("Included_Databases/wc2.0_5m_srad_01.tif") #mean temp for January etc.
mean1 = mean1[[c(1)]]
solar1 = extract(mean1,points)
mean2 = raster("Included_Databases/wc2.0_5m_srad_02.tif") 
mean2 = mean2[[c(1)]]
solar2 = extract(mean2,points)
mean3 = raster("Included_Databases/wc2.0_5m_srad_03.tif") 
mean3 = mean3[[c(1)]]
solar3 = extract(mean3,points)
mean4 = raster("Included_Databases/wc2.0_5m_srad_04.tif") 
mean4 = mean4[[c(1)]]
solar4 = extract(mean4,points)
mean5 = raster("Included_Databases/wc2.0_5m_srad_05.tif") 
mean5 = mean5[[c(1)]]
solar5 = extract(mean5,points)
mean6 = raster("Included_Databases/wc2.0_5m_srad_06.tif") 
mean6 = mean6[[c(1)]]
solar6 = extract(mean6,points)
mean7 = raster("Included_Databases/wc2.0_5m_srad_07.tif") 
mean7 = mean7[[c(1)]]
solar7 = extract(mean7,points)
mean8 = raster("Included_Databases/wc2.0_5m_srad_08.tif") 
mean8 = mean8[[c(1)]]
solar8 = extract(mean8,points)
mean9 = raster("Included_Databases/wc2.0_5m_srad_09.tif") 
mean9 = mean9[[c(1)]]
solar9 = extract(mean9,points)
mean10 = raster("Included_Databases/wc2.0_5m_srad_10.tif") 
mean10 = mean10[[c(1)]]
solar10 = extract(mean10,points)
mean11 = raster("Included_Databases/wc2.0_5m_srad_11.tif") 
mean11 = mean11[[c(1)]]
solar11 = extract(mean11,points)
mean12 = raster("Included_Databases/wc2.0_5m_srad_12.tif") 
mean12 = mean12[[c(1)]]
solar12 = extract(mean12,points)
yearsolar = cbind(solar1,solar2,solar3,solar4,solar5,solar6,solar7,solar8,solar9,solar10,solar11,solar12)
solar <<- rowMeans(yearsolar)

locatedspecimens <- cbind(locatedspecimens,solar)

locatedspecimens$temperature = as.numeric(as.character(locatedspecimens$temperature))
locatedspecimens$solar = as.numeric(as.character(locatedspecimens$solar))
locatedspecimens$rainfall = as.numeric(as.character(locatedspecimens$rainfall))
locatedspecimens$altitude = as.numeric(as.character(locatedspecimens$altitude))

colorspecimens <<- specimens[!(is.na(specimens$lightness)), ]
colorlocated <<- locatedspecimens[!(is.na(locatedspecimens$lightness)), ]

colortempsolar <- colorlocated[!(is.na(colorlocated$temperature)), ]
colortempsolar <<- colortempsolar[!(is.na(colortempsolar$solar)), ]

colortempsolar$temperature = as.numeric(as.character(colortempsolar$temperature))
colortempsolar$solar = as.numeric(as.character(colortempsolar$solar))
colortempsolar$rainfall = as.numeric(as.character(colortempsolar$rainfall))
colortempsolar$altitude = as.numeric(as.character(colortempsolar$altitude))
}
