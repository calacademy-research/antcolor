#aggregate test

aggregate(x$Frequency, by=list(Category=x$Category), FUN=sum)

View(aggregate(allspecimens$decimalLatitude, by=list(Category=allspecimens$antwebTaxonName), FUN=n))
tally(allspecimens$antwebTaxonName)

allspecimens %>% 
  group_by(allspecimens$antwebTaxonName) %>% 
  summarise_if(funs(sum))
library(tidyr)

allspecimenstest <- tidyr::gather(allspecimens, 'antwebTaxonName','decimalLatitude')
View(allspecimenstest)

select(metadata, sample, clade, cit, genome_size)

filter(allspecimens, )

#dplyr notes

filter(df, genus == "male")

select(df, lightness, decimalLatitude, etc)

pipe

df %>%
  filter(genus == "male")
  select(lightness, decimalLatitude)

mutate(df, lightness_mean = )

df <- allspecimens
df <- colorspecimensworkers
df <- df %>%
  group_by(antwebTaxonName) %>%
  summarize(lightness_mean = mean(lightness, na.nm = TRUE), n = n())
View(df)
head(filter(df,genus == 'Adetomyrma'))

View(df)
