#simple confidence interval 

nrow(colorspecimensworkers)
mean(colorspecimensworkers$lightness)
sd(colorspecimensworkers$lightness)
mean(colorspecimensmales$lightness)
a <- 0.40
s <- 0.09
n <- 39323
error <- qnorm(0.975)*s/sqrt(n)
left <- a-error
right <- a+error
left
right
