from datetime import date
import data
import logging
import pprint
from positions import *
from algorithm import Algorithm
from indicators import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

cube = data.load(['GOOG', 'YHOO'], '20120101', '20120131')
#cube.write_to_csv('test.csv')
#cube.pretty_print()

oms = OMS()

t1 = Transaction('GOOG', date(2012, 1, 1), 10, 100)
t2 = Transaction('GOOG', date(2012, 3, 1), 15, 150)
t3 = Transaction('GOOG', date(2012, 10, 1), 50, 500)
t4 = Transaction('IBM', date(2012, 4, 1), -5, 50)
t5 = Transaction('IBM', date(2012, 11, 1), 5, 35)

oms.add(t1)
oms.add(t2)
oms.add(t3)
oms.add(t4)
oms.add(t5)

for t in oms.blotter.all():
	print t
	
for t in oms.portfolio.all():
	print t
 	
class SMATest(Algorithm):
	def pre_run(self):
		self.sma5 = SMA(series=self.cube.data[('GOOG', 'adjclose')], period=5).calculate()
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			for key in keys:
				pass #print dt, symbol, key, data[(symbol, key)]

	def post_run(self):
		sma = {'name': 'GOOG_SMA_5', 'data' : self.sma5 }
		extra_series = []
		extra_series.append(sma)
		self.cube.write_to_csv('test.csv', extra_series)
		
SMATest('GOOG', '20120101', '20120131').run()
