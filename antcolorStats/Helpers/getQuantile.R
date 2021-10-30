
#get subset above and below the specified quantile (qval)

getQuantile <- function(df, column, qval, under) {

q = quantile(column, qval,na.rm = TRUE)

if(under){
inquantile = df[column < q, ] 
}
else{
inquantile = df[column > q, ]
}

return (inquantile)
} 

#q <- quantile(df[, field],qval)