

connect() # connect to elasticsearch
jsonspecimens = Search(index= "allants2", size = 50000, raw = TRUE) #get specimens from index
specimens <- fromJSON(jsonspecimens)
specimens = specimens$hits$hits$'_source' #format
View(specimens)

print(summary(specimens))
View(summary(specimens))

#filter for specimens with coords and format coords
locatedspecimens = specimens
locatedspecimens = locatedspecimens[!(is.na(locatedspecimens$decimalLatitude) | locatedspecimens$decimalLatitude==""), ]
View(locatedspecimens)
specimenlats = locatedspecimens$decimalLatitude
specimenlons = locatedspecimens$decimalLongitude
coords <- data.frame(x=specimenlons,y=specimenlats)
coords$x = as.numeric(as.character(coords$x))
coords$y = as.numeric(as.character(coords$y))
View(coords)

#pull data from WorldClim
r <- getData("worldclim",var="bio",res=10) 
r <- r[[c(1)]]
names(r) <- c("Temp")

#extract data
points <- SpatialPoints(coords, proj4string = r@crs)
values <- extract(r,points)
df <- cbind.data.frame(coordinates(points),values)
View(df)

#get lightness from locatedspecimens
locatedspecimens$lightness
