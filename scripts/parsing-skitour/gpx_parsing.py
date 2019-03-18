"""
Test script for quick gps parsing, in order to get the position of the slopes from a gpx file
Computes the mean coordinates of the gps trace
"""

import logging  # For debugging information
import sys

import gpxpy

# Comment or uncomment if you want debug information
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def mean_coordinates(filename):
    """
    Computes the mean coordinates and elevation of a .gpx file.
    :param filename: .gpx file to be parsed
    :return:
    """
    logging.info("file : {}".format(filename))

    lat_mean = 0
    long_mean = 0
    alt_mean = 0
    n = 0  # Number of points in the route

    with open(filename, 'r') as fin:
        gpx = gpxpy.parse(fin)
        points = []

        routes_nb = len(gpx.routes)
        if routes_nb > 0:
            points = gpx.routes[0].points
            if routes_nb > 1:
                logging.warning("{} routes found in the gpx file".format(routes_nb))

        tracks_nb = len(gpx.tracks)
        if tracks_nb > 0:
            points = gpx.tracks[0].segments[0].points
            if tracks_nb > 1:
                logging.warning("{} tracks found in the gpx file".format(tracks_nb))
            if len(gpx.tracks[0].segments) > 1:
                logging.warning("{} segments found in the track".format(len(gpx.tracks[0].segments)))

        n = len(points)
        logging.info("Number of points : {}".format(n))

        for point in points:
            lat_mean += point.latitude
            long_mean += point.longitude
            alt_mean += point.elevation

        lat_mean /= n
        long_mean /= n
        alt_mean /= n
        logging.debug("Moyennes : lat {} long {} alt {}".format(lat_mean, long_mean, alt_mean))

        return lat_mean, long_mean, alt_mean
