this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

# Data collection


##########################################################
# EPA
#epa.raw = read.csv("../data/epa/epa.csv")


##########################################################
# EPA Belledone
epa.belledone.raw = read.csv("../data/epa/epa_belledone.csv")


##########################################################
# Datavalanche
datavalanche.raw = read.csv("../data/datavalanche/datavalanche.csv")

# keeping only the usefull predictors
datavalanche.names2keep = c("Orientation", "Date", "longitude", "latitude")
datavalanche.reduced = subset(datavalanche.raw, select = datavalanche.names2keep)

# marking the psoitiveness of those events
datavalanche.reduced = cbind(factor(rep(1, dim(datavalanche.reduced)[1])), datavalanche.reduced)
names(datavalanche.reduced) = c("avalanche", "orientation", "date", "long", "lat")
  
convert_date_datavalanche = function(old.date.string){
  old.date = strsplit(old.date.string, "/")[[1]]
  
  day = old.date[1]
  month = old.date[2]
  year = old.date[3]
  
  new.date.string = paste(month, day, year, sep="/")
  
  return(new.date.string)
}

new.dates = c()
for (i in 1:dim(datavalanche.reduced)[1]){
  new.dates[i] = convert_date_datavalanche(
    as.character(
      (datavalanche.reduced$date)[i]
    )
  )
}
datavalanche.reduced$date = new.dates



##########################################################
# Skitour

skitour.raw = read.csv("../data/skitour/skitour.csv")
skitour.names2keep = c("orientation", "date", "long_depart", "lat_depart")
skitour.reduced = subset(skitour.raw, select = skitour.names2keep)

skitour.reduced = cbind(factor(rep(0, dim(skitour.reduced)[1])), skitour.reduced)
names(skitour.reduced) = c("avalanche", "orientation", "date", "long", "lat")


convert_date_skitour = function(old.date.string){
  old.date = strsplit(old.date.string, " ")[[1]]
  
  day = old.date[1]
  months = c("01", "02", "03", "04", "05", "05", "06", "07", "08", "09", "10", "11", "12")
  months.string = c("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre")
  month = months[which(months.string == old.date[2])]
  year = old.date[3]
  
  new.date.string = paste(month, day, year, sep="/")
  
  return(new.date.string)
}

new.dates = c()
for (i in 1:dim(skitour.reduced)[1]){
  new.dates[i] = convert_date_skitour(
                                        as.character(
                                          (skitour.reduced$date)[i]
                                          )
                                      )
}
skitour.reduced$date = new.dates

#Only from October 1st to April 30
skitour.reduced <- skitour.reduced[skitour.reduced$date %in% c("10","11","12","01","02","03","04")]

global.data = rbind(skitour.reduced, datavalanche.reduced)

#At last do not keep events which aren't from the alps
#Rewrite code
for (i in 1:dim(global.data)[1]){
  lon = global.data[i,4]
  lat = global.data[i,5]
  if (lon>13.75 || lon<5.25 || is.na(lon)){
    global.data<-global.data[c(-i),]
  }
  else if (lat>49.25 || lat<40.5 || is.na(lat)){
    global.data<-global.data[c(-i),]
  }
}

write.csv(global.data, "../data/all_data.csv")
sum(global.data$avalanche == 0)
