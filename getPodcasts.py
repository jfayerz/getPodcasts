#! /usr/bin/env python3

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
#   - option to continue scrolling down list of episodes after downloading
#       your first selection

import sys
import re
import feedparser as fp
import urllib
import configparser as cp
from datetime import date
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS

arg1 = len(sys.argv)
todays_date = str(date.today())
configPath = ''
configFile = 'podConfig'
histFile = 'podHistory'
rssparams = 'rssparams'
config = cp.ConfigParser()
history = cp.ConfigParser()
config.read(configPath + configFile)
history.read(configPath + histFile)
config_Sections = config.sections()
history_Sections = history.sections()

def getPodcasts(config_Sections,history_Sections,rssparams):
    for item in config_Sections:
        if todays_date != history[item]['last_downloaded_date']:
            # rss_param_left = int(config[item][rssparams].split(",")[0])
            # rss_param_right = int(config[item][rssparams].split(",")[1])
            print("Getting rss info for " + item + ".")
            rss = fp.parse(config[item]['rss'])
            if config[item]['podpath'] != "":
                podPath = config[item]['podpath']
            else:
                podPath = ""
            i = config.get(item,"parameters")
            if i != "":
                params = i.split(",")
            title = []
            c = rss.entries[0].title.strip()
            title.append(c)
            fileName = []
            b = re.sub('/',' ', title[0]) + ".mp3"
            fileName.append(b)
            artist = config[item]['artist']
            album = config[item]['album']
            album_artist = config[item]['album_artist']
            last_url = history[item]['last_url']
            position = rss.entries[0].links[0].href.find(".mp3")
            url = []
            if position != -1:
                if rss.entries[0].links[0].href.find(".mp3",(position + 4)) != -1:
                    position2 = rss.entries[0].links[0].href.find(".mp3",(position + 4))
                    url.append(rss.entries[0].links[0].href[0:(position2 + 4)])
                else:
                    url.append(rss.entries[0].links[0].href[0:(position + 4)])
            else:
                try:
                    position = rss.entries[0].links[1].href.find(".mp3")
                except:
                    continue
                if rss.entries[0].links[1].href.find(".mp3",(position + 4)) != -1:
                    position2 = rss.entries[0].links[1].href.find(".mp3",(position + 4))
                    url.append(rss.entries[0].links[1].href[0:(position2 + 4)])
                else:
                    url.append(rss.entries[0].links[1].href[0:(position + 4)])
            if config[item]['eploc'] == '':
                if config[item]['epnum'] == 'no':
                    epNum = ''
                else:
                    try:
                        epNum = rss.entries[0].itunes_episode
                    except:
                        epNum = ""
            elif config[item]['eploc'] == 'title':
                epNum = get_episode_num(title,params)
            else:
                epNum = get_episode_num(url,params)
            if config[item]['snnum'] == 'yes':
                snNum = rss.entries[0].itunes_season
            else:
                snNum = ''
            if item in history_Sections:
                if url[0] != last_url:
                    history[item]['last_url'] = url[0]
                    history[item]['last_downloaded_date'] = todays_date
                    with open(configPath + histFile,'w') as pH:
                        history.write(pH)
                    print("Downloading " + title[0] + " from the " + item + " podcast.")
                    if podPath != "":
                        try:
                            urllib.request.urlretrieve(url[0],podPath +
                                                       fileName[0])
                        except urllib.error.HTTPError:
                            print("Download error with " + title[0] + " episode.")
                            continue
                    else:
                        try:
                            urllib.request.urlretrieve(url[0],podPath +
                                                       fileName[0])
                        except urllib.HTTPError:
                            print("Download error with " + title[0] + " episode.")
                            continue
                    writeID3(podPath,fileName,title,epNum,snNum,album,album_artist,artist)
                else:
                    print("Already Downloaded " + item + " episode.")
            else:
                print("Error")
        else:
            print("Already checked " + config[item]['album'] + " podcast today.")

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

def display_five(i,a,rss,podcast_name,multiples,remainder):
    if a > len(rss.entries):
        print("You've Reached the Maximum",
              "\nStarting from the beginning of the list.")
        multiples = int((len(rss.entries) / 5))
        i = 0
        return i,multiples
    else:
        number_of_eps = len(rss.entries)
        print("Episodes from " + podcast_name + " Podcast",
              "\nThere are currently " + str(number_of_eps) + " Episodes",
              " for this Podcast rss.")
        while i < a:
            print("[" + str(i+1) + "] - " + rss.entries[i].title)
            i += 1
        multiples-=1
        return i,multiples

def a_plus_five(i,multiples,remainder):
    if multiples == 0:
        a = (i+remainder)
    else:
        a = (i+5)
    return a

def enterSelection(options,rss,podcast_name):
    remainder = int(len(rss.entries) % 5)
    multiples = int((len(rss.entries) / 5))
    i = 0
    if multiples < 5:
        a = remainder
    else:
        a = 5
    selection = 'm'
    entries_total = len(rss.entries)-1
    while selection.lower() == 'm':
        i,multiples = display_five(i,a,rss,podcast_name,multiples,remainder)
        a = a_plus_five(i,multiples,remainder)
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
            if t[0].isalpha():
                r.add(t[0])
            else:
                r.add(int(t[0]))
    options = list(r)
    if options[0] == 'n':
        return options
    elif options[0] == 'q':
        return options
    else:
        for z in options:
            if z > len(rss.entries):
                print("Your selection is out of range")
                break
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
    print(url,title)
    return url,title    # returns a list with the mp3 download url of
                            # the selection and the title of the selection
                        #TODO: eventually add the ability to select more than
                        # one

def get_episode_num(urltitle_list,parameters):
#function to get episode number from non standard location
    foo1 = parameters[0]
    bar1 = int(parameters[1])
    foo2 = parameters[2]
    bar2 = int(parameters[3])
    epNum_list = []
    for x in urltitle_list:
        left_part = x.partition(foo1)[bar1]
        epNum_list.append(re.sub('[A-Za-z]','',
                                 left_part.partition(foo2)[bar2]).strip())
    print(epNum_list)
    return epNum_list
    #return re.sub('[A-Za-z]','',name)

def writeID3(podPath,file_name,titles,epNum,snNum,alb,albart,art):
    for x in file_name:
        n = file_name.index(x)
        try:
            audio = ID3(podPath + x)
            audio.delete()
            audio = ID3()
        except ID3NoHeaderError:
            audio = ID3()
        audio.add(TIT2(encoding=3, text=titles[n]))
        if len(epNum) != 0:
            audio.add(TRCK(encoding=3, text=epNum[n]))
        else:
            print("No Ep Num")
        if len(snNum) != 0:
            audio.add(TPOS(encoding=3, text=snNum[n]))
        else:
            print("No Sn Num")
        audio.add(TPE1(encoding=3, text=art))
        audio.add(TPE2(encoding=3, text=albart))
        audio.add(TALB(encoding=3, text=alb))
        audio.save(podPath + x)

def download_selection(podPath, url_list, title_list, history_info, item):
    file_names = []
    if len(url_list) > 1:
        i = 0
        while i < len(url_list):
            print("Downloading episode: ", title_list[i])
            title_formatted = re.sub("/","",title_list[i])
            file_names.append(title_formatted + ".mp3")
            urllib.request.urlretrieve(
                url_list[i],
                podPath +
                file_names[i])
            print("Downloaded ", title_formatted)
            i+=1
    else:
        if history_info[item]['last_downloaded_date'] == todays_date:
            print("Already checked " + item + " podcast today.")
        elif history_info[item]['last_url'] == url_list[0]:
            print("Already downloaded this episode: ", title_list[0])
        else:
            print("Downloading episode: ", title_list[0])
            title_formatted = re.sub("/","",title_list[0])
            file_names.append(title_formatted + ".mp3")
            urllib.request.urlretrieve(
                url_list[0],
                podPath +
                file_names[0])
            history_info[item]['last_url'] == url_list[0]
            history_info[item]['last_downloaded_date'] == todays_date
            with open(histFile,'w') as hist:
                history_info.write(hist)
    return file_names

def primary_function(delim1,delim2,config):
    for item in config.sections()[delim1:delim2]:
        rss_url = config[item]['rss']
        rss,parsedRSSFeed = get_parsed_rss(rss_url)
        selection_list = selection_options(parsedRSSFeed)
        options = enterSelection(selection_list,rss,item)
        if isinstance(options[0],str) and options[0].lower() == 'n':
            delim1+=1
            delim2 = (delim1 + 1)
            if delim1 >= len(config.sections()):
                print("The End!")
                break
            else:
                print("Next Podcast Coming Right Up!")
                primary_function(delim1,delim2,config)
                #continue
        elif isinstance(options[0],str) and options[0].lower() == 'q':
            print("Thanks for using my app!")
            break
        else:
            snNum_list = []
            url,title = getSelectionURL_Title(options,rss)
            if config[item]['podpath'] != "":       # get path for saving .mp3
                podPath = config[item]['podpath']   #
            else:
                podPath = ""
            fileName_list = download_selection(podPath, url, title, history, item)
            number_options = len(options)
            i = config.get(item,"parameters")
            epNum_list = []
            if i != "":                    # checking to see if the parameters
                params = i.split(",")       # option under the selection is populated
            if config[item]['eploc'] == '': # checks to see where the ep# is located
                if config[item]['epnum'] == 'no':   # no episode number indicated
                    epNum_list.append("")
                else:
                    f = 0
                    while f < number_options:
                        g = options[f]
                        epNum_list.append(rss.entries[g].itunes_episode)
                        f += 1
            elif config[item]['eploc'] == 'title':  # is item set to "title" for pod ep
                epNum_list = get_episode_num(title,params)  #TODO update function
            else:                                           #to handle a list
                epNum_list = get_episode_num(url,params) # gets ep from url
            if config[item]['snnum'] == 'yes':  # checks for season number
                f = 0
                while f < number_options:
                    g = options[f]
                    snNum_list.append(rss.entries[g].itunes_season)
                    f += 1
            else:
                snNum_list = []
            artist = config[item]['artist']
            album = config[item]['album']
            album_artist = config[item]['album_artist']
            writeID3(podPath,fileName_list,title,epNum_list,snNum_list,album,album_artist,artist)
            print("File Saved.\nMetadata written.\n")

if arg1 != 1:
    if sys.argv[1].lower() == '-h' or sys.argv[1].lower() == '--help':
        print("getPodcasts - https://github.com/jfayers/getPodcasts/",
              "\n\n\tOptions\t\tDescription",
              "\n\n\t-h, --help\t\tThis help screen",
              "\n\t-m, --menu\t\tGives menu options",
              "\n\n\tDefault: No Arguments",
              "\n\t\tProceed with auto download",
              "\n\t\tof newest episodes.")
    elif sys.argv[1].lower() == '-m' or sys.argv[1].lower() == '--menu':
        all_or_one = input("[A]ll podcasts or [C]hoose from list? ")
        if isinstance(all_or_one,str) and all_or_one.lower() == 'c':
            sections = 0
            while sections < len(config.sections()):
                print("[" + str(sections+1) + "] - " + config.sections()[sections])
                sections += 1
            choice = int(input("Choose One: "))-1
            choice2 = choice + 1
            primary_function(choice,choice2,config)
        else:
            choice = 0
            choice2 = len(config.sections())
            primary_function(choice,choice2,config)
    else:
        print("Invalid Option\nuse \"-h\" for help")
else:
       getPodcasts(config_Sections,history_Sections,rssparams)
