# No Ads No Sh*t Lyrics ONLY ! ! ! LyricsX
from sys import exit
import faceRec
if faceRec.getStatus()==False:exit()
import passwdInput
import os
from os import startfile
import shutil
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import speech_recognition as sr
from googleapiclient.discovery import build
import billboard
import random
import apiai
import json
import pytube
import lxml
from lxml import etree
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import wikipedia
from langdetect import detect
import facebook
import sqlite3
import time
import datetime
import unicodedata
from nltk.tokenize import sent_tokenize,word_tokenize
import youtubeApi
import spotifyApiWithMoreFunction
import viewsCountYoutubeVideo
from textblob import TextBlob
import geniusLyrics
import googleTrend
### Fill in your secrects ###
token = util.prompt_for_user_token(username='pongpisit',scope='user-library-read',client_id='',client_secret='',redirect_uri='')
sp = spotipy.Spotify(auth=token)
my_api_key = ""
my_cse_id = ""
client_credentials_manager = SpotifyClientCredentials(client_id='',client_secret='')
sp2 = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp2.trace=False
class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
class songs_suggestion: # songs suggestion from billboard
    def __init__(self):
        chart = billboard.ChartData('hot-100') # 'pop-songs' You can use this instead of 'hot-100'
        self.chart = chart
    def print_songs(self):
        print("-----------------------------")
        print(self.chart)
    def get_song(self,n):
        return str(self.chart[n])
class apiAi:
    def __init__(self,que):
        ### Fill in your secrects ###
        CLIENT_ACCESS_TOKEN = ''
        ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        requestToAi=ai.text_request()
        requestToAi.lang='en'  # optional, default value equal 'en'
        requestToAi.session_id=""
        requestToAi.query=que
        self.aiResponse=json.loads(requestToAi.getresponse().read())
    def getAiResponse(self):
        return self.aiResponse['result']['metadata']
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']
def seek(pat,inn_string,i,j):
    m = re.search(pat,inn_string)
    if m:
        if(j==-1):return m.group(i)
        else:
            return m.group(i)+m.group(j)
    else:
        return 'not found'
def print_artist_name(url):
    url = url.replace("https://genius.com/","").replace('-',' ')
    url = "-> " + url
    print(url)
### Play music from file system ### This function should be inside the class ###
def play(v_title):
    directory = 'C:\\Users\\Pongpisit\\PythonCode\\videos'
    os.chdir(directory)
    startfile('C:\\Users\\Pongpisit\\PythonCode\\videos\\'+v_title+'.mp4')
def playTmpVideo(v_title):
    tmpDirectory = 'C:\\Users\\Pongpisit\\PythonCode\\videos\\tmpVideo'
    os.chdir(tmpDirectory)
    startfile('C:\\Users\\Pongpisit\\PythonCode\\videos\\tmpVideo\\'+v_title)
### Play music from file system ###
def get_artist(name):
    global sp
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return {'name':'Not found'}
def show_recommendations_for_artist(artist):
    global sp
    albums = []
    results = sp.recommendations(seed_artists = [artist['id']])
    for track in results['tracks']:
        print(track['name'], '-', track['artists'][0]['name'])
def show_tracks_from_album(al):
    global sp
    res=sp.search(q = "album:" + al, type = "album")
    album_id = res['albums']['items'][0]['uri']
    allTracks = sp.album_tracks(album_id)
    for eachTrack in allTracks['items']:
        print(' > '+eachTrack['name'])
def show_artist_albums(artist):
    global sp
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            print(name)
            show_tracks_from_album(name)
            seen.add(name)
def show_related_artists(artistName):# shows related artists for the given seed artist
    global sp
    res = sp.search(q='artist:' + artistName, type='artist')
    try:
        searchedName = res['artists']['items'][0]['name']
        uri = res['artists']['items'][0]['uri']
        related = sp.artist_related_artists(uri)
        print('--- Related artists for',searchedName,'---')
        for a in related['artists']:
            print(' ',a['name'])
        print('<--------------------->')
    except:
        print("Oops!")
def show_tracks_in_myplaylist(rst):
    for i, ite in enumerate(rst['items']):
        trk = ite['track']
        print(i+1, trk['artists'][0]['name'], trk['name'])
def show_songs_in_myplaylist():
    global sp
    playlists = sp.user_playlists('pongpisit')
    for playlist in playlists['items']:
        if playlist['owner']['id'] == 'pongpisit':
            print("--- From "+playlist['name']+" playlist ---")
            print('  total tracks', playlist['tracks']['total'])
            rsts = sp.user_playlist('pongpisit', playlist['id'], fields="tracks,next")
            trks = rsts['tracks']
            show_tracks_in_myplaylist(trks)
            while trks['next']:
                trks = sp.next(trks)
                show_tracks_in_myplaylist(trks)
def removeRemix(stringInput):
    remixPart = '''[(][\w\s:;\/&'"‘’,.!¡?-—-]*remix[)]'''
    regObj = re.search(remixPart,stringInput,re.IGNORECASE)
    if regObj:
        return stringInput.replace(regObj.group(),'')
    else:
        return stringInput
###Database###
def data_entry(username,sName,aName,vTitle,youLink,opinion):
    connection=sqlite3.connect('lyricsX.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(Datestamp text,Username text,Song text,Artist text,Title text,Link text,Comment text)")
    date=str(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
    cursor.execute("INSERT INTO stuffToPlot (Datestamp,Username,Song,Artist,Title,Link,Comment) VALUES(?,?,?,?,?,?,?)",(date,username,sName,aName,vTitle,youLink,opinion))
    connection.commit()
    cursor.close()
    connection.close()
def read_from_db():
    allArtists={}
    allSongs={}
    connection=sqlite3.connect('lyricsX.db')
    cursor=connection.cursor()
    cursor.execute("SELECT Song,Artist FROM stuffToPlot")
    for eachRow in cursor.fetchall():
        artistName=unicodedata.normalize("NFKC",eachRow[1].replace('\u200b',''))
        artistName=unicodedata.normalize("NFKD",artistName)
        songName=unicodedata.normalize("NFKC",eachRow[0].replace('\u200b',''))
        songName=unicodedata.normalize("NFKD",songName)
        if artistName not in allArtists:
            allArtists[artistName]=1
        else:
            allArtists[artistName]+=1
        if songName not in allSongs:
            allSongs[songName]=1
        else:
            allSongs[songName]+=1
    print("--- Recently played ---")
    for s in allSongs:
        print(s,' : ',allSongs[s])
    print("--- Saved artists in my database ---")
    for a in allArtists:
        print(a,' : ',allArtists[a])
    connection.close()
# My regex
reg_genius = '''https://genius.com/([\w\s:;\/&'"’,.!¡()?-—-_+Ø]+)-lyrics'''
reg_wiki = '''https://en.wikipedia.org/wiki/([^&]+)&s.*'''
reg_title = '''(<title>)([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(</title>)'''
reg_verse_1 = r'(<p>)(\[Verse\s1(:\s\w*)*\])(<br>)' #[Verse 1...] is in group(2)
reg_more_sign1 = '''(">)([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(<br>|</a>)''' #"false">  
reg_more_sign2 = '''(">)([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]*)(</a>)*([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(<br>)'''
reg_sentence = '''([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(</a>)([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(<br>|</p>)'''
reg_sentence1 = '''([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(<a|</a>)'''
reg_sentence2 = '''([\w\s:;\/$&'"‘’,.!¡()?-—-_+ØΛ]+)(</a>)*(<br>|</p>)''' 
reg_start_lyrics = '''<div class="song_body'''
reg_end_lyrics = "<!--/sse-->"
# My regex  
canProcess = True
canStart = False
canEnd = False
hasTitle = False
voiceMode = False
getFromSuggestion = False
listener = ""
history = {}
print('--- This version does not support Thai lang ---')
print('Current working directory : ',os.getcwd()) 
if os.path.exists(os.path.join(os.getcwd(),'videos'))==False:
    os.mkdir('videos')
print("--- Saved tracks in my Spotify app ---")
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    idx = 1 
    for item in results['items']:
        track = item['track']
        print(str(idx)+' '+track['name'] + ' - ' + track['artists'][0]['name'])
        if track['artists'][0]['name'] not in history:
            history[track['artists'][0]['name']] = 1
        else:
            history[track['artists'][0]['name']] += 1
        idx+=1
else:
    print("Can't get token for", username)
print("--- Your top artists ---")
for statistic in sorted(((c,ar)for ar,c in history.items()),reverse=True):
    print(statistic[1],statistic[0])
show_songs_in_myplaylist()
read_from_db()
print("*** Get top songs from a artist ***")
while 1:
    option_get_topSongs = input("Get top songs from a artist (Press 'n' to skip this) : ")
    if(option_get_topSongs!='n'):
        artist_name = get_artist(option_get_topSongs)['name']
        if artist_name!='Not found':
            print('--- Top '+artist_name+' songs ---')
            result = sp.search(artist_name)
            seen_top_tracks = set()
            num = 1
            for tmp, t in enumerate(result['tracks']['items']):# tmp equals num if there is no dups
                if t['name'] not in seen_top_tracks:
                    print( num, t['name'])
                    seen_top_tracks.add(t['name'])
                    num+=1
            print("--- Albums ---")
            show_artist_albums(get_artist(option_get_topSongs))
            show_related_artists(artist_name)
        else:
            print(option_get_topSongs+" "+artist_name)
            print("--- Did you mean ---")
            for eachGeniusResult in geniusLyrics.get_possible_songs(option_get_topSongs):
                print(eachGeniusResult[0])
            print("--- More Information from genius.com ---")
            for eachLink in google_search(option_get_topSongs, my_api_key, my_cse_id, num=10):
                print(eachLink['formattedUrl'])
            print("--- I found these terms from wikipedia pages ---")
            wiki_page=requests.get("https://www.google.co.th/search?q="+urllib.request.quote(option_get_topSongs))
            wiki_soup=BeautifulSoup(wiki_page.content,"html.parser")
            for wiki_link in  wiki_soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
                if re.search(reg_wiki,str(re.split(":(?=http)",wiki_link["href"].replace("/url?q=",""))[0])):
                    print(re.search(reg_wiki,str(re.split(":(?=http)",wiki_link["href"].replace("/url?q=",""))[0])).group(1).replace('_',' '))
            print("--- FUN FACTS FROM GOOGLE TRENDS ---")
            googleTrend.getSuggestionsFromGoogle(option_get_topSongs)
            googleTrend.getTrendsFromGoogle(option_get_topSongs)
            print("----------------------")
    else:
        break
print("--- Search for a song or let me suggest you ---") # Add search for a artist option
##Input is below here --------------------
mode = input("Voice mode (on/off) : ")
if mode == "on":
    while(1) :
        input("Press any keys to start talking !")
        print("Tell me the song name you're looking for . . . ")
        r = sr.Recognizer()
        with sr.Microphone() as source:
                audio = r.listen(source)                   
        try:
                print("You search for " + r.recognize_google(audio)) # Name of a song
                song = r.recognize_google(audio)
                myAi=apiAi(song)
                if(len(word_tokenize(song))>=3 and 'intentName' in myAi.getAiResponse() and myAi.getAiResponse()['intentName']=="music.suggestion"):
                    if "new" not in song.lower() and "recent" not in song.lower() and "latest" not in song.lower():
                        song_sug = songs_suggestion()
                        song_sug.print_songs()
                        if(input("Want from this list : ") == 'y'):
                            n = input("What song's number do you want : ")
                            if(n=="random"):n=random.randint(1,100)
                            song = song_sug.get_song(int(n)-1)
                            song = song + " genius lyrics"
                            getFromSuggestion = True
                            break
                    else:
                        print("--- NEW RELEASES ---")
                        spotifyApiWithMoreFunction.get_new_release()
                        print("--------------------")   
                else:
                    con_isWant = False
                    song = song + " genius lyrics"    
                    print("Is it what you are looking for ? . . .")
                    isWant = input()
                    if(isWant == 'y'):
                        break
        except LookupError:
                print("Could not understand your voice")
        except sr.UnknownValueError:   
                print("Could not hear your voice, please tell me again")
        except:
                print("Oops, Something went worng here")
else:
    while(1):
        song = input("Song : ") # Name of a song
        myAi = apiAi(song)
        if(len(word_tokenize(song))>=3 and 'intentName' in myAi.getAiResponse() and myAi.getAiResponse()['intentName']=="music.suggestion"):#re.search("Suggest me",song,re.IGNORECASE)            
            if "new" not in song.lower() and "recent" not in song.lower() and "latest" not in song.lower():
                song_sug = songs_suggestion()
                song_sug.print_songs()
                if(input("Want from this list : ") == 'y'):
                    n = input("What song's number do you want : ")
                    if(n=="random"):n=random.randint(1,100)
                    song = song_sug.get_song(int(n)-1)
                    song = song + " genius lyrics"
                    getFromSuggestion = True
                    break
            else:
                print("--- NEW RELEASES ---")
                spotifyApiWithMoreFunction.get_new_release()
                print("--------------------")
        else:
            if detect(song)=='th':print('--- I cannot understand Thai lang ---')
            else:
                song = song + " genius lyrics" # song = song + " genius lyrics"
                break
##Input is up here --------------------
while(1):
    encoded = urllib.request.quote(song.strip())
    page = requests.get("https://www.google.co.th/search?dcr=0&source=hp&q="+encoded)
    soup = BeautifulSoup(page.content,"html.parser")
    links = soup.findAll("a")
    link = ''
    try:
        for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            if re.search(reg_genius,str(re.split(":(?=http)",link["href"].replace("/url?q=",""))[0])):
                link = re.search(reg_genius,str(re.split(":(?=http)",link["href"].replace("/url?q=",""))[0])).group(0)
                if(getFromSuggestion == True):
                    print_artist_name(link) # We can't provide more than 10 links
                    isOk = 'y'
                    break
                print_artist_name(link)
                isOk = input("Are you OK with the result : ")
                if(isOk=='y'):break
    except:
        print("\nException happened and one possible reason was that BeautifulSoup couldn't provide 10 results. I will try Google Api instead.")
    if(isOk!='y'):
        try:
            inn = input("song (Search a song name only) : ")
            results = google_search(inn, my_api_key, my_cse_id, num=10)
            for result in results:
                print_artist_name(result['formattedUrl'])
                isOk = input("Are you OK with the result : ")
                if(isOk=='y'):
                    link = result['formattedUrl']
                    break
        except:
            print("You might not connnect to internet ??? OR some IP ADDRESS ISSUES ???")
    if(isOk!='y'):
        print("Sorry, I can't find that song you want.")
        continue
    if(link != ''):
        try :
            opener = AppURLopener()
            music = opener.open(link)
        except urllib.error.URLError:
            print("Oops! Page not found")
            canProcess = False
    else: print("We can't find the song, sorry T T")
    if(canProcess):
        print("--- This's an extracted version form "+link+" ---")
        for line in music:
            line = str(line.strip().decode('utf8'))
            if(len(line)!=0 and canStart and hasTitle):
                if re.search(reg_end_lyrics,line):
                    canEnd = True
                    break
                line = (line.replace('<i>','')).replace('</i>','')
                line = (line.replace('<b>','')).replace('</b>','')
                line = (line.replace('<strong>','')).replace('</strong>','')
                line = (line.replace('<strike>','')).replace('</strike>','')
                line = line.replace('&amp;','&')
                if seek(reg_more_sign1,line,2,-1)!='not found':
                    if(seek(reg_more_sign2,line,2,4)!='not found' and len(seek(reg_more_sign2,line,2,4))>1):
                        if((seek(reg_more_sign2,line,2,4)[0]!="[" and seek(reg_more_sign2,line,2,4)[len(seek(reg_more_sign2,line,2,4))-1]!="]") or (seek(reg_more_sign2,line,2,4)[0]=="[" and seek(reg_more_sign2,line,2,4)[len(seek(reg_more_sign2,line,2,4))-1]=="]")):
                            print(seek(reg_more_sign2,line,2,4))
                    else:
                        if(len(seek(reg_more_sign1,line,2,-1))>1):
                            print(seek(reg_more_sign1,line,2,-1))
                else:
                    if(seek(reg_more_sign2,line,2,4)!='not found' and len(seek(reg_more_sign2,line,2,4))>1):
                        print(seek(reg_more_sign2,line,2,4))
                    else:
                        if seek(reg_sentence,line,1,3)!='not found' and len(seek(reg_sentence,line,1,3))>1:
                            print(seek(reg_sentence,line,1,3))
                        else:
                            if seek(reg_sentence1,line,1,-1)!='not found' and len(seek(reg_sentence1,line,1,-1))>1:
                                print(seek(reg_sentence1,line,1,-1),)
                            else:
                                if seek(reg_sentence2,line,1,-1)!='not found' and len(seek(reg_sentence2,line,1,-1))>1:
                                    print(seek(reg_sentence2,line,1,-1),)
            else:
                if(hasTitle):
                    if(len(line)!=0 and re.search(reg_start_lyrics,line)):canStart = True
                else:
                    if(len(line)!=0 and re.search(reg_title,line)):
                        line = line.replace('&amp;','&')
                        print("Title : "+re.search(reg_title,line).group(2))
                        searchInYoutube = re.search(reg_title,line).group(2).replace("Lyrics | Genius Lyrics","")
                        searchInYoutube = removeRemix(searchInYoutube)
                        searchInYoutube = searchInYoutube.strip()
                        hasTitle = True   
    print('\n   <---DONE--->\nIf the lyrics is not what you want please search again using more specific words')
    isResultOk = input("\nAre you OK with this result ? (y for yes/n for no) : ")
    if(isResultOk=='y'):break
    else:
        canProcess = True
        canStart = False
        canEnd = False
        hasTitle = False
        voiceMode = False
        listener = ""
        if mode == "on":
            while(1) :
                input("Press any keys to start talking !")
                print("Tell me the song name you're looking for . . . ")
                r = sr.Recognizer()
                with sr.Microphone() as source:
                        audio = r.listen(source)                   
                try:
                        print("You search for " + r.recognize_google(audio)) # Name of a song
                        song = r.recognize_google(audio)
                        myAi = apiAi(song)
                        if(len(word_tokenize(song))>=3 and 'intentName' in myAi.getAiResponse() and myAi.getAiResponse()['intentName']=="music.suggestion"):#re.search("Suggest me",song,re.IGNORECASE)
                            if "new" not in song.lower() and "recent" not in song.lower() and "latest" not in song.lower():
                                song_sug = songs_suggestion()
                                song_sug.print_songs()
                                if(input("Want from this list : ") == 'y'):
                                    n = input("What song's number do you want : ")
                                    if(n=="random"):n=random.randint(1,100)
                                    song = song_sug.get_song(int(n)-1)
                                    song = song + " genius lyrics"
                                    getFromSuggestion = True
                                    break
                            else:
                                print("--- NEW RELEASES ---")
                                spotifyApiWithMoreFunction.get_new_release()
                                print("--------------------")
                        else:
                            song = song + " genius lyrics"    
                            con_isWant = False
                            isWant = input("Is it what you are looking for ? : ")
                            if(isWant == 'y'):
                                break
                except LookupError:
                    print("Could not understand your voice")
                except sr.UnknownValueError:   
                    print("Could not hear your voice, please tell me again.")
        else:
            while(1):
                song = input("Song : ") # Name of a song
                myAi = apiAi(song)
                if(len(word_tokenize(song))>=3 and 'intentName' in myAi.getAiResponse() and myAi.getAiResponse()['intentName']=="music.suggestion"):#re.search("Suggest me",song,re.IGNORECASE)
                    if "new" not in song.lower() and "recent" not in song.lower() and "latest" not in song.lower():
                        song_sug = songs_suggestion()
                        song_sug.print_songs()
                        if(input("Want from this list : ") == 'y'):
                            n = input("What song's number do you want : ")
                            if(n=="random"):n=random.randint(1,100)
                            song = song_sug.get_song(int(n)-1)
                            song = song + " genius lyrics"
                            getFromSuggestion = True
                            break
                    else:
                        print("--- NEW RELEASES ---")
                        spotifyApiWithMoreFunction.get_new_release()
                        print("--------------------")
                else:
                    song = song + " genius lyrics"
                    break
youtubeOpen = False
searchedSong_artist = searchInYoutube.split('–')[0].strip()
v_title='';youtube_link=''
command1 = input("Do you want me to suggest any videos ? (y for yes/n for no) : ")
if(command1!='y'):
    pass
else:
    command2 = input("Do you want me to open one of them ? (y for yes/n for no) : ")
    command2 = command2.split(" ")
    if(command2[0] == 'n'):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:/Users/Pongpisit/AppData/Local/Google/Chrome/User Data/default/")
        driver=webdriver.Chrome(executable_path="C:/Users/Pongpisit/PythonCode/chromedriver.exe",chrome_options=options)
        driver.implicitly_wait(20)
        driver.get("https://youtube.com")
        elem = driver.find_element_by_name("search_query")
        elem.clear()
        if len(command2)!=1:elem.send_keys(searchInYoutube+' '+' '.join(command2[1:]))
        else:elem.send_keys(searchInYoutube)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
    else:
        if(command2[0] == 'y'):#Disable opening Youtube using chrome for now
            sent_analysis_res = {"Positive comments":0,"Non-positive comments":0}
            if len(command2)>1:searchInYoutube+=(' '+' '.join(command2[1:]))
            print('--- '+searchInYoutube+' ---')
            query_string = urllib.parse.urlencode({"search_query" : searchInYoutube})
            html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            for number in range(3):
                v_title = ''.join(etree.HTML(urllib.request.urlopen("https://www.youtube.com/watch?v=" + search_results[number]).read()).xpath("//span[@id='eow-title']/@title"))
                print(str(number+1)+' '+v_title+' '+viewsCountYoutubeVideo.getViews("https://www.youtube.com/watch?v=" + search_results[number])+' views')
            print("--- Be aware that the video's name containing weird characters cannot be opened ---")
            number = int(input("Get number? : "))
            youtube_link = "http://www.youtube.com/watch?v=" + search_results[number-1]
            v_title = ''.join(etree.HTML(urllib.request.urlopen("https://www.youtube.com/watch?v=" + search_results[number-1]).read()).xpath("//span[@id='eow-title']/@title"))
            print("--- Description ---")
            try:
                print("From "+youtubeApi.getVideoInformation(v_title)["channelTitle"]+" : "+youtubeApi.getVideoInformation(v_title)["localized"]["description"])
            except TypeError:
                print("Oops, No description here")
            print("-------------------")
            ###Show comments from the choosen Youtube video###
            print("--- Comments from the choosen Youtube video ---")
            try:
                if len(youtubeApi.getComments(v_title))>0:
                    for com in youtubeApi.getComments(v_title):
                        print("Comment by",com[0]," : ",com[1]," : ",TextBlob(com[1]).sentiment)
                        polar = TextBlob(com[1]).sentiment.polarity
                        if polar<=-1:
                            sent_analysis_res["Non-positive comments"]+=1
                        else:
                            sent_analysis_res["Positive comments"]+=1
                    print(sent_analysis_res)
                else:
                    print("Oops, No comments here")
            except :
                print("Oops, No comments here")
            print("-----------------------------------------------")
            for bad_cha in '''.,'"/''':
                v_title = v_title.replace(bad_cha,'')            
            ###--- Download the video here ---###
            try:
                yt = pytube.YouTube(youtube_link)
                videos = yt.get_videos()
                s = 1
                for v in videos:
                    print(str(s)+". "+str(v))
                    s+=1
                n = int(input("What version ? : "))                
                if n!=4:
                    video = videos[2]
                else:
                    video = videos[3]
            except pytube.exceptions.AgeRestricted:
                print("Uable to download this video")
            destination = 'C:\\Users\\Pongpisit\\PythonCode\\videos'
            try:
                video.download(destination)
                print("--- Successfully downloaded ---")
                try:
                    play(v_title)
                except FileNotFoundError:
                    try:
                        play(sorted(os.listdir(),key=os.path.getmtime,reverse=True)[0].replace('.mp4',''))
                    except:
                        print("--- The system cannot open this specific file ---")
            except OSError:
                print("This video was already downloaded into your file system")
                try:
                    play(v_title)
                except FileNotFoundError:# List all songs we have here !
                    if os.path.exists(os.path.join(os.getcwd(),'tmpVideo'))==True:
                        shutil.rmtree('tmpVideo')
                    os.mkdir('tmpVideo')
                    video.download('C:\\Users\\Pongpisit\\PythonCode\\videos\\tmpVideo')
                    try:
                        os.chdir('C:\\Users\\Pongpisit\\PythonCode\\videos\\tmpVideo')
                        playTmpVideo(os.listdir()[0])
                    except:
                        print("--- The system cannot open this specific file ---")
            ## Download the video here ###
print("--- Playing music ---")
command3 = input("Want to know more about this song ? (y for yes/n for no) : ")
import bs4 as bs
if(command3=='y'):
    sauce = AppURLopener().open(link)
    soup = bs.BeautifulSoup(sauce,"html.parser")
    ls = []
    print()
    for div in soup.find_all('div',class_="rich_text_formatting"):
        message = div.text.replace("\n","")+"\n"
        for eachSentenceInMessage in sent_tokenize(message,language='english'):
            if(len(eachSentenceInMessage)>1):
                print(eachSentenceInMessage)
        print()
print("Open "+link+" to gain more information")
print("** Recommended songs **")
try:
    show_recommendations_for_artist(get_artist(searchedSong_artist))
except requests.exceptions.HTTPError:
    print("** requests.exceptions.HTTPError **")
except spotipy.client.SpotifyException:
    print("** The access token expired ? **")
except KeyError:
    for eachArtist in searchedSong_artist.split('&'):
        print('--- Because you listened to '+eachArtist.strip()+' song ---')
        try:
            show_recommendations_for_artist(get_artist(eachArtist.strip()))
        except KeyError:
            print('Oops, cannot find anything to recommend for',eachArtist.strip())
print("**-------------------**")
clear_videos_dir = input("Type clear to clear your videos directory : ")
os.chdir('C:\\Users\\Pongpisit\\PythonCode')
if clear_videos_dir.lower()=='clear':
    shutil.rmtree('videos')
###Post on facebook to let others know about the song you are listening###
fbShare = input("Share feeling on Facebook wall (Press 'q' to quit) : ")
if fbShare!='q':
    ### Fill in your secrects ###
    facebookAccessToken=''
    try:
        facebook.GraphAPI(facebookAccessToken).put_object("me", "feed", message="Listening to "+v_title+" "+youtube_link+" : "+fbShare)
        print("- Done! -")
    except facebook.GraphAPIError:
        print("*Expired access token*")#Contact devolper.facebook
data_entry('Pongpisit',searchInYoutube.split('–')[1].strip(),searchedSong_artist,v_title,youtube_link,fbShare)
print('Current working directory : ',os.getcwd())
print("--- END ---")