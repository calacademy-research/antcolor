#phylogenetic regression

library(phylolm)
library(ape)
#pgls.Ives(genustree, castegenusthreshed1$propmaletoworker, castegenusthreshed1$meanlightness.x, Vx=NULL, Vy=NULL, Cxy=NULL, lower=c(1e-8,1e-8))

df <- castegenusthreshed1_wm
tree <- genustree
row.names(df) <- df$term

length(tree$tip.label)
nrow(df)

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
missingtips <- getmissing(tree$tip.label,df$term)
missingtips <- as.character(missingtips)
tree <- drop.tip(tree,missingtips)

#drop traits
missingtraits <- getmissing(df$term, tree$tip.label)
finalgenustraits <- df
for(i in 1:length(missingtraits))
{
  finalgenustraits <- finalgenustraits[finalgenustraits[,"term"] != missingtraits[i],]
}

nrow(finalgenustraits)
length(tree$tip.label)

View(finalgenustraits)

phylm <- phylolm(WQdiff ~ meanlightness.x, data = finalgenustraits, tree, model = c("BM", "OUrandomRoot",
                                               "OUfixedRoot", "lambda", "kappa", "delta", "EB", "trend"),
        lower.bound = NULL, upper.bound = NULL,
        starting.value = NULL, measurement_error = FALSE,
        boot=0,full.matrix = TRUE)
plot(phylm)
summary(phylm)
plot(finalgenustraits$meanlightness.x,finalgenustraits$WMdiff)

nrow(castegenusthreshed1)
nrow(genustree$tip.label)

#PIC 

pic.X <- pic(finalgenustraits$WMdiff, tree)
pic.Y <- pic(finalgenustraits$meanlightness.x, tree)
cor.test(pic.X, pic.Y)
cor.test(finalgenustraits$WQdiff, finalgenustraits$meanlightness.x)
pic.X <- pic(finalgenustraits$meanlightness.y, tree)
pic.Y <- pic(finalgenustraits$meanlightness.x, tree)
cor.test(pic.X, pic.Y)


cor.test(castegenusthreshed1_wq$WQdiff, castegenusthreshed1_wq$meanlightness.x)
cor.test(castegenusthreshed1_wq$meanlightness.y, castegenusthreshed1_wq$meanlightness.x)

reg <- lm(meanlightness.y ~ meanlightness.x, data = castegenusthreshed1_wq)
summary(reg)
