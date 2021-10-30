library(raster)
library(rgdal)

#Generate color gradient raster to be visualized in QGIS

#Make shape file of spatial information
colorspecimens4gradient <- colorlocated
coordinates(colorspecimens4gradient) <- cbind(colorspecimens4gradient$decimalLongitude, colorspecimens4gradient$decimalLatitude)


#plot(colorspecimens4gradient)
#colorspecimens4gradient
projection(colorspecimens4gradient) <- "+init=EPSG:4326"

#View EPSG info
EPSG <- make_EPSG()
EPSG$prj4

#Make raster
#Resolution is cell size (lat/long degrees) 
gradientraster <- raster(colorspecimens4gradient, resolution = 0.833)#0.00833
gradientraster <- rasterize(colorspecimens4gradient, gradientraster, field = colorspecimens4gradient@data$lightness)

#make a shape file bounding box
(-124.848974, 24.396308) - (-66.885444, 49.384358)
bb <- as(extent(42.95,51.02, -25.76,-11.82),'SpatialPolygons')
crs(bb) <- CRS("+init=EPSG:4326")

gradientraster <- crop(gradientraster,bb)
##for pixel in raster
##  find all specimens within X units 
##  calculate mean color of specimens (possibly scaling inversely with distance) 
##  set pixel color to mean color of specimens 
plot(gradientraster)
