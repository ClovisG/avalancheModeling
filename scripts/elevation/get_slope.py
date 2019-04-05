import csv
import requests
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import geopy.distance


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


def add_slope(filename, ip, lat_ref, lon_ref):
    """
    adds a column with the slope in a new csv
    :param filename: original data
    :param ip: ip (or url) to the open-elevation api
    :param lat_ref: name of the latitude column
    :param lon_ref: name of the longitude column
    :return:
    """
    with open(filename) as data:
        data_reader = csv.DictReader(data, fieldnames=data.readline().split(','), delimiter=',')
        for i, line in enumerate(data_reader):
            latitude = float(line[lat_ref])
            longitude = float(line[lon_ref])
            slope = get_slope(latitude, longitude, ip)
            print(slope)


def arcsec_to_deg(arc):
    """

    :param arc: angle in arcseconds
    :return: its equivalent in degrees
    """
    return 0.000277778 * arc


def meter_to_deg(m):
    """
    :param m: distance in meters
    :return: roughly its equivalent in degrees, to be used in coordinates
    """
    return arcsec_to_deg(m / 30)


def get_slope(lat, lon, ip):
    # we take two points around the center, with a resolution of 1 arcsecond
    radius = arcsec_to_deg(2)
    resolution = arcsec_to_deg(1)

    X = np.arange(lat - radius, lat + radius, resolution)
    Y = np.arange(lon - radius, lon + radius, resolution)
    ZZ = np.asarray([[get_elevation(x, y, ip) for y in Y] for x in X])
    XX, YY = np.meshgrid(X, Y)
    Z = ZZ.flatten()
    Xf, Yf = XX.flatten(), YY.flatten()

    interpolation_res = len(Z)  # resolution of the interpolation
    xi = np.linspace(X.min(), X.max(), interpolation_res)
    yi = np.linspace(Y.min(), Y.max(), interpolation_res)
    xig, yig = np.meshgrid(xi, yi)
    zi = griddata((Xf, Yf), Z, (xig, yig), method="cubic")

    # fig = plt.figure(figsize=plt.figaspect(1))
    # ax = fig.add_subplot(221, projection='3d')
    # surf = ax.plot_surface(XX, YY, ZZ, cmap='gist_earth')
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.title('Original')

    # ax = fig.add_subplot(222, projection='3d')
    # surf = ax.plot_surface(xig, yig, zi, cmap='gist_earth')
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.title('Interpolated')
    # plt.show()

    center_alt = get_elevation(lat, lon, ip)
    slopes = []
    for i, x in enumerate(xi):
        for j, y in enumerate(yi):
            dist = geopy.distance.distance((lat, lon), (x, y)).m
            if dist > 0:
                slope = np.arctan(abs(zi[i][j] - center_alt)/dist)*180/np.pi
                # when the point is too close to the original center
                if slope < 88:
                    slopes.append(slope)

    # has to be improved
    return np.max(slopes)


def main():
    filename = "../../data/datavalanche/datavalanche.csv"
    lat_ref = 'latitude'
    lon_ref = 'longitude\n'
    ip = '192.168.1.27:8080'
    add_slope(filename, ip, lat_ref, lon_ref)


main()
