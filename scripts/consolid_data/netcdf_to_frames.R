# From netcdf file to data frame store in csv file
# library(RNetCDF)
# Build a data frame from a NetCDF and store the data frame like a csv file
# nc_to_csv<-function(ncin) {
#   names <- NULL
#   long <-  var.get.nc(ncin, 0)
#   names <- c(names, var.inq.nc(ncin, 0)$name)
#   lat <-  lat <- var.get.nc(ncin, 1)
#   names <- c(names, var.inq.nc(ncin, 1)$name)
#   data <-  as.matrix(expand.grid(long,lat))
#   nvars <- file.inq.nc(ncin)$nvar
#   for (var in 3:(nvars-1)) {
#     var_data <- var.get.nc(ncin, var)
#     names <- c(names, var.inq.nc(ncin, var)$name)
#     data <- cbind(data, as.vector(var_data))
#   }
#   print(dim(data))
#   data_fram <- as.data.frame(data)
#   names(data_fram) <- names
#   
#   csv_path <- "~/2A_cours/Avanlaches/scripts/consolid_data/" 
#   csv_name <- "test.csv"
#   csv_file <- paste(csv_path, csv_name, sep = "")
#   write.table(na.omit(data_fram),csv_file, row.names=FALSE, sep=" ")
# }
# 
# #test
# 
# # open a netcdf file 
# ncin <- open.nc("~/2A_cours/Avanlaches/scripts/consolid_data/test.nc")
# 
# nc_to_csv(ncin)
# 
# # class data frame 
# data<-read.csv(file = "~/2A_cours/Avanlaches/scripts/consolid_data/test.csv", sep = " ")
# 
# # print the firs line
# data[1,]

#Get a data depending on (lon,lat,day)
#format: "month/day/year"
getData<-function(lon, lat, day, df){
  if (lon>13.75 || lon<5.25){
    cat("Error: longitude out of range \n")
    break;
  }
  if (lat>49.25 || lat<40.5){
    cat("Error: latitude out of range \n")
    break;
  }
  days = getNbDays(day)
  if(days < 1 || days > 5943){
    cat("Error: date out of range \n")
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
  return(df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,(start+2):(end+2)])
}

#Function that returns the values for the variables during the last nb.months prior to argument date
#Coordinates have to be rounded ! 
monthsMeans<-function(nb.months,lon,lat,day,df){
  start = as.integer(getNbDays(dates(day)-nb.months*28))
  if (start<0){
    start = 1
  }
  end = as.integer(getNbDays(dates(day)))
  if (end>getNbDays(dates("04/30/2018")+2)){
    cat("Error: data non available \n")
  }

  values = df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,(start+2):(end+2)]
  return(apply(values,1,mean))
}

#format: "month/day/year"
#Much more complicated because we gave gaps in our data so we have to count these gaps...
#TODO 
getNbDays<-function(date){
  #We have to substract the number of days between 10/01/xx and 30/04/xx per year
  const = 154
  end = dates(date)
  start = dates("01/01/1991")
  years = as.integer((end-start)%/%365)
  return (end-(start+years*const))
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
  print(nc)
  
  # Variables
  t2m <- "t2m"
  cdir <- "cdir"
  lsp <- "lsp"
  lsf <- "lsf"
  rsn <- "rsn"
  sd <- "sd"
  smlt <- "smlt"
  
  #get longitude
  lon <- ncvar_get(nc, "longitude")         
  nlon <- dim(lon)
  head(lon)
  
  #get latitude
  lat <- ncvar_get(nc, "latitude")
  nlat <- dim(lat)
  head(lat)
  
  print(c(nlon,nlat))
  
  #get time
  time <- ncvar_get(nc, "time")
  tunits <- ncatt_get(nc,"time","units")
  nt<- dim(time)
  head(time)
  nt
  tunits
  
  nt<- dim(time)
  head(time)
  
  t2m_df = getDataframe(nc, t2m, time, lon, lat, nlon, nlat)
  cdir_df = getDataframe(nc, cdir, time, lon, lat, nlon, nlat)
  lsp_df = getDataframe(nc, lsp, time, lon, lat, nlon, nlat)
  lsf_df = getDataframe(nc, lsf, time, lon, lat, nlon, nlat)
  rsn_df = getDataframe(nc, rsn, time, lon, lat, nlon, nlat)
  sd_df = getDataframe(nc, sd, time, lon, lat, nlon, nlat)
  smlt_df = getDataframe(nc, smlt, time, lon, lat, nlon, nlat)

  return (list("t2m"=t2m_df,"cdir"=cdir_df,"lsp"=lsp_df,"lsf"=lsf_df,"rsn"=rsn_df,"sd"=sd_df,"smlt"=smlt_df))
}

frames=getFrames()

t2m_df=frames$t2m

getData(8,49,"01/03/1991",t2m_df)
lastDays(2,8,49,"01/03/1991",t2m_df)
lastDays(2,8,49,"04/30/2018",t2m_df)


monthsMeans(3,8,49,"01/03/1991",t2m_df)
monthsMeans(3,8,49,"04/30/2005",t2m_df)
monthsMeans(3,7,45.75,"04/30/2018",t2m_df)
