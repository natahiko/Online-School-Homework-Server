from flask import jsonify
from utils import get_error
from utils import get_hash
import json


class Admin():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if (('login' not in json) or ('email' not in json) or ('password' not in json)
            or ('name' not in json) or ('surname' not in json)):
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
            sql = "INSERT INTO admins (login, email, password, notes, name, surname) " \
                  "VALUES ('%s','%s', '%s', %s);" % (json['login'], json['email'],
                                                     json['password'], json['notes'],
                                                     json['name'], json['surname'])
            self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return "ok", 201

    def login(self, data):
        # check all fields
        if ((not 'login' in data) or (not 'password' in data)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400
        # hash password
        data['password'] = get_hash(data['password'])
        try:
            sql = "SELECT * FROM admins WHERE (email='%s' OR login='%s') AND password='%s';" % (
                data['login'], data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id":res[0][0]}), 200
        except Exception as e:
            return get_error(e)
