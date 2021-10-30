#export for digital repository

colorspecimensexport <- colorspecimens

library(dplyr)

colorspecimensexport <- select(colorspecimensexport, -c(60:80))
View(colorspecimensexport)
colorspecimensexport <- colorspecimensexport[,c(1:51,65,59,52:64)]
colorspecimensexport <- select(colorspecimensexport, -c(61))

options(java.parameters = "-Xmx8000m")
write.csv2(colorspecimensexport, "C:/Users/OWNER/Desktop/data.csv")
library(xlsx)
write.xlsx(colorspecimensexport, "C:/Users/OWNER/OneDrive - Hendrix College/Desktop/data.xlsx")
its ht ewrong fucking path u IDIIOT