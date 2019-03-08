"""
Some tools used here and there in the rest of the library.
Created on 23/02/19
Author : Antoine SANNER
"""
import re
from pandas import DataFrame


class ParsingException(Exception):
    pass


class DataFormatException(Exception):
    @staticmethod
    def assert_format(pattern, text, error_msg):
        """
        Asserts that a text follows a given pattern and raises an exception if not
        :type pattern: str
        :param pattern: a regular expression describing the pattern
        :type text: str
        :param text: the text which should be checked
        :type error_msg: str
        :param error_msg: the error message which should be displayed if the text does not match the pattern
        """
        if not re.match(pattern, text):
            raise DataFormatException(error_msg + " (" + text + ")")


def is_keyset_filtered(keyset):
    """
    Checks if a keys et is filtered ie it is a subset of FILTERED_TABLE_COLUMN_NAMES.
    :type keyset: set
    :param keyset: a key set:
    :rtype bool
    :return a boolean indicating if the keyset is filtered.
    """
    return keyset == set(FILTERED_TABLE_COLUMN_NAMES)


def is_dataframe_filtered(df):
    """
    Checks if the DataFrame's column names are filtered.
    :type df: DataFrame
    :param df: a DataFrame
    :rtype bool
    :return a boolean indicating if the DataFrame is filtered.
    """
    return is_keyset_filtered(set(df.columns))


def is_keyset_pretty(keyset):
    """
    Checks if a keys et is pretty ie it is a subset of PRETTIFIED_TABLE_COLUMN_NAMES.
    :type keyset: set
    :param keyset: a key set:
    :rtype bool
    :return a boolean indicating if the keyset is pretty.
    """
    return keyset == set(PRETTIFIED_TABLE_COLUMN_NAMES)


def is_dataframe_pretty(df):
    """
    Checks if the DataFrame's column names are pretty.
    :type df: DataFrame
    :param df: a DataFrame
    :rtype bool
    :return a boolean indicating if the DataFrame is pretty.
    """
    return is_keyset_pretty(set(df.columns))


def get_dataframe_prettiness(df):
    """
    Returns the DataFrame's prettiness level.
    :type df: DataFrame
    :param df: a DataFrame
    :rtype int
    :return returns the DataFrame's prettiness level.
    """
    if is_dataframe_pretty(df):
        return 2
    if is_dataframe_filtered(df):
        return 1
    return 0


# List of the names used in the filtered dataset
FILTERED_TABLE_COLUMN_NAMES = ["id", "date1", "date2", "releaseAlt", "runoutAlt", "oppSlope", "flatArea", "length",
                               "width", "height", "type", "groundVisibility", "wettness", "path", "aerosol",
                               "snowDeposit", "3DaysSnowDepth", "3DaysStrongWind", "3DaysWindDirection",
                               "3DaysMildWeather", "3DaysRain", "4HoursSnow", "4HoursRain", "4HoursStrongWind",
                               "4HoursClearSky", "4HoursClouds", "4HoursFog", "natural", "accidental", "artificial",
                               "unknown", "noVictim", "injured", "dead", "noDammage", "construction", "poles", "forest",
                               "roads", "rivers", "visibility", "alertEventDB"]


# List of the names used in the prettified dataset
# If there are multiple keys in a single line,
# it means that the data found in one column has been split in multiple fields
PRETTIFIED_TABLE_COLUMN_NAMES = ["siteNum", "id",  # Site
                                 "date1",  # Dates
                                 "date2",
                                 "releaseAlt",  # Altitudes
                                 "runoutAlt",
                                 "oppSlope",
                                 "flatArea",
                                 "length",  # Dépots
                                 "width",
                                 "height",
                                 "type",  # Caractéristiques
                                 "groundVisibility",
                                 "wetness",
                                 "path",
                                 "aerosol",
                                 "snowDeposit",
                                 "3DaysSnowDepthMin", "3DaysSnowDepthMax",  # Météo 3 jours précédents
                                 "3DaysStrongWind",
                                 "3DaysWindNorth", "3DaysWindEast", "3DaysWindSouth", "3DaysWindWest",
                                 "3DaysMildWeather",
                                 "3DaysRain",
                                 "4HoursSnow",  # Météo 4 heures précédentes
                                 "4HoursRain",
                                 "4HoursStrongWind",
                                 "4HoursClearSky",
                                 "4HoursClouds",
                                 "4HoursFog",
                                 "natural",  # Causes
                                 "accidental",
                                 "artificial",
                                 "unknown",
                                 "noVictim",  # Victimes
                                 "injured",
                                 "dead",
                                 "noDamage",  # Dégats ou lieux atteints
                                 "construction",
                                 "poles",
                                 "forest",
                                 "roads",
                                 "rivers",
                                 "visibility",  # Obs
                                 "alertEventDB"]
