#partial least squares regression using plsdepot

library(plsdepot)
forpls = colorlocatedworkers[complete.cases(colorlocatedworkers$brownnessHSV), ]
pls1 = plsreg1(forpls[,83:86],forpls[,63, drop=FALSE], comps=3)
summary(pls1)
pls1
pls1$R2
plot(pls1)
