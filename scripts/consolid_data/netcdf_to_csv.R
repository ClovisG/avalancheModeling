# From netcdf file to data frame store in csv file

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
  print(dim(data))
  data_fram <- as.data.frame(data)
  names(data_fram) <- names
  
  csv_path <- "~/2A_cours/Avanlaches/scripts/consolid_data/" 
  csv_name <- "test.csv"
  csv_file <- paste(csv_path, csv_name, sep = "")
  write.table(na.omit(data_fram),csv_file, row.names=FALSE, sep=" ")
}

#test

# open a netcdf file 
ncin <- open.nc("~/2A_cours/Avanlaches/scripts/consolid_data/test.nc")

nc_to_csv(ncin)

# class data frame 
data<-read.csv(file = "~/2A_cours/Avanlaches/scripts/consolid_data/test.csv", sep = " ")

# print the firs line
data[1,]