class Indicator(object):
	def __init__(self, *args, **kwargs):
		pass

	def get_dates(self):
		pass
		
	def calculate(self):
		pass
		
class SMA(Indicator):
	def __init__(self, **kwargs):
		super(SMA, self).__init__(kwargs)
		self.series = kwargs.pop('series')
		self.period = kwargs.pop('period')

	def get_dates(self):
		return sorted(self.series.keys())
		
	def calculate(self):	
		sorted_dates = self.get_dates()
		
		_sma = {}
		for i in range(0, min(len(self.series), self.period-1)):		
			_sma[sorted_dates[i]] = None		
		for i in range(self.period-1, len(self.series)):
			_sma[sorted_dates[i]] = sum([self.series[a] for a in sorted_dates[i-self.period+1:i+1]]) / self.period
		return _sma