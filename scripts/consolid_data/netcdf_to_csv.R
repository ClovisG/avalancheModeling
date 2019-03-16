getw# TODO : comment the code
library(RNetCDF)

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
  
  csv_path <- "./" # TODO : find the right path
  csv_name <- "test0.csv" # TODO : find the right name
  csv_file <- paste(csv_path, csv_name, sep = "")
  write.table(na.omit(data_fram),csv_file, row.names=FALSE, sep=",")
}

# TODO : tests

# open a netcdf file 
#ncin <- open.nc("../data/forecast/adaptor.mars.internal-1552154124.7698312-30208-13-7fa26858-6")
ncin <- open.nc("projet/download/download0.nc")

