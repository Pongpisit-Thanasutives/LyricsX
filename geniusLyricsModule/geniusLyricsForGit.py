import requests
from bs4 import BeautifulSoup
import unicodedata
# import translateToEnglish -> This Module is not updated yet so you cannot use getTranslatedLyricsList.
base_url = "http://api.genius.com"
myApiKey=''#Add your Genius Api Here.
headers = {'Authorization': 'Bearer '+myApiKey}
search_url = base_url + "/search"
def get_proper_name(stringIn):
	stringIn=stringIn.replace('\xa0',' ').replace('\u200b',' ')
	stringIn=unicodedata.normalize("NFKD",stringIn)
	stringIn=unicodedata.normalize("NFKC",stringIn)
	return stringIn
def get_possible_songs(song_title):
	global base_url,headers,search_url
	lisOfPossibleSongs=[]
	params = {'q': song_title}
	res = requests.get(search_url, params=params, headers=headers)
	json=res.json()
	for hit in json["response"]["hits"]:
		fullTitle=get_proper_name(hit["result"]["full_title"])
		title=get_proper_name(hit["result"]["title"])
		artistName=get_proper_name(hit["result"]["primary_artist"]["name"])
		lisOfPossibleSongs.append((fullTitle,title,artistName,hit["result"]["api_path"]))
	return lisOfPossibleSongs
def lyrics_from_song_api_path(song_api_path):
	global base_url,headers,search_url
	song_url = base_url + song_api_path
	response = requests.get(song_url, headers=headers)
	json = response.json()
	path = json["response"]["song"]["path"]
	page_url = "http://genius.com" + path
	page = requests.get(page_url)
	html = BeautifulSoup(page.text, "html.parser")
	#remove script tags that they put in the middle of the lyrics
	[h.extract() for h in html('script')]
	#at least Genius is nice and has a tag called 'lyrics'
	#updated css where the lyrics are based in HTML
	lyrics = html.find("div", class_="lyrics").get_text()
	#return lyrics #There are 2 options for this function to return
	#List containing each line
	#A string version of Lyrics 
	return lyrics.split('\n')
# def getTranslatedLyricsList():
# 	ls=[]
# 	originalLisOfLyrics = translateToEnglish.translateLisOfSentence(lyrics_from_song_api_path(song))
# 	for sen in originalLisOfLyrics:
# 		ls.append(sen.text)
# 	return ls



