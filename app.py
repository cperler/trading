import logging
from positions import *
from algorithm import Algorithm
from indicators import *
import pprint

stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","C","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS"]
stocks = ['SPY']

class SMATest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(SMATest, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(SMATest, self).pre_run()

		for symbol in self.symbols:
			close_series = self.cube.data[(symbol, 'adjclose')]
			self.add_indicator(SMA('ShortSMA-' + symbol, close_series, 5))
			self.add_indicator(SMA('LongSMA-' + symbol, close_series, 20))
			self.add_indicator(RSMA('LongRSMA-' + symbol, close_series, 20))
			self.add_indicator(BBandLower('BBandLower-20-' + symbol, close_series, 20, 2))
			self.add_indicator(BBandUpper('BBandUpper-20-' + symbol, close_series, 20, 2))
			self.add_indicator(ROC('ROC-' + symbol, self.i('LongSMA-' + symbol)))
			self.add_indicator(ATR('ATR-' + symbol, self.i('ATR-' + symbol)))
		
	def handle_data(self, dt, symbols, keys, data):
		yesterday = self.cube.go_back(dt, 1)

		for symbol in symbols:
			shortsma = self.i('ShortSMA-' + symbol)
			shortsma_yesterday = shortsma[yesterday]
			shortsma_today = shortsma[dt]
			longsma = self.i('LongSMA-' + symbol)
			longsma_yesterday = longsma[yesterday]
			longsma_today = longsma[dt]
			bbandlower = self.i('BBandLower-20-' + symbol)
			bbandlower_yesterday = bbandlower[yesterday]
			bbandlower_today = bbandlower[dt]
			roc = self.i('ROC-' + symbol)
			roc_yesterday = roc[yesterday]
			roc_today = roc[dt]
			close_yesterday = self.cube.data[(symbol, 'adjclose')][yesterday]
			px = data[(symbol, 'adjclose')]
			
			if roc_yesterday is not None:
				if roc_yesterday < -0.5:
					if symbol not in self.oms.portfolio.positions or not self.oms.portfolio.positions[symbol].is_open():						
						self.oms.add(Transaction(symbol, dt, px, 10000.0/px))
				elif roc_yesterday > 0.5:
					if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
						self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))

	def post_run(self):
		self.results()
		#for symbol in self.symbols:
		#self.plot(symbol=symbol, indicator_list=['ROC-' + symbol, 'Fixed-0']).show()
		
results = {}
from plot import *
for stock in stocks:
	test = SMATest([stock], '20100101', '20130131')
	test.run()
	result = test.results()
	results[stock] = result

	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(results)
	
	plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
									[[test.cube.get_values(stock, 'adjclose'), test.i('LongSMA-' + stock).as_series()],[test.i('ROC-' + stock).as_series()], [test.i('LongRSMA-' + stock).as_series()]],
									'Date',
									['Price','Value', 'Value'],
									'-',
									[['Close', 'ShortSMA'],['ROC'], ['LongRSMA']],
									stock)
	for t in test.oms.blotter.all(symbols=stock):
		dt = t.dt
		high = test.cube.data[(stock, 'high')][dt] 
		subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.05), xytext=(dt, high*1.08), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
	plt.show()