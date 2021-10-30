#madag night

colorspecimensNightMadag <- dplyr::filter(colorspecimensworkers, grepl('night', microhabitat,fixed = TRUE)) #set to desired field and value
colorspecimensNightMadag <- dplyr::filter(colorspecimensNightMadag, grepl('Malagasy', bioregion))


#bounding box
#43.67, -23.67 ### 45.54, -23.67
#43.67, -25.60 ### 45.54  -25.60
#81 : lat, 82: lon
latmin <- -25.60
latmax <- -25.52
lonmin <- 45.09
lonmax <- 45.28
colorlocatedbb <- colorlocated[(colorlocated[,82] > lonmin),]
colorlocatedbb <- colorlocatedbb[(colorlocatedbb[,82] < lonmax),]
colorlocatedbb <- colorlocatedbb[(colorlocatedbb[,81] < latmin ),]
colorlocatedbb <- colorlocatedbb[(colorlocatedbb[,81] > latmax),]
nrow(colorlocatedbb)
View(colorlocatedbb)
mean(colorlocatedbb$lightness)
sd(colorlocatedbb$lightness)

mean(colorlocatedbb$saturation)
sd(colorlocatedbb$saturation)
boxplot(colorlocatedbb$lightness)
boxplot(colorspecimensMadag$lightness)
cbind(colorlocatedbb$caste,colorlocatedbb$lightness, colorlocatedbb$microhabitat,colorlocatedbb$antwebTaxonName)

colorlocatedbbStone <- dplyr::filter(colorlocatedbb, grepl('under stone', microhabitat))
colorlocatedbbGround <- dplyr::filter(colorlocatedbb, grepl('ground', microhabitat))
mean(colorlocatedbbStone$lightness)
mean(colorlocatedbbGround$lightness)

#under stone - very light Royidris
#ground foragers - very dark 
colorlocated$abslat <- sapply(colorlocated$abslat, abs)
colorlocated$abslat <- colorlocated$geolat
colorlocated$abslat <- as.numeric(colorlocated$abslat)
colorlocated$abslat <- abs(colorlocated$abslat)
colorlocatedClade <- dplyr::filter(colorlocated, grepl('Crematogaster', genus))
cor.test(colorlocatedClade$altitude, colorlocatedClade$lightness)

source("Helpers/casteCladeThreshold.R")
castetaxathreshed1 <- casteCladeThreshold('antwebTaxonName', 1, 1)
cor.test(castegenusthreshed1$propmaletoworker, castegenusthreshed1$meanaltitude.x)
cor.test(castegenusthreshed1$propmaletoworker, castegenusthreshed1$meanlat.x)

castegenusthreshed1 <- casteCladeThreshold('genus', 1, 2)
cor.test(castegenusthreshed1$propmaletoworker, castegenusthreshed1$meanaltitude.x)
cor.test(castegenusthreshed1$propmaletoworker, castegenusthreshed1$meanlat.x)

#testing
df <- dplyr::filter(colorlocated, grepl('Malagasy', bioregion))
nrow(df)
