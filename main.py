'''
Created on 5 Nov 2018

@author: st3v3
'''


import get_data


# Initialise variables
base_url = 'http://www.metrolyrics.com/'

# Import data from file into dictionary
song_dict = get_data.get_data_from_file('80sLyrics-v1.txt')

# Iterate over dictionary and create URL for each song (specific for metrolyrics)
for item in song_dict:
    #print('Searching for... %s : %s' % (item, song_dict[item]))
    curr_song = song_dict[item]
    mod_curr_song = curr_song.replace(" ","-").lower()
    curr_artist = item
    mod_curr_artist = curr_artist.replace(" ","-").lower()
    url = base_url + mod_curr_song + '-lyrics-' + mod_curr_artist

    #print('Searching at URL = %s...' % url)
    #print('Artist = %s, Song = %s' % (curr_artist,  curr_song))

    lyrics = get_data.get_lyrics(url)
    #print(lyrics)
    if lyrics:
        print('%s, %s : %s' % (curr_artist, curr_song, lyrics))


if __name__ == '__main__':
    pass
