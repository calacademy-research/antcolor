library("dplyr", lib.loc="~/R/win-library/3.5")
library("magrittr", lib.loc="~/R/win-library/3.5")

#get a dataframe of specimens filtered by specific fields

filterSpecimens <- function(df, field, value){

df = colorspecimens
value = 'Pheidole'
field= 'genus'
typeof(field)

col = df[ , colnames(df) == field]
filtered = df[!(is.na(col)), ]
filtered = dplyr::filter(df, grepl(value, eval(parse(text= field)))) #filter by value at field
View(filtered)
filtered <- dplyr::filter(colorlocated, grepl('Formica', genus)) #set to desired subset
#filtered = dplyr::filter(filtered, grepl('Nearctic', bioregion)) #set to desired subset

return(filtered)

#filtered = filtered[!(is.na(filtered$lightness)), ] 
#View(filtered)

#filtered %>% group_by(genus) %>% summarise(sderr(lightness))
#filtered %>% summarise(funs(mean(lightness),sd(lightness),se=sd(lightness)/sqrt(n())))
#filtered %>% summarize_each(funs(mean,sd,se=sd(.)/sqrt(n())))
#filtered %>% summarise_each(funs(mean,sd,se=sd(.)/sqrt(n())))
scaled <- scale(colorlocated6$brownnessHSV)
scaled$brownnessHSV = scale(colorlocated6$brownnessHSV)
colorlocated6 = colorlocated6[!(is.na(colorlocated6$brownnessHSV)), ] 
#plot distribution and IQR of sampled set
par(mfrow=c(1, 2))  # divide graph area in 2 columns
plot(density(colorlocated6$brownnessHSV), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(colorlocated6$brownnessHSV), 2)))
polygon(density(colorlocated6$brownnessHSV), col="red")
boxplot(colorlocated6$brownnessHSV, main="", sub=paste("Outlier rows: ", boxplot.stats(colorlocated6$brownnessHSV)$out))

#plot distribution and IQR of sampled set
par(mfrow=c(1, 2))  # divide graph area in 2 columns
scaled$brownnessHSV = as.numeric(as.character(scaled$brownnessHSV))
plot(density(scaled), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(scaled), 2)))
plot(density(colorlocated6$brownnessHSV), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(colorlocated6$brownnessHSV), 2)))
polygon(density(scaled$brownnessHSV), col="red")
boxplot(scaled$brownnessHSV, main="", sub=paste("Outlier rows: ", boxplot.stats(scaled$brownnessHSV)$out))
}