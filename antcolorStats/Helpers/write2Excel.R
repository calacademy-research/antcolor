library("openxlsx", lib.loc="~/R/win-library/3.5")

#write a df to a .xlsx

write2Excel <- function(df,path){
write.xlsx(df, path)
}
#"C:/Users/OWNER/Desktop/data.xlsx"