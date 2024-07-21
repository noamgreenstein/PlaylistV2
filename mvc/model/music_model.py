from mvc.model import database_functions
from mvc.model.spotify_conn import SpotifyConn
import constants as c


class MusicModel:
    def __init__(self):
        self.spotify = SpotifyConn()
        self.db = database_functions.DB()

    def read_data(self, data):
        if data['type'] == 'db':
            self.use_db(data['command'])
        else:
            self.use_spotify(data['command'])

    def use_db(self, data):
        try:
            return self.db.execute(data['action'] == 'insert into', data['action'] == 'select'
                                   or data['action'] == 'delete from', **data)
        except AttributeError:
            return 'Error'

    def use_spotify(self, data):
        if data['method'] == 'name':
            return self.spotify.search(**data['params'])
        elif data['secondary'] != {}:
            return self.spotify.get_items(**data['primary'], **data['secondary'],
                                          groups=data.get('params', None))
        else:
            return self.spotify.get_item(**data['primary'])

    def update(self):
        q_ids = self.db.get_updates()
        for q in q_ids:
            name = self.spotify.get_item(q[0], q[1], q=False)['name']
            self.db.execute(True, False, 'insert into', q[0],
                            c.column_data[q[0]], c.format_params(name, q[1:-1]
                                                                 if q[0] == 'artists' else q[1:]))
            self.db.delete_from_queue(q[1])

    def update_row(self, table, updates, conditions):
        self.db.update_row(table, updates, conditions)

