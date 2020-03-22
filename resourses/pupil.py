from flask import jsonify
from utils import get_error
from utils import get_hash
import json


class Pupil():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if ((not 'id' in json) or (not 'name' in json) or (not 'surname' in json) or (not 'class' in json) or (
        not 'email' in json) or
                (not 'school_id' in json) or (not 'password' in json)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400

        # check fields that can be NULL
        if not 'patronymic' in json:
            json['patronymic'] = 'NULL'
        else:
            json['patronymic'] = "'" + json['patronymic'] + "'"
        if not 'phone' in json:
            json['phone'] = 'NULL'
        else:
            json['phone'] = "'" + json['phone'] + "'"
        if not 'birth_date' in json:
            json['birth_date'] = 'NULL'
        else:
            json['birth_date'] = "'" + json['birth_date'] + "'"

        # hash password
        json['password'] = get_hash(json['password'])

        # try to add to db
        try:
            sql = "INSERT INTO pupils (student_id,name, surname, patronymic, class, email, phone, birth_date, school_id, password) " \
                  "VALUES ('%s','%s', '%s', %s, '%s', '%s', %s, %s, '%s', '%s');" % (
                  json['id'], json['name'], json['surname'],
                  json['patronymic'], json['class'],
                  json['email'], json['phone'],
                  json['birth_date'], json['school_id'],
                  json['password'])
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
            sql = "SELECT * FROM pupils WHERE email='%s' AND password='%s';" % (data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id":res[0][0]}), 200
        except Exception as e:
            return get_error(e)
