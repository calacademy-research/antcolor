
# PCA with function prcomp

df <- dplyr::select_if(colorlocated, is.numeric)
df= df[complete.cases(df), ]

pca1 = prcomp(df, scale. = TRUE)

# sqrt of eigenvalues
pca1$sdev

# loadings
head(pca1$rotation)

# PCs (aka scores)
head(pca1$x)

summary(pca1)
