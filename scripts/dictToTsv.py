from fieldDesc import *
import pickle

with open("events.dict","rb") as f:
	events = pickle.load(f)

for field in orderedFields[:-1]:
	print(field+"\t",end="")
print()

for event in events:
	for field in orderedFields[:-1]:
		print(event.get(field,str()).strip()+"\t",end="")
	print()


