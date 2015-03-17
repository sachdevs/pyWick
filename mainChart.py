import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

stocksToPull = 'AAPL','GOOG','MSFT','CMG','TSLA','FB'

def pullData(stock, m, d, y):
	try:
		fileLine = 'Quotes/'+stock+'.txt'
		urlToVisit = 'http://ichart.yahoo.com/table.csv?s='+stock+'&a='+str(m-1)+'&b='+str(d)+'&c='+str(y)
		sourceCode = urllib2.urlopen(urlToVisit).read()
		splitSource = sourceCode.split('\n')

		for eachLine in splitSource:
			splitLine = eachLine.split(',')
			if 'Date' not in eachLine:
				saveFile = open(fileLine, 'a')
				lineToWrite = eachLine+'\n'
				saveFile.write(lineToWrite)

		print 'Pulled', stock
		print 'sleeping'
		time.sleep(1)

	except Exception, e:
		print 'main loop', str(e)

def graphData(stock):
	try:
		stockFile = 'Quotes/'+stock+'.txt'
		date, openp, highp, lowp, closep, volume, adjClose = np.loadtxt(stockFile, delimiter=',', unpack = True,
			converters={0: mdates.strpdate2num('%Y-%m-%d')})

		fig = plt.figure()
		ax1 = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
		ax1.plot(date, openp)
		ax1.plot(date, closep)
		ax1.plot(date, highp)
		ax1.plot(date, lowp)
		plt.ylabel('Price')
		ax1.grid(True)

		ax2 = plt.subplot2grid((4,4), (3,0), sharex=ax1, rowspan=1, colspan=4)
		ax2.bar(date, volume)
		plt.ylabel('Volume')
		ax2.grid(True)

		ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

		for label in ax1.xaxis.get_ticklabels():
			label.set_visible(False)
		for label in ax2.xaxis.get_ticklabels():
			label.set_rotation(75)

		plt.subplots_adjust(left=0.1, bottom=.25, right=0.93, top=0.95, wspace=.20, hspace=0.07)

		plt.suptitle(stock+" Price")
		plt.xlabel('Date')
		
		plt.show()

	except Exception, e:
		print 'failed main loop', str(e)

graphData('CMG')