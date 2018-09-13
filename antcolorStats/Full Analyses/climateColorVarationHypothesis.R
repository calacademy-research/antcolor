
#Hypothesis- groups that show greater variation in the temperatures at which they are located will show greater variation in lightness
df = colorlocated1workers

df <- dplyr::filter(df, grepl('worker', caste)) #set to desired field and value
df <- dplyr::filter(df, grepl(FALSE, fossil)) #set to desired field and value

#df = df[complete.cases(df$solar), ]
df = df[complete.cases(df$temperature), ]

source("Helpers/prepareSubsetDataframe.R")
df <- prepareSubsetDataframe(df= df,subsetBy= 'genus',threshold = 25)
View(df)

df$sdsolar = as.numeric(as.character(df$sdsolar))
df$sdtemp = as.numeric(as.character(df$sdtemp))
df$sdlightness = as.numeric(as.character(df$sdlightness))
df$sdbrownness = as.numeric(as.character(df$sdbrownness))

plot(df$sdsolar, df$sdbrownness,log="")
reg <- lm(sdbrownness ~ sdsolar,data=df) 
summary(reg)
abline(reg)

plot(df$sdsolar, df$sdbrownness,log="")
reg <- lm(sdbrownness ~ sdsolar,data=df) 
summary(reg)
abline(reg)