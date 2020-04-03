from flask import jsonify
from utils import get_error, get_hash, check_id, check_all_parameters, check_for_null
import json


class Pupil():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if not check_all_parameters(json, ['id', 'name', 'surname', 'surname', 'school_id', 'password', 'email', 'class']):
            return jsonify({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL

        json['patronymic'] = check_for_null(json, 'patronymic')
        json['phone'] = check_for_null(json, 'phone')
        json['birth_date'] = check_for_null(json, 'birth_date')

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
        if not check_all_parameters(data, ['login', 'password']):
            return jsonify({ "error": "Недостатньо данних"}), 400
        # hash password
        data['password'] = get_hash(data['password'])
        try:
            sql = "SELECT * FROM pupils WHERE email='%s' AND password='%s';" % (data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id": res[0][0]}), 200
        except Exception as e:
            return get_error(e)

    def get_info(self, id):
        try:
            sql = "SELECT * FROM pupils INNER JOIN schools ON schools.code = pupils.school_id WHERE student_id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено учня в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "name": res[1],
                "surname": res[2],
                "patronymic": "" if res[3] is None else res[3],
                "email": res[5],
                "phone": "" if res[6] is None else res[6],
                "class": res[4],
                "birthdate": "" if res[7] is None else res[7],
                "schoolid": res[9],
                "schoolname": res[12],
                "notes": "" if res[8] is None else res[8]
            }), 200
        except Exception as e:
            return get_error(e)

    def edit_info(self, data):
        if not check_id(data):
            return json.dumps({"error": "Некоректні дані (відсутнє id)"}), 400
        try:
            sql = "UPDATE pupils SET name='%s', surname='%s', patronymic='%s', email='%s', phone='%s'," \
                  " class='%s', notes='%s' WHERE student_id=%s;" % (data['name'], data['surname'], data['patronymic'],
                                                                    data['email'], data['phone'], data['class'],
                                                                    data['notes'], data['id'])
            res = self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return json.dumps({"data": True}), 200
