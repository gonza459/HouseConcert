import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

import SpotifyPlaylist
import SearchSetlist

#Introduction to program and instructions to logging in
print 'Welcome to Setify! The application where we create a playlist just for \n you as simply as searching for a concert'
print 'To get started, please enter your Spotify username when prompted.'
print 'After you have entered your username, log in to your spotify account \n and copy and paste the url as directed back in the terminal.'
print 'Lets get started!'

#spotify API
token = util.prompt_for_user_token(
    username = raw_input("Please enter your username: "),
    scope = 'playlist-modify-private playlist-modify-public',
    #Enter Spotify API ID
    client_id ='3817588cd345435c86c9a60e6c0cb70a',
    #Enter Spotify API Secret
    client_secret ='ce6c55f9f3c343bb919d917257661a3b',
    #Enter Spotify API Redirect URI
    redirect_uri='http://spotify.com/us'
)
#create session token for spotify
spotify = SpotifyPlaylist.createSpotifyToken(token)
username = spotify.me()['id']

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

print
#instructions for retrieving setlists
print 'You can now search for a setlist!'
print 'If you would like to create a playlist based on the most recent performance \n by an artist, enter 1.'
print 'If you would like the most recent concert performed at a venue, enter 2.'
print 'If you would like to create a playlist according to a specific performance, \n enter 3 to enter the artist name, venue name, and year.'
print

#boolean for running the program
run = True;

print 'Please enter how you wish to search for looking up the setlist'
selection = ''

#Runs the program while run condition is true
while run:
    while selection != '1' or '2' or '3':
        selection = raw_input('Enter 1 for artist name or 2 for venue or 3 for specific setlist: ')
        print

        #Input search term type (artist, or city/venue)
        if selection == '1':
            name = raw_input("Enter artist name: ")
            #Searches setlist.fm data for artist mbid
            artistID = SearchSetlist.getArtistID(headers, name)

            artistSetlist = SearchSetlist.getArtistSetlist(artistID, headers) #debug
            setList = SearchSetlist.createSetlist(artistSetlist)

            #Creates list of track ids from the songs from the setlist to be searched in Spotify
            trackList = SpotifyPlaylist.createTrackList(spotify, username, name, setList)

            #searches spotify data for info relating to artist name
            playlistName = raw_input("Enter the name of your Playlist: ")

            #Creates the playlist in the user's account
            playlist = SpotifyPlaylist.createSpotifyPlaylist(spotify, username, playlistName)

            #This retrieves the playlistID as jsut created by the user
            playlistID = SpotifyPlaylist.getSpotifyPlaylistID(spotify, username, playlistName)

            #Adds the songs to the playlist on the user's spotify account
            SpotifyPlaylist.addTrackList(spotify, username, playlistID, trackList)

                        #Asks if you would like to run the program again to create another playlist
            print "Your playlist is now in your Spotify account and ready for you to enjoy!"
            runAgain = raw_input ("Would you like to make another playlist? ")
            if runAgain == 'no':
                print "Thank you for your search."
                run = False
                break
            else:
                run = True

        #Search for most recent setlist according to venue name
        elif selection == '2':
            venue = raw_input('Enter the venue name: ')
            #searches setlit.fm data for venue id
            cityID = SearchSetlist.getVenueID(headers, venue)
            #gets the name of the artist who performed the most recent concert at the searched veue
            name = SearchSetlist.getVenueArtistName(cityID, headers)

            print "The artist of the concert at this venue was " + name
            makePlaylist = raw_input("Would you like to still make a playlist of this artist's setlist? ")
            print

            if makePlaylist == 'yes':
                #reteives the setlist based on the venue and artistname
                venueSetlist = SearchSetlist.getVenueSetlist(cityID, headers)

                #creates a list of the songs from the venue setlist retieved
                setList = SearchSetlist.createSetlist(venueSetlist)
                print
                #Creates list of track ids from the songs from the setlist to be searched in Spotify
                trackList = SpotifyPlaylist.createTrackList(spotify, username, name, setList)

                playlistName = raw_input("Enter the name of your Playlist: ")

                #Creates the playlist in the user's account
                playlist = SpotifyPlaylist.createSpotifyPlaylist(spotify, username, playlistName)

                #This retrieves the playlistID as jsut created by the user
                playlistID = SpotifyPlaylist.getSpotifyPlaylistID(spotify, username, playlistName)

                #Adds the songs to the playlist on the user's spotify account
                SpotifyPlaylist.addTrackList(spotify, username, playlistID, trackList)

                            #Asks if you would like to run the program again to create another playlist
                print "Your playlist is now in your Spotify account and ready for you to enjoy!"
                runAgain = raw_input ("Would you like to make another playlist? ")
                if runAgain == 'no':
                    print "Thank you for your search."
                    run = False
                    break
                else:
                    run = True

            elif makePlaylist == 'no':
                print "Thank you for your search."
                break

        #Search for most recent setlist according to artist name, venue name, and year
        elif selection == '3':
            name = raw_input("Enter artist name: ")
            venue = raw_input('Enter the venue name: ')
            year = raw_input("Enter a year: ")

            #searches setlit.fm data for setlist id
            setlistID = SearchSetlist.getSetlistID(name, year, venue, headers)

            #takes setlistID and obtains the setlist data stored here
            FullSetlist = SearchSetlist.getSetlist(setlistID, headers)
            setList = SearchSetlist.createSetlist(FullSetlist)

            #Creates list of track ids from the songs from the setlist to be searched in Spotify
            trackList = SpotifyPlaylist.createTrackList(spotify, username, name, setList)

            #searches spotify data for info relating to artist name
            playlistName = raw_input("Enter the name of your Playlist: ")

            #Creates the playlist in the user's account
            playlist = SpotifyPlaylist.createSpotifyPlaylist(spotify, username, playlistName)

            #This retrieves the playlistID as jsut created by the user
            playlistID = SpotifyPlaylist.getSpotifyPlaylistID(spotify, username, playlistName)

            #Adds the songs to the playlist on the user's spotify account
            SpotifyPlaylist.addTrackList(spotify, username, playlistID, trackList)

            #Asks if you would like to run the program again to create another playlist
            print "Your playlist is now in your Spotify account and ready for you to enjoy!"
            runAgain = raw_input ("Would you like to make another playlist? ")
            if runAgain == 'no':
                print "Thank you for your search."
                run = False
                break
            else:
                run = True
        else:
            print('Not a valid input. Try again.')
