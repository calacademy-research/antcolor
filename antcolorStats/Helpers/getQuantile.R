
#get subset above and below the specified quantile (qval)

getQuantile <- function(column, qval, under) {

q = quantile(column, qval)

if(under){
inquantile = df[column < q, ] 
}
else{
inquantile = df[column > q, ]
}

return (inquantile)
} 

#q <- quantile(df[, field],qval)