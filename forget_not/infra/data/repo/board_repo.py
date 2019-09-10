from .repository import Repository


class BoardRepo(Repository):
    def __init__(self, db):
        super(BoardRepo, self).__init__(db, 'board')
        self._create_table('''
                           id BINARY(16) PRIMARY KEY,
                           name TEXT
                           ''')
