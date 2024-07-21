import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Acess.secret import CLIENT_ID, SECRET
from chat_gpt import ChatGPT


class PlaylistEditor:

    def __init__(self, user_id):
        self.user_id = user_id
        self.me = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                      client_secret=SECRET,
                                      redirect_uri="https://payme-4556f.web.app/",
                                      scope="playlist-modify-public"))
        self.gpt = ChatGPT()
        self.search_url = 'https://api.spotify.com/v1/search'
        self.playlists = []
        self.get_all_playlists()

    def generate_new_playlist(self, name: str):
        description = f'Playlist generated for {self.user_id} by PerfectPlaylist App'
        self.me.user_playlist_create(self.user_id, name, description=description)

    def perfect_playlist(self, description: str,
                         num_songs: int,
                         exists: bool,
                         playlist_name: str) -> str:
        song_list = self.gpt.generate_song_list(description, num_songs)
        song_list = song_list.split("\n")

        if not exists or not self.playlists.get(playlist_name):
            self.generate_new_playlist(playlist_name)
            self.get_all_playlists()

        uris = []
        for song in song_list:
            song = song.replace("\"", '')
            if song[1] == ".":
                song = song[2:]
            index = song.index("-")
            song_name = song[:index - 1]
            artist = song[index + 2:]
            query = f'track:{song_name} artist:{artist}'
            uris.append(self.get_song_uri(query))

        uris = filter(lambda x: x != '', uris)

        self.me.playlist_add_items(self.playlists.get(playlist_name), uris)
        return "Success"

    def get_song_uri(self, query: str) -> str:
        track = self.me.search(query, type='track', limit=1)
        if len(track.get('tracks').get('items')) > 0:
            return track.get('tracks').get('items')[0].get('uri')
        else:
            return ''

    def get_all_playlists(self):
        temp = {}
        playlists = self.me.current_user_playlists().get('items')
        for playlist in playlists:
            temp[playlist.get('name')] = playlist.get('uri')
        self.playlists = temp


test = PlaylistEditor("ngreenstein3-us")
test.perfect_playlist("background vocals and some synths to make me feel like im floating", 25, True, "super")
