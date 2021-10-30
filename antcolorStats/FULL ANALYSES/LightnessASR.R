#APE ancestral state reconstruction test - kind of a mess currently

install.packages("ape")
library(ape)
geospizatree <- read.nexus("C:/Users/OWNER/Desktop/Geospiza.nex")
geospizatraits <- read.table("C:/Users/OWNER/Desktop/Geospiza.txt")

geospizatree <- drop.tip(geospizatree, "olivacea")
View(geospizatraits)

#Make sure row.names of df matches tip.labels of phylogeny
row.names(geospizatraits)
geospizatree$tip.label

wingL <- geospizatraits$wingL
names(wingL) <- row.names(geospizatraits)

#3 options: ML, phylogenetic independent contrasts, GLS

#BM-based ML
library(ape)
MLasr <- ace(wingL, geospizatree, type="continuous", method = "ML")
MLasr$ace

#plot
plot(geospizatree, show.tip.label=FALSE)
tiplabels(pch = 21, cex=(wingL-3.9)*10)
nodelabels(pch = 21, cex=(MLasr$ace-3.9)*10)
## (pch = 21 is just telling plot.phylo which symbol to use)

#WITH ANTZ
library(ape)
antspeciestree <- read.tree("C:/Users/OWNER/Desktop/Dryad_Supplementary_File_7_ML_TREE_treepl_185.txt")
plot(antspeciestree,show.tip.label = FALSE)

antspeciestraits <- colorspecimensworkersspecies

#fix string format to match tree tips
modstring <- function(string) {
  string <- as.character(string)
  length <- nchar(string)
  substring(string,1,1)
  substring(string,2,length)
  string <- paste(toupper(substring(string,1,1)),substring(string,2,length), sep = "")
  string <- gsub(" ", "_", string)
  return(string)
}
antspeciestraits$term <- lapply(antspeciestraits$term, modstring)

#get list of tip labels that DONT have matching trait data
missingtips <- vector(mode="character")
z <- 1

for(i in 1:length(antspeciestree$tip.label))
{
  tip <- antspeciestree$tip.label[i]
  match <- FALSE
  for(k in 1:length(antspeciestraits$term))
  {
    if(antspeciestraits$term[k] == tip)
    {
      match <- TRUE
    }
  }
  if(match == FALSE) {
    missingtips[z] <- tip
    z <- z + 1
  }
}
#drop tips
antspeciestree <- drop.tip(antspeciestree,missingtips)

#get list of trait labels that DONT have matching tip data
missingtraits <- vector(mode="character")
z <- 1

for(i in 1:length(antspeciestraits$term))
{
  trait <- antspeciestraits$term[i]
  match <- FALSE
  for(k in 1:length(antspeciestree$tip.label))
  {
    #if(!is.na(antspeciestree$tip.label[k]))
    if(antspeciestree$tip.label[k] == trait)
    {
      match <- TRUE
    }
  }
  if(match == FALSE) {
    missingtraits[z] <- trait
    z <- z + 1
  }
}

#drop traits
library(dplyr)
newAST <- antspeciestraits
missingtraits[2]
newAST$term <- complete.cases(newAST$term)
for(i in 1:length(missingtraits))
{
  #if(is.null(missingtraits[i]))
  #antspeciestraits <- antspeciestraits[!antspeciestraits$term==missingtraits[i]]
  #newAST <- dplyr::filter(newAST,term == missingtraits[i], na.rm )
  newAST <- newAST[newAST[,"term"] != missingtraits[i]]
}
newAST <- newAST[which()]

#fix indices

#OR 

lightness <- antspeciestraits$meanlightness
View(antspeciestraits)
names(lightness) <- row.names(antspeciestraits)
View(lightness)
#remove NA
lightness <- lightness[complete.cases(lightness)]
complete.cases(antspeciestree$tip.label)

missing <- which(is.na(antspeciestree$tip.label))
missing
#run asr
MLasr <- ace(lightness, antspeciestree, type="continuous", method = "ML")
length(lightness)
lightness
length(antspeciestree$tip.label)
antspeciestree$tip.label
MLasr$ace

#ANT GENERA ONLY
library(ape)
genustree <- read.tree("C:/Users/OWNER/Desktop/Dryad_Supplementary_File_7_ML_TREE_treepl_185.txt")
tips <- genustree$tip.label
genera<-unique(sapply(strsplit(tips,"_"),function(x) x[1]))
#genera

## now drop all but one of each
ii<-sapply(genera,function(x,y) grep(x,y)[1],y=tips)
genustree<-drop.tip(genustree,setdiff(genustree$tip.label,tips[ii]))
plot(genustree, show.tip.label=TRUE)
genustree$tip.label

#fix string format to match tree tips
modtips <- function(string) {
  string <- string[1]
  string <- as.character(string)
  length <- nchar(string)
  pos <- regexpr("_",string)
  string <- substring(string,1,pos-1)
  return(string)
}
genustreemod <- genustree
genustreemod$tip.label <- lapply(genustreemod$tip.label, modtips)
genustreemod

genustree <- genustreemod

genustraits <- colorspecimensworkersgenera
nrow(genustraits)
length(genustreemod$tip.label)

#get list of tip/trait labels that DONT have matching trait/tip data
getmissing <- function(vector2drop, reference)
{
  missing <- vector(mode="character")
  z <- 1
  
  for(i in 1:length(vector2drop))
  {
    tip <- as.character(vector2drop[i])
    match <- FALSE
    for(k in 1:length(reference))
    {
      if(reference[k] == tip)
      {
        match <- TRUE
      }
    }
    if(match == FALSE) {
      missing[z] <- tip
      z <- z + 1
    }
  }
  return(missing)
}


#drop tips
missingtips <- getmissing(genustree$tip.label,genustraits$term)
missingtips <- as.character(missingtips)
drop.tip(genustree, missingtips)
genustree <- drop.tip(genustree,missingtips)

#drop traits
missingtraits <- getmissing(genustraits$term, genustree$tip.label)
finalgenustraits <- genustraits
for(i in 1:length(missingtraits))
{
  finalgenustraits <- finalgenustraits[finalgenustraits[,"term"] != missingtraits[i],]
}
nrow(finalgenustraits)
length(genustree$tip.label)

#prep traits for asr
lightness <- finalgenustraits$meanlightness
names(lightness) <- finalgenustraits$term

#unlist tree tips
finalgenustree <- genustree
finalgenustree$tip.label <- unlist(finalgenustree$tip.label)

#function for hsl to rgb
hsl_to_rgb <- function(h, s, l) {
  h <- h / 360
  r <- g <- b <- 0.0
  if (s == 0) {
    r <- g <- b <- l
  } else {
    hue_to_rgb <- function(p, q, t) {
      if (t < 0) { t <- t + 1.0 }
      if (t > 1) { t <- t - 1.0 }
      if (t < 1/6) { return(p + (q - p) * 6.0 * t) }
      if (t < 1/2) { return(q) }
      if (t < 2/3) { return(p + ((q - p) * ((2/3) - t) * 6)) }
      return(p)
    }
    q <- ifelse(l < 0.5, l * (1.0 + s), l + s - (l*s))
    p <- 2.0 * l - q
    r <- hue_to_rgb(p, q, h + 1/3)
    g <- hue_to_rgb(p, q, h)
    b <- hue_to_rgb(p, q, h - 1/3)
  }
  return(rgb(r,g,b))
}

#makes trait indices match order of tree tips
matchorder <- function(tree, traitvect)
{
  ordered <- traitvect
  for(i in 1:length(tree$tip.label))
  {
    tipstr <- tree$tip.label[i]
    for(ii in 1:length(traitvect))
    {
      if(tipstr == names(traitvect[ii]))
      {
        ordered[i] <- traitvect[ii]
        names(ordered)[i] <- tipstr
      }
    }
  }
  return(ordered)
}

ordered <- matchorder(finalgenustree, lightness)
mean(colorspecimens$red)
mean(colorspecimens$green)
mean(colorspecimens$blue)
colorspecimens[3913,]
#run ASR on all genera
allordered <- matchorder(finalgenustree, lightness)
obj<-contMap(finalgenustree,allordered,plot=FALSE)
plot(obj,type="fan",legend=0.7*max(nodeHeights(finalgenustree)), fsize=c(0.6,0.9))

MLasr <- ace(ordered, finalgenustree, type="continuous", method = "ML")
plot(finalgenustree, show.tip.label=TRUE, cex=0.3)
tiplabels(pch = 16, cex=(ordered)*7, col = (hsl_to_rgb(52,1,ordered)))
nodelabels(pch = 16, cex=(MLasr$ace)*7, col = (hsl_to_rgb(52,1,MLasr$ace)))

#node labels with text
nodelabels(text= MLasr$ace,pch = 16, cex=1, col = (hsl_to_rgb(33,0.51,MLasr$ace)))
## (pch = 21 is just telling plot.phylo which symbol to use)
View(MLasr)
MLasr$ace
MLasr$sigma2
MLasr$CI95

#run asr on Myrmicinae tips 151:254
tips2drop <- finalgenustree$tip.label[1:150]
myrmicinaetree <- drop.tip(finalgenustree,tips2drop)
ordered <- matchorder(myrmicinaetree, lightness)
ordered <- ordered[1:104]
myrmASR <- ace(ordered,myrmicinaetree,type="continuous", method = "ML")
plot(myrmicinaetree, show.tip.label=TRUE, cex=0.3)
tiplabels(pch = 16, cex=(ordered)*7, col = (hsl_to_rgb(0,0,ordered)))
nodelabels(pch = 16, cex=(myrmASR$ace)*7, col = (hsl_to_rgb(0,0,myrmASR$ace)))
library(phytools)
obj<-contMap(myrmicinaetree,ordered,plot=FALSE)
plot(obj,type="fan",legend=0.7*max(nodeHeights(myrmicinaetree)),
     fsize=c(0.7,0.9))
n<-length(obj$cols)
## change to grey scale
obj$cols[1:n]<-grey(0:(n-1)/(n-1))
plot(obj)

#run asr on Formicinae tips 102:145
finalgenustree$tip.label[103:145]
tips2drop <- finalgenustree$tip.label[146:254]
formicinaetree <- drop.tip(finalgenustree,tips2drop)
formicinaetree$tip.label
tips2drop <- formicinaetree$tip.label[1:102]
formicinaetree <- drop.tip(formicinaetree,tips2drop)

ordered <- matchorder(formicinaetree, lightness)
ordered <- ordered[1:43]
ordered
length(formicinaetree$tip.label)
formASR <- ace(ordered,formicinaetree,type="continuous", method = "ML")
formASR$CI95
plot(formicinaetree, show.tip.label=TRUE, cex=0.3)
tiplabels(pch = 16, cex=(ordered)*7, col = (hsl_to_rgb(0,0,ordered)))
nodelabels(pch = 16, cex=(formASR$ace)*7, col = (hsl_to_rgb(0,0,formASR$ace)))
library(phytools)

obj<-contMap(formicinaetree,ordered,plot=FALSE)
plot(obj,type="fan",legend=0.7*max(nodeHeights(formicinaetree)),
     fsize=c(0.7,0.9))
n<-length(obj$cols)
## change to grey scale
obj$cols[1:n]<-grey(0:(n-1)/(n-1))
plot(obj)
nodelabels()

#run ASR on Dolychoderinae tips 76:99
finalgenustree$tip.label[76:99]
tips2drop <- finalgenustree$tip.label[100:254]
dolitree <- drop.tip(finalgenustree,tips2drop)

tips2drop <- dolitree$tip.label[1:75]
dolitree <- drop.tip(dolitree,tips2drop)
doliorder <- matchorder(dolitree, lightness)
doliorder <- doliorder[1:24]

obj<-contMap(dolitree,doliorder,plot=FALSE)
plot(obj,type="fan",legend=0.7*max(nodeHeights(dolitree)),
     fsize=c(0.7,0.9))

length(myrmicinaetree$tip.label)
MLasr$ace
plot(firstcladetree)
tiplabels(pch = 16, cex=(lightness)*7, col = (hsl_to_rgb(52,1,newlightness)))
firstcladetree$tip.label
lightness
MLasr$ace
nodelabels(pch = 16, cex=(MLasr$ace)*7, col = (hsl_to_rgb(52,1,MLasr$ace)))
newlightness <- lightness

#makes trait indices match order of tree tips
matchorder <- function(tree, traitvect)
{
  ordered <- traitvect
  for(i in 1:length(tree$tip.label))
  {
    tipstr <- tree$tip.label[i]
    for(ii in 1:length(traitvect))
    {
      if(tipstr == names(traitvect[ii]))
      {
        ordered[i] <- traitvect[ii]
        names(ordered)[i] <- tipstr
      }
    }
  }
  return(ordered)
}

tips2drop <- finalgenustree$tip.label[1:200]
secondcladetree <- drop.tip(finalgenustree,tips2drop)
ordered <- matchorder(secondcladetree, lightness)
ordered <- ordered[1:54]
MLasr3 <- ace(ordered, secondcladetree,type="continuous", method = "ML")
plot(secondcladetree)
tiplabels(pch = 16, cex=(ordered)*7, col = (hsl_to_rgb(52,1,ordered)))
nodelabels(pch = 16, cex=(MLasr3$ace)*7, col = (hsl_to_rgb(52,1,MLasr3$ace)))

install.packages("phytools")
library(phytools)
obj<-contMap(secondcladetree,ordered,plot=FALSE)
plot(obj,type="fan",legend=0.7*max(nodeHeights(anole.tree)), fsize=c(0.7,0.9))


secondcladetree$tip.label

newlightness <- newlightness[1:49]
MLasr2 <- ace(newlightness, firstcladetree,type="continuous", method = "ML")
plot(firstcladetree)
tiplabels(pch = 16, cex=(newlightness)*7, col = (hsl_to_rgb(52,1,newlightness)))
nodelabels(pch = 16, cex=(MLasr2$ace)*7, col = (hsl_to_rgb(52,1,MLasr2$ace)))
length(firstcladetree$tip.label)
length(newlightness)
newlightness
