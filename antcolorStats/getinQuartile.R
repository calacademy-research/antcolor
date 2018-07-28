
#get subset above and below the specified quantile (qval)
toquantile = subset
qval = 0.1
q = quantile(toquantile$meantemp,qval)

underq = toquantile[toquantile$meantemp < q, ] 
overq = toquantile[toquantile$meantemp > q, ] 
View(underq1)
View(overq4)

#mean(overq4$meanlightness)
#mean(underq1$meanlightness)
#overq4$meanlightness = as.numeric(as.character(overq4$meanlightness))
#subset$selightness = as.numeric(as.character(subset$selightness))
#mean(underq1$lightness)
