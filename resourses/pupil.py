from flask import jsonify
from utils import get_error


class Pupil():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if ((not 'name' in json) or (not 'surname' in json) or (not 'class' in json) or (not 'email' in json) or
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

        # try to add to db
        try:
            sql = "INSERT INTO pupils (name, surname, patronymic, class, email, phone, birth_date, school_id, password) " \
                  "VALUES ('%s', '%s', %s, '%s', '%s', %s, %s, '%s', '%s')" % (json['name'], json['surname'],
                                                                               json['patronymic'], json['class'],
                                                                               json['email'], json['phone'],
                                                                               json['birth_date'], json['school_id'],
                                                                               json['password'])
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
        try:
            sql = "SELECT * FROM pupils WHERE email='%s' AND password='%s'" % (json['login'], json['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
        except Exception as e:
            return get_error(e)
        return "ok", 201
