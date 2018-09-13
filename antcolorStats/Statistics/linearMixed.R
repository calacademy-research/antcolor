
#run a linear mixed model on a dataframe using lme4
mixed.lmer = lmer(lightness ~ temperature + solar + (1|bioregion/region/country), data = colorlocated1)

#(1|bioregion/region/country)
summary(mixed.lmer)
plot(mixed.lmer)
qqnorm(resid(mixed.lmer))
qqline(resid(mixed.lmer)) 

summary(subset)
q1 = quantile(subset$meanlightness,0.25)
q4 = quantile(subset$meanlightness,0.75)

underq1 = subset[subset$meanlightness < q1, ] 
overq4 = subset[subset$meanlightness > q4, ] 
