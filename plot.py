import matplotlib.pyplot as plt
from numpy import nan
from pylab import *
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.gridspec as gridspec

def plot_data_with_dates(x_list, y_list, x_label, y_label, format, label_list, title):
	if len(y_list) != len(label_list):
		raise Exception('# of series to plot does not match # of labels for legend.')
	
	fig = plt.figure(figsize=(6*3.13,4*3.13))
	graph = fig.add_subplot(111)
	data = zip(x_list, y_list, label_list)	

	for x, y, label in data:
		y_values = y
		if type(y).__name__ == 'OrderedDict':
			y_values = y.values()
		plt.plot_date(x, y_values, format, label=label)
	plt.legend(loc=3, prop={'size':8})
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.grid(True)
	return plt
	
def multi_plot_data_with_dates(x_list, y_lists, x_label, y_labels, format, label_lists, title):
	if len(y_lists) != len(label_lists):
		raise Exception('subplot mismatch')
	for y_list, label_list in zip(y_lists, label_lists):
		if len(y_list) != len(label_list):
			raise Exception('# of series to plot does not match # of labels for legend.')

	subplots = []
	fig = plt.figure(figsize=(6*3.13,4*3.13))
	for i in range(0, len(y_lists)):
		data = zip([x_list] * len(y_lists[i]), y_lists[i], label_lists[i])		
		if i == 0:
			graph = plt.subplot2grid((len(y_lists) + 2, 1), (i, 0), rowspan=3)
		else:
			graph = plt.subplot2grid((len(y_lists) + 2, 1), (i+2, 0))
		subplots.append(graph)
		sum_y = 0
		num_y = 0
		for x, y, label in data:
			y_values = y
			if type(y).__name__ == 'OrderedDict':
				y_values = y.values()
			
			sum_y += sum([y for y in y_values if y])
			num_y += len(y_values)
			plt.plot_date(x, y_values, format, label=label)
		
		plt.plot_date(x_list, [sum_y / num_y] * len(x_list), visible=False)
		plt.legend(loc=3, prop={'size':8})
		if i == 0:
			plt.title(title)
		if i == len(y_lists)-1:
			plt.xlabel(x_label)
		plt.ylabel(y_labels[i])
		plt.grid(True)
	return (plt, subplots)

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
