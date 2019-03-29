

# Data collection

#epa.raw = read.csv("../data/epa/epa.csv")

##########################################################
# Datavalanche
datavalanche.raw = read.csv("../data/datavalanche/datavalanche.csv")

# keeping only the usefull predictors
datavalanche.names2keep = c("Orientation", "Date", "longitude", "latitude")
datavalanche.reduced = subset(datavalanche.raw, select = datavalanche.names2keep)

# marking the psoitiveness of those events
datavalanche.reduced = cbind(factor(rep(1, dim(datavalanche.reduced)[1])), datavalanche.reduced)
names(datavalanche.reduced) = c("avalanche", "orientation", "date", "long", "lat")
  

##########################################################
# Skitour
skitour.raw = read.csv("../data/skitour/skitour.csv")
skitour.names2keep = c("orientation", "date", "avg_long", "avg_lat")
skitour.reduced = subset(skitour.raw, select = skitour.names2keep)

skitour.reduced = cbind(factor(rep(1, dim(skitour.reduced)[1])), skitour.reduced)

convert_date = function(old.date.string){
  old.date = strsplit(old.date.string, " ")
  day = old.date[1]
  month = months.string[which(months.string == old.date[2])]
  months = c("01", "02", "03", "04", "05", "05", "06", "07", "08", "09", "10", "11", "12")
  months.string = c("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre")
  paste(day, month, year, sep="/")
}


for (i in 1:dim(skitour.reduced)[1]){
  skitour.reduced$date[i] = convert_date(levels(skitour.reduced$date[i]))
}
