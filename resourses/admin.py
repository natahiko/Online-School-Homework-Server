from flask import jsonify
from utils import get_error
from utils import get_hash


class Admin():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if (('login' not in json) or ('email' not in json) or ('password' not in json)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400

        # check fields that can be NULL
        if not 'notes' in json:
            json['notes'] = 'NULL'
        else:
            json['notes'] = "'" + json['notes'] + "'"

        # hash password
        json['password'] = get_hash(json['password'])

        # try to add to db
        try:
            sql = "INSERT INTO admins (login, email, password, notes) " \
                  "VALUES ('%s','%s', '%s', %s);" % (json['login'], json['email'],
                                                     json['password'], json['notes'])
            self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return "ok", 201

    def login(self, json):
        # check all fields
        if ((not 'login' in json) or (not 'password' in json)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400
        # hash password
        json['password'] = get_hash(json['password'])
        try:
            sql = "SELECT * FROM admin WHERE (email='%s' OR login='%s') AND password='%s';" % (
                json['login'], json['login'], json['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return "ok", 200
        except Exception as e:
            return get_error(e)
