# getPodcasts


This is a script that will check a dictionary file, get and parse an rss feed, and then download/rename podcast files

* ~~The podDictionary.json file is a json dictionary of podcasts that the python script uses for reference~~
* Switched to a config file instead as it was more userfriendly
* also using a config file for history
* It needs to be in the same directory as the python script or you need to alter the python script to point to the new directory
* Dependencies for the script include
	- feedparser
		- [https://pythonhosted.org/feedparser/](https://pythonhosted.org/feedparser/)
	- json
		- [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
	- mutagen
		- [https://mutagen.readthedocs.io/en/latest/](https://mutagen.readthedocs.io/en/latest/)		
	- configparser
		- [https://docs.python.org/2/library/configparser.html](https://docs.python.org/2/library/configparser.html)

Future plans include:

* ~~Ability for script to check the mp3 url against the dictionary to determine if the episode has already been downloaded~~
* Interactive CLI option to add new podcast info
* Other items as they present themselves
* ~~standardize way to get episode number from non-standard location~~
* option to present a list of the most recent n episodes and select for download
