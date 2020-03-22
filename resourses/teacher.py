from flask import jsonify
from utils import get_error
from utils import get_hash
import json


class Teacher():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if ((not 'id' in json) or (not 'name' in json) or (not 'surname' in json) or (not 'email' in json) or
                (not 'school_id' in json) or (not 'password' in json) or (not 'education' in json)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400
        if (not 'phd' in json):
            json['phd'] = False
        # check fields that can be NULL
        if not 'patronymic' in json:
            json['patronymic'] = 'NULL'
        else:
            json['patronymic'] = "'" + json['patronymic'] + "'"
        if not 'phone' in json:
            json['phone'] = 'NULL'
        else:
            json['phone'] = "'" + json['phone'] + "'"

        # hash password
        json['password'] = get_hash(json['password'])

        # try to add to db
        try:
            sql = "INSERT INTO teachers (teacher_id, name, surname, patronymic, phd, email, phone, school_id, education, password) " \
                  "VALUES ('%s', '%s','%s', %s, '%s', '%s', %s, '%s', '%s','%s');" % (
                  json['id'], json['name'], json['surname'],
                  json['patronymic'], json['phd'],
                  json['email'], json['phone'],
                  json['school_id'], json['education'],
                  json['password'])
            self.db.execute(sql)
        except Exception as e:
            return get_error(e, 1)
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
            sql = "SELECT * FROM teachers WHERE email='%s' AND password='%s'" % (data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id": res[0][0]}), 200
        except Exception as e:
            return get_error(e)

    def get_info(self, id):
        try:
            sql = "SELECT name, surname, patronymic, email, phone, education, phd, notes" \
                  " FROM teachers WHERE teacher_id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"err": "Не знайдено вчителя в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "name": res[0],
                "surname": res[1],
                "pathronymic": "" if res[2] is None else res[2],
                "email": res[3],
                "phone": "" if res[4] is None else res[4],
                "education": res[5],
                "phd": res[6],
                "notes": "" if res[7] is None else res[7],
            }), 200
        except Exception as e:
            return get_error(e)
