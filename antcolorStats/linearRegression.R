#run a linear regression on a prepared dataframe

forlinear = filtered
#forlinear$solar = abs(forlinear$solar)

#CORRELATION
cor(forlinear$solar, forlinear$lightness, use = "complete.obs") 

#forlinear = forlinear[!(is.na(forlinear$meantemp)), ]
#PLOT: scatter
plot(forlinear$solar, forlinear$lightness,log="")

reg1 <- lm(lightness~solar,data=forlinear) 
summary(reg1)
abline(reg1)

