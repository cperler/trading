import logging
from positions import *
from algorithm import Algorithm
from plot import *
from indicators import *
import pprint
stocks = ["MMM","AA","MO","AXP","AIG","T","BA","CAT","KO","DD","XOM","GE","GM","HPQ","HD","HON","IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","PFE","PG","UTX","VZ","WMT","DIS", "SPY"]
stocks = ['ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LLTC','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','GOLD','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO','SPY','EEM','GDX','XLF','IWM','QQQ','EWJ','FXI','VWO','EWZ','EFA','XIV','VXX','TZA','IYR','XLU','SDS','SLV','TNA','XLE','GLD','XLI','TLT','XLP','UVXY','DIA','XLK','ITB','FAZ','USO','EWT','SSO','XHB','XLV','XLY','SPXU','FAS','XLB','DXJ','DUST','JNK','EPI','XOP','NUGT','IVV','UNG','IAU','VGK','HYG','EZU','TVIX','SH','OIH','TBT','RSX','QID','VEA','VNQ','EWW','EWH','XRT','AMLP','XME','KRE','MDY','BKLN','EWG','SQQQ','EWY','EWU','VTI','TWM','DBC','UPRO','QLD','AGQ','LQD','IWF','PFF','SPXL','EWM','SPXS','EDC','FEZ','SCO','IJH','EWA','RWM','REM','EWS','IWD','EWI','UGAZ','KBE','EWC','SPLV','TQQQ','IEF']

stocks = ['SPY', 'VXX', 
# nasdaq
'ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','XRAY','DTV','DISCA','DLTR','EBAY','EQIX','EXPE','EXPD','ESRX','FFIV','FB','FAST','FISV','FOSL','GRMN','GILD','GOOG','GMCR','HSIC','INTC','INTU','ISRG','KLAC','KRFT','LBTYA','LINTA','LMCA','LLTC','MAR','MAT','MXIM','MCHP','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NUAN','NVDA','ORLY','PCAR','PAYX','PCLN','QCOM','REGN','ROST','SNDK','SBAC','STX','SHLD','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','FOXA','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO',
# s&P
'A','AA','AAPL','ABBV','ABC','ABT','ACE','ACN','ACT','ADBE','ADI','ADM','ADP','ADSK','ADT','AEE','AEP','AES','AET','AFL','AGN','AIG','AIV','AIZ','AKAM','ALL','ALTR','ALXN','AMAT','AME','AMGN','AMP','AMT','AMZN','AN','ANF','AON','APA','APC','APD','APH','ARG','ATI','AVB','AVP','AVY','AXP','AZO','BA','BAC','BAX','BBBY','BBT','BBY','BCR','BDX','BEAM','BEN','BF.B','BHI','BIIB','BK','BLK','BLL','BMS','BMY','BRCM','BRK.B','BSX','BTU','BWA','BXP','C','CA','CAG','CAH','CAM','CAT','CB','CBG','CBS','CCE','CCI','CCL','CELG','CERN','CF','CFN','CHK','CHRW','CI','CINF','CL','CLF','CLX','CMA','CMCSA','CME','CMG','CMI','CMS','CNP','CNX','COF','COG','COH','COL','COP','COST','COV','CPB','CRM','CSC','CSCO','CSX','CTAS','CTL','CTSH','CTXS','CVC','CVS','CVX','D','DAL','DD','DE','DFS','DG','DGX','DHI','DHR','DIS','DISCA','DLPH','DLTR','DNB','DNR','DO','DOV','DOW','DPS','DRI','DTE','DTV','DUK','DVA','DVN','EA','EBAY','ECL','ED','EFX','EIX','EL','EMC','EMN','EMR','EOG','EQR','EQT','ESRX','ESV','ETFC','ETN','ETR','EW','EXC','EXPD','EXPE','F','FAST','FCX','FDO','FDX','FE','FFIV','FIS','FISV','FITB','FLIR','FLR','FLS','FMC','FOSL','FOXA','FRX','FSLR','FTI','FTR','GAS','GCI','GD','GE','GILD','GIS','GLW','GM','GME','GNW','GOOG','GPC','GPS','GRMN','GS','GT','GWW','HAL','HAR','HAS','HBAN','HCBK','HCN','HCP','HD','HES','HIG','HOG','HON','HOT','HP','HPQ','HRB','HRL','HRS','HSP','HST','HSY','HUM','IBM','ICE','IFF','IGT','INTC','INTU','IP','IPG','IR','IRM','ISRG','ITW','IVZ','JBL','JCI','JCP','JDSU','JEC','JNJ','JNPR','JOY','JPM','JWN','K','KEY','KIM','KLAC','KMB','KMI','KMX','KO','KR','KRFT','KSS','KSU','L','LEG','LEN','LH','LIFE','LLL','LLTC','LLY','LM','LMT','LNC','LO','LOW','LRCX','LSI','LUK','LUV','LYB','M','MA','MAC','MAR','MAS','MAT','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','MHFI','MJN','MKC','MMC','MMM','MNST','MO','MOLX','MON','MOS','MPC','MRK','MRO','MS','MSFT','MSI','MTB','MU','MUR','MWV','MYL','NBL','NBR','NDAQ','NE','NEE','NEM','NFLX','NFX','NI','NKE','NLSN','NOC','NOV','NRG','NSC','NTAP','NTRS','NU','NUE','NVDA','NWL','NWSA','OI','OKE','OMC','ORCL','ORLY','OXY','PAYX','PBCT','PBI','PCAR','PCG','PCL','PCLN','PCP','PDCO','PEG','PEP','PETM','PFE','PFG','PG','PGR','PH','PHM','PKI','PLD','PLL','PM','PNC','PNR','PNW','POM','PPG','PPL','PRGO','PRU','PSA','PSX','PVH','PWR','PX','PXD','QCOM','QEP','R','RAI','RDC','REGN','RF','RHI','RHT','RL','ROK','ROP','ROST','RRC','RSG','RTN','SBUX','SCG','SCHW','SE','SEE','SHW','SIAL','SJM','SLB','SLM','SNA','SNDK','SNI','SO','SPG','SPLS','SRCL','SRE','STI','STJ','STT','STX','STZ','SWK','SWN','SWY','SYK','SYMC','SYY','T','TAP','TDC','TE','TEG','TEL','TER','TGT','THC','TIF','TJX','TMK','TMO','TRIP','TROW','TRV','TSN','TSO','TSS','TWC','TWX','TXN','TXT','TYC','UNH','UNM','UNP','UPS','URBN','USB','UTX','V','VAR','VFC','VIAB','VLO','VMC','VNO','VRSN','VRTX','VTR','VZ','WAG','WAT','WDC','WEC','WFC','WFM','WHR','WIN','WLP','WM','WMB','WMT','WPX','WU','WY','WYN','WYNN','X','XEL','XL','XLNX','XOM','XRAY','XRX','XYL','YHOO','YUM','ZION','ZMH','ZTS',
#dow
'AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','T','TRV','UNH','UTX','V','VZ','WMT','XOM']

class BBCross(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(BBCross, self).__init__(symbols, start_date, end_date)				
		self.cash = 10000
		self.buys = {}
		self.stops = {}
		
	def pre_run(self):
		super(BBCross, self).pre_run()			

		for symbol in self.symbols:		
			close_series = self.cube.data[(symbol, 'close')]
			
			self.add_indicator(SMA('SMA20-' + symbol, close_series, 20))			
			self.add_indicator(BBandLower('BBandLower-' + symbol, close_series, 20, 2, self.i('SMA20-' + symbol)))
			self.add_indicator(EMA('EMA200-' + symbol, close_series, 200))

	def handle_data(self, dt, symbols, keys, data):
		yesterday = self.cube.go_back(dt, 1)
		
		for symbol in symbols:
			try:
				px = data[(symbol, 'close')]
				ema200 = self.i('EMA200-' + symbol)[dt]
				prior_ema200 = self.i('EMA200-' + symbol)[yesterday]
				bb = self.i('BBandLower-' + symbol)[dt]
				prior_bb = self.i('BBandLower-' + symbol)[yesterday]
								
				entry_condition = prior_ema200 < prior_bb and ema200 > bb
				exit_condition = prior_ema200 > prior_bb and ema200 < bb

				if dt == datetime.datetime(2014, 1, 17):
					if entry_condition:
						print 'BUY', dt, symbol
			except:
				pass

test = BBCross(stocks, '20120101', '20140117')
test.run()
test.results()
'''
stock = stocks[0]
plt, subplots = multi_plot_data_with_dates(test.cube.get_dates(), 
	[[test.cube.get_values(stock, 'adjclose'), test.i('EMA200-' + stock).as_series(), test.i('BBandLower-'+stock).as_series()]], 
	'Date',
	['Price'],
	'-',
	[['Close', 'EMA200', 'BBandLower']],
	stock)
for t in test.oms.blotter.all(symbols=stock):
	dt = t.dt
	high = test.cube.data[(stock, 'high')][dt] 
	subplots[0].annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.02), xytext=(dt, high*1.03), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
plt.show()
'''