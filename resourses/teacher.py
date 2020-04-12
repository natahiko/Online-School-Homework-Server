from utils import get_error, get_hash, check_id, check_for_null, check_all_parameters
import json


class Teacher():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if not check_all_parameters(json, ['id', 'name', 'surname', 'email', 'school_id', 'password', 'education']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        if (not 'phd' in json):
            json['phd'] = False
        # check fields that can be NULL
        json['patronymic'] = check_for_null(json, 'patronymic')
        json['phone'] = check_for_null(json, 'phone')

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
        if not check_all_parameters(data, ['login', 'password']):
            return json.dumps({"error": "Недостатньо данних"}), 400

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

    def get_info(self, id: str):
        try:
            sql = "SELECT * FROM teachers INNER JOIN schools ON schools.code = teachers.school_id WHERE teacher_id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено вчителя в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "name": res[1],
                "surname": res[2],
                "patronymic": "" if res[3] is None else res[3],
                "email": res[4],
                "phone": "" if res[5] is None else res[5],
                "education": res[6],
                "phd": res[7],
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
            sql = "UPDATE teachers SET name='%s', surname='%s', patronymic='%s', email='%s', phone='%s'," \
                  " education='%s', phd='%s', notes='%s' WHERE teacher_id=%s;" % (data['name'], data['surname'],
                                                                                  data['patronymic'], data['email'],
                                                                                  data['phone'], data['education'],
                                                                                  data['phd'], data['notes'],
                                                                                  data['id'])
            res = self.db.execute(sql)
        except Exception as e:
            return get_error(e)
        return json.dumps({"data": True}), 200

    def get_all_answers(self, id):
        try:
            sql = "SELECT answer_id, text, hyperlink, response, mark, p.name, p.surname, p.class FROM answers " \
                  "INNER JOIN pupils p ON answers.student_id = p.student_id WHERE task_id='%s';" % id
            res = self.db.execute(sql)
            print(res)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "text": i[1],
                    "hyperlink": i[2],
                    "response": "" if i[3] is None else i[3],
                    "mark": "" if i[4] is None else i[4],
                    "name": i[5] + ' ' + i[6] + ' (' + str(i[7]) + ')'
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def change_answer(self, data):
        data['response'] = check_for_null(data, 'response')
        data['mark'] = check_for_null(data, 'mark')

        try:
            sql = "UPDATE answers SET mark=%s, response=%s WHERE answer_id='%s';" % (
                data['mark'], data['response'], data['id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def get_olimp_teacher_іnfo(self, id):
        try:
            sql = "SELECT * FROM teachers INNER JOIN schools ON schools.code = teachers.school_id INNER JOIN olimpiads " \
                  "ON teachers.teacher_id = olimpiads.teach_id WHERE olimp_id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено вчителя в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "name": res[1],
                "surname": res[2],
                "patronymic": "" if res[3] is None else res[3],
                "email": res[4],
                "phone": "" if res[5] is None else res[5],
                "education": res[6],
                "phd": res[7],
                "schoolid": res[9],
                "schoolname": res[12],
                "notes": "" if res[8] is None else res[8]
            }), 200
        except Exception as e:
            return get_error(e)

    def get_subject_teacher_іnfo(self, id):
        try:
            sql = "SELECT * FROM teachers INNER JOIN schools ON schools.code = teachers.school_id INNER JOIN subjects s " \
                  "on teachers.teacher_id = s.teacher_id WHERE sub_id='%s';" % id
            res = self.db.execute(sql)
            if len(res) < 1:
                return json.dumps({"error": "Не знайдено вчителя в базі даних"}), 400
            res = res[0]
            return json.dumps({
                "name": res[1],
                "surname": res[2],
                "patronymic": "" if res[3] is None else res[3],
                "email": res[4],
                "phone": "" if res[5] is None else res[5],
                "education": res[6],
                "phd": res[7],
                "schoolid": res[9],
                "schoolname": res[12],
                "notes": "" if res[8] is None else res[8]
            }), 200
        except Exception as e:
            return get_error(e)
