
#removes outliers by genera above q4 + 1.5q or below q1 - 1.5q

# list of column names on which to remove outliers
vars <- c("lightness")

# store outliers for removal
Outliers <- c()

#filter for genus
terms = colorspecimens[!(is.na(colorspecimens$genus)), ]
terms = terms$genus
terms = terms[!duplicated(terms)]

#for every genus
for(term in terms)
{
  #all specimens of the genus
  members = dplyr::filter(colorspecimens, grepl(term, genus))
  if(nrow(members) >= 5)
  {
    for(i in vars){
      
      # Get the Min/Max values
      max <- quantile(members[,i],0.75, na.rm=TRUE) + (IQR(members[,i], na.rm=TRUE) * 1.5 )
      min <- quantile(members[,i],0.25, na.rm=TRUE) - (IQR(members[,i], na.rm=TRUE) * 1.5 )
      
      # Get the id's using which
      idx <- which(members[,i] < min | members[,i] > max)
      
      # Output the number of outliers in each variable
      print(members$genus[1])
      print(paste(i, length(idx), sep=''))
      
      # Append the outliers list
      Outliers <- c(Outliers, idx) 
    }
  }
}

# Sort, I think it's always good to do this
Outliers <- sort(Outliers)

# Remove the outliers
xoutliers <- colorspecimens[-Outliers,]

#plot distribution and IQR of input and with outliers removed
par(mfrow=c(1, 2))
plot(density(colorspecimens$lightness), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(colorspecimens$lightness), 2)))
polygon(density(colorspecimens$lightness), col="red")
plot(density(xoutliers$lightness), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(xoutliers$lightness), 2)))
polygon(density(xoutliers$lightness), col="red")
boxplot(xoutliers$lightness, main="", sub=paste("Outlier rows: ", boxplot.stats(xoutliers$lightness)$out))
