"""
Web scraping of skitour.com, in order to find data on outings having a negative avalanch activity.
Gets data like location (approximate), date, inclination

Created on 18/02/19
Author : Théo Larue
"""

from bs4 import BeautifulSoup # Parsing library for html files
import requests # Enable us to use html resquests
import re # Regular expressions)

last_page = 121 # TODO : find automatically the number of pages

# Adress where you can find the outings
URL = 'http://www.skitour.fr/conditions/'

# Key words used to determine if there was an avalanch activity
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
                    parse_outing(outing, ref)

"""
Parses the outing from the website into a dictionnary, whose fields describe the activity
(date, approximate location, value of the inclination)

Argument :
    outing : BeautifulSoup object representing the negative activity detected
    ref : reference to the content to be parsed
"""
def parse_outing(outing, ref):
    req = requests.get("{}{}".format(URL, ref))
    soup = BeautifulSoup(req.text, "lxml")

    date = re.search("Sortie du (.*)par", soup.title.text).group(1)
    print(date)

find_negatives(last_page, key_words)
