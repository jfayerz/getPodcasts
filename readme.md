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
- If you run it with the "-a" option it will simply go through the list from config and get the newest episode that it has no already downloaded from each podcast.
	- it uses the podHistory config file in order to determine if it's already downloaded that episode (keeps the most recently downloaded url)

## Setup
- edit the podConfig file and add your podcast info following the model
