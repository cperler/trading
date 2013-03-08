import logging
from positions import *
from algorithm import Algorithm
from indicators import *
from plot import *
import pprint

stocks = ['SPY']
cnt = 0
gain = []
bhgain = []
bhcnt = 0
results = {}

class DownTest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		self.check = 0.1
		super(DownTest, self).__init__(symbols, start_date, end_date)		
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:					
			yesterday = self.cube.go_back(dt, 1)			
			yesterday_c = self.cube.data[(symbol, 'close')][yesterday]
			yesterday_l = self.cube.data[(symbol, 'low')][yesterday]
			yesterday_h = self.cube.data[(symbol, 'high')][yesterday]
			yesterday_o = self.cube.data[(symbol, 'open')][yesterday]
			today_o = data[(symbol, 'open')]
			today_c = data[(symbol, 'close')]			

			check = (yesterday_c - yesterday_l) / (yesterday_h - yesterday_l)
			yesterday_move = 100 * (yesterday_c / yesterday_o)
			gap_down = (today_o / yesterday_c)
			
			global bhcnt
			global bhgain
			bhcnt += 1
			bhgain.append(100 * ((today_c / today_o) - 1))
			
			if yesterday != dt and check < self.check and gap_down < 1:
				shares = int(10000/today_o)
				global cnt
				cnt+=1
				global gain
				gain.append(100 * ((today_c / today_o) - 1))
				self.oms.add(Transaction(symbol, dt, today_o, shares))
				self.oms.add(Transaction(symbol, dt, today_c, -shares))

	def post_run(self):
		self.results(bhfield='close')
		for symbol in self.symbols:
			self.plot(symbol=symbol).show()

test = DownTest(stocks, '20050101', '20130226')
test.run()

print cnt, 'trades'
print 'strategy avg trade',(sum(gain) / cnt)
print 'bh avg trade', (sum(bhgain) / bhcnt)
print 'tx cost', 8 * cnt
