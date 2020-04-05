
"""Class to manage lyric related affairs"""

import csv
import requests
import bs4
import logging


class LyricManager(object):

    def __init__(self):
        """Initialisation of LyricManager class"""

        self.song_dict = {}
        self.base_url = 'http://www.metrolyrics.com/'
        self.song_url = ''
        self.full_lyrics = []

    def get_data_from_file(self, filename):
        """
        Method for getting song data from csv file provided into
        class dictionary "song_dict"

        Parameter:
            filename: str - path & filename of file to be parsed

        Returns:
            self.song_dict: dict - returns the dictionary for external use

        """

        print('Opening file, %s' % filename)
        with open(filename, mode='r') as my_file:
            reader = csv.reader(my_file)
            for line in reader:
                my_key = line[0]
                my_value = line[1]
                self.song_dict[my_key] = my_value

        return self.song_dict

    def get_all_lyrics(self, number_of_lines):

        my_lyric_list = []
        for song in self.song_dict:
            self.create_lyric_url(self.song_dict[song], song)
            self.parse_lyrics()
            if number_of_lines == 0:
                #print('number_of_lines = 0. Returning all the lyrics...')
                curr_song_lyrics = self.full_lyrics
            else:
                #print('number_of_lines <> 0. Returning some of the the lyrics...')
                curr_song_lyrics = self.get_opening_line(number_of_lines)
            #if not curr_song_lyrics:
            my_lyric_dict = {'artist':song, 'song':self.song_dict[song], 'lyrics': curr_song_lyrics}
            if my_lyric_dict['lyrics'] is not None:
                my_lyric_list.append(my_lyric_dict)

        return my_lyric_list

    def create_lyric_url(self, song_title, artist):
        """
        Method for creating song specific url from base url

        Parameter:
            song_title: str - title of the song
            artist: str - artist of the song

        Returns:
            self.song_url: str - returns the song specific url for external use

        """

        mod_song_title = song_title.replace(" ", "-").lower()
        mod_artist = artist.replace(" ", "-").lower()
        self.song_url = self.base_url + mod_song_title + '-lyrics-' + mod_artist

        return self.song_url

    def get_lyrics(self):
        try:
            res = requests.get(self.song_url)
            #print res
            res.raise_for_status()
            #print('Getting Soup...')

            return res.text

        except requests.exceptions.HTTPError as err:
            #  Don't worry if it doesn't work, just carry on with the next search
            pass
            # print err
            # sys.exit(1)
            return ""

    def parse_lyrics(self):
        """
        Method gets_lyrics method to get html from usre
        and the uses BeautifulSoup to extract data from html

        Returns:
            self.full_lyrics: str - returns the song specific lyrics
        """
        res_text = self.get_lyrics()

        #print('Making soup...')
        soup = bs4.BeautifulSoup(res_text, 'lxml')

        # Get "lyrics-body-text"
        body_text = soup.find_all(id="lyrics-body-text")
        y = len(body_text)

        # Assuming on 1, look for the p tag
        if body_text:
            lyrics = body_text[0].find_all('p')
        else:
            lyrics = []
        # Strip out br tag and create lyric string
        # print("lyrics are...")
        # print lyrics
        self.full_lyrics = []
        for lyric_chunk in lyrics:
            for br in lyric_chunk.find_all("br"):
                br.replace_with("")
            try:
                chunk_lyrics_list = lyric_chunk.text.split('\n')
                # self.full_lyrics = u' '.join((self.full_lyrics, lyric_chunk.text)).encode('utf-8').strip()
                self.full_lyrics += chunk_lyrics_list
            except:
                print('Something went wrong!')
        # print('full_lyrics are...%s', self.full_lyrics)
        # try:
        #     print('self.full_lyrics[0] = "%s"' % self.full_lyrics[0])
        # except:
        #     pass
        return self.full_lyrics

    def get_opening_line(self, number_of_lines):
        """
        Method gets x number of lines from self.full_lyrics

        Parameter:
            number_of_lines: int - number of lines required
        Returns:
            first_x_lines: str - returns string containing first x lines (where x = number_of_lines)

        """

        return self.full_lyrics[0:number_of_lines]

    def create_blanked_lyrics(self, lyric_list):
        """
        Method for creating a blanks out song and printing it to the screen

        Parameter:
            lyric_list: list - list of lyrics from a specific song

        """

        modified_song = []
        for line in lyric_list:
            # print line
            line_upper = line.upper()
            words = line_upper.split()
            # print words
            new_line = []
            for word in words:
                # print word
                new_word = ''
                first_char = True
                for char in word:
                    # print char
                    if not first_char and char.isalpha():
                        # replace with
                        new_word += '_'
                    else:
                        new_word += char
                    first_char = False
                # Always add a space after word
                new_word += ' '
                # print new_word
                new_line.append(new_word)

            modified_song.append(new_line)

        for line in modified_song:
            new_line_str = ''
            print new_line_str.join(line)



def main():
    """
    Main stuff goes here
    """

    lm = LyricManager()

    lm.get_data_from_file('song.txt')
    print lm.song_dict


if __name__ == "__main__":
    main()