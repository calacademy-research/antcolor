#partial least squares regression using plsdepot

pls1 = plsreg1(colorlocated1[,83:86],colorlocated1[,51, drop=FALSE], comps=3)
summary(pls1)
pls1
pls1$R2
plot(pls1)

forpls = colorlocated1[complete.cases(colorlocated1$brownnessHSV), ]
pls1 = plsreg1(forpls[,83:86],forpls[,63, drop=FALSE], comps=3)
summary(pls1)
pls1
pls1$R2
plot(pls1)


forpls = colorlocated1[complete.cases(colorlocated1$brownnessHSV), ]
pls2 = plsreg2(forpls[,83:86],forpls[,60:69, drop=FALSE], comps=2)
summary(pls2)
pls2
pls2$R2
plot(pls2)