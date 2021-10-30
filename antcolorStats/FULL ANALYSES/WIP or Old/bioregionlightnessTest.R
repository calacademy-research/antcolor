colorspecimens[80]

colSums(!is.na(colorspecimens[80]))
summary(colorspecimens[80])
summary(colorspecimens)
table(colorspecimens$microhabitatInferred)

colorspecimens[39]
colorspecimens$scientificName[!is.na(colorspecimens[80])]
unique(colorspecimens$scientificName[!is.na(colorspecimens[80])])
table(colorspecimens$bioregion)
summary(colorspecimens$lightness[colorspecimens$bioregion == 'Malagasy'])
summary(colorspecimens$lightness[colorspecimens$bioregion == 'Nearctic'])
summary(colorspecimens$lightness[colorspecimens$bioregion == 'Australasia'])
summary(colorspecimens$lightness[colorspecimens$bioregion == 'Neotropical'])


anova <- aov(lightness ~ bioregion, data=colorspecimens)
summary(anova)
pvals <- TukeyHSD(anova)$bioregion
summary()
print(pvals)
print('Worker-to-Male Lightness p-value:')
pvals[33,4]
print('Worker-to-Queen Lightness p-value:')
pvals[36,4]
print('Queen-to-Male Lightness p-value:')
pvals[32,4]
