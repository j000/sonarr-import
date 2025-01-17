import sqlite3


class Database:
    def __init__(self, file_path):
        self.connection = sqlite3.connect(file_path)
        self.cur = self.connection.cursor()

    def get_shows(self):
        cur = self.cur.execute("Select Title,TvdbId from Series")
        for row in cur:
            yield row
