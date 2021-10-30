#Adds a numeric date column and examines effect of date on lightness
date <- colorspecimensworkers$dateCollectedStart
date <- substr(date, start = 0, stop = 4)
date <- as.numeric(date)
colorspecimensworkers$date <- date
plot(colorspecimensworkers$lightness, colorspecimensworkers$date, ylim= c(1850,2050))
reg1 <- lm(saturation ~ date, data = colorspecimensworkers)
summary(reg1)
