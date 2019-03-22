getw# TODO : comment the code
library(RNetCDF)
library(ncdf)


# Build a data frame from a NetCDF and store the data frame like a csv file
nc_to_csv<-function(ncin) {
  names <- NULL
  long <-  var.get.nc(ncin, 0)
  names <- c(names, var.inq.nc(ncin, 0)$name)
  lat <-  lat <- var.get.nc(ncin, 1)
  names <- c(names, var.inq.nc(ncin, 1)$name)
  data <-  as.matrix(expand.grid(long,lat))
  
  nvars <- file.inq.nc(ncin)$nvar
  for (var in 3:(nvars-1)) {
    var_data <- var.get.nc(ncin, var)
    names <- c(names, var.inq.nc(ncin, var)$name)
    data <- cbind(data, as.vector(var_data))
  }
  
  data_fram <- as.data.frame(data)
  names(data_fram) <- names
  
  #return(data_fram)
  
  csv_path <- "./" # TODO : find the right path
  csv_name <- "weather.csv" # TODO : find the right name
  csv_file <- paste(csv_path, csv_name, sep = "")
  write.table(na.omit(data_fram),csv_file, row.names=FALSE, sep=",")
}

# TODO : tests

# open a netcdf file 
#ncin <- open.nc("../data/forecast/adaptor.mars.internal-1552154124.7698312-30208-13-7fa26858-6")
setwd("Documents/2A/Avalanches/projet")
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

# get temperature
t2m_array <- ncvar_get(nc,t2m)
t2mlname <- ncatt_get(nc,t2m,"long_name")
dunits <- ncatt_get(nc,t2m,"units")
fillvalue <- ncatt_get(nc,t2m,"_FillValue")
dim(t2m_array) #lon*lat*time

dname <- "t2m"                         # name of variable which can be found by using print(nc)

nt<- dim(time)
head(time)

# load some packages
library(chron)
library(lattice)
library(RColorBrewer)

# convert time -- split the time units string into fields
tustr <- strsplit(tunits$value, " ")
tdstr <- strsplit(unlist(tustr)[3], "-")
tmonth <- as.integer(unlist(tdstr)[2])
tday <- as.integer(unlist(tdstr)[3])
tyear <- as.integer(unlist(tdstr)[1])
chron(time,origin=c(tmonth, tday, tyear))

# replace netCDF fill values with NA's
t2m_array[t2m_array==fillvalue$value] <- NA

length(na.omit(as.vector(t2m_array[,,1])))


# get a single slice or layer (January)
m <- 1
t2m_slice <- t2m_array[,,m]
# quick map
image(lon,rev(lat),t2m_slice, col=rev(brewer.pal(10,"RdBu")))


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

# options(width=96)
head(na.omit(t2m_df, 20))

# write out the dataframe as a .csv file
csvpath <- ""
csvname <- "weather.csv"
csvfile <- paste(csvpath, csvname, sep="")
print(csvfile)
write.table(na.omit(t2m_df),csvfile, sep=",",row.names=FALSE)

