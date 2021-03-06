from helper.html_helper import get_bs, get_lines
from fuzzywuzzy import process

SEARCH_ROOT = "https://lyrics.com/lyrics"
SITE_ROOT = "https://lyrics.com/"


# ====================
def get_search_url(lyrics):

    lyrics_http_encoded = lyrics.replace(" ", "%20")
    return f'{SEARCH_ROOT}/{lyrics_http_encoded}'


# ====================
def get_top_match(search_page):

    bs = get_bs(search_page)
    first_result = bs.find(name='div', class_='sec-lyric')

    song_name = first_result.find(name='p', class_='lyric-meta-title').text
    song_link = SITE_ROOT + first_result.find(name='p', class_='lyric-meta-title').find(name='a')['href']
    artist_name = first_result.find(name='p', class_='lyric-meta-album-artist').text

    print('here')
    return song_name, artist_name, song_link


# ====================
def get_lyric_lines(lyrics_url):

    bs = get_bs(lyrics_url)
    lyrics = get_lines(bs.find(name='pre'))
    for line in lyrics:
        print(line)
    return lyrics


# ====================
def get_next_line(first_line_raw: str, lyric_lines: list) -> str:

    this_line, confidence = process.extractOne(first_line_raw, lyric_lines)
    this_line_index = lyric_lines.index(this_line)
    next_line = lyric_lines[this_line_index + 1]
    return next_line, confidence


# ====================
def answer_question(first_line_raw: str):

    try:
        search_url = get_search_url(first_line_raw)
        print(search_url)
        song_name, artist_name, song_link = get_top_match(search_url)
        lyric_lines = get_lyric_lines(song_link)
        next_line, confidence = get_next_line(first_line_raw, lyric_lines)
    except Exception as e:
        return {
            'success': False, 'err_msg': str(e)
        }
    else:
        return {
            'success': True,
            'song_name': song_name, 'artist_name': artist_name,
            'next_line': next_line, 'confidence': confidence
        }


# ===========
def next_question():

    first_line_raw = input('>> ')
    answer_question(first_line_raw)


# ===========
if __name__ == "__main__":

    while True:
        next_question()
