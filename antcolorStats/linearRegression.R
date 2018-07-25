#run a linear regression on a prepared dataframe

forlinear = locatedspecimens

#CORRELATION
cor(forlinear$solar, forlinear$temperature, use = "complete.obs") 

#PLOT: scatter
plot(forlinear$temperature, forlinear$solar,log="")

#reg1 <- lm(lightness~temperature + genus + caste + subfamily,data=forlinear) 
reg1 <- lm(temperature~solar,data=forlinear) 
summary(reg1)
abline(reg1)

forlinear = forlinear[!(is.na(forlinear$solar)), ]
forlinear = forlinear[!(is.na(forlinear$temperature)), ]
cov(forlinear$solar,forlinear$temperature)

