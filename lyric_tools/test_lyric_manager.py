from hamcrest import assert_that, equal_to
import unittest
import mock
from . import lyric_manager


class TestLyricManager(unittest.TestCase):

    def test_get_data_from_file(self):
        my_lm = lyric_manager.LyricManager()
        my_lm.get_data_from_file('lyric_tools/test_csv_file.txt')
        print my_lm.song_dict
        assert_that(my_lm.song_dict, equal_to({'Oasis': 'Live Forever'}))

    def test_create_lyric_url(self):
        my_lm = lyric_manager.LyricManager()
        my_lm.create_lyric_url('My Song', 'My Artist')
        assert_that(my_lm.song_url, equal_to('http://www.metrolyrics.com/my-song-lyrics-my-artist'))

    # Commented out as we don't generally want to hit the website during unit test
    # def test_parse_lyrics_live(self):
    #     my_lm = lyric_manager.LyricManager()
    #     my_lm.create_lyric_url('torn', 'Natalie Imbruglia')
    #     print my_lm.song_url
    #     my_lm.parse_lyrics()

    @mock.patch('lyric_tools.lyric_manager.LyricManager.get_lyrics')
    def test_parse_lyrics_mocked(self, mock_res_txt):
        # get example data from test.html
        with open("lyric_tools/test.html", 'r') as file:
            res_text = file.read()
        # Mock up return value
        mock_res_txt.return_value = res_text

        my_lm = lyric_manager.LyricManager()
        my_lm.parse_lyrics()
        print my_lm.full_lyrics
        assert_that(my_lm.full_lyrics, equal_to('This is my song\nIt is a lovely song\nSucha lovely song This is still my song\nStill a lovely song\nSucha lovely song'))

    @mock.patch('lyric_tools.lyric_manager.LyricManager.get_lyrics')
    def test_get_opening_2_line_mocked(self, mock_res_txt):
        # get example data from test.html
        with open("lyric_tools/test.html", 'r') as file:
            res_text = file.read()
        # Mock up return value
        mock_res_txt.return_value = res_text

        my_lm = lyric_manager.LyricManager()
        my_lm.parse_lyrics()
        print my_lm.full_lyrics
        my_opening_lines = my_lm.get_opening_line(2)
        assert_that(my_opening_lines, equal_to([u'This is my song', u'It is a lovely song']))

    @mock.patch('lyric_tools.lyric_manager.LyricManager.get_lyrics')
    def test_get_opening_6_line_mocked(self, mock_res_txt):
        # get example data from test.html
        with open("lyric_tools/test.html", 'r') as file:
            res_text = file.read()
        # Mock up return value
        mock_res_txt.return_value = res_text

        my_lm = lyric_manager.LyricManager()
        my_lm.parse_lyrics()
        print my_lm.full_lyrics
        my_opening_lines = my_lm.get_opening_line(6)
        assert_that(my_opening_lines, equal_to([u'This is my song', u'It is a lovely song', u'Sucha lovely song', u'This is still my song', u'Still a lovely song', u'Sucha lovely song']))

    @mock.patch('lyric_tools.lyric_manager.LyricManager.parse_lyrics')
    def test_create_blanked_lyrics_mocked(self, mock_parse_lyrics):
        # get example data from test.html
        with open("lyric_tools/test.html", 'r') as file:
            res_text = file.read()
        # Mock up return value
        #mock_res_txt.return_value = res_text

        my_lm = lyric_manager.LyricManager()
        my_lm.full_lyrics = [u'This is my song', u'It is a lovely song', u'Sucha lovely song', u'This is still my song', u'Still a lovely song', u'Sucha lovely song']
        my_lm.song_dict = {'Oasis': 'Live Forever'}

        my_lyrics = my_lm.get_all_lyrics(6) # my_lm.parse_lyrics()
        print my_lyrics

        my_lm.create_blanked_lyrics(my_lyrics[0]['lyrics'])



        #assert_that(my_opening_lines, equal_to('This is my song It is a lovely song Sucha lovely song This is still my song Still a lovely song Sucha lovely song...'))

if __name__ == '__main__':
    unittest.main()
