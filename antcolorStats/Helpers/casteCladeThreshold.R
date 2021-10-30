
#Creates a dataframe of all clades (genus, scientificName etc.) that meet the threshold of specimens for all castes
casteCladeThreshold <- function(cladetype, min_threshold, comparison_type = 1){
  source("Helpers/prepareSubsetDataframe.R")
  source("Helpers/oldSubset.R")
  colorspecimensworkersclades<- prepareSubsetDataframe(df= colorspecimensworkers,subsetBy= cladetype,threshold = min_threshold)
  colorspecimensmalesclades<- prepareSubsetDataframe(df= colorspecimensmales,subsetBy= cladetype,threshold = min_threshold)
  colorspecimensqueensclades<- prepareSubsetDataframe(df= colorspecimensqueens,subsetBy= cladetype,threshold = min_threshold)
  
  if(comparison_type == 1)
  {
  castecladesthreshed <- merge(colorspecimensworkersclades,colorspecimensmalesclades, by= "term")
  castecladesthreshed <- merge(castecladesthreshed, colorspecimensqueensclades, by = "term")
  }
  if(comparison_type == 2)
  {
    castecladesthreshed <- merge(colorspecimensworkersclades,colorspecimensmalesclades, by= "term")
  }
  if(comparison_type == 3)
  {
    castecladesthreshed <- merge(colorspecimensworkersclades,colorspecimensqueensclades, by= "term")
  }
  if(comparison_type == 4)
  {
    castecladesthreshed <- merge(colorspecimensqueensclades,colorspecimensmalesclades, by= "term")
  }
  return(castecladesthreshed)
}