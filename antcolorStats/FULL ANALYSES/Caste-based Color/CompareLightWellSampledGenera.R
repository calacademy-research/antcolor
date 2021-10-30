#Analysis finding and comparing unusually light well-sampled ants

#Prep light genera subset
colorspecimensStrumigenys <- dplyr::filter(colorspecimens, grepl("Strumigenys", genus)) #set to desired field and value
colorspecimensSolenopsis <- dplyr::filter(colorspecimens, grepl("Solenopsis", genus)) #set to desired field and value
colorspecimensCarebara <- dplyr::filter(colorspecimens, grepl("Carebara", genus)) #set to desired field and value

#Compare means
anova <- aov(lightness ~ caste, data=colorspecimensStrumigenys)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

anova <- aov(lightness ~ caste, data=colorspecimensSolenopsis)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

anova <- aov(lightness ~ caste, data=colorspecimensCarebara)
summary(anova) # display Type I ANOVA table
TukeyHSD(anova)

