import sqlite3


class DB:

    def __init__(self):
        self.connection = sqlite3.connect(
            '/Users/noamgreenstein/Documents/Projects/DiscTracker/disc_tracker.sqlite',
            check_same_thread=False)

        self.cursor = self.connection.cursor()

    def execute(self, save, select, action, table, columns, params):
        cond = 'values' if save else 'where'
        try:
            if select:
                if params == '':
                    self.cursor.execute(f'{action} {columns} FROM main.{table}')
                else:
                    self.cursor.execute(f'{action} {columns} FROM main.{table} {cond} {params}')
                return self.cursor.fetchall()
            else:
                self.cursor.execute(f'{action} main.{table}{columns} {cond} {params}')
                self.connection.commit()
                return 'Success'
        except sqlite3.IntegrityError:
            raise AttributeError(f'Values: {params} already exist in database')

    def get_updates(self):
        return self.cursor.execute('select obj_type, obj_id, obj_image_url, secondary_id '
                                   'from update_queue').fetchall()

    def delete_from_queue(self, obj_id):
        self.cursor.execute('DELETE FROM main.update_queue WHERE obj_id = ?', (obj_id,))
        self.connection.commit()
        return 'Success'

    def update_row(self, table, updates, conditions):
        update_parts = [f"{u['row']} = ?" for u in updates]
        update_string = ", ".join(update_parts)

        condition_parts = [f"{c['row']} = ?" for c in conditions]
        condition_string = " AND ".join(condition_parts)

        sql_command = f"UPDATE {table} SET {update_string} WHERE {condition_string}"

        values = [u['value'] for u in updates] + [c['value'] for c in conditions]
        self.cursor.execute(sql_command, values)
        self.connection.commit()
        return 'Success'

