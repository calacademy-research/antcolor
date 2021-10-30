#kmeans
short <- colorspecimens[c("hue","saturation","lightness")]
View(short)     
# Determine number of clusters
wss <- (nrow(short)-1)*sum(apply(short,2,var))
for (i in 2:15) wss[i] <- sum(kmeans(short,
                                     centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")

km <- kmeans(short,3)
km
