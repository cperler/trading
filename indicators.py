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
				
class EMA(SMA):
	def __init__(self, name, series, period, **kwargs):
		super(EMA, self).__init__(name, series, period, **kwargs)
		
	def calculate(self):
		super(EMA, self).calculate()
		
		yesterday = None
		for dt in self.dates():
			sma = self.values[dt]
			if sma is not None:
				prior_ema = self.values[yesterday]
				if prior_ema is not None:
					multiplier = (2.0 / (self.period + 1.0))
					ema_val = ((self.series[dt] - prior_ema) * multiplier) + prior_ema
					self.values[dt] = ema_val
			yesterday = dt			
			
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

class ZScore(StdDev):
	def __init__(self, name, series, period, **kwargs):
		super(ZScore, self).__init__(name, series, period, **kwargs)
		
	def calculate(self):
		super(ZScore, self).calculate()
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			stddev = self.values[dt]
			if i >= 0 and i < min(len(self.series), self.period-1):
				self.values[dt] = None
			else:
				values = [self.series[a] for a in dates[i-self.period+1:i+1]]
				if None in values:
					self.values[dt] = None
				else:
					avg = sum(values) / self.period
					self.values[dt] = (self.series[dt] - avg) / stddev
					
class BBandLower(StdDev):
	def __init__(self, name, series, period, deviations, ma_series, **kwargs):
		super(BBandLower, self).__init__(name, series, period, **kwargs)
		self.deviations = deviations
		self.ma_series = ma_series
		
	def calculate(self):
		super(BBandLower, self).calculate()

		if not self.ma_series.ready:
			self.algorithm.setup_indicator(self.ma_series)
		
		for dt in self.dates():
			stddev = self.values[dt]
			ma_val = self.ma_series[dt]
			if stddev is not None and ma_val is not None:
				self.values[dt] = ma_val - (self.deviations * stddev)
			else:
				self.values[dt] = None
				
class BBandUpper(StdDev):
	def __init__(self, name, series, period, deviations, ma_series, **kwargs):
		super(BBandUpper, self).__init__(name, series, period, **kwargs)
		self.deviations = deviations
		self.ma_series = ma_series
		
	def calculate(self):
		super(BBandUpper, self).calculate()
		
		if not self.ma_series.ready:
			self.algorithm.setup_indicator(self.ma_series)
		
		for dt in self.dates():
			stddev = self.values[dt]
			ma_val = self.ma_series[dt]
			if stddev is not None and ma_val is not None:
				self.values[dt] = ma_val + (self.deviations * stddev)
			else:
				self.values[dt] = None
				
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
					
class DV(Indicator):
	def __init__(self, name, price_series, volume_series, **kwargs):
		super(DV, self).__init__(name, price_series, **kwargs)
		self.price_series = price_series
		self.volume_series = volume_series
		
	def calculate(self):
		super(DV, self).calculate()
		
		dates = self.dates()
		for i, dt in enumerate(dates):
			self.values[dt] = self.price_series[dt] * self.volume_series[dt]

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

class ATR(TR):
	def __init__(self, name, period, high_series, low_series, close_series, **kwargs):
		super(ATR, self).__init__(name, high_series, low_series, close_series, **kwargs)
		self.period = period
	
	def calculate(self):
		super(ATR, self).calculate()
		
		dates = self.dates()
		initial_tr_sum = 0
		yesterday = None
		for i, dt in enumerate(dates):
			if i >= 0 and i < min(len(dates), self.period-1):
				initial_tr_sum += self.values[dt]
				self.values[dt] = None
			elif i == self.period-1:
				initial_tr_sum += self.values[dt]
				avg_tr = initial_tr_sum / self.period
				self.values[dt] = avg_tr
			else:
				prior_atr = self.values[yesterday]
				current_tr = self.values[dt]
				current_atr = ((prior_atr * (self.period - 1)) + current_tr) / self.period
				self.values[dt] = current_atr
			yesterday = dt

class KeltnerLower(ATR):
	def __init__(self, name, period, ema_series, deviations, high_series, low_series, close_series, **kwargs):
		super(KeltnerLower, self).__init__(name, period, high_series, low_series, close_series, **kwargs)
		self.ema_series = ema_series
		self.deviations = deviations
		
	def calculate(self):
		super(KeltnerLower, self).calculate()

		if not self.ema_series.ready:
			self.algorithm.setup_indicator(self.ema_series)
		
		for dt in self.dates():
			atr_val = self.values[dt]
			ema_val = self.ema_series[dt]
			if atr_val is not None and ema_val is not None:				
				self.values[dt] = ema_val - (self.deviations * atr_val)		

class KeltnerUpper(ATR):
	def __init__(self, name, period, ema_series, deviations, high_series, low_series, close_series, **kwargs):
		super(KeltnerUpper, self).__init__(name, period, high_series, low_series, close_series, **kwargs)
		self.ema_series = ema_series
		self.deviations = deviations
		
	def calculate(self):
		super(KeltnerUpper, self).calculate()

		if not self.ema_series.ready:
			self.algorithm.setup_indicator(self.ema_series)
		
		for dt in self.dates():
			atr_val = self.values[dt]
			ema_val = self.ema_series[dt]
			if atr_val is not None and ema_val is not None:				
				self.values[dt] = ema_val + (self.deviations * atr_val)		
				
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
				if s != 0:
					dx = abs(d / s) * 100
				else:
					dx = 0
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
			else:
				self.values[dt] = None
			yesterday = dt
			
class Squeeze(Indicator):
	def __init__(self, name, bband_lower, bband_upper, keltner_lower, keltner_upper, **kwargs):
		super(Squeeze, self).__init__(name, bband_lower, **kwargs)
		self.bband_lower = bband_lower
		self.bband_upper = bband_upper
		self.keltner_lower = keltner_lower
		self.keltner_upper = keltner_upper
	
	def calculate(self):
		super(Squeeze, self).calculate()

		if not self.bband_lower.ready:
			self.algorithm.setup_indicator(self.bband_lower)
		if not self.bband_upper.ready:
			self.algorithm.setup_indicator(self.bband_upper)			
		if not self.keltner_lower.ready:
			self.algorithm.setup_indicator(self.keltner_lower)			
		if not self.keltner_upper.ready:
			self.algorithm.setup_indicator(self.keltner_upper)
			
		dates = self.dates()
		yesterday = None
		for dt in dates:
			bband_lower_val = self.bband_lower[dt]
			bband_upper_val = self.bband_upper[dt]
			keltner_lower_val = self.keltner_lower[dt]
			keltner_upper_val = self.keltner_upper[dt]
			if bband_lower_val and bband_upper_val and keltner_lower_val and keltner_upper_val:
				prior_squeeze = 0
				if yesterday:
					prior_squeeze = self.values[yesterday]
				
				if bband_lower_val > keltner_lower_val and bband_upper_val < keltner_upper_val:
					self.values[dt] = prior_squeeze + 1 if prior_squeeze > 0 else 1
				else:
					self.values[dt] = 0 #prior_squeeze -1 if prior_squeeze < 0 else -1
			else:
				self.values[dt] = 0
			yesterday = dt
			
class HeikinAshi(Indicator):
	class HeikinAshiFrame(object):
		def __init__(self, dt, o, c, h, l):
			self.dt = dt
			self.o = o
			self.c = c
			self.h = h
			self.l = l		

	def __init__(self, name, open_series, close_series, high_series, low_series, **kwargs):
		super(HeikinAshi, self).__init__(name, close_series, **kwargs)
		self.open_series = open_series
		self.close_series = close_series
		self.high_series = high_series
		self.low_series = low_series
		
	def calculate(self):
		super(HeikinAshi, self).calculate()
		
		dates = self.dates()
		yesterday = None
		for dt in dates:
			o = self.open_series[dt]
			c = self.close_series[dt]
			h = self.high_series[dt]
			l = self.low_series[dt]
			
			prior_ha_o = o
			prior_ha_c = c

			if yesterday:
				prior_ha_o = self.values[yesterday].o
				prior_ha_c = self.values[yesterday].c
			
			ha_c = (o + h + l + c) / 4.0
			ha_o = (prior_ha_o + prior_ha_c) / 2.0
			ha_h = max(h, ha_o, ha_c)
			ha_l = min(l, ha_o, ha_c)
			
			ha = HeikinAshi.HeikinAshiFrame(dt, ha_o, ha_c, ha_h, ha_l)
			self.values[dt] = ha
			yesterday = dt
			
class AverageGain(Indicator):
	def __init__(self, name, close_series, period, **kwargs):
		super(AverageGain, self).__init__(name, close_series, **kwargs)
		self.period = period
	
	def calculate(self):
		super(AverageGain, self).calculate()
		
		dates = self.dates()
		initial_gain = 0
		yesterday = None
		for i, dt in enumerate(dates):	
			current_px = self.series[dt]
			prior_px = self.series[yesterday] if yesterday else current_px
			gain = max(0, current_px - prior_px)
			
			if i >= 0 and i < min(len(dates), self.period-1):
				initial_gain += gain
				self.values[dt] = None
			elif i == self.period-1:
				avg_gain = initial_gain / self.period
				self.values[dt] = float(avg_gain)
			else:
				prior_gain = self.values[yesterday]
				avg_gain = ((prior_gain * (self.period - 1)) + gain) / self.period
				self.values[dt] = float(avg_gain)
			yesterday = dt
			
class AverageLoss(Indicator):
	def __init__(self, name, close_series, period, **kwargs):
		super(AverageLoss, self).__init__(name, close_series, **kwargs)
		self.period = period
	
	def calculate(self):
		super(AverageLoss, self).calculate()
		
		dates = self.dates()
		initial_loss = 0
		yesterday = None
		for i, dt in enumerate(dates):	
			current_px = self.series[dt]
			prior_px = self.series[yesterday] if yesterday else current_px
			loss = abs(min(0, current_px - prior_px))
			
			if i >= 0 and i < min(len(dates), self.period-1):
				initial_loss += loss
				self.values[dt] = None
			elif i == self.period-1:
				avg_loss = initial_loss / self.period
				self.values[dt] = float(avg_loss)
			else:
				prior_loss = self.values[yesterday]
				avg_loss = ((prior_loss * (self.period - 1)) + loss) / self.period
				self.values[dt] = float(avg_loss)
			yesterday = dt
			
class RSI(Indicator):
	def __init__(self, name, ag_series, al_series, **kwargs):
		super(RSI, self).__init__(name, ag_series, **kwargs)
		self.ag_series = ag_series
		self.al_series = al_series
		
	def calculate(self):
		super(RSI, self).calculate()

		if not self.ag_series.ready:
			self.algorithm.setup_indicator(self.ag_series)
		if not self.al_series.ready:
			self.algorithm.setup_indicator(self.al_series)
		
		dates = self.dates()
		is_first = True
		for dt in dates:
			ag_val = self.ag_series[dt]
			al_val = self.al_series[dt]
			
			if ag_val is not None and al_val is not None:
				rs = ag_val / al_val
				rsi = 100.0 - (100.0 / (1 + rs))
				self.values[dt] = rsi
			else:			
				self.values[dt] = None

class Streak(Indicator):
	def __init__(self, name, series, **kwargs):
		super(Streak, self).__init__(name, series, **kwargs)
		
	def calculate(self):
		super(Streak, self).calculate()
		sorted_dates = self.dates()
		
		dates = self.dates()
		
		prior = None
		prior_value = None
		for dt in dates:
			current = self.series[dt]
			if prior:
				if current > prior:
					if prior_value < 0:
						self.values[dt] = 1
					else:
						self.values[dt] = prior_value + 1
				elif current < prior:
					if prior_value < 0:
						self.values[dt] = prior_value - 1
					else:
						self.values[dt] = -1
				else:
					self.values[dt] = 0
			else:
				self.values[dt] = 0
				
			prior = current
			prior_value = self.values[dt]
			
class PercentChange(Indicator):
	def __init__(self, name, series, **kwargs):
		super(PercentChange, self).__init__(name, series, **kwargs)
		
	def calculate(self):
		super(PercentChange, self).calculate()
		
		last_dt = None
		for dt in self.dates():
			if last_dt is None: 
				self.values[dt] = None
			else:
				if self.series[dt] and self.series[last_dt]:
					self.values[dt] = 100 * ((self.series[dt] - self.series[last_dt]) / float(self.series[dt]))
				else:
					self.values[dt] = None
			last_dt = dt

class PercentRank(PercentChange):
	def __init__(self, name, series, period, **kwargs):
		super(PercentRank, self).__init__(name, series, **kwargs)
		self.period = period
		
	def calculate(self):
		super(PercentRank, self).calculate()
		
		dates = self.dates()
		rank_values = OrderedDict()
		for i, dt in enumerate(dates):
			current_change = self.values[dt]			
			rank = None
			
			if i >= self.period:
				rank = 0
				for j, dt2 in enumerate(dates):
					if j >= max(0, i-self.period) and j < i:
						percent_change = self.values[dt2]
						if percent_change is None: percent_change = 0
						if current_change > percent_change:
							rank += 1
			rank_values[dt] = rank if rank is None else 100 * (rank / float(self.period))
		self.values = rank_values
		
class ConnorsRSI(Indicator):
	def __init__(self, name, series, rsi_series, streak_series, percent_rank_series, **kwargs):
		super(ConnorsRSI, self).__init__(name, series, **kwargs)
		self.rsi_series = rsi_series
		self.streak_series = streak_series
		self.percent_rank_series = percent_rank_series
		
	def calculate(self):
		super(ConnorsRSI, self).calculate()
		
		if not self.rsi_series.ready:
			self.algorithm.setup_indicator(self.rsi_series)
		if not self.streak_series.ready:
			self.algorithm.setup_indicator(self.streak_series)
		if not self.percent_rank_series.ready:
			self.algorithm.setup_indicator(self.percent_rank_series)

		dates = self.dates()			
		for i, dt in enumerate(dates):
			rsi = self.rsi_series[dt]
			streak = self.streak_series[dt]
			percent_rank = self.percent_rank_series[dt]
			
			current = None
			if rsi is not None and streak is not None and percent_rank is not None:
				current = (rsi + streak + percent_rank) / 3.0
			self.values[dt] = current
			
class MACD(Indicator):
	def __init__(self, name, series, fast_ema_series, slow_ema_series, **kwargs):
		super(MACD, self).__init__(name, series, **kwargs)
		self.fast_ema_series = fast_ema_series
		self.slow_ema_series = slow_ema_series
		
	def calculate(self):
		super(MACD, self).calculate()
		
		if not self.fast_ema_series.ready:
			self.algorithm.setup_indicator(self.fast_ema_series)
		if not self.slow_ema_series.ready:
			self.algorithm.setup_indicator(self.slow_ema_series)
		
		for dt in self.dates():
			fast_ema = self.fast_ema_series[dt]
			slow_ema = self.slow_ema_series[dt]
			if fast_ema is not None and slow_ema is not None:
				self.values[dt] = fast_ema - slow_ema
			else:
				self.values[dt] = None	

class IBS(Indicator):
	def __init__(self, name, open_series, close_series, high_series, low_series, **kwargs):
		super(IBS, self).__init__(name, close_series, **kwargs)
		self.open_series = open_series
		self.close_series = close_series
		self.high_series = high_series
		self.low_series = low_series		
	
	def calculate(self):
		super(IBS, self).calculate()
	
		dates = self.dates()
		
		for dt in dates:
			o = self.open_series[dt]
			c = self.close_series[dt]
			h = self.high_series[dt]
			l = self.low_series[dt]
		
			self.values[dt] = ((c - l) / (h - l)) * 100