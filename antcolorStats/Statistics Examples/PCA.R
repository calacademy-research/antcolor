
# PCA with function prcomp
df <- dplyr::select_if(colorspecimensmales, is.numeric)
df <- df[complete.cases(df),]
lightness <- df$lightness
df <- colorspecimensmales
df <- data.frame(df$lightness,df$saturation,df$hue)
#df <- data.frame(df$rednessHSV,df$orangenessHSV,df$yellownessHSV,df$brownnessHSV,df$darkbrownnessHSV,df$brownblacknessHSV)
#df$rednessHSV, df$orangenessHSV,df$brownnessHSV,df$darkbrownnessHSV)
#df <- data.frame(df$temperature,df$altitude,df$solar,df$rainfall)

pca <- prcomp(df, center = TRUE, scale = TRUE, rank = 3)

# sqrt of eigenvalues
pca$sdev

# loadings
library(xtable)
xtable(head(pca$rotation))
head(pca$rotation)
# PCs (aka scores)
head(pca$x)

xtable(summary(pca))
summary(pca)
pca$rotation
plot(pca1)

library(ggfortify)

autoplot(pca[1:100])
pca1$x
pca$x
pc1 <- pca$x[,1] # 1st component

View(pc1)
df <- cbind(colorspecimens, pc1)
df <- dplyr::filter(df, grepl('worker', caste))
mean(df$pc1)
anov <- aov(pc1 ~ caste, data = df)

summary(anov)
length(pc1)
length(lightness)
forlin <- cbind(lightness, pc1)
forlin <- as.data.frame.table(forlin)
reg1 <- lm(lightness ~ pc1,data=forlin) 
summary(reg1)

length(pca$rotation)
summary(pca1)

#Add pc1 to colorspecimens
colorspecimensmales$PC1 <- pc1

