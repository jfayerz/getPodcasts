#!/usr/bin/python3

"""
Notes:
Simple podcast downloader
- gets the rss
- gets the url
- downloads the most recent episode
- edits the metadata

written by Jonathan Ayers
https://github.com/jfayerz/getPodcasts
"""
import re
import feedparser
import urllib
import configparser
from datetime import date
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS

todays_date = str(date.today())
configFile = 'podConfig'
histFile = 'podHistory'
rssparams = 'rssparams'
config = configparser.ConfigParser()

history = configparser.ConfigParser()
config.read(configFile)
history.read(histFile)
config_Sections = config.sections()
history_Sections = history.sections()

def get_episode_num(s,parameters):
#function to get episode number from non standard location
    foo1 = parameters[0]
    bar1 = int(parameters[1])
    foo2 = parameters[2]
    bar2 = int(parameters[3])
    name = s.partition(foo1)[bar1]
    return re.sub('[A-Za-z]','', name.partition(foo2)[bar2]).strip()
    #return re.sub('[A-Za-z]','',name)

def getPodcasts(config_Sections,history_Sections,rssparams):
    for item in config_Sections:
        if todays_date != history[item]['last_downloaded_date']:
            rss_param_left = int(config[item][rssparams].split(",")[0])
            rss_param_right = int(config[item][rssparams].split(",")[1])
            print("Getting rss info for " + item + ".")
            rss = feedparser.parse(config[item]['rss'])
            if config[item]['podpath'] != "":
                podPath = config[item]['podpath']
            i = config.get(item,"parameters")
            if i != "":
                params = i.split(",")
            title = rss.entries[rss_param_left].title.strip()
            fileName = re.sub('/',' ', title) + ".mp3"
            artist = config[item]['artist']
            album = config[item]['album']
            album_artist = config[item]['album_artist']
            last_url = history[item]['last_url']
            position = rss.entries[0].links[1].href.find(".mp3")
            if position != -1:
                url = rss.entries[0].links[1].href[0:(position + 4)]
            else:
                position = rss.entries[0].links[0].href.find(".mp3")
                url = rss.entries[0].links[0].href[0:(position + 4)]
            #if config[item]['urlFormat'] == 'questionmark':
            #   url = rss.entries[rss_param_left].links[rss_param_right].href.partition("?")[0].strip()
            #else:
            #   url = rss.entries[rss_param_left].links[rss_param_right].href
            if config[item]['eploc'] == '':
                if config[item]['epnum'] == 'no':
                    epNum = ''
                else:
                    epNum = rss.entries[rss_param_left].itunes_episode
            elif config[item]['eploc'] == 'title':
                epNum = get_episode_num(title,params)
            else:
                epNum = get_episode_num(url,params)
            if config[item]['snnum'] == 'yes':
                snNum = rss.entries[rss_param_left].itunes_season
            else:
                snNum = ''
            #fileName = title + ".mp3"
            if item in history_Sections:
                if url != last_url:
                    history[item]['last_url'] = url
                    history[item]['last_downloaded_date'] = todays_date
                    with open('podHistory','w') as pH:
                        history.write(pH)
                    print("Downloading " + title + " from the " + item + " podcast.")
                    if podPath != "":
                        urllib.request.urlretrieve(url,podPath + fileName)
                    else:
                        urllib.request.urlretrieve(url,fileName)
                    writeID3(podPath,fileName,title,epNum,snNum,album,album_artist,artist)
                else:
                    print("Already Downloaded " + item + " episode.")
            else:
                print("Error")
        else:
            print("Already checked " + config[item]['album'] + " podcast today.")

def writeID3(podPath,fileName,title,epNum,snNum,alb,albart,art):
    try:
        audio = ID3(podPath + fileName)
        audio.delete()
        audio = ID3()
    except ID3NoHeaderError:
        audio = ID3()
    audio.add(TIT2(encoding=3, text=title))
    if epNum != "":
        audio.add(TRCK(encoding=3, text=epNum))
    else:
        print("No Ep Num")
    if snNum != "":
        audio.add(TPOS(encoding=3, text=snNum))
    else:
        print("No Sn Num")
    audio.add(TPE1(encoding=3, text=art))
    audio.add(TPE2(encoding=3, text=albart))
    audio.add(TALB(encoding=3, text=alb))
    audio.save(podPath + fileName)


getPodcasts(config_Sections,history_Sections,rssparams)
