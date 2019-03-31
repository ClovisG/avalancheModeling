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
  df[16*(13.75-5)*(49.25-lat)+4*(lon-5.25)+1,days+3]
}

#format: "month/day/year"
getNbDays<-function(date){
  return (dates(c(date))-dates(c("01/01/1991")))
}

writeCsv<-function(df){
  # write out the dataframe as a .csv file
  csvpath <- ""
  csvname <- "weather.csv"
  csvfile <- paste(csvpath, csvname, sep="")
  print(csvfile)
  write.table(na.omit(df),csvfile, sep=", ",row.names=FALSE)
}

getDataframe<-function(var, time, lon, lat, nlon, nlat){
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
  #setwd("Documents/2A/Avalanches/projet")
  # load some packages
  library(chron)
  library(lattice)
  library(RColorBrewer)
  library(ncdf4)
  nc <- nc_open("download/weather.nc")
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
  
  t2m_df = getDataframe(t2m, time, lon, lat, nlon, nlat)
  cdir_df = getDataframe(cdir, time, lon, lat, nlon, nlat)
  lsp_df = getDataframe(lsp, time, lon, lat, nlon, nlat)
  lsf_df = getDataframe(lsf, time, lon, lat, nlon, nlat)
  rsn_df = getDataframe(rsn, time, lon, lat, nlon, nlat)
  sd_df = getDataframe(sd, time, lon, lat, nlon, nlat)
  smlt_df = getDataframe(smlt, time, lon, lat, nlon, nlat)

  return (list("t2m"=t2m_df,"cdir"=cdir_df,"lsp"=lsp_df,"lsf"=lsf_df,"rsn"=rsn_df,"sd"=sd_df,"smlt"=smlt_df))
}

frames=getFrames()

t2m_df=frames$t2m
getData(8,49,"01/03/1991",t2m_df)
