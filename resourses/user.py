

class User():
    def __init__(self, database):
        self.db = database

    def addUser(self):
        con = self.db.get_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO pupils (name, surname, class, email, school_id) VALUES ('nata','shkarovska',11,'n.shkarow@gmail.com','0000000000')")
        # result = cursor.fetchall()
        con.commit()
        return "Yes"

