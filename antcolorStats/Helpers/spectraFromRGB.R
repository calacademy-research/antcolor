#Estimate spectra from RGB using LLSS and add to dataframes

#Export specimens csv
write.csv(cbind(colorspecimens$specimenCode, as.numeric(colorspecimens$red),as.numeric(colorspecimens$green), as.numeric(colorspecimens$blue)),'data.txt')
nrow(colorspecimens)

#Run each R,G,B value through Octave pipeline and add resulting spectral bands vector to new csv 
#Grab new csv in R
spectrawooo <- read.csv('RGBspectra.csv')
spectrawooo <- spectrawooo[,4:39]
colnames(spectrawooo) <- c(1:36)

for(i in 1:100)
{
  print(i)
  print(sum(spectrawooo[i,30:36]))
}


sum(spectrawooo[i,])

View(sum(spectrawooo[,]))
for(i in 1:100)
{
  spectrawooo[i,37] = sum(spectrawooo[i,])
}
View(spectrawooo)


### Run PCA ON WAVELENGTH BANDS

pca <- prcomp(spectrawooo, center = TRUE, scale = TRUE, rank = 3)

# sqrt of eigenvalues
pca$sdev

# loadings
pca$rotation
write.csv(pca$rotation,'newdata.csv')

# PCs (aka scores)
summary(pca)

plot(pca)

### CLUSTER SPECTRA

#Hierachical clustering
dist_mat <- dist(spectrawooo, method = 'euclidean')
hclust_avg <- hclust(dist_mat, method = 'average')
cut_avg <- cutree(hclust_avg, k = 3)
spectrawooo <- cbind(spectrawooo,cut_avg)

clust <- dplyr::filter(spectrawooo, grepl(3, cut_avg)) #no fossils, for example
nrow(clust)
View(colMeans(clust))

#K-means
km <- kmeans(spectrawooo[,1:36], 5)
spectrawooo <- cbind(spectrawooo,km$cluster)

clust <- dplyr::filter(spectrawooo, grepl(5,km$cluster)) #no fossils, for example
nrow(clust)
View(colMeans(clust))

#model-based clustering
install.packages('mclust')
install.packages('factoextra')
library(factoextra)
df <- scale(spectrawooo[,1:36]) # Standardize the data
library(mclust)
mc <- Mclust(df)
summary(mc)
