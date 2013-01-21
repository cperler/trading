from positions import OMS
import data

class Algorithm(object):
	def __init__(self, symbols, start_date, end_date):
		self.oms = OMS()
		self.symbols = symbols
		self.start_date = start_date
		self.end_date = end_date
	
	def pre_run(self):
		pass
	
	def handle_data(self, dt, symbols, keys, data):
		pass
	
	def post_run(self):
		pass
	
	def run(self):
		self.cube = data.load(self.symbols, self.start_date, self.end_date)
		self.pre_run()
		for dt in self.cube.get_dates():
			step_data = {}
			symbols = []
			keys = []
			for (symbol, key) in self.cube.data:
				if symbol not in symbols:
					symbols.append(symbol)
				if key not in keys:
					keys.append(key)
				step_data[(symbol, key)] = self.cube.data[(symbol, key)][dt]
			self.handle_data(dt, symbols, keys, step_data)
		self.post_run()