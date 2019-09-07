from .repository import Repository


class TaskRepo(Repository):
    def __init__(self, db):
        super(TaskRepo, self).__init__(db)
