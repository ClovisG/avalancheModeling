#Get a data depending on (lon,lat,day)
#format: "month/day/year"
getData<-function(lon, lat, day, df){
  if (lon>13.75 || lon<5.25 || is.na(lon)){
    cat("Error: longitude ",lon," out of range \n")
    return(NULL);
  }
  if (lat>49.25 || lat<40.5 || is.na(lat)){
    cat("Error: latitude ",lat," out of range \n")
    return(NULL)
  }
  days = as.integer(getNbDays(day))
  if(days < 1 || days > 5943){
    #cat("Error: date ",day," out of range \n")
    return(NULL)
  }
  df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,days+2]
}

#Function that returns the values for the variables during the last nb.days prior to argument date
#Coordinates have to be rounded !
lastDays<-function(nb.days,lon,lat,day,df){
  start = as.integer(getNbDays(dates(day)-nb.days))
  if (start<0){
    start = 1
  }
  end = as.integer(getNbDays(day))
  if (end>getNbDays(dates("12/31/2018")+2)){
    #cat("Error: data for ",day, " non available \n")
    return(NULL)
  }
  return(df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,(start+2):(end+2)])
}

#Function that returns the values for the variables during the last nb.days prior to argument date
#Coordinates have to be rounded ! 
daysMeans<-function(nb.days,lon,lat,date,df){
  #print(day)
  start = as.integer(getNbDays(dates(date)-nb.days))
  if (start<0){
    start = 1
  }
  end = as.integer(getNbDays(date))
  if (end>getNbDays(dates("12/31/2018")+2)){
    cat("Error: data for ",date, " non available \n")
    return(NULL)
  }
  if (end<0 || end == start){
    return(NULL)
  }
  #cat("start = ",start,"\n")
  #cat("end = ",end,"\n")
  #values = df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,(start+2):(end+2)]
  values = c()
  for(i in 1:(end-start)){
    day = dates(date)-i
    values=c(values,getData(lon,lat,day,df))
  }
  return(mean(values))
}

#format: "month/day/year"
#Much more complicated because we gave gaps in our data so we have to count these gaps...
#TODO 
getNbDays<-function(date){
  #We have to substract the number of days between 10/01/xx and 04/30/xx per year
  const = 153
  end = dates(date)
  start = dates("01/01/1991")
  years = as.integer((end-start+92)%/%365)
  if (end-dates("04/30/1991")>0 && end-dates("12/31/1991")<=0){
    years = 1
  }
  res = end-(start+years*const)+1
  return (res)
}

#Round coordinates for the grid
roundCoord<-function(coord){
  # Integer part
  integer = coord%/%1
  # 2 decimals truncature
  decimals = ((coord-integer)*100)%/%1
  # Convertion into a grid element
  decimals = round(decimals/25)*0.25
  return(integer+decimals)
}


writeCsv<-function(df){
  # write out the dataframe as a .csv file
  csvpath <- ""
  csvname <- "weather.csv"
  csvfile <- paste(csvpath, csvname, sep="")
  print(csvfile)
  write.table(na.omit(df),csvfile, sep=", ",row.names=FALSE)
}

getDataframe<-function(nc, var, time, lon, lat, nlon, nlat){
  # get var
  var_array <- ncvar_get(nc,var)
  varlname <- ncatt_get(nc,var,"long_name")
  dunits <- ncatt_get(nc,var,"units")
  fillvalue <- ncatt_get(nc,var,"_FillValue")
  #dim(t2m_array) #lon*lat*time
  
  nt<- dim(time)
  head(time)
  
  # replace netCDF fill values with NA's
  var_array[var_array==fillvalue$value] <- NA
  
  length(na.omit(as.vector(var_array[,,1])))
  
  # create dataframe -- reshape data
  # reshape the array into vector
  var_vec_long <- as.vector(var_array)
  length(var_vec_long)
  
  # reshape the vector into a matrix
  var_mat <- matrix(var_vec_long, nrow=nlon*nlat, ncol=nt)
  dim(var_mat)
  
  # create a dataframe
  lonlat <- as.matrix(expand.grid(lon,lat))
  var_df <- data.frame(cbind(lonlat,var_mat))
  
  return (var_df)
}


getFrames<-function(){
  cat("Please set your working directory to 'scripts' \n")
  # load some packages
  library(chron)
  library(lattice)
  library(RColorBrewer)
  library(ncdf4)
  nc <- nc_open("../download/weather.nc")
  #print(nc)
  
  # Variables
  cdir <- "cdir"
  lsp <- "lsp"
  lsf <- "lsf"
  rsn <- "rsn"
  sd <- "sd"
  smlt <- "smlt"
  
  #get longitude
  lon <- ncvar_get(nc, "longitude")         
  nlon <- dim(lon)
  #head(lon)
  
  #get latitude
  lat <- ncvar_get(nc, "latitude")
  nlat <- dim(lat)
  #head(lat)
  
  print(c(nlon,nlat))
  
  #get time
  time <- ncvar_get(nc, "time")
  tunits <- ncatt_get(nc,"time","units")
  nt<- dim(time)
  #head(time)
  nt
  tunits
  
  nt<- dim(time)
  #head(time)
  
  cdir_df = getDataframe(nc, cdir, time, lon, lat, nlon, nlat)
  lsp_df = getDataframe(nc, lsp, time, lon, lat, nlon, nlat)
  lsf_df = getDataframe(nc, lsf, time, lon, lat, nlon, nlat)
  rsn_df = getDataframe(nc, rsn, time, lon, lat, nlon, nlat)
  sd_df = getDataframe(nc, sd, time, lon, lat, nlon, nlat)
  smlt_df = getDataframe(nc, smlt, time, lon, lat, nlon, nlat)

  return (list("cdir"=cdir_df,"lsp"=lsp_df,"lsf"=lsf_df,"rsn"=rsn_df,"sd"=sd_df,"smlt"=smlt_df))
}


##Only for t2m : temperature
get_t2m<-function(nc){
  cat("Please set your working directory to 'scripts' \n")
  # load some packages
  library(chron)
  library(lattice)
  library(RColorBrewer)
  library(ncdf4)
  nc <- nc_open(paste("../download/",nc,sep=""))
  print(nc)
  
  # Variables
  t2m <- "t2m"
  
  #get longitude
  lon <- ncvar_get(nc, "longitude")         
  nlon <- dim(lon)
  #head(lon)
  
  #get latitude
  lat <- ncvar_get(nc, "latitude")
  nlat <- dim(lat)
  #head(lat)
  
  print(c(nlon,nlat))
  
  #get time
  time <- ncvar_get(nc, "time")
  tunits <- ncatt_get(nc,"time","units")
  nt<- dim(time)
  #head(time)
  nt
  tunits
  
  nt<- dim(time)
  #head(time)
  
  # get var
  t2m_array <- ncvar_get(nc,t2m)
  t2mlname <- ncatt_get(nc,t2m,"long_name")
  dunits <- ncatt_get(nc,t2m,"units")
  fillvalue <- ncatt_get(nc,t2m,"_FillValue")
  #dim(t2m_array) #lon*lat*time
  
  # replace netCDF fill values with NA's
  t2m_array[t2m_array==fillvalue$value] <- NA
  
  length(na.omit(as.vector(t2m_array[,,1])))
  
  # create dataframe -- reshape data
  # reshape the array into vector
  t2m_vec_long <- as.vector(t2m_array)
  length(t2m_vec_long)
  
  # reshape the vector into a matrix
  t2m_mat <- matrix(t2m_vec_long, nrow=nlon*nlat, ncol=nt)
  dim(t2m_mat)
  
  # create a dataframe
  lonlat <- as.matrix(expand.grid(lon,lat))
  t2m_df <- data.frame(cbind(lonlat,t2m_mat))
  
  return (t2m_df)

}
  
  

frames=getFrames()
lsp_df = frames$lsp

cdir_df = frames$cdir

t2m_6_df=get_t2m("t2m_6.nc")
t2m_16_df=get_t2m("t2m_16.nc")

getData(8,49,"01/01/1991",lsp_df)
lastDays(2,8,49,"01/03/1991",lsp_df)
lastDays(2,8,49,"04/30/2018",lsp_df)

daysMeans(3,7,45.75,"01/02/2018",lsp_df)



