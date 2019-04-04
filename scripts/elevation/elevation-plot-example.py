"""
Created by Théo Larue on 03/04/2019

Script used for testing and playing around with the SRTMv3 data, exploited through the open-elevation
open source api.
At the time this code is writtent the api is hosted locally, however it is also available online.
(full documentation on https://open-elevation.com)
"""

import requests
import sys
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from scipy.interpolate import griddata

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
ip = "192.168.1.27:8080"  # ip (or url) of the api


def get_elevation(lat, lon, ip):
    """
     script for getting elevation from lat, long, based on open elevation data
     which in turn is based on SRTM

    :param lat: latitude
    :param lon: longitude
    :param ip: ip or url where the api is hosted
    :return: the evelation of the point
    """
    query = ('http://{}/api/v1/lookup?locations={},{}'.format(ip, lat, lon))
    r = requests.get(query).json()
    return r["results"][0]["elevation"]


def arcsec_to_deg(arc):
    return 0.000277778 * arc


# center
lat = 45.917677
lon = 6.866667

# Paramaters in arcseconds, then converted to degrees
# 1 arcsecond is roughly equivalent to 30m on the surface
# The dataset has a resolution of 1 arcsecond, going below that leads to modelisation problems.
# In order to get a higher resolution, the data is interpolated.
radius_arc = 10
radius = arcsec_to_deg(radius_arc)
res_arc = 1
resolution = arcsec_to_deg(res_arc)

# 3d plotting
fig = plt.figure()
ax = plt.axes(projection="3d")

X = np.arange(lat - radius, lat + radius, resolution)
Y = np.arange(lon - radius, lon + radius, resolution)

logging.info("Downloading the data...")
ZZ = np.asarray([[get_elevation(x, y, ip) for x in X] for y in Y])
XX, YY = np.meshgrid(X, Y)
# surf = ax.plot_surface(XX, YY, Z, cmap='gist_earth')
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.show()

logging.info("Interpolation in progress...")
Z = ZZ.flatten()
xi = np.linspace(X.min(), X.max(), (len(Z) / 3))
yi = np.linspace(Y.min(), Y.max(), (len(Z) / 3))
zi = griddata((XX.flatten(), YY.flatten()), Z, (xi[None, :], yi[:, None]), method='cubic')
xig, yig = np.meshgrid(xi, yi)
surf = ax.plot_surface(xig, yig, zi, cmap='gist_earth')
ax.plot([lat], [lon], [get_elevation(lat, lon, ip)], marker='o', markersize=5, color='r')  # center
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_title('Terrain topography, source : SRTM v3 (Nasa), one side = {}m'.format(radius_arc * 30))
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Elevation (m)')

plt.show()
