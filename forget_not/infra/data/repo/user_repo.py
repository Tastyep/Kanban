from .repository import Repository


class UserRepo(Repository):
    def __init__(self, db):
        super(UserRepo, self).__init__(db, 'user')
        self._create_table('''
                           id BINARY(16) PRIMARY KEY,
                           board_id BINARY(16) NOT NULL
                           ''')
