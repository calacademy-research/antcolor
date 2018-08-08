#WIP code to plot bar graphs with standard error

forbars = subset
forbars <- forbars[order(forbars$meanlightness),] 
forbars$term = factor(forbars$term, levels = forbars$term[order(forbars$meanlightness)])
forbars$meanlightness <- factor(forbars$meanlightness, levels = forbars$meanlightness[order(forbars$meanlightness)])
forbars$name  # notice the changed order of factor levels
View(forbars)

ordered = 
ggplot(forbars) +
  geom_bar(aes(x=reorder(meanlightness, -table(term)[term]), y=meanlightness), stat="identity", fill="skyblue", alpha=0.7) +
  geom_errorbar( aes(x=term, ymin=meanlightness - selightness, ymax=meanlightness + selightness), width=0.4, colour="orange", alpha=0.9, size=1.3)