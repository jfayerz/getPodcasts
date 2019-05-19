# get_podcasts.py

## Problem Encountered:
- I like using a command line interface for most of my computing.
- I also like using non-standard audio applications on my mobile devices (e.g. Plex)
- I like podcasts
- I found a good command-line podcast application for subscribing to and downloading podcasts

_**HOWEVER**_

- I quickly discovered that the **metadata** provided on these downloaded files was severely lacking
- Additionally, this was a problem because some of those rss feeds (I'm looking at you, Patreon) use a random alphanumeric naming scheme for their 20-30 character long episode name.
- It was at this point that I really started valuing iTunes and other podcast repositories.

## Problem Solved:
This script:

- checks a list of rss feeds
- checks for new episodes using etag, date-modified, or other methods
- grabs information from the xml feed for metadata encoding
- downloads the episode(s)
- properly encodes the metadata
- deposits the audio file in a location specified by you.

This script *also*:

- allows the user to run it and select multiple episodes from a podcasts rss feed

This script *does not*:

- require you to download every single episode from the rss feed in order to make use of it (no thank you, i already have all 300+ episodes of The Dollop, I don't need to download it again just because my sqlite db got corrupted).

## How to use:
- default running of getPodcasts.py auto download the newest episode of each podcast in the config file if it hasn't already been downloaded (based on the podHistory file)
- running with -h or --help as an argument will display help
- running with -m or --menu will display the menu options for "All" or "Choose"

## What this thing does
- When you run it (using python3) with the -m or --menu argument it will present you with two options.  All or Choose.
- If you hit All it will then start cycling through your podConfig file entries
	- it pulls in and parses the rss feed from the url listed in the config file
	- it gets the titles etc. and displays the first 5 entries on the list
	- at that point you can choose to download one or a range/selection of episodes
		- you specify a range or a selection of episodes in the follow way
			- for episodes 3, 5, and 7 through 9 you'd enter: 3,5,7-9
	- After it downloads your selections it will then list the first five episodes of the next podcast in the list and so on.
- If you hit Choose it will then present you with a list of podcasts gleaned from the config file
	- you choose a podcast and then it gives you a list of the first five episodes etc.
	- at that point you can choose to download one or a range/selection of episodes
		- you specify a range or a selection of episodes in the follow way
			- for episodes 3, 5, and 7 through 9 you'd enter: 3,5,7-9
- If you run it with no arguments it will simply go through the list from config and get the newest episode that it has not already downloaded from each podcast.
	- it uses the podHistory config file in order to determine if it's already downloaded that episode (keeps the most recently downloaded url)
	- this is what you want to use if you want to automate it since it doesn't require any further input from you

## Setup

### edit the podConfig file:

* **rss** - the rss url for the podcast. You may have to search for this.
* **artist, album, album\_artist** - these are for the metadata and will apply to every episode for this podcast that you download
* **urlFormat** - not used currently but i haven't removed it yet
* **parameters** - this is for situations where the podcast episode is not listed via an itunes\_episode tag in the xml, but rather the episode number is in the title or the filename
	- this is tricky
	- **_example_**: Let's say that the title from the rss feed for this episode is "Ep372 - The Dollop - Episode Title"
	- in the script there is a function for getting the episode number
	- if eploc = title and epnum = no then:
		- the get episode number function will partition off the parts of the title that are not the episode number, but it needs some info from you
		- in the example above you want the partition function to look for the following parameters: p,2,-,0
		- here's what this does:
			- p,2: tells partition to partition things at the first "p" it sees in the string.
			- the string is the episode title listed above from the rss xml feed
			- the 2 tells it to keep everything after the "p" and drop the "p" and everything before the "p"
			- similarly, the -,0 tells it to looks for the first "-" in the string.  The 0 means keep everything before the "-" but not the "-" or anything after it.
			- don't worry about the space or white space before or after the number, the script will strip that off.
		- the script will use the first two out of the four **first** and then it will do the second two. 
		- keep that in mind when you are setting these
* **eploc** - if the itunes\_episode tag is not present in the xml for the rss feed then you use this field to indicate "title" or "urlFilename" to indicate where the episode number is
* **epnum** - "yes" if itunes\_episode tag *is* present, "no" if not
* **snnum** - "yes" if itunes\_season tag *is* present, "no" if not
* **rssparams** - not used, but i haven't removed it yet
* **podpath** - where, in your file system, you want to save episodes of this podcast

### edit the podHistory file:
- NOTE: You do not need to manually type any actual dates or tags or urls in this file.  Just make a place for similar to the model provided in the pod\_history file.

* **last_url** - last recorded mp3's url from the rss feed used
* **last_downloaded_date** - records the date of the last time downloaded
* **etag** - if the rss feed is populated with an etag (for use with identifying that a feed has been updated) it will store it here
* **last_modified** - if the rss feed, instead of an etag, uses a last\_modified field it will store that date here
