"""
Web scraping of skitour.com, in order to find data on outings having a negative avalanch activity.
Gets data like location (approximate), date, inclination, orientation.

Created on 18/02/19
Author : Théo Larue
"""

import logging  # For debugging information
import re  # Regular expressions)
import pickle
import csv
import sys

import requests  # Enables us to use html resquests
from bs4 import BeautifulSoup  #  Parsing library for html files

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
    req = requests.get(URL + "?lim=")
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
        req = requests.get("{}?lim=&p={}".format(URL, i))
        soup = BeautifulSoup(req.text, "lxml")
        outings = soup.find("table", {"class": "topos"}).find_all('a')[10:]

        for outing_ref in outings:
            ref = outing_ref["href"]  # Adress to the actual content of the outing
            event = parse_outing(ref, key_words)
            logging.info("Parsing {}".format(ref))
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
    data = {}

    logging.debug(URL + "../" + ref)
    req = requests.get("{}".format(URL + "../" + ref))
    soup = BeautifulSoup(req.text, "lxml")

    topo_neige = soup.find("div", {"class": "neige_topo"}).getText()
    activity = re.search("Activité avalancheuse observée : (.*)Skiabilité", topo_neige)
    if not (activity is not None and any(word in activity.group(1) for word in key_words)):
        # if an avalanche activity is detected, do not parse.
        return None

    date = re.search("Sortie du (.*)par", soup.title.text).group(1)
    data["date"] = date

    # The general informations are situated in the first "table" tag
    outing_data = soup.find("table")
    massif = outing_data.find("strong", text="Massif : ").nextSibling
    orientation = outing_data.find("strong", text="Orientation : ").nextSibling
    data["massif"] = massif
    data["orientation"] = orientation

    # Sometimes the sector is not specified
    secteur = outing_data.find("strong", text="Secteur : ")
    if secteur:
        data["secteur"] = secteur.nextSibling
    else:
        data["secteur"] = ""

    # Parsing of the gps coordinates
    link_to_location = outing_data.find("strong", text="Départ : ").findNext("a")
    coordinates = parse_starting_point(link_to_location["href"])
    data["lat_depart"], data["lon_depart"] = coordinates

    # Parsing of the inclination
    inclination = outing_data.find("strong", text="Pente : ").nextSibling
    data["pente"] = inclination

    data["activity"] = activity.group(1)

    return data


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


def do_parsing(stride=200):
    """
    Launches the parsing of the entire website
    :param stride: number of pages to store on each csv file (each page of the website contains 30 outings)
    By default, stride=200
    :return:
    """
    n = find_last_page()

    for j, i in enumerate(range(1, n, stride)):
        events = []
        start = i
        end = min(i + stride - 1, n)
        parse_html(start, end, negative_activity_key_words, events)

        filename = "events{}".format(j)
        logging.info("Dumping pages {} to {} into {}.csv...".format(start, end, filename))
        with open("{}.csv".format(filename), "w") as file:
            writer = csv.DictWriter(file, events[0].keys())
            writer.writeheader()
            writer.writerows(events)
        logging.info("")

    logging.info("Paring Done.")


do_parsing()
