# Sorterr
Media sorting scripted based on Guessit.  Personally this runs after Unpackkerr does a unpack.  I also have run it on large collections I already had.

### Supported Media Type:
mp4, avi, mkv, m4v

### Expected Output of Moving files.

> [TVPath]/[ShowName]/[Season # or Specials]/[ShowName] [Season#/Epi#] [Epi Title] [Video info] [AudioChannels].extension

> [MoviePath]/[Movie Title] [Year] [Alt Title or Other info] [Video Info] [Audio Channels].extension

### There are few configution options.  Which you can see below

#### This should be where Sorterr finds the unsorted files.
> downloadPath = "/srv/mergerfs/pool0/Downloads/"

#### This is where it should sort TV shows to
> TVPath = "/srv/mergerfs/pool0/TV/"

#### This is where it should sort Movies to.
> MoviesPath = "/srv/mergerfs/pool0/Movies/"

#### Use ffmpeg to check for Resolution and sample audio if Im already sampling Resolution.
> Use_FFMPEG = 		1

#### Delete the sub directies when done.
> DeletionEnabled = 	1

#### Moves the Renamed files into TV and Movie Path.  Doesnt work without renaming me on.
> MoveEnabled = 		1

#### Controls whether to rename or not.
> RenameEnabled = 	1

#### Debugging stuff.   Testmode should probably be run on anything with a weird folder setup first.
> NOISEY =			0

> TESTMODE =			0
