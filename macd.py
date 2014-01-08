import logging
from positions import *
from algorithm import Algorithm
from indicators import *
from plot import *
import pprint

stocks = ['SPY', 'VXX', 
# nasdaq
'ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LMCA','LLTC','MAR','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO',
# s&P
'A','AA','AAPL','ABBV','ABC','ABT','ACE','ACN','ACT','ADBE','ADI','ADM','ADP','ADSK','ADT','AEE','AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALL','ALTR','ALXN','AMAT','AME','AMGN','AMP','AMT','AMZN','AN','ANF','AON','APA','APC','APD','APH','ARG','ATI','AVB','AVP','AVY','AXP','AZO','BA','BAC','BAX','BBBY','BBT','BBY','BCR','BDX','BEAM','BEN','BF.B','BHI','BIIB','BK','BLK','BLL','BMS','BMY','BRCM','BRK.B','BSX','BTU','BWA','BXP','C','CA','CAG','CAH','CAM','CAT','CB','CBG','CBS','CCE','CCI','CCL','CELG','CERN','CF','CFN','CHK','CHRW','CI','CINF','CL','CLF','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNP','CNX','COF','COG','COH','COL','COP','COST','COV','CPB','CRM','CSC','CSCO','CSX','CTAS','CTL','CTSH','CTXS','CVC','CVS','CVX','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS','DISCA','DLPH','DLTR','DNB','DNR','DO','DOV','DOW','DPS','DRI','DTE','DTV','DUK','DVA','DVN','EA','EBAY','ECL','ED','EFX','EIX','EL','EMC','EMN','EMR','EOG','EQR','EQT','ESRX','ESV','ETFC','ETN','ETR','EW','EXC','EXPD','EXPE','F','FAST','FCX','FDO','FDX','FE','FFIV','FIS','FISV','FITB','FLIR','FLR','FLS','FMC','FOSL','FOXA','FRX','FSLR','FTI','FTR','GAS','GCI','GD','GE','GILD','GIS','GLW','GM','GME','GNW','GOOG','GPC','GPS','GRMN','GS','GT','GWW','HAL','HAR','HAS','HBAN','HCBK','HCN','HCP','HD','HES','HIG','HOG','HON','HOT','HP','HPQ','HRB','HRL','HRS','HSP','HST','HSY','HUM','IBM','ICE','IFF','IGT','INTC','INTU','IP','IPG','IR','IRM','ISRG','ITW','IVZ','JBL','JCI','JCP','JDSU','JEC','JNJ','JNPR','JOY','JPM','JWN','K','KEY','KIM','KLAC','KMB','KMI','KMX','KO','KR','KRFT','KSS','KSU','L','LEG','LEN','LH','LIFE','LLL','LLTC','LLY','LM','LMT','LNC','LO','LOW','LRCX','LSI','LUK','LUV','LYB','M','MA','MAC','MAR','MAS','MAT','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MHFI','MJN','MKC','MMC','MMM','MNST','MO','MOLX','MON','MOS','MPC','MRK','MRO','MS','MSFT','MSI','MTB','MU','MUR','MWV','MYL','NBL','NBR','NDAQ','NE','NEE','NEM','NFLX','NFX','NI','NKE','NLSN','NOC','NOV','NRG','NSC','NTAP','NTRS','NU','NUE','NVDA','NWL','NWSA','OI','OKE','OMC','ORCL','ORLY','OXY','PAYX','PBCT','PBI','PCAR','PCG','PCL','PCLN','PCP','PDCO','PEG','PEP','PETM','PFE','PFG','PG','PGR','PH','PHM','PKI','PLD','PLL','PM','PNC','PNR','PNW','POM','PPG','PPL','PRGO','PRU','PSA','PSX','PVH','PWR','PX','PXD','QCOM','QEP','R','RAI','RDC','REGN','RF','RHI','RHT','RL','ROK','ROP','ROST','RRC','RSG','RTN','SBUX','SCG','SCHW','SE','SEE','SHW','SIAL','SJM','SLB','SLM','SNA','SNDK','SNI','SO','SPG','SPLS','SRCL','SRE','STI','STJ','STT','STX','STZ','SWK','SWN','SWY','SYK','SYMC','SYY','T','TAP','TDC','TE','TEG','TEL','TER','TGT','THC','TIF','TJX','TMK','TMO','TRIP','TROW','TRV','TSN','TSO','TSS','TWC','TWX','TXN','TXT','TYC','UNH','UNM','UNP','UPS','URBN','USB','UTX','V','VAR','VFC','VIAB','VLO','VMC','VNO','VRSN','VRTX','VTR','VZ','WAG','WAT','WDC','WEC','WFC','WFM','WHR','WIN','WLP','WM','WMB','WMT','WPX','WU','WY','WYN','WYNN','X','XEL','XL','XLNX','XOM','XRAY','XRX','XYL','YHOO','YUM','ZION','ZMH','ZTS',
#dow
'AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','T','TRV','UNH','UTX','V','VZ','WMT','XOM']

class ADXTest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(ADXTest, self).__init__(symbols, start_date, end_date)		
		self.cash = 10000
		
	def pre_run(self):
		super(ADXTest, self).pre_run()

		for symbol in self.symbols:
			close_series = self.cube.data[(symbol, 'adjclose')]
			self.add_indicator(EMA('EMA12-'+symbol, close_series, 12))
			self.add_indicator(EMA('EMA26-'+symbol, close_series, 26))
			self.add_indicator(EMA('EMA55-'+symbol, close_series, 55))
			self.add_indicator(MACD('MACD-'+symbol, close_series, self.i('EMA12-'+symbol), self.i('EMA26-'+symbol)))
			self.add_indicator(EMA('MACD_Signal-'+symbol, self.i('MACD-'+symbol), 9))
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			try:
				yesterday = self.cube.go_back(dt, 1)

				macd_yesterday = self.i('MACD-'+symbol)[yesterday]
				macd = self.i('MACD-'+symbol)[dt]
				signal_yesterday = self.i('MACD_Signal-'+symbol)[dt]
				signal = self.i('MACD_Signal-'+symbol)[dt]
				
				ema26 = self.i('EMA26-'+symbol)[dt]
				ema55 = self.i('EMA55-'+symbol)[dt]
				
				px = data[(symbol, 'adjclose')]
				
				v_yesterday = None
				v = None
				if macd_yesterday is not None and signal_yesterday is not None:
					v_yesterday = macd_yesterday - signal_yesterday
					v = macd - signal
					
				if v_yesterday is not None:
					if v < 2 and v > 0 and v_yesterday < 0 and v - v_yesterday > .25:
						if dt == datetime.datetime(2014,1,7):
							print dt, 'BUY', symbol
						'''if symbol not in self.oms.portfolio.positions or not self.oms.portfolio.positions[symbol].is_open():
							qty = 100 #int(self.cash / px)
							self.oms.add(Transaction(symbol, dt, px, qty))
							self.cash = 0
						'''
						
					elif v > 0 and v < v_yesterday and v_yesterday > 0:
						'''if dt == datetime.datetime(2013,12,19):
							print dt, 'SELL', symbol
						if symbol in self.oms.portfolio.positions and self.oms.portfolio.positions[symbol].is_open():
							gains_cash = px * self.oms.portfolio.positions[symbol].amount
							self.cash += gains_cash
							self.oms.add(Transaction(symbol, dt, px, -self.oms.portfolio.positions[symbol].amount))
						'''
						
			except:
				pass
							
test = ADXTest(stocks, '20120101', '20140107')
test.run()
test.results()

#test.write_to_csv('adx.csv', indicator_list=['TR', 'PlusDM', 'MinusDM', 'ATR', 'PlusDM14', 'MinusDM14', 'PlusDI', 'MinusDI', 'DX', 'ADX'])
'''
stock = stocks[0]
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
									[[test.cube.get_values(stock, 'adjclose')],[test.i('MACD').as_series(), test.i('MACD_Signal').as_series()]],
									'Date',
									['Price','Value'],
									'-',
									[['Close'],['MACD', 'Signal']],
									stock)
for t in test.oms.blotter.all(symbols=stock):
		dt = t.dt
		high = test.cube.data[(stock, 'high')][dt] 
		subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.05), xytext=(dt, high*1.08), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()
'''