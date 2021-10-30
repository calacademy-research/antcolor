library("dplyr", lib.loc="~/R/win-library/3.5")

#subsets all specimens, taking the average of fields for each term 
#and storing in a dataframe. 

prepareSubsetDataframe <- function(df, subsetBy, threshold, locatedonly = FALSE, validonly = TRUE) {
  
  
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
    
    if(numfinished %% 50 == 0)
      print(numfinished)
    
    #all specimens of the caste, species etc
    members = dplyr::filter(df, grepl(term, eval(parse(text= subsetBy))))
    
    #only specimens with valid names FIX TO ACCOUNT FOR CASTE SUBSETTING
    #if(members$status[1] == 'valid')
    if(nrow(members) >= threshold)
    {
      numfinished <- numfinished + 1
      row <- c(term)
      samplesize <- nrow(members)
      row <- cbind(row, samplesize)
      
      #count number of valid taxa in subset
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
      
      meanlightness = mean(members$lightness)
      sdlightness = sd(members$lightness)
      selightness = sdlightness/sqrt(length(members$lightness))
      
      meanaltitude = mean(members$minimumElevationInMeters,na.rm = TRUE)
      sdaltitude = sd(members$minimumElevationInMeters, na.rm = TRUE)
      sealtitude = sdaltitude/sqrt(length(members$minimumElevationInMeters))
      
      members$geolat <- as.numeric(members$geolat)
      meanlat = mean(abs(members$geolat),na.rm = TRUE)
      sdlat = sd(abs(members$geolat), na.rm = TRUE)
      selat = sdlat/sqrt(length(abs(members$geolat)))
      
      meansaturation = mean(members$saturation)
      sdsaturation= sd(members$saturation)
      sesaturation = sdsaturation/sqrt(length(members$saturation))

      meanhue = mean(members$hue)
      sdhue= sd(members$hue)
      sehue = sdhue/sqrt(length(members$hue))

      meanred = mean(members$red)
      sdred = sd(members$red)
      sered= sdred/sqrt(length(members$red))

      meangreen = mean(members$green)
      sdgreen = sd(members$green)
      segreen = sdgreen/sqrt(length(members$green))

      meanblue = mean(members$blue)
      sdblue = sd(members$blue)
      seblue = sdblue/sqrt(length(members$blue))

      meansolar = mean(members$solar)
      sdsolar = sd(members$solar)
      sesolar = sdsolar/sqrt(length(members$solar))

      meantemp = mean(members$temperature)
      sdtemp = sd(members$temperature)
      setemp = sdtemp/sqrt(length(members$temperature))

      meanredness = mean(members$rednessHSV)
      sdredness = sd(members$rednessHSV)
      seredness = sdredness/sqrt(length(members$rednessHSV))

      meanorangeness = mean(members$orangenessHSV)
      sdorangeness = sd(members$orangenessHSV)
      seorangeness = sdorangeness/sqrt(length(members$orangenessHSV))

      meanyellowness = mean(members$yellownessHSV)
      sdyellowness = sd(members$yellownessHSV)
      seyellowness = sdyellowness/sqrt(length(members$yellownessHSV))

      meanbrownness = mean(members$brownnessHSV)
      sdbrownness = sd(members$brownnessHSV)
      sebrownness = sdbrownness/sqrt(length(members$brownnessHSV))

      meandarkbrownness = mean(members$darkbrownnessHSV)
      sddarkbrownness = sd(members$darkbrownnessHSV)
      sedarkbrownness = sddarkbrownness/sqrt(length(members$darkbrownnessHSV))

      meanbrownblackness = mean(members$brownblacknessHSV)
      sdbrownblackness = sd(members$brownblacknessHSV)
      sebrownblackness = sdbrownblackness/sqrt(length(members$brownblacknessHSV))

      meanblueness = mean(members$bluenessHSV)
      sdblueness = sd(members$bluenessHSV)
      seblueness = sdblueness/sqrt(length(members$bluenessHSV))

      meangreenness = mean(members$greennessHSV)
      sdgreenness = sd(members$greennessHSV)
      segreenness = sdgreenness/sqrt(length(members$greennessHSV))

      meanpurpleness = mean(members$purplenessHSV)
      sdpurpleness = sd(members$purplenessHSV)
      sepurpleness = sdpurpleness/sqrt(length(members$purplenessHSV))

      meanpixSD = mean(members$pixSD)
      sdpixSD = sd(members$pixSD)
      sepixSD = sdpixSD/sqrt(length(members$pixSD))

      meanpixUsed = mean(members$pixUsed)
      sdpixUsed = sd(members$pixUsed)
      sepixUsed = sdpixUsed/sqrt(length(members$pixUsed))

      row = cbind(term,samplesize,meanlightness,sdlightness,selightness,meanlat, sdlat, selat, meanaltitude,sdaltitude,sealtitude,meansaturation,sdsaturation,sesaturation,meanhue,sdhue,sehue, meanred,sdred,sered,meangreen,sdgreen,segreen,meanblue,sdblue,seblue,meansolar,sdsolar, sesolar, meantemp,sdtemp, setemp)
      row = cbind(row, meanredness, sdredness, seredness, meanorangeness, sdorangeness, seorangeness, meanyellowness, sdyellowness, seyellowness, meanbrownness, sdbrownness, sebrownness, meandarkbrownness, sddarkbrownness, sedarkbrownness, meanbrownblackness, sdbrownblackness, sebrownblackness)
      row = cbind(row, meanblueness, sdblueness, seblueness, meangreenness, sdgreenness, segreenness, meanpurpleness, sdpurpleness,sepurpleness, meanpixSD, sdpixSD, sepixSD, meanpixUsed, sdpixSD, sepixSD, numvalidtaxa)

      subset = rbind(subset,row)
    }
  }
  
  
  subset$samplesize = as.numeric(as.character(subset$samplesize))
  subset$meanlightness = as.numeric(as.character(subset$meanlightness))
  subset$sdlightness = as.numeric(as.character(subset$sdlightness))
  subset$selightness = as.numeric(as.character(subset$selightness))
  
  subset$meanaltitude = as.numeric(as.character(subset$meanaltitude))
  subset$sdaltitude = as.numeric(as.character(subset$sdaltitude))
  subset$sealtitude = as.numeric(as.character(subset$sealtitude))
  
  subset$meanlat = as.numeric(as.character(subset$meanlat))
  subset$sdlat = as.numeric(as.character(subset$sdlat))
  subset$selat = as.numeric(as.character(subset$selat))
  
  subset$meansaturation = as.numeric(as.character(subset$meansaturation))
  subset$sdsaturation = as.numeric(as.character(subset$sdsaturation))
  subset$sesaturation = as.numeric(as.character(subset$sesaturation))

  subset$meanhue = as.numeric(as.character(subset$meanhue))
  subset$sdhue = as.numeric(as.character(subset$sdhue))
  subset$sehue = as.numeric(as.character(subset$sehue))

  subset$meanred = as.numeric(as.character(subset$meanred))
  subset$sdred = as.numeric(as.character(subset$sdred))
  subset$sered = as.numeric(as.character(subset$sered))

  subset$meangreen = as.numeric(as.character(subset$meangreen))
  subset$sdgreen = as.numeric(as.character(subset$sdgreen))
  subset$segreen = as.numeric(as.character(subset$segreen))

  subset$meanblue = as.numeric(as.character(subset$meanblue))
  subset$sdblue = as.numeric(as.character(subset$sdblue))
  subset$seblue = as.numeric(as.character(subset$seblue))

  subset$meanpixSD = as.numeric(as.character(subset$meanpixSD))
  subset$sdpixSD = as.numeric(as.character(subset$sdpixSD))
  subset$sepixSD = as.numeric(as.character(subset$sepixSD))

  subset$meanpixUsed = as.numeric(as.character(subset$meanpixUsed))
  subset$numvalidtaxa = as.numeric(as.character(subset$numvalidtaxa))

  subset$meantemp = as.numeric(as.character(subset$meantemp))
  subset$meansolar = as.numeric(as.character(subset$meansolar))
  
  dim(subset)
  return(subset)
}