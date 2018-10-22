# getPodcasts


This is a script that will check a dictionary file, get and parse an rss feed, and then download/rename podcast files

## How to use:
- default running of .py will look as you to choose All or One podcast to work with
- running with -h or --help as an argument will display help
- running with -a or --all will check for and download the newest, undownloaded episode for each podcast in your Config.

## What this thing does
- When you run it (using python3) with no arguments it will present you with two options.  All or Choose.
- If you hit All it will then start cycling through your podConfig file entries
	- it pulls in and parses the rss feed from the url listed in the config file
	- it gets the titles etc. and displays the first 5 entries on the list
	- at that point you can choose to download one or a range/selection of episodes
	- Note: hitting 'n' and 'q' are broken at the moment, but in the future they will work.
	- After it downloads your selections it will then list the first five episodes of the next podcast in the list and so on.
- If you hit Choose it will then present you with a list of podcasts gleaned from the config file
	- you choose a podcast and then it gives you the first five episodes etc.
	- yes, n and q are still broken on this option as well
- If you run it with the "-a" option it will simply go through the list from config and get the newest episode that it has not already downloaded from each podcast.
	- it uses the podHistory config file in order to determine if it's already downloaded that episode (keeps the most recently downloaded url)
	- this is what you want to use if you want to automate it since it doesn't require any further input from you

## Setup
- edit the podConfig file and add your podcast info following the model

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
