import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

def plot_data_with_dates(x_list, y_list, x_label, y_label, format, label_list, title):
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
	#graph.plot(ind, [q[2] for q in quotes], '-')
	graph.xaxis.set_minor_formatter(ticker.FuncFormatter(format_date))		
	graph.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))		
	setp(gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	return plt

def plot_candles(cube):
	time = [mdates.date2num(dt) for dt in cube.get_dates()]
	open = cube.get_values('GOOG', 'open')
	close = cube.get_values('GOOG', 'close')
	low = cube.get_values('GOOG', 'low')
	high = cube.get_values('GOOG', 'high')
	return candles(time, zip(cube.get_dates(), time, open, close, low, high))

