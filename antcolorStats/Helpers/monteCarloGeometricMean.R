
data <- read.csv('C:/Users/OWNER/Desktop/Book1.csv')
#Monte-Carlo geometric mean
mcgm <- function(R, A, B, numiters)
{
  min_e <- c(rep(1,35))
  bestx <- 1
  for(i in 1:numiters)
  {
    x <- runif(1,0,1)
    AB <- (A^x) * (B^(1-x))
    e <- abs(R - AB)
    if(sum(e^2) < sum(min_e^2))
    {
      min_e <- e
      bestx <- x
    }
  }
  return(c(min_e, bestx))
}

result <- mcgm(data[1],data[2],data[3],1000)
View(result[1][["X0.01533"]])

R <- data[1]
A <- data[2]
B <- data[3]
View(data)
nrow(R)
#R
#A
#B
numiters <- 10000
min_e <- c(rep(1,35))
bestx <- 1
for(i in 1:numiters)
{
  x <- runif(1,0,1)
  AB <- (A^x) * (B^(1-x))
  e <- abs(R - AB)
  if(sum(e^2) < sum(min_e^2))
  {
    min_e <- e
    bestx <- x
  }
}
min_e
bestx
