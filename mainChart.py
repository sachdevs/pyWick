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


for i in stocksToPull:
	pullData(i, 3, 7, 2014)

def graphData(stock):
	try:
		stockFile = 'Quotes/'+stock+'.txt'
		date, openp, highp, lowp, closep, volume, adjClose = np.loadtxt(stockFile, delimiter=',', unpack = True,
			converters={0: mdates.strpdate2num('%Y-%m-%d')})

		fig = plt.figure()
		ax1 = plt.subplot(1,1,1)
		ax1.plot(date, openp)
		ax1.plot(date, closep)
		ax1.plot(date, highp)
		ax1.plot(date, lowp)

		plt.show()

	except Exception, e:
		print 'failed main loop', str(e)

graphData('MSFT')