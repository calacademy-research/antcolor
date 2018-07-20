library("dplyr", lib.loc="~/R/win-library/3.5")
library("magrittr", lib.loc="~/R/win-library/3.5")

#get a dataframe of specimens filtered by specific fields and plot variance of specified variable

filtered <- dplyr::filter(colorspecimens, grepl('Aphaenogaster', genus)) #set to desired subset
filtered = dplyr::filter(filtered, grepl('worker', caste)) #set to desired subset
#filtered = dplyr::filter(filtered, grepl('Nearctic', bioregion)) #set to desired subset

filtered = filtered[!(is.na(filtered$lightness)), ] #use find and replace to set to desired variable- currently lightness
View(filtered)
filtered %>% group_by(genus) %>% summarise(sderr(lightness))
filtered %>% summarise(funs(mean(lightness),sd(lightness),se=sd(lightness)/sqrt(n())))
filtered %>% summarize_each(funs(mean,sd,se=sd(.)/sqrt(n())))
filtered %>% summarise_each(funs(mean,sd,se=sd(.)/sqrt(n())))

#plot distribution and IQR of sampled set
par(mfrow=c(1, 2))  # divide graph area in 2 columns
plot(density(filtered$lightness), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(filtered$lightness), 2)))
polygon(density(filtered$lightness), col="red")
boxplot(filtered$lightness, main="", sub=paste("Outlier rows: ", boxplot.stats(filtered$lightness)$out))

filtered2 = filtered
filtered3 = rbind(filtered,filtered2)
chisq.test(filtered$genus,filtered$lightness)
