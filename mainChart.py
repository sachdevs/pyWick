import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
plt.rcParams.update({'font.size': 11})

stocksToPull = 'AAPL','GOOG','MSFT','CMG','TSLA','FB'

##################################################################
#        Scrapes historical data from Yahoo Finance API
##################################################################
def pullData(stock, m, d, y):
	try:
		fileLine = 'Quotes/'+stock+'.txt'
		# API call URL
		urlToVisit = 'http://ichart.yahoo.com/table.csv?s='+stock+'&a='+str(m-1)+'&b='+str(d)+'&c='+str(y)
		sourceCode = urllib2.urlopen(urlToVisit).read()
		splitSource = sourceCode.split('\n')

		# CSV formatting
		for eachLine in splitSource:
			splitLine = eachLine.split(',')
			if 'Date' not in eachLine:
				saveFile = open(fileLine, 'a')
				lineToWrite = eachLine+'\n'
				saveFile.write(lineToWrite)

		# Debugging statements
		print 'Pulled', stock
		print 'sleeping'
		# Time b/w each pull
		time.sleep(1)

	except Exception, e:
		print 'main loop', str(e)

##################################################################
#                 SMA calculator (using numpy)
##################################################################
def simpleMovingAvg(values, window):
	# sma formula 
	weights = np.repeat(1.0, window)/window
	# smoother (convolve smooths)
	smas = np.convolve(values, weights, 'valid')
	return smas

##################################################################
#       Grapher, params (Name of stock, SMA1 day, SMA2 day)
##################################################################
def graphData(stock, SMA1, SMA2):
	try:
		# -------Process Stock Data--------
		stockFile = 'Quotes/'+stock+'.txt'
		date, openp, highp, lowp, closep, volume, adjClose = np.loadtxt(stockFile, delimiter=',', unpack = True,
			converters={0: mdates.strpdate2num('%Y-%m-%d')})
		
		x = 0
		y = len(date)
		candleArr = []
		# Data into candlestick parameter format
		while x<y:
			appendLine = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
			candleArr.append(appendLine)
			x+=1


		# simplemovingavg
		av1 = simpleMovingAvg(closep, SMA1)
		av2 = simpleMovingAvg(closep, SMA2)

		# starting point of sma (since the x day moving average cannot start until x days have first been completed)
		#TODO ###### NEED TO MAKE DYNAMIC ################
		startingPoint = len(date[SMA2-1:])

		# legend label stuffs
		label1 = str(SMA1)+' SMA'
		label2 = str(SMA2)+' SMA'

		fig = plt.figure(facecolor='#07000d')

		# -------PRICE GRAPH--------
		ax1 = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4, axisbg='#07000d')

		# Candlestick plot details
		candlestick(ax1, candleArr, width=1, colorup='#9eff15', colordown='#ff1717')
		# uncomment this section and comment line above to switch b/w line graph and candlestick
		# ax1.plot(date, openp)
		# ax1.plot(date, closep)
		# ax1.plot(date, highp)
		# ax1.plot(date, lowp)

		# plot the SMA on axis 1
		ax1.plot(date[:startingPoint], av1[:startingPoint], '#5998ff', label= label1, linewidth=1.2)
		ax1.plot(date[:startingPoint],av2[:startingPoint], '#e1edf9', label= label2, linewidth=1.2)

		# Mostly styling
		plt.ylabel('Price')
		ax1.grid(True, color='w')
		ax1.yaxis.label.set_color('w')
		ax1.spines['bottom'].set_color('#5998ff')
		ax1.spines['left'].set_color('#5998ff')
		ax1.spines['top'].set_color('#5998ff')
		ax1.spines['right'].set_color('#5998ff')
		ax1.tick_params(axis='y', colors='w')

		# Legend stuffs
		plt.legend(loc=2, prop={'size': 10}, fancybox=True)

		# -------VOLUME GRAPH--------
		volumeMin = 0

		ax2 = plt.subplot2grid((4,4), (3,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
		ax2.plot(date, volume, '#00ffe8', linewidth=.8)
		ax2.fill_between(date, volumeMin, volume, facecolor='#00ffe8', alpha=.5)

		# Mostly styling
		ax2.axes.yaxis.set_ticklabels([])
		plt.ylabel('Volume')
		ax2.grid(True, color="w")
		ax2.yaxis.label.set_color('w')
		ax2.xaxis.label.set_color('w')
		ax2.spines['bottom'].set_color('#5998ff')
		ax2.spines['left'].set_color('#5998ff')
		ax2.spines['top'].set_color('#5998ff')
		ax2.spines['right'].set_color('#5998ff')

		ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

		# Rotate xaxis labels on volume graph and delete xaxis labels on price graph
		for label in ax1.xaxis.get_ticklabels():
			label.set_visible(False)
		for label in ax2.xaxis.get_ticklabels():
			label.set_rotation(75)
			label.set_color("w")

		plt.subplots_adjust(left=0.07, bottom=.24, right=0.95, top=0.93, wspace=.20, hspace=0.00)

		plt.suptitle(stock+" Price", color='w')
		
		plt.show()

	except Exception, e:
		print 'failed main loop', str(e)

#INSERT LOGIC TO DO PULLS VIA  pullData(stock, month, day, year) function
#########################################################################

# Call the graph function on run
graphData('MSFT', 12, 26)