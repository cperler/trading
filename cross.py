import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint

stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","C","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS", "SPY"]
results = {}
for stock in stocks:
	for speriod in [2,3,5,10,15,20,30,50,100,200]:
		for lperiod in [2,3,5,10,15,20,30,50,100,200]:
			class SMATest(Algorithm):
				def __init__(self, symbols, start_date, end_date):
					super(SMATest, self).__init__(symbols, start_date, end_date)				
					self.cash = 10000
					
				def pre_run(self):
					super(SMATest, self).pre_run()			

					for symbol in self.symbols:
						close_series = self.cube.data[(symbol, 'adjclose')]
						self.add_indicator(SMA('SMA-' + symbol, close_series, speriod))
						self.add_indicator(SMA('LSMA-' + symbol, close_series, lperiod))
						self.add_indicator(RSMA('RSMA-' + symbol, close_series, speriod))
						self.add_indicator(SMA('SSS-' + symbol, self.i('RSMA-' + symbol), speriod))
						self.add_indicator(BBandLower('BBandLower-' + symbol, close_series, speriod, 2))
						self.add_indicator(BBandUpper('BBandUpper-' + symbol, close_series, speriod, 2))
						self.add_indicator(ROC('ROC-' + symbol, self.i('SSS-' + symbol)))
						self.add_indicator(VWAP('VWAP-' + symbol, close_series, self.cube.data[(symbol, 'volume')], speriod))
					
				def handle_data(self, dt, symbols, keys, data):
					yesterday = self.cube.go_back(dt, 1)
					for symbol in symbols:
						vwap = self.i('VWAP-' + symbol)
						px = data[(symbol, 'adjclose')]
						shortsma = self.i('SMA-' + symbol)
						shortsma_yesterday = shortsma[yesterday]
						shortsma_today = shortsma[dt]
						longsma = self.i('LSMA-' + symbol)
						longsma_yesterday = longsma[yesterday]
						longsma_today = longsma[dt]
										
						if shortsma_yesterday and longsma_yesterday:
							if shortsma_yesterday < longsma_yesterday and shortsma_today > longsma_today:
								if self.cash > 0:
									self.oms.add(Transaction(symbol, dt, px, self.cash / px))
									self.cash = 0
							elif shortsma_yesterday > longsma_yesterday and shortsma_today < longsma_today:
								if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
									gains_cash = px * self.oms.portfolio.positions[symbol].amount
									self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
									self.cash += gains_cash			
						
				def post_run(self):
					pass
					#self.results()
					#for symbol in self.symbols:
					#	self.plot(symbol=symbol, indicator_list=['VWAP-' + symbol, 'BBandLower-' + symbol, 'BBandUpper-' + symbol, 'SMA-' + symbol, 'LSMA-' + symbol, 'RSMA-'+ symbol, 'SSS-' + symbol, 'ROC-' + symbol]).show()
					
			test = SMATest([stock], '20050101', '20130131')
			test.run()
			results[(stock, speriod, lperiod)] = test.results()		
			'''
			plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
				[[test.cube.get_values(stock, 'adjclose'), test.i('VWAP-' + stock).as_series(), test.i('SMA-' + stock).as_series(), test.i('LSMA-' + stock).as_series(), test.i('BBandLower-' + stock).as_series(), test.i('BBandUpper-' + stock).as_series()],[test.i('RSMA-' + stock).as_series(), test.i('SSS-' + stock).as_series()],[test.i('ROC-' + stock).as_series()]],
				'Date',
				['Price','Value', 'Value'],
				'-',
				[['Close', 'VWAP', 'SMA', 'LSMA', 'BBandLower', 'BBandUpper'],['RSMA', 'SSS'],['ROC']],
				stock)
			for t in test.oms.blotter.all(symbols=stock):
				dt = t.dt
				high = test.cube.data[(stock, 'high')][dt] 
				subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.05), xytext=(dt, high*1.08), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
			#plt.show()
			'''
file = open('crossover.out', 'w')
pp = pprint.PrettyPrinter(indent=4, stream=file)
pp.pprint(results)