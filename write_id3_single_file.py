from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, TRCK, TPOS


def write_id3_single_file(path, filename, title, episode, season, album, album_artist, artist):
    print(episode)
    print(season)
    try:
        audio = ID3(path + filename)
        audio.delete()
        audio = ID3()
    except ID3NoHeaderError:
        audio = ID3()

    audio.add(TIT2(encoding=3, text=title))
    if episode != '':
        audio.add(TRCK(encoding=3, text=episode))
    else:
        print('No Episode Number')

    if season != '':
        audio.add(TPOS(encoding=3, text=season))
    else:
        print('No Season Number')

    audio.add(TPE1(encoding=3, text=artist))
    audio.add(TPE2(encoding=3, text=album_artist))
    audio.add(TALB(encoding=3, text=album))
    audio.save(path + filename)


