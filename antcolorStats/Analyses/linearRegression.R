#run a linear regression on a prepared dataframe

forlinear = locatedspecimens
View(locatedspecimens)

#CORRELATION
cor(forlinear$lightness, forlinear$rainfall, use = "complete.obs") 

#PLOT: scatter
plot(forlinear$rainfall, forlinear$lightness,log="")

#reg1 <- lm(lightness~solar + genus + caste + subfamily,data=forlinear) 
reg1 <- lm(lightness ~ rainfall,data=forlinear) 
summary(reg1)
abline(reg1)

forlinear = forlinear[!(is.na(forlinear$solar)), ]
forlinear = forlinear[!(is.na(forlinear$solar)), ]
cov(forlinear$solar,forlinear$solar)


