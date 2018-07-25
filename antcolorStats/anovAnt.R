
#run an ANOVA on the dataframe

fit <- aov(lightness ~ temperature, data=filtered)
summary(fit) # display Type I ANOVA table
drop1(fit,~.,test="F") # type III SS and F Tests