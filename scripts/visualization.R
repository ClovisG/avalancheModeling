######################################################
#Positiv data
data = read.csv("data/all_data.csv")
######################################################
#Load weather forecast module
source("scripts/consolid_data/netcdf_to_frames.R")
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