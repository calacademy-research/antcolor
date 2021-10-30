library(dplyr)
colorspecimenschile <- filter(colorspecimens, grep1('Chile', adm1)
View(colorspecimenschile)                              

sd(castegenusthreshed1)

library(nlme)
library(ape)
mod <- lme(saturation ~ 1, random = ~ 1 | subfamily / genus / species / caste, data = colorspecimens, na.action = na.omit)
var.mod <- varcomp(mod, scale = TRUE)
var.mod

fit <- lm(meanlightness ~ Caste, data=castegenusthreshed1anovaformatted)
summary(fit) # show results

fit <- aov(meanlightness ~ Caste, data=castegenusthreshed1anovaformatted)
summary(fit)
