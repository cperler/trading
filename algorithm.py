from positions import OMS, Transaction
from indicators import Indicator
import data
import plot

class Algorithm(object):
	def __init__(self, symbols, start_date, end_date, cash=1000):
		self.oms = OMS()
		self.symbols = symbols
		self.start_date = start_date
		self.end_date = end_date
		self.cash = cash
		self.initial_cash = cash
		self.indicators = {}
		
	def add_indicator(self, indicator):
		indicator.algorithm = self
		self.indicators[indicator.name] = indicator
		
	def get_indicator(self, name):
		return self.indicators.get(name)
		
	def i(self, name):
		return self.get_indicator(name)
		
	def setup_indicator(self, indicator):
		if indicator.ready == True or indicator is None:
			return

		if issubclass(type(indicator.series), Indicator):			
			self.setup_indicator(indicator.series)
		
		indicator.calculate()
		indicator.ready = True
		
	def setup_indicators(self):
		for indicator in self.indicators.values():
			self.setup_indicator(indicator)
	
	def pre_run(self):
		pass
	
	def handle_data(self, dt, symbols, keys, data):
		pass
	
	def post_run(self):
		pass
	
	def run(self):
		self.cube = data.load(self.symbols, self.start_date, self.end_date)
		self.pre_run()		
		self.setup_indicators()
		for dt in self.cube.get_dates():
			step_data = {}
			symbols = []
			keys = []
			for (symbol, key) in self.cube.data:
				if symbol not in symbols:
					symbols.append(symbol)
				if key not in keys:
					keys.append(key)
				if dt in self.cube.data[(symbol, key)]:
					step_data[(symbol, key)] = self.cube.data[(symbol, key)][dt]
				else:
					step_data[(symbol, key)] = None
			self.handle_data(dt, symbols, keys, step_data)
		self.post_run()

	def write_to_csv(self, file_name, indicator_list=None):
		extra_series = []		
		if indicator_list:
			if type(indicator_list) is str: indicator_list = [indicator_list]
			for indicator in indicator_list:
				i = self.i(indicator)
				extra_series.append({'name': i.name, 'data': i})
		self.cube.write_to_csv(file_name, extra_series)
		
	def plot(self, symbol=None, indicator_list=None, show_signals=True, exclude_price=False):
		if not symbol:
			symbol = self.symbols[0]
			
		indicators = []
		indicator_names = []
		if indicator_list:
			if type(indicator_list) is str: indicator_list = [indicator_list]
			indicators.extend([self.i(indicator).as_series() for indicator in indicator_list])
			indicator_names.extend([self.i(indicator).name for indicator in indicator_list])					
		num_series = len(indicators) + 1

		date_series_list = [self.cube.get_dates()] * num_series
		plot_series_list = [self.cube.get_values(symbol, 'close')] + indicators
		plot_names_list = ['Close'] + indicator_names		
		if exclude_price:
			date_series_list = [self.cube.get_dates()] * (num_series-1)
			plot_series_list = indicators
			plot_names_list = indicator_names

		plt = plot.plot_data_with_dates(date_series_list, plot_series_list, 'Date', '' if exclude_price else 'Px', '-', plot_names_list, symbol)
		
		if show_signals:
			for t in self.oms.blotter.all(symbols=symbol):
				dt = t.dt
				high = self.i(indicator_list[0]).value[dt] if exclude_price else self.cube.data[(symbol, 'high')][dt] 
				plt.annotate('BUY' if t.qty > 0 else 'SELL', xy=(dt, high*1.02), xytext=(dt, high*1.03), arrowprops=dict(facecolor='green' if t.qty > 0 else 'red', shrink=0.05))
		
		return plt
		
	def get_buy_and_hold(self, field='close'):
		bh = {}
		dates = self.cube.get_dates()
		for symbol in self.symbols:
			idx = 0
			while dates[idx] not in self.cube.data[(symbol, field)]:
				idx += 1
			p1 = self.cube.data[(symbol, field)][dates[idx]]			
			px = self.cube.data[(symbol, field)][dates[-1]]
			v = px / p1 * self.initial_cash
			bh[symbol] = v - self.initial_cash
		return bh
	
	def calculate_pandl(self):
		closeout = 0.0
		for symbol, position in self.oms.portfolio.positions.items():
			if position.is_open():
				dt = self.cube.get_dates()[-1]
				px = self.cube.data[(symbol, 'close')][dt]
				closeout += Transaction(symbol, dt, px, position.amount).cost()
		pandl = self.oms.blotter.calculate_pandl()
		return {'only_closed' : pandl, 'only_open' : closeout, 'total' : closeout+pandl}
		
	def results(self, bhfield='close'):
		print('')
		print('-- Results for {} on symbols {} from {} to {} --'.format(self.__class__.__name__, self.symbols, self.start_date, self.end_date))
		print ('')
		print ('Transactions:')
		transactions = list(self.oms.blotter.all())
		for t in transactions:
			print ('\t{}'.format(t))
		if len(transactions) == 0:
			print('\tno transactions')
		print('')
		print('Holdings:')
		holdings = self.oms.portfolio.all(only_open=True)
		for p in holdings:			
			print('\t{} (px = {})'.format(p, self.cube.data[(p.symbol, 'close')][self.cube.get_dates()[-1]]))
		if len(holdings) == 0:
			print('\tno open holdings')
		pandl = self.calculate_pandl()
		print('Unrealized = {}'.format(pandl['only_open']))
		print('Realized = {}'.format(pandl['only_closed']))
		print('Total P&L = {}'.format(pandl['total']))
		print('B&H = {}'.format(sum([v-10000 for _, v in self.get_buy_and_hold(field=bhfield).items()])))
		print('')
		return {'strategy' : int(pandl['total']), 'bh' : int(sum([v for _, v in self.get_buy_and_hold().items()])-10000)}