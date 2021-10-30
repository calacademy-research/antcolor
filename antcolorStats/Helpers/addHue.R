library(plotwidgets)

colorspecimens$hue <- NA

for (i in 1:nrow(colorspecimens))
{
  brow <- colorspecimens[i,]
  rgb = rbind(brow$red, brow$green, brow$blue)
  bgenus <- brow$genus
  hsl = rgb2hsl(rgb)
  colorspecimens[i,86] = hsl[1,1]
}