
#z transform and range a column

scaleRange <- function(column){
column = colorlocated$solar
column <<- scale(column)
View(column)
range01 <- function(x){(x-min(x))/(max(x)-min(x))}
column <<- range01(column)
View(column)
return(column)
}