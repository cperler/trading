import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint

stock = 'SPY'
results = {}
for period in [5]:
	class SMATest(Algorithm):
		def __init__(self, symbols, start_date, end_date):
			super(SMATest, self).__init__(symbols, start_date, end_date)				
			self.cash = 10000
			
		def pre_run(self):
			super(SMATest, self).pre_run()			

			for symbol in self.symbols:
				close_series = self.cube.data[(symbol, 'adjclose')]
				self.add_indicator(SMA('SMA-' + symbol, close_series, period))
				self.add_indicator(RSMA('RSMA-' + symbol, close_series, period))
				self.add_indicator(SMA('SSS-' + symbol, self.i('RSMA-' + symbol), period))
				self.add_indicator(BBandLower('BBandLower-20-' + symbol, close_series, 20, 2))
				self.add_indicator(BBandUpper('BBandUpper-20-' + symbol, close_series, 20, 2))
				self.add_indicator(ROC('ROC-' + symbol, self.i('SSS-' + symbol)))
				self.add_indicator(VWAP('VWAP-' + symbol, close_series, self.cube.data[(symbol, 'volume')], period))
			
		def handle_data(self, dt, symbols, keys, data):
			for symbol in symbols:
				vwap = self.i('VWAP-' + symbol)
				px = data[(symbol, 'adjclose')]

				if vwap[dt] is not None:
					if px < vwap[dt] * 1.005:
						shares = self.cash / px
						if shares > 0:
							self.oms.add(Transaction(symbol, dt, px, shares))
							self.cash = 0
					elif px > vwap[dt] * .995:
						if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
							gains_cash = px * self.oms.portfolio.positions[symbol].amount
							self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
							self.cash += gains_cash				
				
		def post_run(self):
			self.results()
			for symbol in self.symbols:
				self.plot(symbol=symbol, indicator_list=['VWAP-' + symbol, 'BBandLower-20-' + symbol, 'BBandUpper-20-' + symbol, 'SMA-' + symbol, 'RSMA-'+ symbol, 'SSS-' + symbol, 'ROC-' + symbol]).show()
			
	test = SMATest([stock], '20050101', '20130131')
	test.run()
	results[period] = test.results()
		
	plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
		[[test.cube.get_values(stock, 'adjclose'), test.i('VWAP-' + stock).as_series(), test.i('SMA-' + stock).as_series(), test.i('BBandLower-20-' + stock).as_series(), test.i('BBandUpper-20-' + stock).as_series()],[test.i('RSMA-' + stock).as_series(), test.i('SSS-' + stock).as_series()],[test.i('ROC-' + stock).as_series()]],
		'Date',
		['Price','Value', 'Value'],
		'-',
		[['Close', 'VWAP', 'SMA', 'BBandLower', 'BBandUpper'],['RSMA', 'SSS'],['ROC']],
		stock)
	for t in test.oms.blotter.all(symbols=stock):
		dt = t.dt
		high = test.cube.data[(stock, 'high')][dt] 
		subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.05), xytext=(dt, high*1.08), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
	plt.show()
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(results)