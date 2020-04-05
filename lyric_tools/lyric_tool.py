import argparse
import logging
import sys
import textwrap
from lyric_manager import LyricManager as lm


def main(argv):

    # set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # create command line args
    parser = argparse.ArgumentParser(
            prog='lyric_tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Utility to to do stuff with lyrics',
            epilog=textwrap.dedent('''\
                    Examples:
                    ---------
                    lyric_tool -g 
            ''')
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', required=False, action='store_true',help='dunno yet')
    group.add_argument('-g', required=False, nargs='+', help='Parse csv file and get lyrics')

    parser.add_argument('-n', required=False, nargs='+', help='Number of line')
    parser.add_argument('-p', required=False, action='store_true', help='Prettify the output')
    parser.add_argument('-x', required=False, action='store_true', help='Print blank song')
    # parser.add_argument('-p', required=False, action='store_true', help='Print Windows to stdout at the end of the keypress sequence')

    parser.parse_args()
    args = parser.parse_args()
    #print(vars(args))

    # Instantiate connection for lyric manager
    my_lm = lm()
    if args.g:
        logging.info('Getting date from %s' % args.g)
        my_dict = my_lm.get_data_from_file(args.g[0])
        print my_dict

        if args.n:
            my_lyrics = my_lm.get_all_lyrics(int(args.n[0]))
        else:
            my_lyrics = my_lm.get_all_lyrics(0)

        if args.p:
            for song in my_lyrics:
                print song
                print('============================================')
                print('Song: %s, Artist: %s' % (song['song'], song['artist']))
                print('--------------------------------------------')
                for line in song['lyrics']:
                    print line.encode('utf-8')
                print('--------------------------------------------')
                if args.x:
                    print my_lm.create_blanked_lyrics(song['lyrics'])

                print('============================================')
        else:
            print my_lyrics


    print('Finished!')


if __name__ == '__main__':
    main(sys.argv[1:])