#Analyses of proportional lightness differences between castes and across microhabitats

source("Helpers/parseGenusHabitatData.R")
parseGenusHabitatData(path ='C:/Users/OWNER/OneDrive - Hendrix College/Desktop/BradleyGenusHabitatData.xlsx')

### LIGHTNESS DIFFERENCES BETWEEN CASTES
#male to worker straight up 
cor.test(castegenusthreshed1_wm$meanlightness.x, castegenusthreshed1_wm$meanlightness.y)
reg <- lm(meanlightness.y ~ meanlightness.x,data=castegenusthreshed1_wm)
summary(reg)

#male to worker
castegenusthreshed1_wm$WMdiff <- (castegenusthreshed1_wm$meanlightness.x - castegenusthreshed1_wm$meanlightness.y)

cor.test(castegenusthreshed1_wm$meanlightness.x, castegenusthreshed1_wm$WMdiff)
nrow(castegenusthreshed1_wm)
reg <- lm(WMdiff ~ meanlightness.x,data=castegenusthreshed1_wm)
summary(reg)

#plot this
library(plotwidgets)
library(extrafont)
library(ggplot2)
font_import()
loadfonts(device="win")
colormatrix <- hsl2col(t(cbind(30/255, 93/255, castegenusthreshed1_wm$meanlightness.x)))
colormatrix <- hsl2col(t(cbind(mean(castegenusthreshed1_wm$meanhue.x), mean(castegenusthreshed1_wm$meansaturation.x), castegenusthreshed1_wm$meanlightness.x)))
plot(castegenusthreshed1_wm$meanlightness.x, castegenusthreshed1_wm$WMdiff, pch = 16, col = colormatrix,xlab = 'Mean worker lightness of genus',ylab ='Mean worker-male lightness difference',ylim=c(-0.3, 0.35))
abline(reg)
temp <- locator(1)
text(temp,"coefficient = 0.44")
temp <- locator(1)
text(temp,"R² = 0.250")

#queen to worker
castegenusthreshed1_wq$WQdiff <- (castegenusthreshed1_wq$meanlightness.x - castegenusthreshed1_wq$meanlightness.y)
nrow(castegenusthreshed1_wq)
cor.test(castegenusthreshed1_wq$meanlightness.x, castegenusthreshed1_wq$WQdiff)

reg <- lm(WQdiff ~ meanlightness.x,data=castegenusthreshed1_wq)
summary(reg)
plot(castegenusthreshed1_wq$meanlightness.x, castegenusthreshed1_wq$WQdiff)
abline(reg)
#plot this
colormatrix <- hsl2col(t(cbind(mean(castegenusthreshed1_wq$meanhue.x), mean(castegenusthreshed1_wq$meansaturation.x), castegenusthreshed1_wq$meanlightness.x)))
plot(castegenusthreshed1_wq$meanlightness.x, castegenusthreshed1_wq$WQdiff, pch = 16, col = colormatrix,xlab = 'Mean worker lightness of genus',ylab ='Mean worker-queen lightness difference', ylim=c(-0.3, 0.35))
abline(reg)
temp <- locator(1)
text(temp,"cor = 0.395")
temp <- locator(1)
text(temp,"R² = 0.153")


### LIGHTNESS EFFECT SIZE BY MICROHABITAT 

#Iterate through dataframe and add hab tags
castegenusthreshed1_wq$isSoil <- NA
castegenusthreshed1_wq$isSurface <- NA
castegenusthreshed1_wq$isArboreal <- NA
for (i in 1:nrow(castegenusthreshed1_wq))
{
  brow <- castegenusthreshed1_wq[i,]
  bgenus <- brow$term
  for(k in 1:nrow(castehab))
  {
    srow <- castehab[k,]
    sgenus <- srow$Genus
    if(bgenus == sgenus)
    {
      castegenusthreshed1_wq[i,133] = castehab[k,3]
      castegenusthreshed1_wq[i,134] = castehab[k,4]
      castegenusthreshed1_wq[i,135] = castehab[k,5]
    }
  }
}

#male to worker
#soil included
a <- castegenusthreshed1_wm[castegenusthreshed1_wm$isSoil == TRUE,]
a <- a[!is.na(a$term),]
nrow(a)

a <- castegenusthreshed1_wm[castegenusthreshed1_wm$isSoil == FALSE,]
a <- a[!is.na(a$term),]
nrow(a)

#soil only
a <- castegenusthreshed1_wm[castegenusthreshed1_wm$isSoil == TRUE,]
a <- a[!is.na(a$term),]
a <- a[a$isSurface == FALSE,]
a <- a[a$isArboreal == FALSE,]
nrow(a)
View(a)
#surface included
a <- castegenusthreshed1_wm[castegenusthreshed1_wm$isSurface == TRUE,]
a <- a[!is.na(a$term),]
nrow(a)
a <- castegenusthreshed1_wm[castegenusthreshed1_wm$isSoil == FALSE,]
a <- a[!is.na(a$term),]
nrow(a)

t.test(castegenusthreshed1_wm$meanlightness.y~castegenusthreshed1_wm$isSurface)
t.test(castegenusthreshed1_wm$WMdiff~castegenusthreshed1_wm$isSoil)

#queen to worker
a <- castegenusthreshed1_wq[castegenusthreshed1_wq$isSoil == TRUE,]

mean(a$WQdiff, na.rm = TRUE)
mean(a$meanlightness.y, na.rm = TRUE)

t.test(castegenusthreshed1_wq$WQdiff~castegenusthreshed1_wq$isSoil)


### PHYLANOVA ON MICROHAB DIFFS
library(phytools)
library(geiger)
tree <- genustree

#drop traits
missingtraits <- getmissing(castegenusthreshed1_wm$term, tree$tip.label)
finalgenustraits <- castegenusthreshed1_wm
finalgenustraits <- finalgenustraits[!is.na(finalgenustraits$isSoil),]

#drop tips
missingtips <- getmissing(tree$tip.label,finalgenustraits$term)
missingtips <- as.character(missingtips)
tree <- drop.tip(tree,missingtips)

for(i in 1:length(missingtraits))
{
  finalgenustraits <- finalgenustraits[finalgenustraits[,"term"] != missingtraits[i],]
}
row.names(finalgenustraits) <- finalgenustraits$term

data <- as.numeric(as.character(finalgenustraits$WMdiff))
names(data) <- finalgenustraits$term
group <- as.factor(finalgenustraits$isSoil)
names(group) <- finalgenustraits$term
data <-as.matrix(data)
summary(group)
newtree <- tree
newtree$tip.label <- unlist(tree$tip.label) ##wow that was the issue

aov.phylo(formula = data ~ group, phy = newtree, nsim = 10000)
phylANOVA(newtree, group, data, nsim=1000, posthoc=TRUE)

### PHYLREGRESSION ON MALE-WORKER DIFFERENCE
#male to worker
castegenusthreshed1_wm$WMdiff <- (castegenusthreshed1_wm$meanlightness.x - castegenusthreshed1_wm$meanlightness.y)

cor.test(castegenusthreshed1_wm$meanlightness.x, castegenusthreshed1_wm$WMdiff)
nrow(castegenusthreshed1_wm)
reg <- lm(WMdiff ~ meanlightness.x,data=castegenusthreshed1_wm)
summary(reg)

#plot this
library(plotwidgets)
library(extrafont)
library(ggplot2)
font_import()
loadfonts(device="win")
colormatrix <- hsl2col(t(cbind(30/255, 93/255, castegenusthreshed1_wm$meanlightness.x)))
colormatrix <- hsl2col(t(cbind(mean(castegenusthreshed1_wm$meanhue.x), mean(castegenusthreshed1_wm$meansaturation.x), castegenusthreshed1_wm$meanlightness.x)))
plot(castegenusthreshed1_wm$meanlightness.x, castegenusthreshed1_wm$WMdiff, pch = 16, col = colormatrix,xlab = 'Mean worker lightness of genus',ylab ='Mean worker-male lightness difference',ylim=c(-0.3, 0.35))
abline(reg)
temp <- locator(1)
text(temp,"cor = 0.502")
temp <- locator(1)
text(temp,"R² = 0.250")

### ADD MICROHAB DATA TO COLORSPECIMENS FRAMES
colorspecimensworkers$isSoil <- NA
colorspecimensworkers$isSurface <- NA
colorspecimensworkers$isArboreal <- NA
for (i in 1:nrow(colorspecimensworkers))
{
  brow <- colorspecimensworkers[i,]
  bgenus <- brow$genus
  for(k in 1:nrow(castehab))
  {
    srow <- castehab[k,]
    sgenus <- srow$Genus
    if(bgenus == sgenus)
    {
      colorspecimensworkers[i,83] = castehab[k,3]
      colorspecimensworkers[i,84] = castehab[k,4]
      colorspecimensworkers[i,85] = castehab[k,5]
    }
  }
}


### PROPORTIONAL LIGHTNESS (OLD)
#Add col for prop male to worker
castegenusthreshed1$propmaletoworker = (castegenusthreshed1$meanlightness.y/castegenusthreshed1$meanlightness.x)
mean(castegenusthreshed1$propmaletoworker)

#Add col for prop queen to worker
castegenusthreshed1$propqueentoworker = (castegenusthreshed1$meanlightness/castegenusthreshed1$meanlightness.x)
mean(castegenusthreshed1$propqueentoworker)

#Add col for prop male to queen
castegenusthreshed1$propmaletoqueen = (castegenusthreshed1$meanlightness.y/castegenusthreshed1$meanlightness)
mean(castegenusthreshed1$propmaletoqueen)

#Run regression & cor on male to worker
cor.test(castegenusthreshed1$meanlightness.x, castegenusthreshed1$propmaletoworker)
reg1 <- lm(meanlightness.x ~ propmaletoworker,data=castegenusthreshed1) 
summary(reg1)
plot(combined$workerlightness, combined$propmaletoworker)
abline(reg1)
abline()

#Run regression & cor on queen to worker
cor.test(castegenusthreshed1$meanlightness.x, castegenusthreshed1$propqueentoworker)
reg1 <- lm(meanlightness.x ~ propqueentoworker,data=castegenusthreshed1) 
summary(reg1)
plot(combined$workerlightness, combined$propmaletoworker)
abline(reg1)
abline()
