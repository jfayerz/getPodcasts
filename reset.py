#! /usr/bin/env python3
import configparser as cp
history = cp.ConfigParser()
history.read('./pod_history')
history['The Dollop']['last_url'] = ''
#history['The NoSleep Podcast']['last_url'] = ''
history['The Dollop']['last_downloaded_date'] = ''
#history['The NoSleep Podcast']['last_downloaded_date'] = ''
with open('./pod_history', 'w') as pH:
    history.write(pH)

