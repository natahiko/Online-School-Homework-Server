from mysql.connector.pooling import MySQLConnectionPool


class Database:

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_connection(self):
        return self.pool.get_connection()

    def execute(self, sql):
        try:
            con = self.get_connection()
            cursor = con.cursor()
            cursor.execute(sql)
            try:
                res = cursor.fetchall()
                con.commit()
                return res
            except:
                con.commit()
                return con.insert_id()
        except Exception as e:
            raise e
