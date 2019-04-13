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

suppNA<-function(x){
  clean_x = c()
  for(i in 1:length(x)){
    if(is.null(x[i]) || !is.na(x[i])){
      clean_x = c(clean_x,x[i])
    }
  }
  return(clean_x)
}

#######################################################################################################################################
#Means for POSITIVE events: DAYS
#######################################################################################################################################
t2m_6_w_mean = c()
t2m_16_w_mean = c()
#lsf_w_mean = c()
#lsp_w_mean = c()
#sd_w_mean = c()
#rsn_w_mean = c()
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
  #rsn_w_mean<-c(rsn_w_mean,daysMeans(3,lon,lat,date,rsn_df))
  #lsf_w_mean<-c(lsf_w_mean,daysMeans(3,lon,lat,date,lsf_df))
  #lsp_w_mean<-c(lsp_w_mean,daysMeans(3,lon,lat,date,lsp_df))
  cdir_w_mean<-c(cdir_w_mean,daysMeans(3,lon,lat,date,cdir_df))
  
}



#######################################################################################################################################
#Means for NEGATIVE events: DAYS
#######################################################################################################################################
t2m_6_w_mean_neg = c()
t2m_16_w_mean_neg = c()
#lsf_w_mean_neg = c()
#lsp_w_mean_neg = c()
#sd_w_mean_neg = c()
#rsn_w_mean_neg = c()
cdir_w_mean_neg = c()
cat("Start : negative events : DAYS \n")
for(i in 1:dim(neg)[1]){
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
  cdir_w_mean_neg<-c(cdir_w_mean_neg,daysMeans(3,lon,lat,date,cdir_df))
}


#######################################################################################################################################
#Means for POSITIVE events: D-DAY
#######################################################################################################################################
#t2m_6_d = c()
#t2m_16_d = c()
#lsf_d = c()
#lsp_d = c()
sd_d = c()
rsn_d = c()
#cdir_d = c()
cat("Start : positive events : D-DAY \n")
for(i in 1:dim(pos)[1]){
  if(i%%1000 == 0){print(i)}
  lon = roundCoord(pos$long[i])
  lat = roundCoord(pos$lat[i])
  date = toString(pos$date[i])
  #t2m_6_d<-c(t2m_6_d,getData(lon,lat,date,t2m_6_df))
  #t2m_16_d<-c(t2m_16_d,getData(lon,lat,date,t2m_16_df))
  sd_d<-c(sd_d,getData(lon,lat,date,sd_df))
  rsn_d<-c(rsn_d,getData(lon,lat,date,rsn_df))
  #lsf_w_mean<-c(lsf_w_mean,daysMeans(2,lon,lat,date,lsf_df))
  #lsp_w_mean<-c(lsp_w_mean,daysMeans(2,lon,lat,date,lsp_df))
  #cdir_d<-c(cdir_d,getData(lon,lat,date,cdir_df))
  
  #cdir_val = getData(lon,lat,date,cdir_df)                     #cdir data is polluted
  #if(!is.null(cdir_val)){
  #  if(cdir_val < 300 && !is.na(cdir_val)){
  #    cdir_d<-c(cdir_d,getData(lon,lat,date,cdir_df))
  #  }
  #}
}



#######################################################################################################################################
#Means for NEGATIVE events: D-DAY
#######################################################################################################################################
#t2m_6_d_neg = c()
#t2m_16_d_neg = c()
#lsf_d = c()
#lsp_d = c()
sd_d_neg = c()
rsn_d_neg = c()
#cdir_d_neg = c()
cat("Start : negative events : D-DAY \n")
for(i in 1:dim(neg)[1]){
  if(i%%1000 == 0){print(i)}
  lon = roundCoord(neg$long[i])
  lat = roundCoord(neg$lat[i])
  date = toString(neg$date[i])
  #t2m_6_d_neg<-c(t2m_6_d_neg,getData(lon,lat,date,t2m_6_df))
  #t2m_16_d_neg<-c(t2m_16_d_neg,getData(lon,lat,date,t2m_16_df))
  sd_d_neg<-c(sd_d_neg,getData(lon,lat,date,sd_df))
  rsn_d_neg<-c(rsn_d_neg,getData(lon,lat,date,rsn_df))
  #lsf_w_mean<-c(lsf_w_mean,daysMeans(2,lon,lat,date,lsf_df))
  #lsp_w_mean<-c(lsp_w_mean,daysMeans(2,lon,lat,date,lsp_df))
  #cdir_d_neg<-c(cdir_d_neg,getData(lon,lat,date,cdir_df))
  
  #cdir_val = getData(lon,lat,date,cdir_df)
  #if(!is.null(cdir_val)){
  #  if(cdir_val < 300 && !is.na(cdir_val)){
  #    cdir_d_neg<-c(cdir_d_neg,getData(lon,lat,date,cdir_df))
  #  }
  #}
}

#######################################################################################################################################
#ROC curves: functions
#######################################################################################################################################
#input parameters: 
# vector of weather variable for events
# min and max value for this variable (250 and 300 for t2m_16)
#output: a vector of couples (E(s),R(s)) ready for plotting
rep<-function(events, min, max){
  F = c()
  norm = length(events)
  for(s in min:max){
    F = c(F,sum(events>s)/norm)
  }
  return(F)
}

den<-function(events, min, max){
  f = c()
  norm = length(events)
  for(s in min:max-1){
    f = c(f,sum((events>s)&&(events<s+1))/norm)
  }
  return(f)
}

#plot roc curve
roc<-function(min,max,pos,neg, step){
  chosen = sample(1:length(pos), size=length(neg))
  pos.reduced = pos[chosen]
  tp = c()
  tn = c()
  fp = c()
  fn = c()
  for(s in seq(min,max,by=step)){
    tp=c(tp,sum(pos.reduced>=s))
    fp=c(fp,sum(neg>s))
    tn=c(tn,sum(neg<=s))
    fn=c(fn,sum(pos.reduced<s))
  }
  #true positive rate
  tpr=tp/(tp+tn)
  #false positive rate
  fpr=fp/(fp+fn)
  plot(fpr,tpr,type="o",col="blue")
}

#######################################################################################################################################
#Plots
#######################################################################################################################################



hist(t2m_6_w_mean_neg, xlab='6 am. temperature mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(t2m_6_w_mean, xlab='6 am. temperature mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topleft", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(t2m_16_w_mean_neg, xlab='16 am. temperature mean', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(t2m_16_w_mean, xlab='16 am. temperature mean', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topleft", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


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

clean_cdir = suppNA(cdir_d)/10
clean_cdir_neg = suppNA(cdir_d_neg)/10
hist(clean_cdir, xlab='clear sky direct solar radiation at surface', col=rgb(0,0,1,1/4), main='3 days prior to event', prob=T)
hist(clean_cdir_neg, xlab='clear sky direct solar radiation at surface', col=rgb(1,0,0,1/4), main='3 days prior to event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(t2m_6_d_neg, xlab='6 am. temperature', col=rgb(0,0,1,1/4), main='day of event', prob=T)
hist(t2m_6_d, xlab='6 am. temperature', col=rgb(1,0,0,1/4), main='day of the event', add=T, prob=T)
legend("topleft", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(t2m_16_d_neg, xlab='16 pm. temperature', col=rgb(0,0,1,1/4), main='day of event', prob=T)
hist(t2m_16_d, xlab='16 pm. temperature', col=rgb(1,0,0,1/4), main='day of the event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))


hist(sd_d_neg, xlab='snow depth', col=rgb(0,0,1,1/4), main='day of event', prob=T)
hist(sd_d, xlab='snow depth', col=rgb(1,0,0,1/4), main='day of the event', add=T, prob=T)
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))

hist(rsn_d_neg, xlab='snow density', col=rgb(0,0,1,1/4), main='day of event', prob=T, ylim=c(0, 0.007))
hist(rsn_d, xlab='snow density', col=rgb(1,0,0,1/4), main='day of the event', add=T, prob=T, ylim = c(0, 0.007))
legend("topright", c("negative",'positive'), col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), lty=c(1,1))

#######################################################################################################################################
#ROC curves
#######################################################################################################################################

#set the mins maxs and pas for each variables
min_t2m_6 = 240
max_t2m_6 = 290
step_t2m_6 = 2

min_t2m_16 = 250
max_t2m_16 = 300
step_t2m_16 = 1

min_sd = 0
max_sd =0.47
step_sd =0.03

min_rsn = 99
max_rsn = 450
step_rsn = 20

min_lsp = 0
max_lsp = 0.0028
step_lsp = 0.0001
  
max_lsf = 0.0028
min_lsf = 0
step_lsf = 0.0001

max_cdir = 304449
min_cdir = 72557
step_cdir = 10000
  
#ROC t2m_6_d
clean_t2m_6_w_mean = suppNA(t2m_6_w_mean)
clean_t2m_6_w_mean_neg = suppNA(t2m_6_w_mean_neg)
roc(min_t2m_6, max_t2m_6, clean_t2m_6_w_mean, clean_t2m_6_w_mean_neg, step_t2m_6)
title(main="ROC for t2m at 6 am means, 3 days prior to event")

#ROC t2m_16_d
clean_t2m_16_w_mean = suppNA(t2m_16_w_mean)
clean_t2m_16_w_mean_neg = suppNA(t2m_16_w_mean_neg)
roc(min_t2m_16, max_t2m_16, clean_t2m_16_w_mean, clean_t2m_16_w_mean_neg, step_t2m_16)
title(main="ROC for t2m at 4 pm means, 3 days prior to event")
  
#ROC rsn_d
roc(min_rsn, max_rsn, rsn_d, rsn_d_neg, step_rsn)
title(main="ROC for rsn, day of the event")
  
#ROC sd_d
roc(min_sd, max_sd, sd_d, sd_d_neg, step_sd)
title(main="ROC for sd, day of the event")  

#ROC lsp
#We have to clean the vectors from NAs...
clean_lsp_w_mean = suppNA(lsp_w_mean)
clean_lsp_w_mean_neg = suppNA(lsp_w_mean_neg)
roc(min_lsp, max_lsp, clean_lsp_w_mean, clean_lsp_w_mean_neg, step_lsp)
title(main="ROC for lsp means, 3 days prior to event")  

#ROC lsf
#We have to clean the vectors from NAs...
clean_lsf_w_mean = suppNA(lsf_w_mean)
clean_lsf_w_mean_neg = suppNA(lsf_w_mean_neg)
roc(min_lsf, max_lsf, clean_lsf_w_mean, clean_lsf_w_mean_neg, step_lsf)
title(main="ROC for lsf means, 3 days prior to event")  

#ROC cdir
#We have to clean the vectors from NAs...
clean_dir 
clean_dir_neg
roc(min_cdir, max_cdir, clean_cdir, clean_cdir_neg, step_cdir)
title(main="ROC for cdir means, 3 days prior to event")  
