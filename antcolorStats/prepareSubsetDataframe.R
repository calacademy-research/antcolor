library("dplr", lib.loc="~/R/win-library/3.5")

#subsets all specimens, taking the average of fields for each term 
#and storing in a dataframe. 

terms = colortempsolar[!(is.na(colortempsolar$genus)), ]
terms = terms$genus
terms = terms[!duplicated(terms)]

length(terms)
View(terms)
subset <- data.frame(Date=as.Date(character()),
                 File=character(), 
                 User=character(), 
                 stringsAsFactors=FALSE) 
#for every term ie. scientificName
for(term in terms)
{
  #all specimens of the scientificName
  members = dplyr::filter(colortempsolar, grepl(term, genus))
  if(nrow(members) >= 5)
  {
    samplesize = nrow(members)
    meanlightness = mean(members$lightness)
    sdlightness = sd(members$lightness)
    selightness = sdlightness/sqrt(length(members$lightness))
    meansolar = mean(members$solar)
    meantemp = mean(members$temperature)
    row = cbind(term,samplesize,meanlightness,sdlightness,selightness,meansolar,meantemp)
    subset = rbind(subset,row)
    subset
  }
}
dim(subset)
subset$samplesize = as.numeric(as.character(subset$samplesize))
View(subset)
subset$samplesize = as.numeric(as.character(subset$samplesize))
subset$meantemp = as.numeric(as.character(subset$meantemp))
subset$meansolar = as.numeric(as.character(subset$meansolar))
subset$meanlightness = as.numeric(as.character(subset$meanlightness))
subset$sdlightness = as.numeric(as.character(subset$sdlightness))
subset$selightness = as.numeric(as.character(subset$selightness))
