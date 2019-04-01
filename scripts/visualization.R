library(ggplot2)
######################################################
#Positiv data
data = read.csv("../data/all_data.csv")
data=data[,-1]

# marking the psoitiveness of those events
names(data) = c("avalanche", "orientation", "date", "long", "lat")

######################################################
#Load weather forecast module
source("consolid_data/netcdf_to_frames.R")
weather.df = getFrames()
#2m_temperature
t2m_df = weather.df$t2m
#clear_sky_direct_solar_radiation_at_surface
cdir = weather.df$cdir
#large_scale_precipitation
lsp = weather.df$lsp
#large_scale_snowfall
lsf = weather.df$lsf
#snow_density
rsn = weather.df$rsn
#snow_depth
sd = weather.df$sd
#snowmelt
smlt = weather.df$smlt



head(data)

#Only datavalanche and EPA have an information about the orientation so this plot isn't relevant
pos = data[-which(data$avalanche==0),] # delete the with 0 in long (lat also)
pos = as.data.frame(pos)
plot(pos$orientation)

pos = pos[(substr(pos$date, 1, 2) %in% c("10","11","12","01","02","03","04")),] #because it didn't properly worked in format_data


#Calcul some variables for positiv events
t2m_means = c()
for(i in 1:length(pos)){
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  print(lon)
  print(lat)
  date = toString(pos$date[i])
  print(date)
  t2m_means<-c(monthsMeans(3,lon,lat,date,t2m_df))
}

