#Use if you need to tranfer R data to Elastic, for example if running new analyses in R

forelastic = subset

elastic("http://localhost:9200", "speciessubset4", "species") %index% forelastic

cor(colorspecimens$green,colorspecimens$blue)
