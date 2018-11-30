
import sys
import xml.etree.ElementTree
import re
import pickle
import glob
from itertools import chain
from fieldDesc import *


txtFiles = list(chain(*[ glob.glob(globName)  for globName in sys.argv[1:] ]))
print("Files as input:", txtFiles)

def parseFields(line,event):
	for idx,field in enumerate(orderedFields):
		if field!="last":
			nextField=orderedFields[idx+1]
			if len(line)>=fields[field]:
				upTo=min(fields[nextField]-2,len(line))
				event[field] = event.get(field,str()) + " " + line[fields[field]-2:upTo].strip()



startWithId = "^ *id [0-9]+"
startWithNum = "^ *n°"
def parse(f):
	events = list()
	shouldParse=False
	for line in f:
		if re.search(startWithNum,line):
			events += [dict()] # a new number is a new event
			shouldParse=True
		if shouldParse:
			parseFields(line,events[-1])
		if re.search(startWithId,line):
			shouldParse=False
		
	return events


events = list()
for fileName in txtFiles:
	with open(fileName,'r') as f:
		event = parse(f)
		events += event
		print("Adding",len(event),"new events,",len(events),"in total :)")	


print("Saving events as pickle object...")
with open("events.dict",'wb') as fileout:
        pickle.dump(events, fileout, protocol=pickle.HIGHEST_PROTOCOL)





