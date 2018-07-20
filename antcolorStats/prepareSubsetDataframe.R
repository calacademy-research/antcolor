#subsets all specimens, taking the average of fields for each term 
#and storing in a dataframe. 

terms = colorspecimens[!(is.na(colorspecimens$genus)), ]
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
  members = dplyr::filter(colorspecimens, grepl(term, genus))
  if(nrow(members) > 1)
  {
    samplesize = nrow(members)
    meanlightness = mean(members$lightness)
    sdlightness = sd(members$lightness)
    selightness = sdlightness/sqrt(length(members$lightness))
    #meansolar = mean(members$solar)
    #meantemp = mean(members$temperature)
    row = cbind(term,samplesize,meanlightness,sdlightness,selightness)
    row
    subset = rbind(subset,row)
    subset
  }
}
dim(subset)
View(subset)
subset$meantemp = as.numeric(as.character(subset$meantemp))
subset$meanlightness = as.numeric(as.character(subset$meanlightness))
subset$sdlightness = as.numeric(as.character(subset$sdlightness))
subset$selightness = as.numeric(as.character(subset$selightness))
