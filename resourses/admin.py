from utils import get_error, get_hash, check_id, check_all_parameters, check_for_null
import json


class Admin():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if not check_all_parameters(json, ['login', 'name', 'surname', 'password', 'email']):
            return json.dumps({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL
        json['notes'] = check_for_null(json, 'notes')
        # hash password
        json['password'] = get_hash(json['password'])

        # try to add to db
        try:
            sql = "INSERT INTO admins (login, email, password, notes, name, surname) " \
                  "VALUES ('%s','%s', '%s', %s, '%s', '%s');" % (json['login'], json['email'],
                                                                 json['password'], json['notes'],
                                                                 json['name'], json['surname'])
            self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return "ok", 201

    def login(self, data):
        # check all fields
        if not check_all_parameters(data, ['login', 'password']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        # hash password
        data['password'] = get_hash(data['password'])
        try:
            sql = "SELECT * FROM admins WHERE (email='%s' OR login='%s') AND password='%s';" % (
                data['login'], data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id": res[0][0]}), 200
        except Exception as e:
            return get_error(e)

    def get_info(self, id):
        try:
            sql = "SELECT * FROM admins WHERE id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено учня в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "login": res[1],
                "email": res[2],
                "notes": "" if res[4] is None else res[4],
                "name": res[5],
                "surname": res[6]
            }), 200
        except Exception as e:
            return get_error(e)

    def edit_info(self, data):
        if not check_id(data):
            return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400
        try:
            sql = "UPDATE admins SET name='%s', surname='%s', email='%s', notes='%s' " \
                  "WHERE id=%s;" % (data['name'], data['surname'], data['email'], data['notes'], data['id'])

            res = self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return json.dumps({"data": True}), 200
