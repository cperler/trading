import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from matplotlib.dates import DayLocator, MONDAY
from datetime import date
import data
import logging
import pprint
from positions import *
from algorithm import Algorithm
from indicators import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

cube = data.load(['GOOG', 'YHOO'], '20120101', '20120131')
#cube.write_to_csv('test.csv')
#cube.pretty_print()

oms = OMS()

t1 = Transaction('GOOG', date(2012, 1, 1), 10, 100)
t2 = Transaction('GOOG', date(2012, 3, 1), 15, 150)
t3 = Transaction('GOOG', date(2012, 10, 1), 50, 500)
t4 = Transaction('IBM', date(2012, 4, 1), -5, 50)
t5 = Transaction('IBM', date(2012, 11, 1), 5, 35)

oms.add(t1)
oms.add(t2)
oms.add(t3)
oms.add(t4)
oms.add(t5)

for t in oms.blotter.all():
	print t
	
for t in oms.portfolio.all():
	print t
 	
class SMATest(Algorithm):
	def __init__(self, symbols, start_date, end_date):
		super(SMATest, self).__init__(symbols, start_date, end_date)		
		
	def pre_run(self):
		super(SMATest, self).pre_run()
		self.sma5 = SMA(series=self.cube.data[('GOOG', 'adjclose')], period=5)
		self.indicators.append(self.sma5)
		
	def handle_data(self, dt, symbols, keys, data):
		for symbol in symbols:
			for key in keys:
				pass #print dt, symbol, key, data[(symbol, key)]

	def post_run(self):
		sma = {'name': 'GOOG_SMA_5', 'data' : self.sma5.value }
		extra_series = []
		extra_series.append(sma)
		self.cube.write_to_csv('test.csv', extra_series)
		
algo = SMATest('GOOG', '20120101', '20121231')
algo.run()

def plot_data_with_dates(x_list, y_list, x_label, y_label, format, label_list, title):
	'''
	Helper function for charting multiple series of data with a date-based X axis.
	'''
	if len(y_list) != len(label_list):
		raise Exception('# of series to plot does not match # of labels for legend.')
	
	fig = plt.figure(figsize=(6*3.13,4*3.13))
	graph = fig.add_subplot(111)
	data = zip(x_list, y_list, label_list)

	for x, y, label in data:
		plt.plot_date(x, y, format, label=label)
	plt.legend(loc=3, prop={'size':8})
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	return plt

def candlestick(ax, quotes, width=0.2, colorup='k', colordown='r', alpha=1.0):
    OFFSET = width/2.0

    lines = []
    patches = []
    idx = 0
    for q in quotes:
        _, t, open, close, high, low = q[:6]

        if close>=open :
            color = colorup
            lower = open
            height = close-open
        else           :
            color = colordown
            lower = close
            height = open-close

        vline = Line2D(
            xdata=(idx, idx), ydata=(low, high),
            color='k',
            linewidth=0.5,
            antialiased=True,
            )

        rect = Rectangle(
            xy    = (idx-OFFSET, lower),
            width = width,
            height = height,
            facecolor = color,
            edgecolor = color,
            )
        rect.set_alpha(alpha)


        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
        idx += 1
    ax.autoscale_view()

    return lines, patches
	
def candles(dates, quotes):
	N = len(dates)
	r = quotes
	def format_date(x, pos=None):
		if x < 0:
			return (mdates.num2date(mdates.date2num(r[0][0])+x)).strftime('%Y-%m-%d')
		else:
			thisind = np.clip(int(x+0.5), 0, N-1)	
			return r[thisind][0].strftime('%Y-%m-%d')
			
	fig = plt.figure(figsize=(6*3.13,4*3.13))
	graph = fig.add_subplot(111)
	ind = range(N)
	candlestick(graph, quotes)
	graph.plot(ind, [q[2] for q in quotes], '-')
	graph.xaxis.set_minor_formatter(ticker.FuncFormatter(format_date))		
	graph.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))		
	setp(gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	return plt
	
#plot_data_with_dates([algo.cube.dates, algo.cube.dates], [algo.cube.get_values('GOOG', 'open'), algo.cube.get_values('GOOG', 'close')], 'Date', 'Px', '-', ['Open', 'Close'], 'Graph').show()

time = [mdates.date2num(dt) for dt in algo.cube.get_dates()]
open = algo.cube.get_values('GOOG', 'open')
close = algo.cube.get_values('GOOG', 'close')
low = algo.cube.get_values('GOOG', 'low')
high = algo.cube.get_values('GOOG', 'high')
candles(time, zip(algo.cube.get_dates(), time, open, close, low, high)).show()