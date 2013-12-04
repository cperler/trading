import logging
from positions import *
from algorithm import Algorithm
from indicators import *
from plot import *
import pprint

stocks = ['SPY']
stocks = ['ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LLTC','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','GOLD','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO','SPY','EEM','GDX','XLF','IWM','QQQ','EWJ','FXI','VWO','EWZ','EFA','XIV','VXX','TZA','IYR','XLU','SDS','SLV','TNA','XLE','GLD','XLI','TLT','XLP','UVXY','DIA','XLK','ITB','FAZ','USO','EWT','SSO','XHB','XLV','XLY','SPXU','FAS','XLB','DXJ','DUST','JNK','EPI','XOP','NUGT','IVV','UNG','IAU','VGK','HYG','EZU','TVIX','SH','OIH','TBT','RSX','QID','VEA','VNQ','EWW','EWH','XRT','AMLP','XME','KRE','MDY','BKLN','EWG','SQQQ','EWY','EWU','VTI','TWM','DBC','UPRO','QLD','AGQ','LQD','IWF','PFF','SPXL','EWM','SPXS','EDC','FEZ','SCO','IJH','EWA','RWM','REM','EWS','IWD','EWI','UGAZ','KBE','EWC','SPLV','TQQQ','IEF']
stocks = ['NFLX']
class Connors(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(Connors, self).__init__(symbols, start_date, end_date)
		self.cash = 10000
		self.buys = {}

	def pre_run(self):
		super(Connors, self).pre_run()			

		for symbol in self.symbols:
			close_series = self.cube.data[(symbol, 'close')]
			high_series = self.cube.data[(symbol, 'high')]
			low_series = self.cube.data[(symbol, 'low')]

			self.add_indicator(AverageGain('AG-' + symbol, close_series, 3))
			self.add_indicator(AverageLoss('AL-' + symbol, close_series, 3))
			self.add_indicator(RSI('RSI-' + symbol, self.i('AG-' + symbol), self.i('AL-' + symbol)))
			
			self.add_indicator(Streak('Streak-' + symbol, close_series))
			self.add_indicator(AverageGain('AGStreak-' + symbol, self.i('Streak-' + symbol), 2))
			self.add_indicator(AverageLoss('ALStreak-' + symbol, self.i('Streak-' + symbol), 2))
			self.add_indicator(RSI('RSIStreak-' + symbol, self.i('AGStreak-' + symbol), self.i('ALStreak-' + symbol)))
			
			self.add_indicator(PercentRank('PercentRank-' + symbol, close_series, 100))
			
			self.add_indicator(ConnorsRSI('ConnorsRSI-'+symbol, close_series, self.i('RSI-'+symbol), self.i('RSIStreak-'+symbol), self.i('PercentRank-'+symbol)))
			
			self.add_indicator(TR('TR-'+symbol, high_series, low_series, close_series))
			self.add_indicator(PlusDM('PlusDM-'+symbol, high_series, low_series))
			self.add_indicator(MinusDM('MinusDM-'+symbol, high_series, low_series))
			self.add_indicator(Smooth('ATR-'+symbol, self.i('TR-'+symbol), 10))
			self.add_indicator(Smooth('PlusDM14-'+symbol, self.i('PlusDM-'+symbol), 10))
			self.add_indicator(Smooth('MinusDM14-'+symbol, self.i('MinusDM-'+symbol), 10))
			self.add_indicator(DI('PlusDI-'+symbol, self.i('PlusDM14-'+symbol), self.i('ATR-'+symbol)))
			self.add_indicator(DI('MinusDI-'+symbol, self.i('MinusDM14-'+symbol), self.i('ATR-'+symbol)))
			self.add_indicator(ADX('ADX-'+symbol, self.i('PlusDI-'+symbol), self.i('MinusDI-'+symbol), 10))
			
	def handle_data(self, dt, symbols, keys, data):
		yesterday = self.cube.go_back(dt, 1)
		
		for symbol in symbols:
			try:
				px = data[(symbol, 'close')]
				h = data[(symbol, 'high')]
				l = data[(symbol, 'low')]
				c = data[(symbol, 'close')]			
				prior_l = self.cube.data[(symbol, 'low')][yesterday]
									
				connors_rsi = self.i('ConnorsRSI-'+symbol)[dt]
				adx = self.i('ADX-'+symbol)[dt]
				
				closing_range = 100 * ((px - l) / (h - l))
				entry_condition = connors_rsi is not None and connors_rsi <= 10 and adx > 30 and l <= prior_l * .94 and closing_range < 25
				exit_condition = connors_rsi >= 80
				
				if symbol in self.buys:
					buy_limit_px = self.buys[symbol]
					if (symbol not in self.oms.portfolio.positions or self.oms.portfolio.positions[symbol].amount == 0) and l <= buy_limit_px and self.cash > 0:
						buy_px = min(buy_limit_px, h)
						qty = int(self.cash / buy_px)
						#qty = int(1000/buy_px)
						print '{} buying {} at {}'.format(dt, qty, buy_px)
						self.oms.add(Transaction(symbol, dt, buy_px, qty))
						self.cash = 0
					#print '{} removing limit to buy {}'.format(dt, buy_limit_px)
					del self.buys[symbol]
				elif entry_condition:
					buy_limit_px = round(px * .92, 2)
					self.buys[symbol] = buy_limit_px
					print '{} setting limit px at {} - crsi={}'.format(dt, buy_limit_px, connors_rsi)
				elif symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].amount > 0:
					if exit_condition:
						print '{} exiting {} at {} - crsi={}'.format(dt, self.oms.portfolio.positions[symbol].amount, px, connors_rsi)
						gains_cash = px * self.oms.portfolio.positions[symbol].amount
						self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
						self.cash += gains_cash
			except:
				pass
							
test = Connors(stocks, '20110101', '20131127')
test.run()
test.results()

stock = stocks[0]
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
	[[test.cube.get_values(stock, 'adjclose')], [test.i('ConnorsRSI-' + stock).as_series()], [test.i('ADX-'+stock).as_series()]], 
	'Date',
	['Price', 'Value', 'Value'],
	'-',
	[['Close'], ['ConnorsRSI'], ['ADX']],
	stock)
for t in test.oms.blotter.all(symbols=stock):
	dt = t.dt
	high = test.cube.data[(stock, 'high')][dt] 
	subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.02), xytext=(dt, high*1.03), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()

#test.write_to_csv('connors.csv', indicator_list=['RSI-MTL', 'RSIStreak-MTL', 'PercentRank-MTL', 'ConnorsRSI-MTL'])