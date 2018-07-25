
#get 1st and 4th quartile from dataframe
toquantile = subset

q1 = quantile(toquantile$meantemp,0.25)
q4 = quantile(toquantile$meantemp,0.75)

underq1 = toquantile[toquantile$meantemp < q1, ] 
overq4 = toquantile[toquantile$meantemp > q4, ] 
View(underq1)
View(overq4)

mean(overq4$meanlightness)
mean(underq1$meanlightness)
overq4$meanlightness = as.numeric(as.character(overq4$meanlightness))
subset$selightness = as.numeric(as.character(subset$selightness))
mean(underq1$lightness)
