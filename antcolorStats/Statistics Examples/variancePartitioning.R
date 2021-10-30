#Variance partitioning 
library(vegan)

X <- cbind(colorspecimens$genus, colorspecimens$antwebTaxonName, colorspecimens$caste,as.numeric(colorspecimens$lightness),as.numeric(colorspecimens$saturation),as.numeric(colorspecimens$hue))
colnames(X) <- c('Genus','Taxon','Caste','Lightness','Sat','Hue')
X <- X[complete.cases(X),]
X <- as.data.frame(X)

Y <- cbind(X$Lightness,X$Sat,X$Hue)

mod <- varpart(Y, ~ Caste, ~ Genus, data=X, transfo="hel")
mod
plot (mod, digits = 2)


mod <- varpart(Y, ~., data=X, transfo="hel")
mod
plot (mod, digits = 2)


mod <- varpart(Y, ~ Caste, ~ Genus, data=X, transfo="hel")
mod
plot (mod, digits = 2)

varpart(X$Light, ~., ..., data, transfo, scale = FALSE, add = FALSE, sqrt.dist = FALSE)
showvarparts(parts, labels, bg = NULL, alpha = 63, Xnames, id.size = 1.2,  ...)
"plot"(x, cutoff = 0, digits = 1, ...)


#test with threshed 

X <- as.data.frame(X)

Y <- cbind(as.numeric(as.character(castegenusthreshed1anovaformatted$meanlightness)),as.numeric(as.character(castegenusthreshed1anovaformatted$sdlightness)))
ncol(Y)
mod <- varpart(Y, ~ Caste, ~ Genus, data=castegenusthreshed1anovaformatted, transfo="hel")
mod
plot (mod, digits = 2)

mod <- varpart(Y, ~ Caste, ~ Genus, data=X, transfo="hel")
mod
plot (mod, digits = 2)

varpart(Y, ~., ..., data, transfo, scale = FALSE, add = FALSE, sqrt.dist = FALSE)
showvarparts(parts, labels, bg = NULL, alpha = 63, Xnames, id.size = 1.2,  ...)


#wouldnt it fuck things up to have like 100 workers for a genus and 1 male and then of course most variance would still be explained by genus

library(nlme)
library(ape)
mod <- lme(lightness ~ 1, random = ~ 1 | subfamily / genus / scientificName / caste, data = colorspecimens, na.action = na.omit)
var.mod <- varcomp(mod, scale = TRUE)
var.mod
mod
