#z transform and range a column
scaled = colorlocated
scaled$lightness = scale(scaled$lightness)
scaled$temperature = scale(scaled$temperature) 
View(scaled)

ranged = scaled
range01 <- function(x){(x-min(x))/(max(x)-min(x))}
ranged$temperature = range01(ranged$temperature)
