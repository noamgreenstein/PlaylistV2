base_url = 'https://api.spotify.com/v1/'
search_url = base_url + 'search'
token_url = 'https://accounts.spotify.com/api/token'
get_url = base_url + '{}/{}'
get_specif_url = base_url + '{}/{}/{}'
column_data = {
    'artists': '(artist_name, artist_id, image_url)',
    'tracks': '(track_name, track_id, artist_id, album_id)',
    'albums': '(album_name, album_id, artist_id, image_url)'
}


def format_params(name, q):
    init = f'("{name}"'
    for qx in q:
        init += f', "{qx}"'
    init += ')'
    return init
