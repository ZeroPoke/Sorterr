#! /bin/python3

import os

from guessit import guessit
from videoprops import get_video_properties
from videoprops import get_audio_properties
import pathlib
import shutil

downloadPath = "/srv/mergerfs/pool0/Downloads/"	## Path of Downloads Folder
TVPath = "/srv/mergerfs/pool0/TV/"				## Path where to save TV shows
MoviesPath = "/srv/mergerfs/pool0/Movies/"		## Path where to save Movies

Use_FFMPEG = 		1							##Do you want to use FFMPEG to check res if not in filename.
DeletionEnabled = 	1
MoveEnabled = 		1
RenameEnabled = 	1
NOISEY =			0
TESTMODE =			0

def SampleMedia(fnFullname):
	vprops = get_video_properties(fnFullname)

	video_codec = vprops['codec_name']
	screen_size = str(vprops['height']) + "p"

	aprops = get_audio_properties(fnFullname)

	if aprops['channels'] == 6:
		audio_channels = "5.1"
	elif aprops['channels'] == 8:
		audio_channels = "7.1" 
	elif aprops['channels'] == 9:
		audio_channels = "7.2"
	else:
		audio_channels = aprops['channels']

	return video_codec, screen_size, audio_channels

def ProcessContent(filename, extension):
	info = guessit(filename)
	
	#print(filename)
	#print(info)

	episode = "00"
	season = "00"

	if info.get("title"):
		titleTest = info['title']
		if isinstance(titleTest, list):			##Test to see if title comes back as a list and if does samples just the filename.
			title_parent, title_filename = os.path.split(filename) 
			newInfo = guessit(title_filename)
			fnTitle = title = newInfo['title'].title()
		else:
			fnTitle = title = info['title'].title()
	type = info['type']

#Guessit Episode number and Season Stuff
	if type == "episode":
		if info.get("season"):			##Season
			season = info['season']
			season = "{0:0>2}".format(info['season'])

		if info.get("episode"):			##Epi Number
			episode_test = info['episode']
			if isinstance(episode_test, list):
				episode_list = [str(element) for element in episode_test]
				episode = "-E".join(episode_list)
				episode = "{0:0>2}".format(episode)
			else:
				episode = "{0:0>2}".format(info['episode'])

		if info.get("episode_title"):	##Epi Title
			episode_title = " " + info['episode_title']
			if episode_title.islower: 
				episode_title = episode_title.title()
		else:
			episode_title =""

		if info.get("part"):
			episode_title += " Part " + str(info['part'])

		fnEpisodeInfo = " S" + season + "E" + episode + episode_title
	else:
		fnEpisodeInfo = ""
		season = ""

	if type == "movie":					##Can grab other info from Movie titles.  Seems useful.  #Trustme.
		if info.get("alternative_title"):
			fnEpisodeInfo = " (" + info['alternative_title'] + ")"
			if fnEpisodeInfo.islower: 
				fnEpisodeInfo = fnEpisodeInfo.title()
		else:
			fnEpisodeInfo = ""
				
		if info.get("cd"):
			fnEpisodeInfo = " (CD" + str(info['cd']) + ")"		##CD Parts for Old Sckool Shit.  You should probably get a new copy IMO.

		if info.get("part"):
			fnEpisodeInfo = " (Part " + str(info['part']) + ")"	##Parts useful for when Guessit detects epi parts.



#Guessit Video Info
	if info.get("screen_size"):
		screen_size = info['screen_size']
	else:
		screen_size = ""
	if info.get("video_codec"):
		video_codec = info['video_codec']
	else:
		video_codec = ""
	if info.get("source"):
		source = info['source']
	else:
		source = ""

#No Res? Sample Media for Info. Might as well Do Audio too.
	audio_channels = ""
	if screen_size == "" and Use_FFMPEG == 1:
		video_codec, screen_size, audio_channels = SampleMedia(filename+extension)
		
#Formatting and Guessit Year Info
	if info.get("year"):
		year = info['year']
		fnYearInfo = " (" + str(year) + ")"
	else:
		fnYearInfo = ""

#Formating and Guessit Video Info
	infoVideoStr = ""
	infoVideoList = []

	if screen_size != "":
		infoVideoList.append(screen_size)
	if video_codec != "":
		infoVideoList.append(video_codec)
	if source != "":
		infoVideoList.append(source)
	
	InfoVideoList_Test = [str(element) for element in infoVideoList]
	infoVideoStr = " - ".join(InfoVideoList_Test)

	if infoVideoStr != "":
		fnVideoInfo = " [" + infoVideoStr + "]"
	else:
		fnVideoInfo = ""

#Formating and Guessit Audio Info
	##Only prints audio channels if better then stereo.
	if audio_channels == "":
		if info.get("audio_channels"):
			audio_channels = info['audio_channels']
			fnAudioInfo = " [" + str(audio_channels) + "]"
	else:
		fnAudioInfo = " [" + str(audio_channels) + "]"

	if (audio_channels == "2.0") or (audio_channels == "2") or (audio_channels == 2) or (audio_channels == ""):
		fnAudioInfo = ""

#Final Formating of File Name
	fnFinalName = fnTitle + fnEpisodeInfo + fnYearInfo + fnVideoInfo + fnAudioInfo
	fnProcessed = "{0}{1}".format(fnFinalName, extension)

	print(fnProcessed)

	return fnProcessed, season, title, type

#Main, Does the Directory scan and runs the other functions.
def Check4Media():
	filetypes = ('*.mp4|*.avi|*.mkv|*.m4v')
	files = list(sorted(pathlib.Path(downloadPath).rglob("**/*.[mMaA][4pPvVkK][4iIvV]")))

#print(files)
	
	prevLine = ""

	for index, content in enumerate(files):
		#print(content)
		content, extension = os.path.splitext(content)
		if (prevLine != ""):
			if os.path.dirname(prevLine) != os.path.dirname(content):
				DeleteContentDir(os.path.dirname(prevLine))
				##Bunch of Stupid path stuff cause Im dumb and I dont know a better way.
				prevLineTest, junk = os.path.split(prevLine)
				prevLineTest1, junk = os.path.split(prevLineTest)
				prevLineTest2, junk = os.path.split(prevLineTest1)
				currLineTest, junk = os.path.split(content) 
				currLineTest1, junk = os.path.split(currLineTest) 
				currLineTest2, junk = os.path.split(currLineTest1)
				if NOISEY == 1:		##Used for Deletion Debugging.
					print("currLineTest "+currLineTest)
					print("currLineTest1 "+currLineTest1)
					print("currLineTest2 "+currLineTest2)
					print("prevLineTest "+prevLineTest)
					print("prevLineTest1 "+prevLineTest1)
					print("prevLineTest2 "+prevLineTest2)
				##Hopefully only deletes the correct directories at the correct time.  Might want to run a test on big weird folder structions.  See options at the top.
				if prevLineTest1 != currLineTest and prevLineTest != currLineTest and prevLineTest != currLineTest2 and prevLineTest2 != currLineTest2 and prevLineTest != currLineTest2 and prevLineTest1 != currLineTest2:
					DeleteContentDir(prevLineTest1)

		if extension in filetypes and content and "sample" not in content.casefold():   ##Ignores Sample files and runs the filename processor, renamer and mover.
			fnProcessed, season, title, type = ProcessContent(content, extension)
			RenameContent(content, extension, fnProcessed)
			MoveContent(content.rsplit('/', 1)[0]+"/"+fnProcessed, season, title, type)
			prevLine = content

		if len(files) == index+1:														##End of For loop clean up.
			prevLineTest = os.path.dirname(prevLine)
			while prevLineTest != downloadPath and prevLineTest+"/" != downloadPath:
				DeleteContentDir(prevLineTest)
				prevLineTest, junk = os.path.split(prevLineTest) 

#If you cant read the Function name then any comment here isnt gonna help.
def RenameContent(content, extension, fnProcessed):
	if RenameEnabled == 1:
		try:
			os.rename(content+extension, content.rsplit('/', 1)[0]+"/"+fnProcessed)
		except OSError as err:
			print("Error: {0}".format(err))

#If you cant read the Function name then any comment here isnt gonna help.
def MoveContent(fnProcessed, season, title, type):
	if MoveEnabled == 1:
		if type == "episode":
			if season == "00":
				nameSeasonFolder = "/Specials/"					##Sets Season 00 episodes to a Specials Folder.  Its better for things like Emby.
			else:
				nameSeasonFolder = "/Season "+season.lstrip("0")+"/"
			try:
				if TESTMODE != 1:
					pathlib.Path(TVPath+title+nameSeasonFolder).mkdir(parents=True, exist_ok=True)
				else:
					print("Check Path "+TVPath+title+nameSeasonFolder)
			except OSError as err:
				print("Error: {0}".format(err))
			try:
				if TESTMODE != 1:
					shutil.move(fnProcessed, TVPath+title+nameSeasonFolder)
				else:
					print("Move: "+fnProcessed, TVPath+title+nameSeasonFolder)
			except OSError as err:
				print("Error: {0}".format(err))

		if type == "movie":
			try:
				if TESTMODE != 1:
					shutil.move(fnProcessed, MoviesPath)
				else:
					print("Move: "+fnProcessed, MoviesPath)
			except OSError as err:
				print("Error: {0}".format(err))

#If you cant read the Function name then any comment here isnt gonna help.  Only deletes sub folders in the download directory.
def DeleteContentDir(Path):
	if DeletionEnabled == 1:
		if Path != downloadPath and Path+"/" != downloadPath:
			try:
				if TESTMODE != 1:
					shutil.rmtree(Path)
				else:
					print("Deleted: " + Path)
			except OSError as err:
				print("Error: {0}".format(err))

#Makes everything work.  Stolen from other scripts YMMV
if __name__ == "__main__":
    while True:
            Check4Media()
            exit()
