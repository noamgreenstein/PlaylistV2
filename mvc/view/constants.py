name_data = {
    'method': 'name',
    'params': {
        'name': '',
        'item': '',
        'limit': ''
    },
}

mt_data = {
    'table': '',
    'columns': '',
    'params': ''
}

save_data = {
    'action': 'insert into',
    **mt_data
}

get_data = {
    'action': 'select',
    **mt_data
}

delete_data = {
    'action': 'delete from',
    **mt_data
}

column_data = {
    'artists': '(artist_name, artist_id, image_url)',
    'tracks': '(track_name, track_id, artist_id, album_id)',
    'albums': '(album_name, album_id, artist_id, image_url)'
}

selects = {
    'artists': 'artist_id, artist_name, total_rating, album_rating',
    'albums': 'album_id, album_name, '
              '(select a.artist_name from artists a where a.artist_id = albums.artist_id) '
              'as artist_name,'
              'rating',
    'tracks': 'track_id, track_name, '
              '(select a.artist_name from artists a where a.artist_id = tracks.artist_id) '
              'as artists_name,'
              '(select al.album_name from albums al where al.album_id = tracks.album_id) '
              'as album_name,'
              'rating'

}

table_column = {
    'artists': ['ID', 'Name', 'Rating', 'Album Rating'],
    'albums': ['ID', 'Name', 'Artist', 'Rating'],
    'tracks': ['ID', 'Name', 'Artist', 'Album', 'Rating']
}


def format_params(name, q):
    init = f'("{name}"'
    for qx in q:
        init += f', "{qx}"'
    init += ')'
    return init
