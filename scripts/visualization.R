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
t2m_6_df = get_t2m("t2m_6.nc")
t2m_16_df = get_t2m("t2m_16.nc")
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
neg = data[-which(data$avalanche==1),]
pos = as.data.frame(pos)
neg = as.data.frame(neg)
plot(pos$orientation)

pos = pos[(substr(pos$date, 1, 2) %in% c("10","11","12","01","02","03","04")),] #because it didn't properly worked in format_data
pos = pos[(substr(pos$date, 7, 10) %in% c("1991","1992","1993","1994","1995",
                                         "1996","1997","1998","1999","2000",
                                         "2001","2002","2003","2004","2005",
                                         "2006","2007","2008","2009","2010",
                                         "2011","2012","2013","2014","2014",
                                         "2015","2016","2017","2018")),]       #because it didn't properly worked in format_data

neg = neg[(substr(neg$date, 1, 2) %in% c("10","11","12","01","02","03","04")),] #because it didn't properly worked in format_data
neg = neg[(substr(neg$date, 7, 10) %in% c("1991","1992","1993","1994","1995",
                                         "1996","1997","1998","1999","2000",
                                         "2001","2002","2003","2004","2005",
                                         "2006","2007","2008","2009","2010",
                                         "2011","2012","2013","2014","2014",
                                         "2015","2016","2017","2018")),] 

###################################################################################################################################
#Means for positive events: MONTH
###################################################################################################################################
#t2m_month_mean = c()
lsf_month_mean = c()
lsp_month_mean = c()
sd_month_mean = c()
rsn_month_mean = c()
cat("Start : positive events : MONTHS \n")
for(i in 1:dim(pos)[1]){
  if(i%%1000 == 0){print(i)}
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  date = toString(pos$date[i])
  #t2m_month_mean<-c(t2m_month_mean,monthsMeans(1,lon,lat,date,t2m_df))
  sd_month_mean<-c(sd_month_mean,monthsMeans(1,lon,lat,date,sd_df))
  rsn_month_mean<-c(rsn_month_mean,monthsMeans(1,lon,lat,date,rsn_df))
  lsf_month_mean<-c(lsf_month_mean,monthsMeans(1,lon,lat,date,lsf_df))
  lsp_month_mean<-c(lsp_month_mean,monthsMeans(1,lon,lat,date,lsp_df))
  
}

#######################################################################################################################################
#Means for POSITIVE events: DAYS
#######################################################################################################################################
t2m_6_w_mean = c()
t2m_16_w_mean = c()
lsf_w_mean = c()
lsp_w_mean = c()
sd_w_mean = c()
rsn_w_mean = c()
cdir_w_mean = c()
cat("Start : positive events : DAYS \n")
for(i in 1:dim(pos)[1]){
  if(i%%1000 == 0){print(i)}
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  date = toString(pos$date[i])
  t2m_6_w_mean<-c(t2m_6_w_mean,daysMeans(3,lon,lat,date,t2m_6_df))
  t2m_16_w_mean<-c(t2m_16_w_mean,daysMeans(3,lon,lat,date,t2m_16_df))
  #sd_w_mean<-c(sd_w_mean,daysMeans(2,lon,lat,date,sd_df))
  #rsn_w_mean<-c(rsn_w_mean,daysMeans(2,lon,lat,date,rsn_df))
  #lsf_w_mean<-c(lsf_w_mean,daysMeans(2,lon,lat,date,lsf_df))
  #lsp_w_mean<-c(lsp_w_mean,daysMeans(2,lon,lat,date,lsp_df))
  #cdir_w_mean<-c(cdir_w_mean,daysMeans(2,lon,lat,date,cdir_df))
  
}



#######################################################################################################################################
#Means for NEGATIVE events: DAYS
#######################################################################################################################################
t2m_6_w_mean_neg = c()
t2m_16_w_mean_neg = c()
lsf_w_mean_neg = c()
lsp_w_mean_neg = c()
sd_w_mean_neg = c()
rsn_w_mean_neg = c()
cdir_w_mean_neg = c()
cat("Start : negative events : DAYS \n")
for(i in 1:dim(pos)[1]){
  if(i%%1000 == 0){print(i)}
  lon = roundCoord(neg$long[i])
  lat = roundCoord(neg$lat[i])
  date = toString(neg$date[i])
  t2m_6_w_mean_neg<-c(t2m_6_w_mean_neg,daysMeans(3,lon,lat,date,t2m_6_df))
  t2m_16_w_mean_neg<-c(t2m_16_w_mean_neg,daysMeans(3,lon,lat,date,t2m_16_df))
  #sd_w_mean_neg<-c(sd_w_mean_neg,daysMeans(3,lon,lat,date,sd_df))
  #rsn_w_mean_neg<-c(rsn_w_mean_neg,daysMeans(3,lon,lat,date,rsn_df))
  #lsf_w_mean_neg<-c(lsf_w_mean_neg,daysMeans(3,lon,lat,date,lsf_df))
  #lsp_w_mean_neg<-c(lsp_w_mean_neg,daysMeans(3,lon,lat,date,lsp_df))
  #cdir_w_mean_neg<-c(cdir_w_mean_neg,daysMeans(3,lon,lat,date,cdir_df))
  
}


#######################################################################################################################################
#Plots
#######################################################################################################################################



hist(t2m_6_w_mean_neg, xlab='6 am. temperature mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(t2m_6_w_mean, xlab='6 am. temperature mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(t2m_16_w_mean_neg, xlab='16 am. temperature mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(t2m_16_w_mean, xlab='16 am. temperature mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(lsf_w_mean_neg, xlab='large scale snow fall mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(lsf_w_mean, xlab='large sclae snow fall mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(lsp_w_mean_neg, xlab='large scale precipitation mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(lsp_w_mean, xlab='large sclae snow precipitation mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(sd_w_mean_neg, xlab='snow depth mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(sd_w_mean, xlab='snow depth mean', col=rgb(1,0,0,1/4), main='3 days prior to event', prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(rsn_w_mean_neg, xlab='snow density mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(rsn_w_mean, xlab='snow density mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(cdir_w_mean_neg, xlab='clear sky direct solar radiation at surface', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(cdir_w_mean, xlab='clear sky direct solar radiation at surface', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
egend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


