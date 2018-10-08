#!/usr/bin/python3

import configparser

url = "http://duh.com"
config = configparser.ConfigParser()
history = configparser.ConfigParser()
config.read('podConfig')
history.read('podHistory')

"""

"""

for item in config.sections(): #iterating through config sections
	print(config[item]['rss'])
	if item in history.sections():          #checks to see if the item from 
                                            #config sections is in history sections
		if url == history[item]['last_url']:    #checks to see if previously
                                                #obtained url from rss is the 
                                                #same as the existing url in the
                                                #podHistory file
			print("yay")
		else:
			history[item]['last_url'] = url #changes the last_url value to the
                                            #new url value
			with open('podHistory','w') as histories:   #opens writeable
        	                                                #version of podHistory
				history.write(histories)    #writes history including the new
                                            #information from above
