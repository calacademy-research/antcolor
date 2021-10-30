library("openxlsx", lib.loc="~/R/win-library/3.5")

#write a df to a .xlsx

write2Excel <- function(df){
write.xlsx(df, "C:/Users/OWNER/Desktop/data.xlsx")
}
#"C:/Users/OWNER/Desktop/data.xlsx"