#bayes factor example
install.packages('BayesFactor')
library(BayesFactor)


df <- rbind(colorspecimens[colorspecimens$caste == 'worker',],colorspecimens[colorspecimens$caste == 'male',])
df <- data.frame(df$lightness,df$caste)
df <- df[complete.cases(df),]
bf <- ttestBF(formula = df.lightness ~ df.caste, rscale = 1,data = df)

colnames(df) <- c('lightness','caste')
View(df)
df$caste <- as.factor(df$caste)
t.test(lightness ~ caste, data = df, var.eq=TRUE)
cor.test(df$lightness, df$caste)

samples = ttestBF(x = sleep$extra[sleep$group==1],
                  y = sleep$extra[sleep$group==2], paired=TRUE,
                  posterior = TRUE, iterations = 1000)
plot(samples[,"mu"])
# }
bf <- ttestBF(formula = df.lightness ~ df.caste, nullInterval = 0, rscale = 1,data = df, posterior = TRUE, iterations = 1000)
plot(bf)
