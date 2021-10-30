#phylogenetic anova
library(phytools)
View(castegenusthreshed1)
df <- castegenusthreshed1anovaformatted
row.names(df) <- df$Genus
View(df)
phylANOVA(genustree, df$Caste, df$meanlightness, nsim=1000, posthoc=TRUE, p.adj="holm")
genustree$tip.label
x[genustree$tip.label]
class(genustree)
