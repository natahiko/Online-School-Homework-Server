from mysql.connector.pooling import MySQLConnectionPool


class Database:

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_connection(self):
        return self.pool.get_connection()

    def execute(self, sql, multi=False):
        try:
            con = self.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, multi=multi)
            try:
                res = cursor.fetchall()
                con.commit()
                return res
            except Exception as e1:
                con.commit()
                return cursor.lastrowid
        except Exception as e:
            print(e)
            raise e
        finally:
            con.close()
