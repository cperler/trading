from positions import OMS
import data

class Algorithm(object):
	def __init__(self, symbols, start_date, end_date):
		self.oms = OMS()
		self.symbols = symbols
		self.start_date = start_date
		self.end_date = end_date
	
	def run(self):
		cube = data.load(self.symbols, self.start_date, self.end_date)
		for dt in cube.get_dates():
			for symbol in cube.symbols:
				print dt, symbol, cube.data[(symbol, 'adjclose')][dt]