import logging
from positions import *
from algorithm import Algorithm
from indicators import *
import pprint

stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","C","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS"]

class SellInMayTest(Algorithm):
	def __init__(self, symbols, start_date, end_date, ):
		super(SellInMayTest, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(SellInMayTest, self).pre_run()
		
	def handle_data(self, dt, symbols, keys, data):		

		for symbol in symbols:			
			px = data[(symbol, 'adjclose')]
			if px:
				if dt.month == 5:
					if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
						self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
				elif dt.month == 10:
					if symbol not in self.oms.portfolio.positions or not self.oms.portfolio.positions[symbol].is_open():						
						self.oms.add(Transaction(symbol, dt, px, 10000.0/px))

	def post_run(self):
		self.results()

test = SellInMayTest(stocks, '20100101', '20130131')
test.run()