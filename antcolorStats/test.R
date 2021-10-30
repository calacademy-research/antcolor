library(dplyr)
temp <- colorspecimens
temp <- temp %>%
  group_by(scientificName) %>%
  summarise(n = n())
temp
hist(temp$n,xlim = c(0,50),ylim = c(0,500))
count(temp$n == 1)
dim(dplyr::filter(temp, n == 4))

View(allspecimens)
View(colorspecimens)
plot(colorspecimens$locatedAt)
