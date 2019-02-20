"""
Web scraping of skitour.com, in order to find data on outings having a negative avalanch activity.
Gets data like location (approximate), date, inclination, orientation.

Created on 18/02/19
Author : Théo Larue
"""

from bs4 import BeautifulSoup # Parsing library for html files
import requests # Enable us to use html resquests
import re # Regular expressions)
import logging, sys # For debugging information

logging.basicConfig(stream = sys.stderr, level=logging.DEBUG)

last_page = 121 # TODO : find automatically the number of pages

# Adress where you can find the outings
URL = 'http://www.skitour.fr/conditions/'

parsed_events = []

# Key words used to determine if there was an avalanch activity
# Idea : usage of a python library in order to match words close to the ones referenced in the
# txt file, in case of typos for example
with open("mots-cles-neg.txt") as f:
    key_words = f.read().splitlines()

"""
Finds all the fields that represent a negative value (relative to avalanch activity) and
parses the field into a list of dictionaries

Note : the words matching is not fully operational, as it recognizes words like "orientation"
because of the "rien" key word, which is not what we want to recognize.

Arguments :
        last_page : number of the last page of the website
        key_words : the words used to determine if the activity was negative
"""
def find_negatives(last_page, key_words):
    # This loop gets the contents of the avalanche activity section of the tour reports
    for i in range(1, last_page+1):
        # Download of the web page
        req = requests.get("{}?p={}".format(URL, i))
        # Parsing of the page using lxml parser
        soup = BeautifulSoup(req.text, "lxml")
        outings = soup.find("div", {"id": "cont"}).find("div", {"class": "cadre"}, recursive = False)
        for title in outings.findChildren("h4", recursive = False):
            ref = title.find("a")["href"] # Adress to the actual content of the outing
            outing = title.findNext("ul")
            if("avalancheuse" in outing.text):
                match = re.search('Activité avalancheuse observée :(.*)Skiabilité', outing.text)
                # Check if the activity is negative
                if(match != None and any(word in match.group(1) for word in key_words)):
                    logging.info("Parsing {}".format(ref))
                    parsed_events.append(parse_outing(ref))
                    logging.info("Done.\n")

"""
Parses the outing from the website into a dictionnary, whose fields describe the activity
(date, approximate location, value of the inclination)

Arguments :
    outing : BeautifulSoup object representing the negative activity detected
    ref : reference to the content to be parsed

Returns :
    A dictionnary containing some data found on the page.
"""
def parse_outing(ref):
    data = {}

    req = requests.get("{}{}".format(URL, ref))
    soup = BeautifulSoup(req.text, "lxml")

    date = re.search("Sortie du (.*)par", soup.title.text).group(1)
    data["date"] = date

    # The general informations are situated in the first "table" tag
    outing_data = soup.find("table")
    massif = outing_data.find("strong",text="Massif : ").nextSibling
    orientation = outing_data.find("strong",text="Orientation : ").nextSibling
    data["massif"] = massif
    data["orientation"] = orientation
    # Sometimes the sector is not specified
    secteur = outing_data.find("strong",text="Secteur : ")
    if(secteur != None):
        data["secteur"] = secteur.nexSibling
    else:
        data["secteur"] = ""
        logging.info("No sector data for {}".format(ref))

    # Parsing of the gps coordinates
    link_to_location = outing_data.find("strong",text="Départ : ").findNext("a")
    coordinates = parse_starting_point(link_to_location["href"])
    data["depart"] = coordinates

    logging.debug(data)
    return data

"""
Parses a page describing a location, and returns the gps coordinates of that location
"""
def parse_starting_point(ref):
    req = requests.get("{}{}".format(URL, ref))
    soup = BeautifulSoup(req.text, "lxml")
    coords = {}

    coordinates = soup.find("abbr", {"title": "WGS84"})
    if(coordinates != None):
        coordinates = coordinates.nextSibling
        logging.debug("Coordonnees : {}".format(coordinates))
        coords["lat"] = re.search(" : (.*) N", coordinates).group(1)
        coords["lon"] = re.search(" / (.*) E", coordinates).group(1)
        logging.debug("Latitude : {}".format(coords["lat"]))
        logging.debug("Longitude : {}".format(coords["lon"]))
    else:
        logging.info("No coordinates for {}".format(ref))
        coords["lat"] = ""
        coords["lon"] = ""

    return coords


find_negatives(last_page, key_words)
