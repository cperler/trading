import logging
from positions import *
from algorithm import Algorithm
from indicators import *
from plot import *
import pprint

stocks = ['AAPL']

class ADXTest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(ADXTest, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(ADXTest, self).pre_run()

		for symbol in self.symbols:
			high_series = self.cube.data[(symbol, 'high')]
			low_series = self.cube.data[(symbol, 'low')]
			close_series = self.cube.data[(symbol, 'close')]
			
			self.add_indicator(TR('TR', high_series, low_series, close_series))
			self.add_indicator(PlusDM('PlusDM', high_series, low_series))
			self.add_indicator(MinusDM('MinusDM', high_series, low_series))
			self.add_indicator(Smooth('ATR', self.i('TR'), 14))
			self.add_indicator(Smooth('PlusDM14', self.i('PlusDM'), 14))
			self.add_indicator(Smooth('MinusDM14', self.i('MinusDM'), 14))
			self.add_indicator(DI('PlusDI', self.i('PlusDM14'), self.i('ATR')))
			self.add_indicator(DI('MinusDI', self.i('MinusDM14'), self.i('ATR')))
			self.add_indicator(DX('DX', self.i('PlusDI'), self.i('MinusDI')))
			self.add_indicator(ADX('ADX', self.i('PlusDI'), self.i('MinusDI'), 14))
		
	def handle_data(self, dt, symbols, keys, data):
		symbol = symbols[0]
		
		yesterday = self.cube.go_back(dt, 1)
		
		adx = self.i('ADX')[dt]
		adx_y = self.i('ADX')[yesterday]
		pdi = self.i('PlusDI')[dt]
		pdi_y = self.i('PlusDI')[yesterday]
		mdi = self.i('MinusDI')[dt]
		mdi_y = self.i('MinusDI')[yesterday]
		px = data[(symbol, 'close')]
		px_y = self.cube.data[(symbol, 'close')][yesterday]
		
		if adx and adx > 25:
			if pdi > mdi and pdi_y < mdi_y:
				if symbol not in self.oms.portfolio.positions or not self.oms.portfolio.positions[symbol].is_open():						
					self.oms.add(Transaction(symbol, dt, px, 500))
			elif pdi < mdi and pdi_y > mdi_y:
				if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
					self.oms.add(Transaction(symbol, dt, px, -500))

	def post_run(self):
		self.results()
		for symbol in self.symbols:
			self.plot(symbol=symbol, indicator_list=['TR', 'PlusDM', 'MinusDM', 'ATR', 'PlusDM14', 'MinusDM14', 'PlusDI', 'MinusDI', 'DX', 'ADX']).show()
		

test = ADXTest(stocks, '20120813', '20130206')
test.run()
test.results()

#test.write_to_csv('adx.csv', indicator_list=['TR', 'PlusDM', 'MinusDM', 'ATR', 'PlusDM14', 'MinusDM14', 'PlusDI', 'MinusDI', 'DX', 'ADX'])

stock = stocks[0]
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
									[[test.cube.get_values(stock, 'adjclose')],[test.i('PlusDI').as_series(), test.i('MinusDI').as_series(),test.i('ADX').as_series()]],
									'Date',
									['Price','Value'],
									'-',
									[['Close'],['+DI', '-DI','ADX']],
									stock)
for t in test.oms.blotter.all(symbols=stock):
		dt = t.dt
		high = test.cube.data[(stock, 'high')][dt] 
		subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.05), xytext=(dt, high*1.08), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()