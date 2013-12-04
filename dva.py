import logging
import datetime
from positions import *
from algorithm import Algorithm
from indicators import *
from plot import *
import pprint

stocks = ['SPY']

class DVATest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		self.one_day = datetime.timedelta(days=1)
		self.target_value = 0 
		self.expected_monthly_return = 1.006
		self.initial_investment = 500
		self.initial_investment_made = False		
		super(DVATest, self).__init__(symbols, start_date, end_date)		
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:					
			
			px = data[(symbol, 'close')]
			if self.initial_investment_made == False:
				shares_to_order = round((self.initial_investment - 9.99) / px)
				self.oms.add(Transaction(symbol, dt, px, shares_to_order))
				print('Initial investment: we buy %s shares for %s on %s' % (shares_to_order, px, dt))
				self.initial_investment_made = True
				self.target_value += self.initial_investment * self.expected_monthly_return
				
			next_trade_day = None
			while next_trade_day is None or next_trade_day.weekday() > 4:
				if next_trade_day is None:
					next_trade_day = dt
				next_trade_day = next_trade_day + self.one_day
			current_month = dt.month
						
			cost = self.oms.portfolio.positions[symbol].amount * px
			if next_trade_day.month != current_month:		
				if cost < self.target_value:
					budget = self.target_value - cost - 9.99
					shares_to_order = round(budget / px)
					if shares_to_order >= 2:
						self.oms.add(Transaction(symbol, dt, px, shares_to_order))
						print('Target value (%s) exceeds portfolio value (%s). We buy %s shares for %s on %s' % (self.target_value, cost, shares_to_order, px, dt))
					else:
						print("Minimum buying threshold not reached")
				elif self.oms.portfolio.positions[symbol].is_open():
					budget = cost - self.target_value - 9.99
					shares_to_sell = round(budget / px)
					if shares_to_sell >= 2:
						self.oms.add(Transaction(symbol, dt, px, -shares_to_sell))
						print('Portfolio value (%s) is below target value (%s). We sell %s shares for %s on %s' % (cost, self.target_value, shares_to_sell, px, dt))
					else:
						print("Minimum selling threshold not reached")
				
				self.target_value += 500

	def post_run(self):
		self.results()
		for symbol in self.symbols:
			self.plot(symbol=symbol).show()

test = DVATest(stocks, '20130103', '20131021')
test.run()