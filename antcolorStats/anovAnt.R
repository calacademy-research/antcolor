
#run an ANOVA on the dataframe
anova <- aov(lightness ~ subfamily, data=colorspecimens)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)
drop1(fit,~.,test="F") # type III SS and F Tests