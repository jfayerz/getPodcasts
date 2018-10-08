#!/usr/bin/python3

"""
Notes:
testpython.py
the purpose of this is to test the function that I wrote
"""

import feedparser
import urllib
import configparser

configFile = 'podConfig'
histFile = 'podHistory'

config = configparser.ConfigParser()
history = configparser.ConfigParser()
config.read(configFile)
history.read(histFile)
config_Sections = config.sections()
history_Sections = history.sections()
rssparams = 'rssparams'

def unnamedFunction(config_Sections,history_Sections,rssparams): #rename? what am I passing to this function
	for item in config_Sections:
		print(item)
		rss = feedparser.parse(config[item]['rss'])
		rss_param_left = int(config[item][rssparams].split(",")[0])
		rss_param_right = int(config[item][rssparams].split(",")[1])
		last_url = history[item]['last_url']
		if config[item]['urlFormat'] == 'questionmark':
			url = rss.entries[rss_param_left].links[rss_param_right].href.partition("?")[0].rstrip()
	else:
		url = rss.entries[rss_param_left].links[rss_param_right].href
		title = rss.entries[rss_param_left].title.rstrip()
		fileName = title + ".mp3"
	if item in history_Sections:
		if url != last_url:
			history[item]['last_url'] = url
			with open('podHistory','w') as pH:
				history.write(pH)   #writes entire podHistory
                                                    #file with new information 
                                                    #in the matching item 
                                                    #last_url field
			urllib.request.urlretrieve(url,fileName)
		else:
			print("Already Downloaded " + item + " episode.")
	else:
		print("Error")

print(config_Sections)
print(history_Sections)
unnamedFunction(config_Sections,history_Sections,rssparams)
