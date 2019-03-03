import parsing
import pickle
import sys


events = parsing.do_parsing()
sys.setrecursionlimit(10000)

with open("events.dict",'wb') as fileout:
        pickle.dump(events, fileout, protocol=pickle.HIGHEST_PROTOCOL)
