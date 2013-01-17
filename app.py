from datetime import date
import data
import logging
import pprint
from positions import *
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

data.load(['GOOG', 'YHOO'], '20120101', '20120131').write_to_csv('test.csv')

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(data.load(['GOOG', 'YHOO'], '20120101', '20120131').data)
'''
oms = OMS()

t1 = Transaction('GOOG', date(2012, 1, 1), 10, 100)
t2 = Transaction('GOOG', date(2012, 3, 1), 15, 150)
t3 = Transaction('GOOG', date(2012, 10, 1), 50, 500)
t4 = Transaction('IBM', date(2012, 4, 1), -5, 50)
t5 = Transaction('IBM', date(2012, 11, 1), 5, 35)

oms.blotter.add(t1)
oms.blotter.add(t2)
oms.blotter.add(t3)
oms.blotter.add(t4)
oms.blotter.add(t5)

for t in oms.blotter.all('IBM', start=date(2012, 1, 1), end=date(2012, 3, 2)):
	print t
'''