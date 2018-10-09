# getPodcasts


This is a script that will check a dictionary file, get and parse an rss feed, and then download/rename podcast files

* ~~The podDictionary.json file is a json dictionary of podcasts that the python script uses for reference~~
* Switched to a config file instead as it was more user friendly
* also using a config file for history
* It needs to be in the same directory as the python script or you need to alter the python script to point to the new directory
* Dependencies for the script include
	- feedparser
		- [https://pythonhosted.org/feedparser/](https://pythonhosted.org/feedparser/)
	- ~~json~~
		- ~~[https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)~~
	- mutagen
		- [https://mutagen.readthedocs.io/en/latest/](https://mutagen.readthedocs.io/en/latest/)		
	- configparser
		- [https://docs.python.org/2/library/configparser.html](https://docs.python.org/2/library/configparser.html)

Future plans include:

* ~~Ability for script to check the mp3 url against the dictionary to determine if the episode has already been downloaded~~
* Interactive CLI option to add new podcast info
* Other items as they present themselves
	- ~~option to add path~~
		- config file now has an option to add path
		- getPodcasts.py now calls the podpath item from the podConfig file
* ~~standardize way to get episode number from non-standard location~~
* option to present a list of the most recent n episodes and select for download

- also, it checks the podHistory file and does not download the file if it finds the url in the last\_url field

## things that don't work

- ~~it's not putting the correct / complete url into the podHistory file for some of the podcasts~~
- ~~also, i don't believe it's actually downloading those episodes either.~~
- ~~this points to a problem with the "partition" parts of the script that are designed to get the mp3url~~
- ~~also, and this is universal at this point, it is not writing the episode number to the metadata.~~
- ~~it *is* writing the season (disc) number to the metadata~~
- ~~i'm not sure if it's just failing to get the episode number or if there's something wrong with the write.~~
- The above items were all due to a problem with an if/then statment and some incorrect rssparameters information in the podConfig file
- All resolved 10/09/2018
