#!/usr/bin/env python3

"""
python script to get the most recent podcast episode from the rss feed
this is a python3 script
"""

import json
import urllib
from datetime import date

import feedparser
# from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
# from mutagen.id3 import COMM, USLT, TCOM, TCON, TDRC  # TODO: These are not used
# TODO: These are "protected members" not intended to be used outside the class.  Check mutagen's docs?
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS


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


# TODO: "s" parameter not used
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
with open('podDictionary.json') as podcasts:
    info = json.load(podcasts)

for podcast in info:
    d = feedparser.parse(podcast['rss'])
    if podcast['episode_number'] == 'yes' and podcast['season_number'] == 'yes':
        if podcast['host'] == 'libsyn':
            url = d.entries[0].links[1].href.partition("?")[0].rstrip()
            title = d.entries[0].title.rstrip()
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
