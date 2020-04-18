from utils import get_error, get_hash, check_id, check_all_parameters, check_for_null
import json
from datetime import datetime


class Pupil():
    def __init__(self, database):
        self.db = database

    def register(self, data):
        # check all fields
        if not check_all_parameters(data, ['id', 'name', 'surname', 'surname', 'school_id',
                                           'password', 'email', 'class']):
            return json.dumps({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL

        data['patronymic'] = check_for_null(json, 'patronymic')
        data['phone'] = check_for_null(json, 'phone')
        data['birth_date'] = check_for_null(json, 'birth_date')

        # hash password
        data['password'] = get_hash(json['password'])

        # try to add to db
        try:
            sql = "INSERT INTO pupils (student_id,name, surname, patronymic, class, email, phone, birth_date, school_id, password) " \
                  "VALUES ('%s','%s', '%s', %s, '%s', '%s', %s, %s, '%s', '%s');" % (
                      data['id'], data['name'], data['surname'],
                      data['patronymic'], data['class'],
                      data['email'], data['phone'],
                      data['birth_date'], data['school_id'],
                      data['password'])
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
            sql = "SELECT * FROM pupils WHERE email='%s' AND password='%s';" % (data['login'], data['password'])
            res = self.db.execute(sql)
            if len(res) < 1:
                return "no", 400
            return json.dumps({"id": res[0][0]}), 200
        except Exception as e:
            return get_error(e)

    def get_info(self, id):
        try:
            sql = "SELECT *, YEAR(CURDATE()) - YEAR(birth_date) - If(Month(birth_date)<Month(CURDate()),0,If(Month" \
                  "(birth_date)>Month(CURDate()),1,If(Day(birth_date)>Day(CURDate()),1,0))) AS age, AVG(mark) " \
                  " FROM pupils p INNER JOIN schools ON schools.code = p.school_id INNER JOIN answers ON " \
                  "p.student_id = answers.student_id WHERE p.student_id='%s' GROUP BY answers.student_id;" % id
            res = self.db.execute(sql)
            print(res)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено учня в базі даних"}), 400
            res = res[0]
            print(len(res))
            return json.dumps({
                "name": res[1],
                "surname": res[2],
                "patronymic": "" if res[3] is None else res[3],
                "email": res[5],
                "phone": "" if res[6] is None else res[6],
                "class": res[4],
                "birthdate": "" if res[7] is None else res[7].strftime("%Y.%m.%d %H:%M"),
                "age": res[27],
                "schoolid": res[9],
                "schoolname": res[12],
                "notes": "" if res[8] is None else res[8],
                "avg": "-" if res[28] is None else float(res[28])
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

    def get_answer(self, data):
        try:
            if not check_all_parameters(data, ['pupil_id', 'task_id']):
                return json.dumps({"error": "Недостатньо данних"}), 400

            sql = "SELECT * FROM answers WHERE student_id='%s' AND task_id='%s';" % (data['pupil_id'], data['task_id'])
            res = self.db.execute(sql)
            if len(res) < 1:
                result = {
                    "has": False
                }
            else:
                print(res)
                result = {
                    "has": True,
                    "id": res[0][0],
                    "text": res[0][1],
                    "hyperlink": "" if res[0][4] is None else res[0][4],
                    "response": "" if res[0][5] is None else res[0][5],
                    "mark": "" if res[0][6] is None else res[0][6],
                    "notes": "" if res[0][7] is None else res[0][7]
                }
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def submit_answer(self, data):
        try:
            if not check_all_parameters(data, ['pupil_id', 'text', 'id']):
                return json.dumps({"error": "Недостатньо данних"}), 400

            data['hyperlink'] = check_for_null(data, 'hyperlink')

            sql = "INSERT INTO answers (text, student_id, task_id, hyperlink) VALUES ('%s', '%s', '%s', %s) " \
                  "ON DUPLICATE KEY UPDATE text='%s', hyperlink=%s;" % (data['text'], data['pupil_id'], data['id'],
                                                                        data['hyperlink'], data['text'],
                                                                        data['hyperlink'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def add_olimpiad(self, data):
        if not check_all_parameters(data, ['student_id', 'olimpiad_id']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        try:
            sql = "INSERT INTO compete (olimp_id, student_id) VALUES ('%s', '%s');" % (
                data['olimpiad_id'], data['student_id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def add_subject(self, data):
        if not check_all_parameters(data, ['student_id', 'sub_id']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        try:
            sql = "INSERT INTO studying (subject_id, student_id) VALUES ('%s', '%s');" % (
                data['sub_id'], data['student_id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def get_avarage_pupil(self, id):
        try:
            sql = "SELECT AVG(mark) FROM answers WHERE student_id='%s' GROUP BY student_id" % id
            res = self.db.execute(sql)
            print(res)
            return json.dumps({"data": float(res[0][0])}), 200
        except Exception as e:
            return get_error(e)

    def delete(self, id):
        try:
            sql = "DELETE FROM pupils WHERE student_id='%s';" % id
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def delete_sub(self, data):
        try:
            sql = "DELETE FROM studying WHERE student_id='%s' AND subject_id='%s';" % (data['student_id'], data['sub_id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def delete_olimp(self, data):
        try:
            sql = "DELETE FROM compete WHERE student_id='%s' AND olimp_id='%s';" % (data['student_id'], data['olimp_id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)
