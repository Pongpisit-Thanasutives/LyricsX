import npyscreen
import geniusLyrics
# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application
class MyTestApp(npyscreen.NPSAppManaged):
  def onStart(self):
    self.registerForm("MAIN", MainForm())
    self.registerForm("SecondMAIN",SecondForm())
# This form class defines the display that will be presented to the user.
class MainForm(npyscreen.Form):
  def create(self):
    self.add(npyscreen.TitleText, name = "LyricsEx_MainPage")
    self.name = self.add(npyscreen.TitleText, name = "Song:", value="Enter a song name here", editable=True)  
  def afterEditing(self):
    self.parentApp.setNextForm("SecondMAIN")
    self.parentApp.getForm("SecondMAIN").searchedSong.value = geniusLyrics.get_possible_songs(self.name.value)[0][1].strip()
    self.parentApp.getForm("SecondMAIN").lyrics.value = geniusLyrics.lyrics_from_song_api_path(geniusLyrics.get_possible_songs(self.name.value)[0][3])
class SecondForm(npyscreen.Form):
  def create(self):
    self.add(npyscreen.TitleText, name = "LyricsEx_SecondPage")
    self.searchedSong = self.add(npyscreen.TitleText, name = "Searched song")
    self.lyrics = self.add(npyscreen.MultiLineEdit,editable=True)
  def afterEditing(self):
    self.parentApp.setNextForm("MAIN")
if __name__ == '__main__':
	TA = MyTestApp()
	TA.run()