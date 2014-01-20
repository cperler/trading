import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint

stocks = ['SPY', 'VXX', 
# nasdaq
'ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LMCA','LLTC','MAR','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO',
# s&P
'A','AA','AAPL','ABBV','ABC','ABT','ACE','ACN','ACT','ADBE','ADI','ADM','ADP','ADSK','ADT','AEE','AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALL','ALTR','ALXN','AMAT','AME','AMGN','AMP','AMT','AMZN','AN','ANF','AON','APA','APC','APD','APH','ARG','ATI','AVB','AVP','AVY','AXP','AZO','BA','BAC','BAX','BBBY','BBT','BBY','BCR','BDX','BEAM','BEN','BF.B','BHI','BIIB','BK','BLK','BLL','BMS','BMY','BRCM','BRK.B','BSX','BTU','BWA','BXP','C','CA','CAG','CAH','CAM','CAT','CB','CBG','CBS','CCE','CCI','CCL','CELG','CERN','CF','CFN','CHK','CHRW','CI','CINF','CL','CLF','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNP','CNX','COF','COG','COH','COL','COP','COST','COV','CPB','CRM','CSC','CSCO','CSX','CTAS','CTL','CTSH','CTXS','CVC','CVS','CVX','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS','DISCA','DLPH','DLTR','DNB','DNR','DO','DOV','DOW','DPS','DRI','DTE','DTV','DUK','DVA','DVN','EA','EBAY','ECL','ED','EFX','EIX','EL','EMC','EMN','EMR','EOG','EQR','EQT','ESRX','ESV','ETFC','ETN','ETR','EW','EXC','EXPD','EXPE','F','FAST','FCX','FDO','FDX','FE','FFIV','FIS','FISV','FITB','FLIR','FLR','FLS','FMC','FOSL','FOXA','FRX','FSLR','FTI','FTR','GAS','GCI','GD','GE','GILD','GIS','GLW','GM','GME','GNW','GOOG','GPC','GPS','GRMN','GS','GT','GWW','HAL','HAR','HAS','HBAN','HCBK','HCN','HCP','HD','HES','HIG','HOG','HON','HOT','HP','HPQ','HRB','HRL','HRS','HSP','HST','HSY','HUM','IBM','ICE','IFF','IGT','INTC','INTU','IP','IPG','IR','IRM','ISRG','ITW','IVZ','JBL','JCI','JCP','JDSU','JEC','JNJ','JNPR','JOY','JPM','JWN','K','KEY','KIM','KLAC','KMB','KMI','KMX','KO','KR','KRFT','KSS','KSU','L','LEG','LEN','LH','LIFE','LLL','LLTC','LLY','LM','LMT','LNC','LO','LOW','LRCX','LSI','LUK','LUV','LYB','M','MA','MAC','MAR','MAS','MAT','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MHFI','MJN','MKC','MMC','MMM','MNST','MO','MOLX','MON','MOS','MPC','MRK','MRO','MS','MSFT','MSI','MTB','MU','MUR','MWV','MYL','NBL','NBR','NDAQ','NE','NEE','NEM','NFLX','NFX','NI','NKE','NLSN','NOC','NOV','NRG','NSC','NTAP','NTRS','NU','NUE','NVDA','NWL','NWSA','OI','OKE','OMC','ORCL','ORLY','OXY','PAYX','PBCT','PBI','PCAR','PCG','PCL','PCLN','PCP','PDCO','PEG','PEP','PETM','PFE','PFG','PG','PGR','PH','PHM','PKI','PLD','PLL','PM','PNC','PNR','PNW','POM','PPG','PPL','PRGO','PRU','PSA','PSX','PVH','PWR','PX','PXD','QCOM','QEP','R','RAI','RDC','REGN','RF','RHI','RHT','RL','ROK','ROP','ROST','RRC','RSG','RTN','SBUX','SCG','SCHW','SE','SEE','SHW','SIAL','SJM','SLB','SLM','SNA','SNDK','SNI','SO','SPG','SPLS','SRCL','SRE','STI','STJ','STT','STX','STZ','SWK','SWN','SWY','SYK','SYMC','SYY','T','TAP','TDC','TE','TEG','TEL','TER','TGT','THC','TIF','TJX','TMK','TMO','TRIP','TROW','TRV','TSN','TSO','TSS','TWC','TWX','TXN','TXT','TYC','UNH','UNM','UNP','UPS','URBN','USB','UTX','V','VAR','VFC','VIAB','VLO','VMC','VNO','VRSN','VRTX','VTR','VZ','WAG','WAT','WDC','WEC','WFC','WFM','WHR','WIN','WLP','WM','WMB','WMT','WPX','WU','WY','WYN','WYNN','X','XEL','XL','XLNX','XOM','XRAY','XRX','XYL','YHOO','YUM','ZION','ZMH','ZTS',
#dow
'AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','T','TRV','UNH','UTX','V','VZ','WMT','XOM']

class Pennant(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(Pennant, self).__init__(symbols, start_date, end_date)				
		self.cash = 10000
		self.buys = {}
		self.stops = {}
		
	def pre_run(self):
		super(Pennant, self).pre_run()			

		for symbol in self.symbols:		
			close_series = self.cube.data[(symbol, 'close')]
			
			self.add_indicator(SMA('SMA200-' + symbol, close_series, 200))			
			self.add_indicator(SMA('SMA50-' + symbol, close_series, 50))			
			self.add_indicator(SMA('SMA13-' + symbol, close_series, 13))			
			self.add_indicator(SMA('SMA10-' + symbol, close_series, 10))			

	def handle_data(self, dt, symbols, keys, data):
		back20 = self.cube.go_back(dt, 20)
		back10 = self.cube.go_back(dt, 10)
		back5 = self.cube.go_back(dt, 5)		
		
		for symbol in symbols:
			try:
				px = data[(symbol, 'close')]
				sma200 = self.i('SMA200-'+symbol)[dt]
				sma50 = self.i('SMA50-'+symbol)[dt]
				sma13 = self.i('SMA13-'+symbol)[dt]
				sma10 = self.i('SMA10-'+symbol)[dt]
				
				sma200_back20 = self.i('SMA200-'+symbol)[back20]
				sma50_back10 = self.i('SMA50-'+symbol)[back10]
				sma13_back5 = self.i('SMA13-'+symbol)[back5]
				
				rising_market = sma200 > sma200_back20 and sma50 > sma50_back10 and sma50 > sma200
				
				min_close = px
				max_sma50 = sma50
				for i in range(1, 6):
					j = self.cube.go_back(dt, i)
					min_close = min(min_close, self.cube.data[(symbol, 'close')][j])
					max_sma50 = max(max_sma50, self.i('SMA50-'+symbol)[j])
				
				falling_prices = sma13 < sma13_back5 and min_close > max_sma50
				
				entry_condition = (px < sma10) and falling_prices and rising_market

				if dt == datetime.datetime(2014, 1, 17):
					if entry_condition:
						print 'BUY', dt, symbol
			except:
				pass

test = Pennant(stocks, '20120101', '20140117')
test.run()
test.results()