"""
Web scraping of skitour.com, in order to find data on outings having a negative avalanch activity.
Gets data like location (approximate), date, inclination, orientation.

Created on 18/02/19
Author : Théo Larue
"""

import csv
import logging  # For debugging information
import os
import re  # Regular expressions)
import sys

import requests  # Enables us to use html resquests
from bs4 import BeautifulSoup  #  Parsing library for html files

from gpx_parsing import *

sys.setrecursionlimit(10000)

# Comment or uncomment if you want debug information
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Adress where you can find the outings
URL = 'http://www.skitour.fr/topos/dernieres-sorties/'

# Key words used to determine if there was an avalanch activity
# Idea : usage of a python library in order to match words close to the ones referenced in the
# txt file, in case of typos for example
with open("mots-cles-neg.txt") as f:
    negative_activity_key_words = f.read().splitlines()


def find_last_page():
    """
    Returns the number of the last html page of the website. Used in 'find_negatives'
    """
    req = requests.get(URL + "?lim=&nbr=50")
    soup = BeautifulSoup(req.text, "lxml")

    n = int(soup.find("a", string="Suivante").findPrevious("a").text)

    logging.info("Found {} pages to parse\n".format(n))
    return n


def parse_html(first_page, last_page, key_words, parsed_events):
    """
    Finds all the fields that represent a negative value (relative to avalanch activity) and
    parses the field into a list of dictionaries

    Note : the words matching is not fully operational, as it recognizes words like "orientation"
    because of the "rien" key word, which is not what we want to recognize.

    Arguments :
            first page, last_page : interval of pages to parse, last_page included
            key_words : the words used to determine if the activity was negative
            parsed_events : the list where the parsed events are to be stored
    """
    # There are a lot of pages, and on every page, a few ski outings to parse
    for i in range(first_page, last_page + 1):
        logging.info("Parsing page {} out of {}".format(i, last_page))
        req = requests.get("{}?lim=&nbr=50&p={}".format(URL, i))
        soup = BeautifulSoup(req.text, "lxml")
        outings = soup.find("table", {"class": "topos"}).find_all('a')[10:]

        for outing_ref in outings:
            ref = outing_ref["href"]  # Adress to the actual content of the outing
            logging.info("Parsing {}".format(ref))
            event = parse_outing(ref, key_words)
            if event is not None:
                parsed_events.append(event)
                logging.debug(parsed_events[-1])
        logging.info("")


def parse_outing(ref, key_words):
    """
    Parses the outing from the website into a dictionnary, whose fields describe the activity
    (date, approximate location, value of the inclination)

    Arguments :
        ref : reference to the content to be parsed

    Returns :
        A dictionnary containing some data found on the page.
    """
    # Initialisation
    data = {}

    logging.debug(URL + "../" + ref)
    req = requests.get("{}".format(URL + "../" + ref))
    soup = BeautifulSoup(req.text, "lxml")

    # Detection of avalanch activity
    topo_neige = soup.find("div", {"class": "neige_topo"}).getText()
    activity = re.search("Activité avalancheuse observée : (.*)Skiabilité", topo_neige)
    if not (activity is not None and any(len(re.findall(word, activity.group(1))) > 0 for word in key_words)):
        # if an avalanche activity is detected, do not parse.
        return None

    # Date
    date = re.search("Sortie du (.*)par", soup.title.text).group(1)
    data["date"] = date

    # Mountain chain, sector
    outing_data = soup.find("table")
    massif = outing_data.find("strong", text="Massif : ").nextSibling
    data["massif"] = massif
    # Sometimes the sector is not specified
    secteur = outing_data.find("strong", text="Secteur : ")
    if secteur:
        data["secteur"] = secteur.nextSibling
    else:
        data["secteur"] = ""

    # Orientation
    orientation = outing_data.find("strong", text="Orientation : ").nextSibling
    data["orientation"] = orientation

    # Starting gps coordinates
    link_to_location = outing_data.find("strong", text="Départ : ").findNext("a")
    coordinates = parse_starting_point(link_to_location["href"])
    data["lat_depart"], data["long_depart"] = coordinates

    # Inclination
    inclination = outing_data.find("strong", text="Pente : ").nextSibling
    data["pente_max"] = max_inclination(inclination)

    # Average gps coordinates and altitude for more precise analysis
    gpx_ref = outing_data.find("a", {"title": "Télécharger le fichier GPX pour votre GPS"})
    if gpx_ref is not None:
        gpx = requests.get(URL + "../" + gpx_ref["href"])
        with open("temp.gpx", "w") as fout:
            fout.write(gpx.text)
        try:
            # Sometimes gpx files are not in the right format
            data["avg_lat"], data["avg_long"], data["avg_alt"] = mean_coordinates("temp.gpx")
        except Exception:
            pass
        os.remove("temp.gpx")
    else:
        data["avg_lat"], data["avg_long"], data["avg_alt"] = "", "", ""

    data["activity"] = activity.group(1)

    return data


def max_inclination(user_input):
    """
    Computes the maximum inclination from a natural user input
    :param user_input: text entered by a user about the inclination
    :return: the maximum inclination
    """
    inclination = ""
    matches = re.findall(r"([0-9]{2})(?![0-9]|m)[°\-/ ]?", user_input)
    if len(matches) > 0:
        inclination = max(int(x) for x in matches)
    return inclination


def parse_starting_point(ref):
    """
    Parses a page describing a location, and returns the gps coordinates of that location

    Arguments :
        ref : html reference to the page needing parsing

    Returns :
        A dictionnary containing the latitude and longitude of the location
    """
    logging.debug(URL + "../" + ref)
    req = requests.get("{}".format(URL + "../" + ref))
    soup = BeautifulSoup(req.text, "lxml")
    lat, lon = "", ""

    coordinates = soup.find("abbr", {"title": "WGS84"})
    if coordinates is not None:
        coordinates = coordinates.nextSibling
        logging.debug("Coordonnees : {}".format(coordinates))
        lat = re.search(" : (.*) N", coordinates).group(1)
        lon = re.search(" / (.*) E", coordinates).group(1)
        logging.debug("Latitude : {}".format(lat))
        logging.debug("Longitude : {}".format(lon))

    return lat, lon


def do_parsing(stride=200, first_page = 1, last_page = 0):
    """
    Launches the parsing of the entire website
    :param stride: number of pages to store on each csv file (each page of the website contains 50 outings)
    By default, stride=200
    :return:
    """
    # Setting up
    page_nbr = find_last_page()
    if last_page <= 0 or last_page > page_nbr:
        last_page = page_nbr
    assert first_page <= last_page
    assert stride > 0

    for i in range(first_page, last_page, stride):
        events = []
        start = i
        end = min(i + stride - 1, last_page)
        parse_html(start, end, negative_activity_key_words, events)
        if len(events) == 0:
            continue

        filename = "events{}-{}".format(start, end)
        logging.info("Dumping pages {} to {} into {}.csv...".format(start, end, filename))
        with open("{}.csv".format(filename), "w") as file:
            writer = csv.DictWriter(file, events[0].keys())
            writer.writeheader()
            writer.writerows(events)
        logging.info("")

    logging.info("Parsing Done.")


do_parsing(first_page = 1601)
