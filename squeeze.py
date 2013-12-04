import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint
stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS", "SPY"]
stocks = ['ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LLTC','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','GOLD','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO','SPY','EEM','GDX','XLF','IWM','QQQ','EWJ','FXI','VWO','EWZ','EFA','XIV','VXX','TZA','IYR','XLU','SDS','SLV','TNA','XLE','GLD','XLI','TLT','XLP','UVXY','DIA','XLK','ITB','FAZ','USO','EWT','SSO','XHB','XLV','XLY','SPXU','FAS','XLB','DXJ','DUST','JNK','EPI','XOP','NUGT','IVV','UNG','IAU','VGK','HYG','EZU','TVIX','SH','OIH','TBT','RSX','QID','VEA','VNQ','EWW','EWH','XRT','AMLP','XME','KRE','MDY','BKLN','EWG','SQQQ','EWY','EWU','VTI','TWM','DBC','UPRO','QLD','AGQ','LQD','IWF','PFF','SPXL','EWM','SPXS','EDC','FEZ','SCO','IJH','EWA','RWM','REM','EWS','IWD','EWI','UGAZ','KBE','EWC','SPLV','TQQQ','IEF']
class SqueezeAlgo(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(SqueezeAlgo, self).__init__(symbols, start_date, end_date)				
		self.cash = 10000
		self.buys = {}
		self.stops = {}
		
	def pre_run(self):
		super(SqueezeAlgo, self).pre_run()			

		for symbol in self.symbols:		
			open_series = self.cube.data[(symbol, 'open')]
			close_series = self.cube.data[(symbol, 'adjclose')]
			high_series = self.cube.data[(symbol, 'high')]
			low_series = self.cube.data[(symbol, 'low')]
						
			self.add_indicator(EMA('EMA-' + symbol, close_series, 20))
			self.add_indicator(BBandLower('BBandLower-' + symbol, close_series, 20, 2))
			self.add_indicator(BBandUpper('BBandUpper-' + symbol, close_series, 20, 2))
			self.add_indicator(KeltnerLower('KeltnerLower-' + symbol, 20, self.i('EMA-' + symbol), 1.5, high_series, low_series, close_series))
			self.add_indicator(KeltnerUpper('KeltnerUpper-' + symbol, 20, self.i('EMA-' + symbol), 1.5, high_series, low_series, close_series))
			self.add_indicator(Squeeze('Squeeze-' + symbol, self.i('BBandLower-' + symbol), self.i('BBandUpper-' + symbol), self.i('KeltnerLower-' + symbol), self.i('KeltnerUpper-' + symbol)))
			
			self.add_indicator(AverageGain('AG3-' + symbol, close_series, 3))
			self.add_indicator(AverageLoss('AL3-' + symbol, close_series, 3))
			self.add_indicator(RSI('RSI3-' + symbol, self.i('AG3-' + symbol), self.i('AL3-' + symbol)))			
			self.add_indicator(Streak('Streak-' + symbol, close_series))
			self.add_indicator(AverageGain('AGStreak-' + symbol, self.i('Streak-' + symbol), 2))
			self.add_indicator(AverageLoss('ALStreak-' + symbol, self.i('Streak-' + symbol), 2))
			self.add_indicator(RSI('RSIStreak-' + symbol, self.i('AGStreak-' + symbol), self.i('ALStreak-' + symbol)))			
			self.add_indicator(PercentRank('PercentRank-' + symbol, close_series, 100))			
			self.add_indicator(ConnorsRSI('ConnorsRSI-'+symbol, close_series, self.i('RSI3-'+symbol), self.i('RSIStreak-'+symbol), self.i('PercentRank-'+symbol)))
			
			self.add_indicator(EMA('EMA13-' + symbol, close_series, 13))
			self.add_indicator(EMA('EMA21-' + symbol, close_series, 21))
			self.add_indicator(EMA('EMA55-' + symbol, close_series, 55))			
			
			self.add_indicator(HeikinAshi('HA-' + symbol, open_series, close_series, high_series, low_series))
			
			self.add_indicator(AverageGain('AG-'+symbol, close_series, 12))
			self.add_indicator(AverageLoss('AL-'+symbol, close_series, 12))
			self.add_indicator(RSI('RSI-' + symbol, self.i('AG-' + symbol), self.i('AL-' + symbol)))
			
			self.add_indicator(TR('TR-' + symbol, high_series, low_series, close_series))
			self.add_indicator(ATR('ATR-' + symbol, 14, high_series, low_series, close_series))

	def handle_data(self, dt, symbols, keys, data):
		yesterday = self.cube.go_back(dt, 1)
		two_days_ago = self.cube.go_back(dt, 2)
		
		for symbol in symbols:
			px = data[(symbol, 'adjclose')]
			try:
				prior_px = self.cube.data[(symbol, 'adjclose')][yesterday]
			
				h = data[(symbol, 'high')]
				l = data[(symbol, 'low')]
				o = data[(symbol, 'open')]
				c = data[(symbol, 'close')]
				prior_h = self.cube.data[(symbol, 'high')][yesterday]
				prior_l = self.cube.data[(symbol, 'low')][yesterday]
			
				squeeze = self.i('Squeeze-' + symbol)[dt]
				prior_squeeze = self.i('Squeeze-' + symbol)[yesterday]
				squeeze_two_days_ago = self.i('Squeeze-' + symbol)[two_days_ago]
				
				ema13 = self.i('EMA13-' + symbol)[dt]
				ema21 = self.i('EMA21-' + symbol)[dt]
				ema55 = self.i('EMA55-' + symbol)[dt]
				
				bbandl = self.i('BBandLower-'+symbol)[dt]
				keltl = self.i('KeltnerLower-'+symbol)[dt]
				bbandu = self.i('BBandUpper-'+symbol)[dt]
				keltu = self.i('KeltnerUpper-'+symbol)[dt]
				
				ha = self.i('HA-' + symbol)[dt]
				prior_ha = self.i('HA-' + symbol)[yesterday]
				ha_two_days_ago = self.i('HA-' + symbol)[two_days_ago]
										
				ha_doji = ((abs(ha.o - ha.c) <= ((ha.h - ha.l) * 0.1)))
				prior_ha_doji = ((abs(prior_ha.o - prior_ha.c) <= ((prior_ha.h - prior_ha.l) * 0.1)))
				
				rsi = self.i('RSI-'+symbol)[dt]
				prior_rsi = self.i('RSI-'+symbol)[yesterday]
				
				tr = self.i('TR-' + symbol)[dt]			
				atr = self.i('ATR-' + symbol)[dt]
				
				in_squeeze = (prior_squeeze > 0 and squeeze >= 0) or (squeeze_two_days_ago > 0 and prior_squeeze >= 0 and squeeze == 0)
				up_trend = ema13 > ema21 and ema21 > ema55
				down_trend = ema13 < ema21 and ema21 < ema55
				rising_ha = ha.c > prior_ha.c and prior_ha.c > ha_two_days_ago.c and ha.c > ha.o and prior_ha.c > prior_ha.o and prior_ha.l == prior_ha.o and ha.o == ha.l
				rising_momentum = rsi > prior_rsi
				rising_atr = tr > atr
							
				entry_condition = in_squeeze and up_trend and rising_ha and rising_momentum and rising_atr
				stop_condition = symbol in self.stops and l <= self.stops[symbol]
				move_stop_condition = h > prior_h or l < prior_l
				exit_condition = rsi < prior_rsi and in_squeeze and (ha_doji or prior_ha_doji)

				if dt == datetime.datetime(2013, 12, 3) and in_squeeze:			
					connors_rsi = self.i('ConnorsRSI-'+symbol)[dt]
					if up_trend and rising_ha:
						print 'BUY', dt, symbol, connors_rsi
					elif down_trend:
						print 'SELL', dt, symbol, connors_rsi
			except:
				print symbol, dt
				continue

			'''
			if symbol in self.buys:
				buy_limit_px = self.buys[symbol]
				if self.cash > 0 and l <= buy_limit_px and ha.o > prior_ha.o:
					print '{} limit to buy {} in range ({}, {})'.format(dt, buy_limit_px, l, h)
					buy_px = min(buy_limit_px, h)
					qty = int(self.cash / buy_px)
					print 'buying {} at {}; adding stop at {}'.format(qty, buy_px, prior_ha.l)
					self.oms.add(Transaction(symbol, dt, buy_px, qty))
					self.cash = 0
					self.stops[symbol] = prior_ha.l
				print 'removing limit to buy {}'.format(buy_limit_px)
				del self.buys[symbol]
			elif entry_condition:
				buy_limit_px = round((ha.h + ha.l) / 2.0, 2)
				self.buys[symbol] = buy_limit_px
				print '{} setting limit px at {}'.format(dt, buy_limit_px)
			elif stop_condition:
				if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].amount > 0:
					stop_px = self.stops[symbol]
					adj_stop_px = min(h, stop_px)
					print '{} stop px ({} -> {}) in range ({}, {})'.format(dt, stop_px, adj_stop_px, l, h)
					gains_cash = adj_stop_px * self.oms.portfolio.positions[symbol].amount
					print 'selling {} at {}'.format(-self.oms.portfolio.positions[symbol].amount, adj_stop_px)
					self.oms.add(Transaction(symbol, dt, adj_stop_px, -self.oms.portfolio.positions[symbol].amount))
					self.cash += gains_cash
				print 'removing stop px {}'.format(stop_px)
				del self.stops[symbol]
			elif symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].amount > 0:
				if exit_condition:
					print 'exiting {} at {}'.format(self.oms.portfolio.positions[symbol].amount, px)
					gains_cash = px * self.oms.portfolio.positions[symbol].amount
					self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
					self.cash += gains_cash
					del self.stops[symbol]
				elif symbol in self.stops and move_stop_condition and self.stops[symbol] != prior_px:
					print 'moving stop from {} to {}'.format(self.stops[symbol], prior_ha.l)
					self.stops[symbol] = prior_ha.l
			'''

test = SqueezeAlgo(stocks, '20130101', '20131203')
test.run()
test.results()

stock = stocks[0]
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
	[[test.cube.get_values(stock, 'adjclose'), test.i('BBandLower-' + stock).as_series(), test.i('BBandUpper-' + stock).as_series(), test.i('KeltnerUpper-' + stock).as_series(), test.i('KeltnerLower-' + stock).as_series()], [test.i('Squeeze-' + stock).as_series()], [test.i('RSI-' + stock).as_series()]], 
	'Date',
	['Price', 'Value', 'Value'],
	'-',
	[['Close', 'BBandLower', 'BBandUpper', 'KeltnerUpper', 'KeltnerLower'], ['Squeeze'], ['RSI']],
	stock)
for t in test.oms.blotter.all(symbols=stock):
	dt = t.dt
	high = test.cube.data[(stock, 'high')][dt] 
	subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.02), xytext=(dt, high*1.03), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()