from .repository import Repository


class TaskRepo(Repository):
    def __init__(self, db):
        super(TaskRepo, self).__init__(db, 'task')
        self._create_table('''
                           id BINARY(16) PRIMARY KEY,
                           board_id BINARY(16) NOT NULL,
                           content TEXT
                           ''')
