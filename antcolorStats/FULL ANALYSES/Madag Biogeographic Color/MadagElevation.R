#Looking at color diversity correlations for Madagascar within a genus or species

colorspecimensCladeMadag <- dplyr::filter(colorspecimensworkers, grepl('Tetramorium', genus)) #set to desired field and value
colorspecimensCladeMadag <- dplyr::filter(colorspecimensworkers, grepl('Malagasy', bioregion))
#colorspecimensCladeMadag <- dplyr::filter(colorspecimensCladeMadag, grepl(TRUE, isArboreal))

#colorspecimensCladeMadagtaxa <- colorspecimensCladeMadag
source("Helpers/prepareSubsetDataframe.R")
source("Helpers/oldSubset.R")
colorspecimensCladeMadagtaxa <- prepareSubsetDataframe(df= colorspecimensCladeMadag,subsetBy= 'antwebTaxonName', threshold = 1)

#colorspecimensCamponotusMadagvalidtaxa <- dplyr::filter(colorspecimensCamponotusMadagtaxa, grepl('numvalidtaxa', 1))
#cor.test(colorspecimensCladeMadagtaxa$lightness,colorspecimensCladeMadagtaxa$minimumElevationInMeters, use = "complete.obs") 
#cor.test(colorspecimensCladeMadagtaxa$meansaturation,colorspecimensCladeMadagtaxa$meanaltitude, use = "complete.obs") 

cor.test(colorspecimensCladeMadagtaxa$meanlightness,colorspecimensCladeMadagtaxa$meanaltitude, use = "complete.obs") 
cor.test(colorspecimensCladeMadagtaxa$meansaturation,colorspecimensCladeMadagtaxa$meanaltitude, use = "complete.obs") 

altplus <- 1850
altminusgreater <- 0
colorspecimensCladeMadagtaxaEplus <- colorspecimensCladeMadagtaxa[colorspecimensCladeMadagtaxa$meanaltitude >= altplus,]
colorspecimensCladeMadagtaxaEminus <- colorspecimensCladeMadagtaxa[colorspecimensCladeMadagtaxa$meanaltitude < altplus,]
colorspecimensCladeMadagtaxaEminus <- colorspecimensCladeMadagtaxaEminus[colorspecimensCladeMadagtaxaEminus$meanaltitude > altminusgreater,]

nrow(colorspecimensCladeMadagtaxaEplus)
nrow(colorspecimensCladeMadagtaxaEminus)

mean(colorspecimensCladeMadagtaxaEplus$meanlightness,na.rm = TRUE)
mean(colorspecimensCladeMadagtaxaEminus$meanlightness,na.rm = TRUE)

nrow(colorspecimensCladeMadagtaxa)
mean(colorspecimensCladeMadagtaxa$meanlightness)

View(colorspecimensCladeMadagtaxaEplus)

#Results
#Tetramorium: -0.19 significant correlation of lightness with alt
#Species above 1850: 1, L = 0.316
#Species below 1850: 1, L = 0.377
#Pheidole - no correlation
#Camponotus - no correlation
#Species above 1850: 6, L = 0.378
#Species below 1850: 168, L = 0.384
#Crematogaster: -0.3 correlation 
#Species above 1850: 1, L = 0.27
#Species below 1850: 42, L = 0.35
#Think we're gonna need to look at phylogenies to determine to what extent relatedness is effecting color here

cor.test(colorspecimensCladeMadag$lightness,colorspecimensCladeMadag$minimumElevationInMeters, use = "complete.obs") 

#intraspecific variation in camponotus vs crematogaster

colorspecimensCladeMadag <- dplyr::filter(colorspecimensworkers, grepl('Camponotus', genus)) #set to desired field and value
colorspecimensCladeMadag <- dplyr::filter(colorspecimensCladeMadag, grepl('Malagasy', bioregion))

source("Helpers/prepareSubsetDataframe.R")
source("Helpers/oldSubset.R")
colorspecimensCladeMadagtaxa <- prepareSubsetDataframe(df= colorspecimensCladeMadag,subsetBy= 'antwebTaxonName', threshold = 1)
mean(colorspecimensCladeMadagtaxa$sdlightness, na.rm = TRUE)
cor.test(castegenusthreshed1$meanlightness.x, castegenusthreshed1$sdlightness.x)
