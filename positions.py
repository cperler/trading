from datetime import datetime
from collections import defaultdict
from util import enum, flexfilter
               
class Transaction(object):
	Side = enum(BUY='buy', SELL='sell')
   
	def __init__(self, symbol, dt, px, qty):
		if qty == 0:
			raise Exception('Cannot transact in 0-value quantity.')
					   
		self.symbol = symbol
		self.dt = dt
		self.px = px
		self.qty = qty
   
	@staticmethod
	def sort(txns):
		# TODO: sort by multiple keys (dt - symbol - px - qty)
		sorted_txns = sorted(txns, key=lambda txn: txn.dt)
		for i in range(0, len(sorted_txns)):
			yield sorted_txns[i]
			   
	def cost(self):
		return self.px * self.qty
   
	def side(self):
		return Transaction.Side.SELL if self.qty < 0 else Transaction.Side.BUY

	def __repr__(self):
		return 'Transaction({}, {}, {}, {})'.format(self.symbol, self.dt, self.px, self.qty)
   
	def __str__(self):
		return '[{}] {} {} of {} @ {}'.format(datetime.strftime(self.dt, '%Y-%m-%d'), self.side(), abs(self.qty), self.symbol, self.px)
 
class Blotter(object):
	def __init__(self):
		self.txns = []
				   
	def add(self, txn):
		self.txns.append(txn)
				   
	def all(self, symbols=None, start=None, end=None):		
		return Transaction.sort([txn for txn in flexfilter(self.txns, 'symbol', symbols) 
			if (start is None or txn.dt >= start) and (end is None or txn.dt < end)])
                               
class Position(object):
	def __init__(self, symbol):
		self.symbol = symbol
		self.txns = []
		self.amount = 0.0
		self.cost_basis = 0.0
                               
	def cost(self):
		return self.cost_basis * self.amount
                               
	def add(self, txn):
		if self.symbol != txn.symbol:
			raise Exception('Attempt to add a transaction to a wrong position!')
 
		self.txns.append(txn)
		if self.amount + txn.qty == 0:
			self.cost_basis = 0.0
			self.amount = 0
		else:
			total_cost = self.cost() + txn.cost()
			self.amount = self.amount + txn.qty
			self.cost_basis = total_cost / self.amount
               
	def is_open(self):
		return self.amount != 0.0
								   
	def transactions(self):
		return Transaction.sort(self.txns)
	   
	def __repr__(self):
		return 'Position({}, {}, {})'.format(self.symbol, self.amount, self.cost_basis)
 
class Portfolio(object):
	def __init__(self):
		self.positions = defaultdict(list)
   
	def add(self, txn, position=None):
		if position is None:
			position = self.positions[txn.symbol]
		position.append(txn)
				   
	def all(self, only_open=False, only_closed=False):
		return [position for position in self.positions.items() if
			~(only_open or only_closed) or
			(only_open and position.is_open()) or
			(only_closed and ~position.is_open())]
                                               
class OMS(object):
	def __init__(self):
		self.blotter = Blotter()
		self.portfolio = Portfolio()