#Calculate and compare caste means + standard deviations and standard errors
se <- function(x) sqrt(var(x)/length(x))

#LIGHTNESS
#Workers
nrow(colorspecimensworkers)
mean(colorspecimensworkers$lightness)
sd(colorspecimensworkers$lightness)
se(colorspecimensworkers$lightness)

#Queens
nrow(colorspecimensqueens)
mean(colorspecimensqueens$lightness)
sd(colorspecimensqueens$lightness)
se(colorspecimensqueens$lightness)

#Males
nrow(colorspecimensmales)
mean(colorspecimensmales$lightness)
sd(colorspecimensmales$lightness)
se(colorspecimensmales$lightness)

#Caste Comparisons
anova <- aov(lightness ~ caste, data=colorspecimens)
summary(anova)
pvals <- TukeyHSD(anova)$caste
print('Worker-to-Male Lightness p-value:')
pvals[33,4]
print('Worker-to-Queen Lightness p-value:')
pvals[36,4]
print('Queen-to-Male Lightness p-value:')
pvals[32,4]

#SATURATION
#Workers
nrow(colorspecimensworkers)
mean(colorspecimensworkers$saturation)
sd(colorspecimensworkers$saturation)
se(colorspecimensworkers$saturation)

#Queens
nrow(colorspecimensqueens)
mean(colorspecimensqueens$saturation)
sd(colorspecimensqueens$saturation)
se(colorspecimensqueens$saturation)

#Males
nrow(colorspecimensmales)
mean(colorspecimensmales$saturation)
sd(colorspecimensmales$saturation)
se(colorspecimensmales$saturation)

#Caste Comparisons
anova <- aov(saturation ~ caste, data=colorspecimens)
summary(anova)
pvals <- TukeyHSD(anova)$caste
print('Worker-to-Male p-value:')
pvals[33,4]
print('Worker-to-Queen p-value:')
pvals[36,4]
print('Queen-to-Male p-value:')
pvals[32,4]

#HUE
#Workers
nrow(colorspecimensworkers)
mean(colorspecimensworkers$hue)
sd(colorspecimensworkers$hue)
se(colorspecimensworkers$hue)

#Queens
nrow(colorspecimensqueens)
mean(colorspecimensqueens$hue)
sd(colorspecimensqueens$hue)
se(colorspecimensqueens$hue)

#Males
nrow(colorspecimensmales)
mean(colorspecimensmales$hue)
sd(colorspecimensmales$hue)
se(colorspecimensmales$hue)

#Caste Comparisons
anova <- aov(hue ~ caste, data=colorspecimens)
summary(anova)
pvals <- TukeyHSD(anova)$caste
print('Worker-to-Male p-value:')
pvals[33,4]
print('Worker-to-Queen p-value:')
pvals[36,4]
print('Queen-to-Male p-value:')
pvals[32,4]

mean(colorspecimensmales$red)
mean(colorspecimensmales$green)
mean(colorspecimensmales$blue)

mean(colorspecimensmales$hue)
mean(colorspecimensmales$lightness)
mean(colorspecimensmales$saturation)

mean(colorspecimensworkers$red)
mean(colorspecimensworkers$green)
mean(colorspecimensworkers$blue)

mean(colorspecimensworkers$hue)
mean(colorspecimensworkers$lightness)
mean(colorspecimensworkers$saturation)

#Bayes Factor Caste Comparisons

df <- rbind(colorspecimens[colorspecimens$caste == 'worker',],colorspecimens[colorspecimens$caste == 'male',])
df <- data.frame(df$lightness,df$caste)
df <- df[complete.cases(df),]
bf <- ttestBF(formula = df.lightness ~ df.caste, rscale = 1,data = df)
bf

df <- rbind(colorspecimens[colorspecimens$caste == 'queen',],colorspecimens[colorspecimens$caste == 'male',])
df <- data.frame(df$saturation,df$caste)
df <- df[complete.cases(df),]
bf <- ttestBF(formula = df.saturation ~ df.caste, rscale = 1,data = df)
bf

df <- rbind(colorspecimens[colorspecimens$caste == 'male',],colorspecimens[colorspecimens$caste == 'worker',])
df <- data.frame(df$hue,df$caste)
df <- df[complete.cases(df),]
bf <- ttestBF(formula = df.hue ~ df.caste, rscale = 1,data = df)
bf

#paired genus subset

df <- data.frame(castegenusthreshed1anovaformatted$Caste,castegenusthreshed1anovaformatted$meanlightness)
colnames(df) <- c('caste','lightness')
df <- cbind(as.numeric(as.character(df[df$caste == 'male',]$lightness)),as.numeric(as.character(df[df$caste == 'queen',]$lightness)))
colnames(df) <- c('caste1','caste2')
df <- data.frame(df)
bf <- ttestBF(x = df$caste1, y = df$caste2,paired = TRUE)
bf

#paired taxon subset

df <- data.frame(castetaxonthreshed1anovaformatted$Caste,castetaxonthreshed1anovaformatted$meanlightness)
colnames(df) <- c('caste','lightness')
df <- cbind(as.numeric(as.character(df[df$caste == 'queen',]$lightness)),as.numeric(as.character(df[df$caste == 'male',]$lightness)))
colnames(df) <- c('caste1','caste2')
df <- data.frame(df)
bf <- ttestBF(x = df$caste1, y = df$caste2,paired = TRUE)
bf

