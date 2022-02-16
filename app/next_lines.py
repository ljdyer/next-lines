from helper.html_helper import get_bs, get_lines
from fuzzywuzzy import process

SONGSEARCH_ROOT = "https://songsear.ch"


# ====================
def http_encode_char_or_space(c):

    if c == ' ':
        return "%20"
    else:
        return c


# ====================
def get_search_url(lyrics):

    lyrics = ''.join([http_encode_char_or_space(c.lower())
                      for c in lyrics if c.isalpha() or c == ' '])
    return f'https://songsear.ch/q/{lyrics}'


# ====================
def get_top_match(search_page):

    bs = get_bs(search_page)
    first_result = bs.find(name='div', class_='result')

    title_tag = first_result.find(name='h2')
    song_name = title_tag.find(name='a').text
    song_link = SONGSEARCH_ROOT + title_tag.find(name='a')['href']

    artist_tag = first_result.find(name='h3')
    artist_name = artist_tag.find(name='b').text

    return song_name, artist_name, song_link


# ====================
def get_lyric_lines(lyrics_url):

    bs = get_bs(lyrics_url)
    lyrics = get_lines(bs.find(name='blockquote'))
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
