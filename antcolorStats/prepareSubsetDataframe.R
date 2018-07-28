library("dplr", lib.loc="~/R/win-library/3.5")

#subsets all specimens, taking the average of fields for each term 
#and storing in a dataframe. 

terms = colorspecimens[!(is.na(colorspecimens$scientificName)), ]
terms = terms$scientificName
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
  members = dplyr::filter(colortempsolar, grepl(term, scientificName))
  if(nrow(members) >= 3)
  {
    samplesize = nrow(members)
    
    meanlightness = mean(members$lightness)
    sdlightness = sd(members$lightness)
    selightness = sdlightness/sqrt(length(members$lightness))
   
    meanred = mean(members$red)
    sdred = sd(members$red)
    sered= sdred/sqrt(length(members$red))
    
    meangreen = mean(members$green)
    sdgreen = sd(members$green)
    segreen = sdgreen/sqrt(length(members$green))
    
    meanblue = mean(members$blue)
    sdblue = sd(members$blue)
    seblue = sdblue/sqrt(length(members$blue))
    
    #meansolar = mean(members$solar)
    #meantemp = mean(members$temperature)
    row = cbind(term,samplesize,meanlightness,sdlightness,selightness,meanred,sdred,sered,meangreen,sdgreen,segreen,meanblue,sdblue,seblue)
    subset = rbind(subset,row)
    subset
  }
}

subset$samplesize = as.numeric(as.character(subset$samplesize))
subset$meanlightness = as.numeric(as.character(subset$meanlightness))
subset$sdlightness = as.numeric(as.character(subset$sdlightness))
subset$selightness = as.numeric(as.character(subset$selightness))

subset$meanred = as.numeric(as.character(subset$meanred))
subset$sdred = as.numeric(as.character(subset$sdred))
subset$sered = as.numeric(as.character(subset$sered))

subset$meangreen = as.numeric(as.character(subset$meangreen))
subset$sdgreen = as.numeric(as.character(subset$sdgreen))
subset$segreen = as.numeric(as.character(subset$segreen))

subset$meanblue = as.numeric(as.character(subset$meanblue))
subset$sdblue = as.numeric(as.character(subset$sdblue))
subset$seblue = as.numeric(as.character(subset$seblue))

#subset$meantemp = as.numeric(as.character(subset$meantemp))
#subset$meansolar = as.numeric(as.character(subset$meansolar))

dim(subset)
View(subset)