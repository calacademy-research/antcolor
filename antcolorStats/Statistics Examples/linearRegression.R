#run a linear regression on a prepared dataframe

forlinear = colorlocatedworkers

#CORRELATION
cor(forlinear$solar, forlinear$temperature, use = "complete.obs") 


#PLOT: scatter
plot(forlinear$rainfall, forlinear$lightness,log="")

#run the regression
reg <- lm(value~ temperature + solar + altitude + rainfall,data=forlinear) 
summary(reg)
plot(reg)

abline(reg1)
vif(reg1)
forlinear = forlinear[!(is.na(forlinear$solar)), ]
forlinear = forlinear[!(is.na(forlinear$solar)), ]
cov(forlinear$solar,forlinear$solar)

install.packages("xtable")
library(xtable)
xtable(reg)