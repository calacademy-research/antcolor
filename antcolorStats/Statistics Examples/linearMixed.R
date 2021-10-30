library(lme4)
#run a linear mixed model on a dataframe using lme4
mixed.lmer = lmer(lightness ~ genus + scientificName + caste + (1|bioregion/region/country), data = colorspecimens)
mixed.lmer = lmer(lightness ~ genus, caste, + (1|country), data = colorspecimens)

#(1|bioregion/region/country)
summary(mixed.lmer)
head(mixed.lmer)
plot(mixed.lmer)
qqnorm(resid(mixed.lmer))
qqline(resid(mixed.lmer)) 


library(ape)
#also do variance partitioning 
varpart <- varcomp(mixed.lmer, scale = FALSE, cum = FALSE)

phylANOVA(tree, x, y, nsim=1000, posthoc=TRUE, p.adj="holm")