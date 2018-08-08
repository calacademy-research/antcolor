
#run an ANOVA on the dataframe
anova <- aov(lightness ~ genus, data=colorspecimens1workers)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)
drop1(fit,~.,test="F") # type III SS and F Tests