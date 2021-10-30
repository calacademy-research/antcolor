#Adds PCs1-3 to colorspecimens or colorspecimensworkers

# PCA with function prcomp
df <- colorspecimensworkers
df <- data.frame(df$lightness,df$saturation,df$hue)

#df <- data.frame(df$rednessHSV,df$orangenessHSV,df$yellownessHSV,df$brownnessHSV,df$darkbrownnessHSV,df$brownblacknessHSV)

pca <- prcomp(df, center = TRUE, scale = TRUE, rank = 3)

#Summary
summary(pca)

#Sqrt of eigenvalues
pca$sdev

#Loadings
head(pca$rotation)

# PCs (aka scores)
head(pca$x)

pca$x[,1]

#Recall that this is based on workers only for now 
colorspecimensworkers$PC1 <- pca$x[,1]
colorspecimensworkers$PC2 <- pca$x[,2]
colorspecimensworkers$PC3 <- pca$x[,3]
