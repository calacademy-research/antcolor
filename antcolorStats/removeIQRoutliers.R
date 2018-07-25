
# Create a variable/vector/collection of the column names you want to remove outliers on.
vars <- c("lightness")

# Create a variable to store the row id's to be removed
Outliers <- c()

# Loop through the list of columns you specified
for(i in vars){
  
  # Get the Min/Max values
  max <- quantile(colorlocated[,i],0.75, na.rm=TRUE) + (IQR(colorlocated[,i], na.rm=TRUE) * 1.5 )
  min <- quantile(colorlocated[,i],0.25, na.rm=TRUE) - (IQR(colorlocated[,i], na.rm=TRUE) * 1.5 )
  
  # Get the id's using which
  idx <- which(colorlocated[,i] < min | colorlocated[,i] > max)
  
  # Output the number of outliers in each variable
  print(paste(i, length(idx), sep=''))
  
  # Append the outliers list
  Outliers <- c(Outliers, idx) 
}

# Sort, I think it's always good to do this
Outliers <- sort(Outliers)

# Remove the outliers
xoutliers <- colorlocated[-Outliers,]

#plot distribution and IQR of sampled set
par(mfrow=c(1, 2))  # divide graph area in 2 columns
plot(density(xoutliers$lightness), main="", ylab="y", sub=paste("Skewness:", round(e1071::skewness(xoutliers$lightness), 2)))
polygon(density(xoutliers$lightness), col="red")
boxplot(xoutliers$lightness, main="", sub=paste("Outlier rows: ", boxplot.stats(xoutliers$lightness)$out))