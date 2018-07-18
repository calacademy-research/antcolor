connect()
jsonspecimens = Search(index= "allants2", size = 100, raw = TRUE)
typeof(jsonspecimens)
print(jsonspecimens)
jsonspecimens <- fromJSON(jsonspecimens)
print(jsonspecimens)
typeof(jsonspecimens)

do.call(rbind, jsonspecimens)
View(jsonspecimens)
nrow(jsonspecimens)

specimensframe <- data.frame(matrix(unlist(jsonspecimens), nrow=132, byrow=T))
View(specimensframe)


jsonspecimens <- lapply(jsonspecimens, function(x) {
  x[sapply(x, is.null)] <- NA
  unlist(x)
})

do.call("rbind", jsonspecimens)

specimensframe <- data.frame(matrix(unlist(jsonspecimens), nrow=132, byrow=T))
View(specimensframe)

do.call("rbind", jsonspecimens)

docs_mget(index = "allants", type = "_doc", fields = "lightness")
docs_get(index = "allants", type = "_doc", id = 'oSxJTWQBFcBa_CYajpGC')
library("tools")
install_github("alexioannides/elasticsearchr")
install.packages("elasticsearchr")
es <- elastic("http://localhost:9200", "allants", "_doc")
queryall <- query('{ "match_all": {}}')
es %search% queryall

