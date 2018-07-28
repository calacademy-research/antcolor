#run a linear regression on a prepared dataframe

forlinear = ranged

#CORRELATION
cor(forlinear$lightness, forlinear$temperature, use = "complete.obs") 

#PLOT: scatter
plot(forlinear$temperature, forlinear$lightness,log="")

#reg1 <- lm(lightness~temperature + genus + caste + subfamily,data=forlinear) 
reg1 <- lm(lightness~temperature,data=forlinear) 
summary(reg1)
abline(reg1)

forlinear = forlinear[!(is.na(forlinear$solar)), ]
forlinear = forlinear[!(is.na(forlinear$temperature)), ]
cov(forlinear$solar,forlinear$temperature)

