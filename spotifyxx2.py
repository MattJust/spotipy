import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#get username from terminal
username = sys.argv[1]

#new code to auto playback:
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# https://open.spotify.com/user/half-truth?si=w6z1NmMMQ36AEmRnz1kylw
# userid: half-truth?si=w6z1NmMMQ36AEmRnz1kylw

#erase cache and prompt for user permission
try:
	token = util.prompt_for_user_token(username, scope)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

#create our spotifyObject with permissions
spotifyObject = spotipy.Spotify(auth=token)	

# Get current devide
devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# Current track information
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

if artist != "":
	print("Currently playing " + artist + " - " + track)

# user information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

#loop
while True:

	print()
	print(">>> Welcome to Spotipy " + displayName + "!")
	print(">>> you have " + str(followers) + " followers.") 
	print()
	print("0 - Search for an artist")
	print("1 - exit")
	print()
	choice = input("Your choice: ")

	# Search for the artist
	if choice == "0":
		print("0")
		searchQuery = input("Ok, what's their name?: ")
		print()

		# Get search results
		searchResults = spotifyObject.search(searchQuery,1,0,"artist")
		print(json.dumps(searchResults, sort_keys=True, indent=4))

		#artist details
		artist = searchResults['artists']['items'][0]
		print(artist['name'])
		print(str(artist['followers']['total']) + " followers")
		print(artist['genres'][0])
		print()
		webbrowser.open(artist['images'][0]['url'])
		artistID = artist['id']

		#album and track details
		trackURIs = []
		trackArt = []
		z = 0

		# extract album data
		albumResults = spotifyObject.artist_albums(artistID)
		albumResults = albumResults['items']

		for item in albumResults:
			print('ALBUM ' + item['name'])
			albumID = item['id']
			albumArt = item['images'][0]['url']

			# extract track data
			trackResults = spotifyObject.album_tracks(albumID)
			trackResults = trackResults['items']

			for item in trackResults:
				print(str(z) + ": "+  item['name'])
				trackURIs.append(item['uri'])
				trackArt.append(albumArt)
				z+=1
			print()
			
		#see album art
		while True:
			songSelection = input("Enter a song number to play the song and see art associated with it (x to exit)")
			if songSelection == "x":
				break
			trackSelectionList = []
			trackSelectionList.append(trackURIs[int(songSelection)])	
			spotifyObject.start_playback(deviceID, None, trackSelectionList)
			webbrowser.open(trackArt[int(songSelection)])			

	# end the program
	if choice == "1":
		break

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))