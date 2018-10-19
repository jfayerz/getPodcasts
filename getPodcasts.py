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
#TODO:
#   - Not listing out first five most recent episodes
#   - No entry in the question for selection downloads the oldest ep
#   - No logic is set up to handle "n" in selection
#   - Not parsing "/" in the title correctly for file name
#   - Need to add additional option to skip
#   - Add option at the beginning to just go through all podcasts and download
#       the most recent episodes only
#   - Add option to pick podcast from a list and work only with its episodes
#   - fix logic to display episode list (breaks right now because if there's
#       only 7 episodes in the list, and you try to display the second 5 it doesn't
#       know what to do
#       * a try/except combo won't do it
#       * need to use algorithm based on len(rss.entries)
#   - option to continue scrolling down list of episodes after downloading
#       your first selection

import re
import feedparser as fp
import urllib
import configparser as cp
from datetime import date
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS

todays_date = str(date.today())
configFile = 'podConfig'
histFile = 'podHistory'
rssparams = 'rssparams'
config = cp.ConfigParser()

history = cp.ConfigParser()
config.read(configFile)
history.read(histFile)
config_Sections = config.sections()
history_Sections = history.sections()

def get_parsed_rss(rss_url):
    rss = fp.parse(rss_url)
    parsedRSSFeed = []
    i = 0
    while i <= (len(rss.entries) - 1):
        parsedRSSFeed.append(rss.entries[i].title)
        i += 1
    return rss,parsedRSSFeed

def selection_options(rss_feed_list):
    i = len(rss_feed_list)
    selection_list = ["n"]
    while i > 0:
        a = str(i)
        selection_list.append(a)
        i -= 1
    return selection_list   # returns list populated with options from
                            # 1 through the last option plus 'n'

def display_five(i,a):
    while i < a:
        print("[" + str(i+1) + "] - " + rss.entries[i].title)
        i += 1
    return i

def a_plus_five(i):
    a = (i+5)
    return a

def enterSelection(options,rss):
    i = 0
    a = (i+5)
    selection = 'm'
    while selection.lower() == 'm':
        i = display_five(i,a)
        a = a_plus_five(i)
        print("Enter the number of the podcast episode you wish to download.",
              "\nOr enter \"m\" for [m]ore episodes,\n",
              "\"n\" for the next podcast,\n",
              "\"q\" to quit application.")
        selection = input("Enter your selection here: ")
    r=set()
    for x in selection.split(","):
        t=x.split("-")
        if len(t) == 2:
            r.update(set(range(int(t[0]),int(t[1])+1)))
        else:
            r.add(int(t[0]))
    options = list(r)
    return options
    """
    if item in options:
        return selection    # returns option to be used as an int
    else:                   # to select episode from entries
        print("You have selected an option outside of the available range.",
              "Try again.")
        second_try = input("[Q]uit or [n]ext podcast: ")
        return second_try
    """

def getSelectionURL_Title(list_options,rss):
    url = []
    title = []
    for item in list_options:
        title.append(rss.entries[item-1].title)
        position = rss.entries[item-1].links[0].href.find(".mp3")
        x = rss.entries[item-1].links[0].href
        try:
            y = rss.entries[item-1].links[1].href
        except:
            pass
        if position != -1:
            if x.find(".mp3",(position + 4)) != -1:
                position2 = x.find(".mp3",(position + 4))
                url.append(x[0:(position2 + 4)])
            else:
                url.append(x[0:(position + 4)])
        else:
            position = y.find(".mp3")
            if y.find(".mp3",(position + 4)) != -1:
                position2 = y.find(".mp3",(position + 4))
                url.append(y[0:(position2 + 4)])
            else:
                url.append(y[0:(position + 4)])
        return url,title    # returns a list with the mp3 download url of
                            # the selection and the title of the selection
                        #TODO: eventually add the ability to select more than
                        # one

def get_episode_num(s,parameters):
#function to get episode number from non standard location
    foo1 = parameters[0]
    bar1 = int(parameters[1])
    foo2 = parameters[2]
    bar2 = int(parameters[3])
    name = s.partition(foo1)[bar1]
    return re.sub('[A-Za-z]','', name.partition(foo2)[bar2]).strip()
    #return re.sub('[A-Za-z]','',name)

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

def download_selection(url_list, title_list, history_info, item):
    if len(url_list) > 1:
        i = 0
        fileName_list = []
        while i < len(url_list):
            print("Downloading episode: ", title_list[i])
            title_formatted = re.sub("/","",title_list[i])
            fileName_list.append(title_formatted + ".mp3")
            urllib.request.urlretrieve(
                url_list[i],
                podPath +
                fileName_list[i])
            print("Downloaded ", title_formatted)
            i+=1
        return fileName_list
    else:
        if history_info[item]['last_downloaded_date'] == todays_date:
            print("Already checked " + item + " podcast today.")
        elif history_info[item]['last_url'] == url_list[0]:
            print("Already downloaded this episode: ", title_list[0])
        else:
            print("Downloading episode: ", title_list[0])
            fileName_list = []
            title_formatted = re.sub("/","",title_list[0])
            fileName_list.append(title_formatted + ".mp3")
            urllib.request.urlretrieve(
                url_list[0],
                podPath +
                fileName_list[0])
            history_info[item]['last_url'] == url_list[0]
            history_info[item]['last_downloaded_date'] == todays_date
            with open(histFile,'w') as hist:
                history_info.write(hist)
            return fileName_list



for item in config_Sections:
    rss_url = config[item]['rss']
    rss,parsedRSSFeed = get_parsed_rss(rss_url)
    selection_list = selection_options(parsedRSSFeed)
    options = enterSelection(selection_list,rss)
    if options[0].lower() == 'n':
        print("Next Podcast Coming Right Up!")
        continue
    elif options[0].lower() == 'q':
        print("Thanks for using my app!")
        break
    else:
        url,title = getSelectionURL_Title(options,rss)
        if config[item]['podpath'] != "":       # get path for saving .mp3
            podPath = config[item]['podpath']   #
        else:
            podPath = ""
        fileName_list = download_selection(url, title, history, item)
        number_options = len(options)
        i = config.get(item,"parameters")
        epNum_list = []
        if i != "":                     # checking to see if the parameters
            params = i.split(",")       # option under the selection is populated
        if config[item]['eploc'] == '': # checks to see where the ep# is located
            if config[item]['epnum'] == 'no':   # no episode number indicated
                epNum_list.append("")
                return epNum_list
            else:
                f = 0
                while f < number_options:
                    g = options[f]
                    epNum_list.append(rss.entries[g].itunes_episode)
                    f += 1
                return epNum_list
        elif config[item]['eploc'] == 'title':  # is item set to "title" for pod ep
            epNum_list = get_episode_num(title,params)  #TODO update function
        else:                                           #to handle a list
            epNum = get_episode_num(url,params) # gets ep from url
        if config[item]['snnum'] == 'yes':  # checks for season number
            snNum = rss.entries[0].itunes_season # gets from metadata
        else:
            snNum = ''
        artist = config[item]['artist']
        album = config[item]['album']
        album_artist = config[item]['album_artist']
        writeID3(podPath,fileName,title,epNum,snNum,album,album_artist,artist)
        print("File Saved.\nMetadata written.\n")

# getPodcasts(config_Sections,history_Sections,rssparams)

