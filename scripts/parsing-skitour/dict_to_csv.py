import pickle
import csv

events = []

with open("events.dict","rb") as f:
    events = pickle.load(f)

with open("events.csv", "w") as f:
    writer = csv.DictWriter(f, events[0].keys())
    writer.writeheader()
    writer.writerows(events)    

