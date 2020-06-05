import yfinance

def get_historical_prices(symbol, start, end):
	ticker = yfinance.Ticker(symbol)
	return ticker.history(start=start, end=end)
