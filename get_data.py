'''
Created on 5 Nov 2018

@author: st3v3
'''
import csv
import requests
import bs4
import logging
import sys


def get_data_from_file(filename):
    """Function for getting song data from csv file provided"""
    my_dict = {}
    print('Opening file, %s' % filename)
    with open(filename, mode='r') as my_file:
        reader = csv.reader(my_file)
        for line in reader:
            my_key = line[0]
            my_value = line[1]
            my_dict[my_key] = my_value

        print my_dict

    return my_dict

def get_lyrics(url):
    """Use BeautifulSoup to extract data from URL"""

    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Get "lyrics-body-text"
        body_text = soup.find_all(id="lyrics-body-text")
        y = len(body_text)

        # Assuming on 1, look for the p tag
        if body_text:
            lyrics = body_text[0].find_all('p')
        else:
            lyrics = []
        # Strip out br tag and create lyric string
        full_lyrics = ""
        for lyric in lyrics:
            for br in lyric.find_all("br"):
                br.replace_with("")
                try:
                    full_lyrics = u' '.join((full_lyrics, lyric.text)).encode('utf-8').strip()
                except:
                    print('Something went wrong!')

        # First two lines
        logging.info("All lines extracted...")

        lyric_list = full_lyrics.splitlines()
        for lyric_line in lyric_list:
            logging.info("> " + str(lyric_line))

        # First two lines
        logging.info("The first two lines...")
        first_two_lines = ""
        for lyric_line in lyric_list[0:6]:
            # print(str(lyric_line))
            first_two_lines = first_two_lines + lyric_line + " "
        first_two_lines = first_two_lines.strip() + "..."
        logging.info("Extracted first_two_lines..." + first_two_lines)
        return first_two_lines

    except requests.exceptions.HTTPError as err:
        pass
        print err
        sys.exit(1)


if __name__ == '__main__':
    pass
