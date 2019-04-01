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
cdir_df = weather.df$cdir
#large_scale_precipitation
lsp_df = weather.df$lsp
#large_scale_snowfall
lsf_df = weather.df$lsf
#snow_density
rsn_df = weather.df$rsn
#snow_depth
sd_df = weather.df$sd
#snowmelt
smlt_df = weather.df$smlt



head(data)

#Only datavalanche and EPA have an information about the orientation so this plot isn't relevant
pos = data[-which(data$avalanche==0),] # delete the with 0 in long (lat also)
pos = as.data.frame(pos)
plot(pos$orientation)

pos = pos[(substr(pos$date, 1, 2) %in% c("10","11","12","01","02","03","04")),] #because it didn't properly worked in format_data

###################################################################################################################################
#Plot some means for positiv events: MONTH
###################################################################################################################################
t2m_month_mean = c()
lsf_month_mean = c()
lsp_month_mean = c()
sd_month_mean = c()
rsn_month_mean = c()
for(i in 1:dim(pos)[1]){
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  date = toString(pos$date[i])
  t2m_month_mean<-c(t2m_month_mean,monthsMeans(1,lon,lat,date,t2m_df))
  sd_month_mean<-c(sd_month_mean,monthsMeans(1,lon,lat,date,sd_df))
  rsn_month_mean<-c(rsn_month_mean,monthsMeans(1,lon,lat,date,rsn_df))
  lsf_month_mean<-c(lsf_month_mean,monthsMeans(1,lon,lat,date,lsf_df))
  lsp_month_mean<-c(lsp_month_mean,monthsMeans(1,lon,lat,date,lsp_df))
  
}

hist(t2m_month_mean, xlab='t2m mean', main='1 month prior to positiv event')
hist(lsf_month_mean, xlab='lsf mean', main='1 month prior to positiv event')
hist(lsp_month_mean, xlab='lsp mean', main='1 month prior to positiv event')
hist(sd_month_mean, xlab='sd mean', main='1 month prior to positiv event')
hist(rsn_month_mean, xlab='rsn mean', main='1 month prior to positiv event')

#######################################################################################################################################
#Plot some means for positiv events: WEEK
#######################################################################################################################################
t2m_w_mean = c()
lsf_w_mean = c()
lsp_w_mean = c()
sd_w_mean = c()
rsn_w_mean = c()
for(i in 1:dim(pos)[1]){
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  date = toString(pos$date[i])
  t2m_w_mean<-c(t2m_w_mean,daysMeans(7,lon,lat,date,t2m_df))
  sd_w_mean<-c(sd_w_mean,daysMeans(7,lon,lat,date,sd_df))
  rsn_w_mean<-c(rsn_w_mean,daysMeans(7,lon,lat,date,rsn_df))
  lsf_w_mean<-c(lsf_w_mean,daysMeans(7,lon,lat,date,lsf_df))
  lsp_w_mean<-c(lsp_w_mean,daysMeans(7,lon,lat,date,lsp_df))
  
}

hist(t2m_w_mean, xlab='t2m mean', main='1 week prior to positiv event')
hist(lsf_w_mean, xlab='lsf mean', main='1 week prior to positiv event')
hist(lsp_w_mean, xlab='lsp mean', main='1 week prior to positiv event')
hist(sd_w_mean, xlab='sd mean', main='1 week prior to positiv event')
hist(rsn_w_mean, xlab='rsn mean', main='1 week prior to positiv event')
