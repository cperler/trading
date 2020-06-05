import logging
from positions import *
from algorithm import Algorithm
from indicators import *
import pprint

stocks = ['SPY']

class SPYReversion(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(SPYReversion, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(SPYReversion, self).pre_run()

		for symbol in self.symbols:
			close_series = self.cube.data[(symbol, 'close')]
			high_series = self.cube.data[(symbol, 'high')]
			low_series = self.cube.data[(symbol, 'low')]
			self.add_indicator(ATR('ATR-' + symbol, 25, high_series, low_series, close_series))		

	def high_from_range(self, starting_dt, symbol, period):
		high = self.cube.data[(symbol, 'high')][starting_dt]
		for i in range(1, period):
			dt = self.cube.go_back(starting_dt, i)
			high = max(high, self.cube.data[(symbol, 'high')][dt])
		return high
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			atr = self.i('ATR-' + symbol)			
			atr_today = atr[dt]									# 1. 25 day average of ATR
						
			px = data[(symbol, 'close')]
			high = data[(symbol, 'high')]
			low = data[(symbol, 'low')]
			
			recent_high = self.high_from_range(dt, symbol, 10)	# 2. 10 day low
			
			ibs_ratio = (px - low) / (high - low)				# 3. IBS ratio (whatever that is)
			
			if atr_today is not None:
				band_below = recent_high - (2.5 * atr_today)			# 4.
			
				if px < band_below:
					if symbol not in self.oms.portfolio.positions or not self.oms.portfolio.positions[symbol].is_open():						
						self.oms.add(Transaction(symbol, dt, px, 10000.0/px))
				else:
					if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
						self.oms.add(Transaction(symbol, dt, px, self.oms.portfolio.positions[symbol].amount))
						
	def post_run(self):
		self.results()
		for symbol in self.symbols:
			self.plot(symbol=symbol, indicator_list=['ATR-' + symbol]).show()
		
for stock in stocks:
	test = SPYReversion([stock], '20000101', '20130131')
	test.run()
	result = test.results()