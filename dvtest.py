import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint

stock = 'SPY'

class SMATest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(SMATest, self).__init__(symbols, start_date, end_date)				
		self.cash = 10000
		
	def pre_run(self):
		super(SMATest, self).pre_run()			

		for symbol in self.symbols:
			close_series = self.cube.data[(symbol, 'adjclose')]
			high_series = self.cube.data[(symbol, 'high')]
			low_series = self.cube.data[(symbol, 'low')]
			self.add_indicator(DV('DV-' + symbol, close_series, self.cube.data[(symbol, 'volume')]))
			self.add_indicator(ZScore('ZScore-' + symbol, self.i('DV-' + symbol), 20))
						
			self.add_indicator(EMA('EMA-' + symbol, close_series, 20))
			self.add_indicator(BBandLower('BBandLower-' + symbol, close_series, 20, 2))
			self.add_indicator(BBandUpper('BBandUpper-' + symbol, close_series, 20, 2))
			self.add_indicator(KeltnerLower('KeltnerLower-' + symbol, 20, self.i('EMA-' + symbol), 1.5, high_series, low_series, close_series))
			self.add_indicator(KeltnerUpper('KeltnerUpper-' + symbol, 20, self.i('EMA-' + symbol), 1.5, high_series, low_series, close_series))
			self.add_indicator(Squeeze('Squeeze-' + symbol, self.i('BBandLower-' + symbol), self.i('BBandUpper-' + symbol), self.i('KeltnerLower-' + symbol), self.i('KeltnerUpper-' + symbol)))
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			px = data[(symbol, 'adjclose')]
			z = self.i('ZScore-' + symbol)[dt]
			if z:
				if z >= 1:
					if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].amount < 0:
						print 'covering {}'.format(-self.oms.portfolio.positions[symbol].amount)
						gains_cash = px * self.oms.portfolio.positions[symbol].amount
						self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
						self.cash += gains_cash
					
					if self.cash > 0:						
						print 'buying {}'.format(self.cash / px)
						self.oms.add(Transaction(symbol, dt, px, self.cash / px))
						self.cash = 0
				elif z <= -1:
					if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].amount > 0:
						print 'selling {}'.format(self.oms.portfolio.positions[symbol].amount)
						gains_cash = px * self.oms.portfolio.positions[symbol].amount
						self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
						self.cash += gains_cash	
					elif symbol not in self.oms.portfolio.positions or self.oms.portfolio.positions[symbol].amount > px * 100:
						print 'shorting {}'.format(self.cash / px)
						self.oms.add(Transaction(symbol, dt, px, -self.cash / px))
						self.cash *= 2
		
test = SMATest([stock], '20130101', '20131017')
test.run()
test.results()
	
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
	[[test.cube.get_values(stock, 'adjclose'), test.i('BBandLower-' + stock).as_series(), test.i('BBandUpper-' + stock).as_series(), test.i('KeltnerUpper-' + stock).as_series(), test.i('KeltnerLower-' + stock).as_series()],[test.i('DV-' + stock).as_series()], [test.i('ZScore-' + stock).as_series()], [test.i('Squeeze-' + stock).as_series()]], 
	'Date',
	['Price', 'Value', 'Value', 'Value'],
	'-',
	[['Close', 'BBandLower', 'BBandUpper', 'KeltnerUpper', 'KeltnerLower'],['DV'], ['ZScore'], ['Squeeze']],
	stock)
for t in test.oms.blotter.all(symbols=stock):
	dt = t.dt
	high = test.cube.data[(stock, 'high')][dt] 
	subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.02), xytext=(dt, high*1.03), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()