library("dplyr", lib.loc="~/R/win-library/3.5")

#EXTREMELY BROKEN RIGHT NOW, DO NOT HAVE THE TIME TO FIX AT THE MOMENT
#subsets all specimens, taking the average of fields for each term 
#and storing in a dataframe. 

prepareSubsetDataframe <- function(df, subsetBy, threshold, locatedonly = FALSE, validonly = FALSE) {

col = df[ , colnames(df) == subsetBy]
terms = df[!(is.na(col)), ]
terms = terms[ , colnames(terms) == subsetBy]
terms = terms[!duplicated(terms)]

length(terms)

subset <- data.frame(Date=as.Date(character()),
                 File=character(), 
                 User=character(), 
                 stringsAsFactors=FALSE) 

numfinished <- 0
totalterms <- nrow(terms)

#for every term ie. caste, species
for(term in terms)
{ 
  
  #all specimens of the caste, species etc
  members = dplyr::filter(df, grepl(term, eval(parse(text= subsetBy))))
  
  #only specimens with valid names FIX TO ACCOUNT FOR CASTE SUBSETTING
  if(nrow(members) >= threshold)
  {
    row <- c(term)
    samplesize <- nrow(members)
    row <- cbind(row, samplesize)

    #count number of valid taxa in subset
    if(validonly)
    {
    validtaxawithin <- c(1)
    for(i in 1:nrow(members)) {
      row <- members[i,]
      if(!any(validtaxawithin == row$antwebTaxonName) && row$status == 'valid' && length(row$antwebTaxonName) != 0L && length(row) != 0L)
        validtaxawithin <- rbind(validtaxawithin, row$antwebTaxonName)
    }
    numvalidtaxa <- nrow(validtaxawithin) - 1
    if(length(numvalidtaxa) == 0L)
      numvalidtaxa = 0 
    
    row <- cbind(row, numvalidtaxa)
    #members <- colorspecimensCamponotusMadag
    }

    for(i in names(members)){
      #print(i)
      #print(members[[i]])
      row[[paste(i, 'mean', sep="_")]] <- mean(as.numeric(as.character(members[[i]]), na.rm = TRUE))
      row[[paste(i, 'sd', sep="_")]] <- sd(as.numeric(as.character(members[[i]]), na.rm = TRUE))
    }
    #warnings()
    #row <- t(row)
    #print(row)

    row <- unname(row)
    subset <- rbind(subset,row)
  }
  
  numfinished <- numfinished + 1
  if(numfinished %% 50 == 0)
    print(numfinished)
}

#subset <- sapply(subset, as.numeric)

# subset$samplesize = as.numeric(as.character(subset$samplesize))
# subset$meanlightness = as.numeric(as.character(subset$meanlightness))
# subset$sdlightness = as.numeric(as.character(subset$sdlightness))
# subset$selightness = as.numeric(as.character(subset$selightness))
# 
# subset$meansaturation = as.numeric(as.character(subset$meansaturation))
# subset$sdsaturation = as.numeric(as.character(subset$sdsaturation))
# subset$sesaturation = as.numeric(as.character(subset$sesaturation))
# 
# subset$meanhue = as.numeric(as.character(subset$meanhue))
# subset$sdhue = as.numeric(as.character(subset$sdhue))
# subset$sehue = as.numeric(as.character(subset$sehue))
# 
# subset$meanred = as.numeric(as.character(subset$meanred))
# subset$sdred = as.numeric(as.character(subset$sdred))
# subset$sered = as.numeric(as.character(subset$sered))
# 
# subset$meangreen = as.numeric(as.character(subset$meangreen))
# subset$sdgreen = as.numeric(as.character(subset$sdgreen))
# subset$segreen = as.numeric(as.character(subset$segreen))
# 
# subset$meanblue = as.numeric(as.character(subset$meanblue))
# subset$sdblue = as.numeric(as.character(subset$sdblue))
# subset$seblue = as.numeric(as.character(subset$seblue))
# 
# subset$meanpixSD = as.numeric(as.character(subset$meanpixSD))
# subset$sdpixSD = as.numeric(as.character(subset$sdpixSD))
# subset$sepixSD = as.numeric(as.character(subset$sepixSD))
# 
# subset$meanpixUsed = as.numeric(as.character(subset$meanpixUsed))
# subset$numvalidtaxa = as.numeric(as.character(subset$numvalidtaxa))

#subset$meantemp = as.numeric(as.character(subset$meantemp))
#subset$meansolar = as.numeric(as.character(subset$meansolar))

dim(subset)
return(subset)
}