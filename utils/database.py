from mysql.connector.pooling import MySQLConnectionPool


class Database:

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_connection(self):
        return self.pool.get_connection()
