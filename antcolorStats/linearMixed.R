
#run a linear mixed model on a dataframe
mixed.lmer = lmer(lightness ~ temperature + solar + (1|genus) + (1|country), data = colorlocated)
summary(mixed.lmer)
plot(mixed.lmer)
qqnorm(resid(mixed.lmer))
qqline(resid(mixed.lmer)) 

summary(subset)
q1 = quantile(subset$meanlightness,0.25)
q4 = quantile(subset$meanlightness,0.75)

underq1 = subset[subset$meanlightness < q1, ] 
overq4 = subset[subset$meanlightness > q4, ] 
