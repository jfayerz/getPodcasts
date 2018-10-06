#!/usr/bin/env python3

"""
python script to get the most recent podcast episode from the rss feed
this is a python3 script
"""

import urllib
from datetime import date

import feedparser
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS

	"""
	Notes:
	configparser
	configparser.ConfigParser()
	config = configparser.ConfigParser()
	config.read(filename)
	config['item']['subitem'] = 'new value'
	with open(filename,"w") as f:
		config.write(f) #this writes the whole file again, but using
				#the config['item']['subitem'] format the only
				#thing changing is that one field or whatever
				#other fields you change
	with open(filename,'a') as f: 	#this opens it in append mode
					#useful for adding a new entry to
					#the config file (e.g. a new podcast
					#section of info
	"""

def downloadEp(url,fileName):
	urllib.request.urlretrieve(url, fileName)
	

def get_episode_num(s, delim1, pos1, delim2, pos2):
    """
    function to get episode number from non standard location

    Args:
        s:
        delim1:
        pos1:
        delim2:
        pos2:

    Returns:
    """
    name = s.partition(delim1)[pos1]
    return name.partition(delim2)[pos2]


def update_last_url(s):
    """
    function to update "last_url" for each podcast entry in the json dictionary

    Args:
        s:

    Returns:

    """
    if s == podcast['last_url']:
        print("Already Downloaded" + title + ".")
    else:
        print("Last URL updated for podcast: " + podcast['name'] + ".")
	return podcast['last_url']


# opens and loads the podcast dictionary
config = configparser.ConfigParser()
history = configparser.ConfigParser()
config.read('podConfig')
history.read('podHistory')

for item in config:
	rss = feedparser.parse(item['rss'])
	if item['epnum'] == 'yes' and item['snnum'] == 'yes':
		if item['urlFormat'] == 'questionmark':
			
			url = rss.entries[0].links[1].href.partition("?")[0].rstrip()
			if url == history[item]['last_url']
			title = rss.entries[0].title.rstrip()
			episodeNum = rss.entries[0].itunes_episode
			seasonNum = rss.entries[0].itunes_season
			filename = title + ".mp3"

			try:
				audio.ID3(filename)
				audio.delete()
				audio.ID3()
			except ID3NoHeaderError:
				audio.ID3()
			
			# add title
            		audio.add(TIT2(encoding=3, text=title))

            		# add track number
            		audio.add(TRCK(encoding=3, text=episodeNum))

            		# add season number 
			audio.add(TPOS(encoding=3, text=seasonNum))

            		# add artist
            		audio.add(TPE1(encoding=3, text=item['artist']))

            		# add album artist
            		audio.add(TPE2(encoding=3, text=item['album_artist']))

            		# add album
            		audio.add(TALB(encoding=3, text=item['album']))
            		audio.save(filename) 

for podcast in info:
    rss = feedparser.parse(podcast['rss'])
    if podcast['episode_number'] == 'yes' and podcast['season_number'] == 'yes':
        if podcast['urlFormat'] == 'questionmark':
            url = rss.entries[0].links[1].href.partition("?")[0].rstrip()
            title = rss.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            seasonNum = d.entries[0].itunes_season
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                # checks to see if the file has existing ID3
                # and if so, blanks it out for consistency
                audio = ID3(fileName)
                audio.delete()
                # creates and ID3 space to add tags until they 
                # are ready to be saved to the .mp3 file
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            # add title
            audio.add(TIT2(encoding=3, text=title))

            # add track number
            audio.add(TRCK(encoding=3, text=episodeNum))

            # add season number (disc)
            audio.add(TPOS(encoding=3, text=seasonNum))

            # add artist
            audio.add(TPE1(encoding=3, text=podcast['artist']))

            # add album artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))

            # add album
            audio.add(TALB(encoding=3, text=podcast['album']))
            audio.save(fileName) 
            
            # This save function only saves the ID3 tags, it does 
            # not resave the mp3. So, if you don't have it pointed 
            # at the actual file location it will just save a text 
            # file full of metadata that will be useless
            
        elif podcast['host'] == 'art19':
            url = d.entries[0].links[0].href
            title = d.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            seasonNum = d.entries[0].itunes_season
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPOS(encoding=3, text=seasonNum))  # add season number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
            """
            audio = eyed3.load(fileName)
            audio.tag.title = title
            audio.tag.track_num = episodeNum
            audio.tag.disc_num = seasonNum
            audio.tag.artist = podcast['artist']
            audio.tag.album_artist = podcast['album_artist']
            audio.tag.album = podcast['album']
            audio.tag.save(version=(2,4,0))
            """
        else:
            url = d.entries[0].links[1].href
            title = d.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            seasonNum = d.entries[0].itunes_season
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPOS(encoding=3, text=seasonNum))  # add season number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
    elif podcast['episode_number'] == 'yes' and podcast['season_number'] == 'no':
        if podcast['host'] == 'libsyn':
            url = d.entries[0].links[1].href.partition("?")[0].rstrip()
            title = d.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
        elif podcast['host'] == 'art19':
            url = d.entries[0].links[0].href
            title = d.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
        else:
            url = d.entries[0].links[1].href
            title = d.entries[0].title.rstrip()
            episodeNum = d.entries[0].itunes_episode
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
    elif podcast['episode_number'] == 'no':
        if podcast['host'] == 'libsyn':
            url = d.entries[0].links[1].href.partition("?")[0].rstrip()
			if url == podcast['last_url']
				print("Episode already downloaded on " + podcast['last_downloaded'] + ".")
			else:
				tmpURL = podcast['last_url']
				tmpDate = podcast['last_downloaded']
				podcast['last_url'] = url
				podcast['last_downloaded'] = str(date.today())
				with open('podDictionary.json', 'w') as podcasts:
					json.dump(podcast,podcasts)
				title = d.entries[0].title.rstrip()
	            fileName = title + ".mp3"
    		        if podcast['epNumLoc'] == "title":
            		    episodeNum = get_episode_num(title, podcast['delim1'], int(podcast['position1']), podcast['delim2'], int(podcast['position2']))
		            elif podcast['epNumLoc'] == "filename":
        		        episodeNum = get_episode_num(url, podcast['delim1'], int(podcast['position1']), podcast['delim2'], int(podcast['position2']))
		            else:
        		        print("No episode location defined")

        		    # episodeNum = d.entries[0].title.partition(" ")[0].rstrip()

		        urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TRCK(encoding=3, text=episodeNum))  # add track number
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
        elif podcast['host'] == 'art19':
            url = d.entries[0].links[0].href
            title = d.entries[0].title.rstrip()
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
        else:
            url = d.entries[0].links[1].href
            title = d.entries[0].title.rstrip()
            fileName = title + ".mp3"
            urllib.request.urlretrieve(url, fileName)

            try:
                audio = ID3(fileName)
                audio.delete()
                audio = ID3()
            except ID3NoHeaderError:
                print("Adding ID3 header")
                audio = ID3()

            audio.add(TIT2(encoding=3, text=title))  # add title
            audio.add(TPE1(encoding=3, text=podcast['artist']))  # add artist
            audio.add(TPE2(encoding=3, text=podcast['album_artist']))  # add album artist
            audio.add(TALB(encoding=3, text=podcast['album']))  # add album
            audio.save(fileName)
