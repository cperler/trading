import ystockquote
from util import *
import logging
import time
from datetime import datetime

class Quote(object):
	def __init__(self, d, o, h, l, c, v, a):
		self.d = datetime(*(time.strptime(d, '%Y-%m-%d')[0:6]))
		self.o = float(o)
		self.h = float(h)
		self.l = float(l)
		self.c = float(c)
		self.v = float(v)
		self.a = float(a)
 
	def __str__(self):
		return '[' + datetime.strftime(self.d, '%Y-%m-%d') + '] ' + str(self.a)
 
	def __repr__(self):
		return self.__str__()

class Cube(object):
	'''symbol -> key -> date -> value'''
	def __init__(self):
		self.dates = []
		self.data = {}
	
	def add_quote(self, symbol, quote):
		self.add(quote.d, symbol, 'open', quote.o)
		self.add(quote.d, symbol, 'high', quote.h)
		self.add(quote.d, symbol, 'low', quote.l)
		self.add(quote.d, symbol, 'close', quote.c)
		self.add(quote.d, symbol, 'volume', quote.v)
		self.add(quote.d, symbol, 'adjclose', quote.a)
	
	def add(self, date, symbol, key, value):
		if date not in self.dates:
			self.dates.append(date)
		if symbol not in self.data:
			self.data[symbol] = {}
		if key not in self.data[symbol]:
			self.data[symbol][key] = {}
		if date not in self.data[symbol][key]:
			self.data[symbol][key][date] = value
		
def load(symbols, start, end):		
	if type(symbols) is str:
		symbols = [symbols]
	
	cube = Cube()
	for symbol in symbols:
		logging.debug('Loading data for {}, {} - {}.'.format(symbol, start, end))
		filename = '{}_{}_{}.pkl'.format(symbol, start, end)
		if file_exists(filename):
			data = pickle_load(filename)
		
		data = ystockquote.get_historical_prices(symbol, start, end)
		pickle_it(filename, data)
		
		for line in data[1:]:
			quote = Quote(*line)
			cube.add_quote(symbol, quote)
	
	return cube