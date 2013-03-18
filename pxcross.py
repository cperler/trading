import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint

stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","C","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS", "SPY"]
#stocks = ['SPY']
results = {}
stocks =['AXP']
for stock in stocks:
	for period in [10]:#[2,3,5,10,15,20,30,50,100,200]:		
		for start_date in ['20050101']:#['20050101','20060101','20070101','20080101','20090101','20100101','20110101','20120101']:
			class SMATest(Algorithm):
				def __init__(self, symbols, start_date, end_date):
					super(SMATest, self).__init__(symbols, start_date, end_date)				
					self.cash = 10000
					
				def pre_run(self):
					super(SMATest, self).pre_run()			

					for symbol in self.symbols:
						close_series = self.cube.data[(symbol, 'adjclose')]
						self.add_indicator(SMA('SMA-' + symbol, close_series, period))					
						self.add_indicator(BBandLower('BBandLower-' + symbol, close_series, period, 2))
						self.add_indicator(BBandUpper('BBandUpper-' + symbol, close_series, period, 2))
					
				def handle_data(self, dt, symbols, keys, data):
					yesterday = self.cube.go_back(dt, 1)
					for symbol in symbols:					
						px = data[(symbol, 'adjclose')]
						px_yesterday = self.cube.data[(symbol, 'adjclose')][yesterday]
						sma = self.i('SMA-' + symbol)
						sma_yesterday = sma[yesterday]
						sma_today = sma[dt]				
										
						if sma_yesterday and px_yesterday:
							if sma_yesterday < px_yesterday and sma_today > px:
								if self.cash > 0:
									self.oms.add(Transaction(symbol, dt, px, (self.cash-5) / px))
									self.cash = 0
							elif sma_yesterday > px_yesterday and sma_today < px:
								if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
									gains_cash = px * self.oms.portfolio.positions[symbol].amount
									self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
									self.cash += (gains_cash-5)
						
				def post_run(self):
					self.results()
					for symbol in self.symbols:
						self.plot(symbol=symbol, indicator_list=['SMA-' + symbol]).show()
					
			test = SMATest([stock], start_date, '20130101')
			test.run()
			results[(stock, period, start_date)] = test.results()		
#file = open('pxcross.out', 'w')
#pp = pprint.PrettyPrinter(indent=4, stream=file)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(results)