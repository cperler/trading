from datetime import date
import data
import logging
import pprint
from positions import *
from algorithm import Algorithm
from indicators import *
import plot
import matplotlib.dates as mdates

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
	def __init__(self, symbols, start_date, end_date):
		super(SMATest, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(SMATest, self).pre_run()
		self.sma50 = SMA(series=self.cube.data[('GOOG', 'adjclose')], period=50)
		self.sma200 = SMA(series=self.cube.data[('GOOG', 'adjclose')], period=200)
		self.indicators.append(self.sma50)
		self.indicators.append(self.sma200)
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			for key in keys:
				pass #print dt, symbol, key, data[(symbol, key)]

	def post_run(self):
		sma50 = {'name': 'GOOG_SMA_50', 'data' : self.sma50.value }
		sma200 = {'name': 'GOOG_SMA_200', 'data' : self.sma200.value }
		extra_series = []
		extra_series.append(sma50)
		extra_series.append(sma200)
		self.cube.write_to_csv('test.csv', extra_series)
		
algo = SMATest('GOOG', '20100101', '20121231')
algo.run()

plot.plot_data_with_dates([algo.cube.get_dates()]*3, [algo.cube.get_values('GOOG', 'close'), algo.sma50.get_values(), algo.sma200.get_values()], 'Date', 'Px', '-', ['Open', 'SMA50', 'SMA200'], 'Graph').show()

plot.plot_candles(algo.cube).show()