from collections import OrderedDict

class Indicator(object):
	def __init__(self, name, series, **kwargs):
		self.ready = False
		self.name = name
		self.series = series
		self.values = OrderedDict()
	
	def dates(self):
		return sorted(self.series.keys())
	
	def calculate(self):
		if issubclass(type(self.series), Indicator):
			self.series = self.series.as_series()
	
	def as_series(self):
		return self.values
	
	def __getitem__(self, dt):
		return self.values[dt]

class SMA(Indicator):
	def __init__(self, name, series, period, **kwargs):
		super(SMA, self).__init__(name, series, **kwargs)
		self.period = period
		
	def calculate(self):
		super(SMA, self).calculate()
		sorted_dates = self.dates()
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			if i >= 0 and i < min(len(dates), self.period-1):
				self.values[dt] = None
			else:
				values = [self.series[x] for x in dates[i-self.period+1:i+1]]				
				if None in values:
					self.values[dt] = None
				else:
					self.values[dt] = sum(values) / self.period

class RSMA(SMA):
	def __init__(self, name, series, period, **kwargs):
		super(RSMA, self).__init__(name, series, period, **kwargs)
	
	def calculate(self):
		super(RSMA, self).calculate()
			
		for dt in self.dates():
			if self.values[dt] != None and self.series[dt] != 0:
				self.values[dt] /= self.series[dt]			
			else:
				self.values[dt] = None

class StdDev(Indicator):
	def __init__(self, name, series, period, **kwargs):
		super(StdDev, self).__init__(name, series, **kwargs)
		self.period = period
		
	def calculate(self):
		super(StdDev, self).calculate()
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			if i >= 0 and i < min(len(self.series), self.period-1):
				self.values[dt] = None
			else:
				values = [self.series[a] for a in dates[i-self.period+1:i+1]]
				if None in values:
					self.values[dt] = None
				else:			
					avg = sum(values) / self.period
					sum_of_squares = sum([(self.series[a]-avg)**2 for a in dates[i-self.period+1:i+1]])
					stdev = (sum_of_squares / (self.period - 1)) ** 0.5
					self.values[dt] = stdev

class BBandLower(StdDev):
	def __init__(self, name, series, period, deviations, **kwargs):
		super(BBandLower, self).__init__(name, series, period, **kwargs)
		self.deviations = deviations
		
	def calculate(self):
		super(BBandLower, self).calculate()
		
		for dt in self.dates():
			stddev = self.values[dt]
			if stddev is not None:
				self.values[dt] = self.series[dt] - (self.deviations * stddev)
				
class BBandUpper(StdDev):
	def __init__(self, name, series, period, deviations, **kwargs):
		super(BBandUpper, self).__init__(name, series, period, **kwargs)
		self.deviations = deviations
		
	def calculate(self):
		super(BBandUpper, self).calculate()
		
		for dt in self.dates():
			stddev = self.values[dt]
			if stddev is not None:
				self.values[dt] = self.series[dt] + (self.deviations * stddev)

class ROC(Indicator):
	def __init__(self, name, series, **kwargs):
		super(ROC, self).__init__(name, series, **kwargs)
		
	def calculate(self):
		super(ROC, self).calculate()
		
		last_dt = None
		for dt in self.dates():
			if last_dt is None: 
				self.values[dt] = None
			else:
				if self.series[dt] and self.series[last_dt]:
					self.values[dt] = self.series[dt] - self.series[last_dt]
				else:
					self.values[dt] = None
			last_dt = dt

class VWAP(Indicator):
	def __init__(self, name, price_series, volume_series, period, **kwargs):
		super(VWAP, self).__init__(name, price_series, **kwargs)
		self.price_series = price_series
		self.volume_series = volume_series
		self.period = period
	
	def calculate(self):
		super(VWAP, self).calculate()
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			if i >= 0 and i < min(len(dates), self.period-1):
				self.values[dt] = None
			else:
				values = [self.series[x] for x in dates[i-self.period+1:i+1]]				
				if None in values:
					self.values[dt] = None
				else:
					numerator = sum([self.price_series[a] * self.volume_series[a] for a in dates[i-self.period+1:i+1]])
					denominator = sum([self.volume_series[a] for a in dates[i-self.period+1:i+1]])
					self.values[dt] = numerator / denominator

class TR(Indicator):
	def __init__(self, name, high_series, low_series, close_series, **kwargs):
		super(TR, self).__init__(name, high_series, **kwargs)
		self.high_series = high_series
		self.low_series = low_series
		self.close_series = close_series
		
	def calculate(self):
		super(TR, self).calculate()
		
		dates = self.dates()
		yesterday = None
		for i, dt in enumerate(dates):
			high = self.high_series[dt]
			low = self.low_series[dt]
			h_minus_l = abs(high-low)
			
			if yesterday is None:
				self.values[dt] = h_minus_l
			else:
				prev_close = self.close_series[yesterday]
				h_minus_pc = abs(high-prev_close)
				l_minus_pc = abs(low-prev_close)
				tr = max(h_minus_l, h_minus_pc, l_minus_pc)				
				self.values[dt] = tr
			yesterday = dt

class DM(Indicator):
	def __init__(self, name, high_series, low_series, **kwargs):
		super(DM, self).__init__(name, high_series, **kwargs)
		self.high_series = high_series
		self.low_series = low_series
	
	def calculate(self):
		super(DM, self).calculate()
	
class PlusDM(DM):
	def __init__(self, name, high_series, low_series, **kwargs):
		super(PlusDM, self).__init__(name, high_series, low_series, **kwargs)
		
	def calculate(self):
		super(PlusDM, self).calculate()
		dates = self.dates()
		yesterday = None
		for i, dt in enumerate(dates):
			if yesterday:
				high = self.high_series[dt]
				low = self.low_series[dt]
				prev_high = self.high_series[yesterday]
				prev_low = self.low_series[yesterday]
				h_minus_ph = high - prev_high
				pl_minus_l = prev_low - low
				
				dm = 0
				if h_minus_ph > pl_minus_l:
					dm = max(0, h_minus_ph)
				self.values[dt] = dm
			else:
				self.values[dt] = None
			yesterday = dt
			
class MinusDM(DM):
	def __init__(self, name, high_series, low_series, **kwargs):
		super(MinusDM, self).__init__(name, high_series, low_series, **kwargs)
		
	def calculate(self):
		super(MinusDM, self).calculate()
		dates = self.dates()
		yesterday = None		
		for i, dt in enumerate(dates):
			if yesterday:
				high = self.high_series[dt]
				low = self.low_series[dt]
				prev_high = self.high_series[yesterday]
				prev_low = self.low_series[yesterday]
				h_minus_ph = high - prev_high
				pl_minus_l = prev_low - low
				
				dm = 0
				if pl_minus_l > h_minus_ph:
					dm = max(0, pl_minus_l)
				self.values[dt] = dm				
			else:
				self.values[dt] = None
			yesterday = dt
			
					
class Smooth(Indicator):
	def __init__(self, name, series, period, **kwargs):
		super(Smooth, self).__init__(name, series, **kwargs)		
		self.period = period
		
	def calculate(self):
		super(Smooth, self).calculate()
		
		dates = self.dates()
		yesterday = None
		for i, dt in enumerate(dates):
			if self.series[dt] is not None:
				prior = 0.0
				if yesterday is not None:
					prior = self.values[yesterday] if yesterday else 0.0					
				if prior is None:
					prior = 0.0
				
				v = self.series[dt]
				self.values[dt] = prior - (prior / self.period) + v
			else:
				self.values[dt] = None
			yesterday = dt
			
class DI(Indicator):
	def __init__(self, name, dm_series, tr_series, **kwargs):
		super(DI, self).__init__(name, dm_series, **kwargs)
		self.dm_series = dm_series
		self.tr_series = tr_series
	
	def calculate(self):
		super(DI, self).calculate()
		if not self.tr_series.ready:
			self.algorithm.setup_indicator(self.tr_series)
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			dm = self.dm_series[dt]
			tr = self.tr_series[dt]
			if dm is not None and tr is not None:
				self.values[dt] = dm / tr * 100.0
			else:
				self.values[dt] = None
				
class DX(Indicator):
	def __init__(self, name, pos_di_series, neg_di_series, **kwargs):
		super(DX, self).__init__(name, pos_di_series)
		self.pos_di_series = pos_di_series
		self.neg_di_series = neg_di_series
		
	def calculate(self):
		super(DX, self).calculate()
		if not self.neg_di_series.ready:
			self.algorithm.setup_indicator(self.neg_di_series)
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			pos_di = self.pos_di_series[dt]
			neg_di = self.neg_di_series[dt]
			if pos_di is not None and neg_di is not None:
				d = pos_di - neg_di
				s = pos_di + neg_di
				dx = abs(d / s) * 100
				self.values[dt] = dx
			else:
				self.values[dt] = None
				
class ADX(DX):
	def __init__(self, name, pos_di_series, neg_di_series, period, **kwargs):
		super(ADX, self).__init__(name, pos_di_series, neg_di_series)
		self.period = period
		
	def calculate(self):
		super(ADX, self).calculate()
		
		dates = self.dates()
		yesterday = None
		for i, dt in enumerate(dates):
			if self.series[dt] is not None:
				prior = 0.0
				if yesterday is not None:
					prior = self.values[yesterday] if yesterday else 0.0					
				if prior is None:
					prior = 0.0
				
				v = self.values[dt]
				self.values[dt] = ((prior * (self.period - 1)) + v) / self.period
				if i == 2:
					print 'prior', prior
					print 'v', v
					print 'adx', self.values[dt]
			else:
				self.values[dt] = None
			yesterday = dt