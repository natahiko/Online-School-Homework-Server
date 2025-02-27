from datetime import datetime
from utils import get_error, check_parameter, check_for_null, check_all_parameters
import json
import random


class Subject():

    def __init__(self, database):
        self.db = database

    def add(self, data):
        # check all fields
        if not check_all_parameters(data, ['title', 'class_num', 'teacher_id']):
            return json.dumps({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL
        data['notes'] = check_for_null(data, 'notes')

        # generate school code
        code = None
        while code is None:
            arr = [str(random.randint(0, 9)) for _ in range(10)]
            code = "".join(arr)
            res = self.db.execute("SELECT * FROM subjects WHERE sub_id='%s';" % code)
            if len(res) > 0:
                code = None

        # try to add to db
        try:
            sql = "INSERT INTO subjects (sub_id, title, class_num, notes, teacher_id) " \
                  "VALUES ('%s', '%s','%s', %s, '%s');" % (code, data['title'], data['class_num'], data['notes'],
                                                           data['teacher_id'])
            self.db.execute(sql)
            return json.dumps({"code": code}), 200
        except Exception as e:
            return get_error(e)

    def get_teacher_subjects(self, teacher_id):
        try:
            sql = "SELECT * FROM subjects WHERE teacher_id='%s' ORDER BY title;" % teacher_id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "title": i[1],
                    "class_num": i[2],
                    "notes": i[3]
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def get_subjects_hometasks(self, id):
        try:
            sql = "SELECT * FROM hometasks WHERE subject_id='%s' ORDER BY deadline;" % id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "title": i[1],
                    "content": "" if i[2] is None else i[2],
                    "deadline": i[3].strftime("%Y.%m.%d %H:%M"),
                    "active": datetime.now() > i[3],
                    "notes": "" if i[5] is None else i[5],
                    "remaining_time": str(abs(datetime.now() - i[3]))
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def get_pupil_subjects(self, pupil_id):
        try:
            sql = "SELECT * FROM subjects WHERE sub_id IN (SELECT subject_id FROM studying WHERE student_id='%s') " \
                  "ORDER BY title;" % pupil_id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "title": i[1],
                    "class_num": i[2],
                    "notes": i[3]
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def get_hometask_info(self, id):
        try:
            sql = "SELECT * FROM hometasks WHERE hw_id=%s;" % id
            res1 = self.db.execute(sql)[0]
            sql = "SELECT hyperlink FROM hometask_hyperlinks WHERE homework_id=%s;" % id
            res2 = self.db.execute(sql)
            links = []
            if res2 is not None:
                for i in res2:
                    links.append(i[0])
            date = str(res1[3])[:-3].replace(" ", 'T')
            result = {
                "hw_title": res1[1],
                "content": res1[2],
                "deadline": res1[3].strftime("%Y.%m.%d %H:%M"),
                "deadline_iso": date,
                "subject_id": res1[4],
                "active": datetime.now() > res1[3],
                "notes": "" if res1[5] is None else res1[5],
                "remaining_time": str(abs(datetime.now() - res1[3])),
                "hyperlinks": links
            }
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def add_hometask(self, data):
        if not check_all_parameters(data, ['title', 'id', 'content', 'deadline']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "INSERT INTO hometasks (hw_title, content, deadline, notes, subject_id) VALUES ('%s','%s', '%s'," \
                  " %s,'%s');" \
                  % (data['title'], data['content'], datetime.strptime(data['deadline'], "%Y-%m-%dT%H:%M"),
                     data['notes'], data['id'])
            res = self.db.execute(sql)
            for link in data['hyperlinks']:
                sql = "INSERT INTO hometask_hyperlinks (hyperlink, homework_id) VALUES ('%s', '%s')" % (link, res)
                self.db.execute(sql)
            return json.dumps({"hw_id": res}), 200
        except Exception as e:
            return get_error(e)

    def edit_hometask(self, data):
        if not check_all_parameters(data, ['hw_title', 'id', 'content', 'deadline']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "UPDATE hometasks SET hw_title='%s', content='%s', deadline='%s', notes=%s WHERE hw_id='%s';" \
                  % (data['hw_title'], data['content'], datetime.strptime(data['deadline'], "%Y-%m-%dT%H:%M"),
                     data['notes'], data['id'])
            self.db.execute(sql)
            sql = "DELETE FROM hometask_hyperlinks WHERE homework_id='%s';" % data['id']
            self.db.execute(sql)
            for link in data['hyperlinks']:
                sql = "INSERT INTO hometask_hyperlinks (hyperlink, homework_id) VALUES ('%s', '%s'); " % (
                    link, data['id'])
                self.db.execute(sql)
            return json.dumps({"hw_id": data['id']}), 200
        except Exception as e:
            return get_error(e)

    def delete_sub(self, id):
        try:
            sql = "DELETE FROM subjects WHERE sub_id='%s';" % id
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def delete_hometask(self, id):
        try:
            sql = "DELETE FROM hometasks WHERE hw_id='%s';" % (
                id)
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def edit(self, data):
        if not check_all_parameters(data, ['title', 'id', 'class_num']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "UPDATE subjects SET title='%s', class_num='%s', notes=%s WHERE sub_id='%s';" % (data['title'],
                                                                                                   data['class_num'],
                                                                                                   data['notes'],
                                                                                                   data['id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def get_all_pupils(self, id):
        print(id)
        try:
            sql = "SELECT p.student_id, p.name, p.surname, p.patronymic, p.birth_date, p.class, p.email, p.notes," \
                  " p.phone, school_id, schools.name, YEAR(CURDATE()) - YEAR(birth_date) - If(Month(birth_date)<Month" \
                  "(CURDate()),0,If(Month(birth_date)>Month(CURDate()),1,If(Day(birth_date)>Day(CURDate()),1,0))) AS age, AVG(mark)  " \
                  "FROM pupils p INNER JOIN studying on studying.student_id = p.student_id INNER JOIN schools" \
                  " ON p.school_id = schools.code LEFT OUTER JOIN answers ON " \
                  "p.student_id = answers.student_id WHERE subject_id='%s' GROUP BY p.student_id" % id
            res = self.db.execute(sql)
            print(res)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "name": i[2] + " " + i[1] + " " + ("" if i[3] is None else i[3]),
                    "birth_date": i[4].strftime("%Y.%m.%d %H:%M"),
                    "age": i[11],
                    "class": i[5],
                    "email": i[6],
                    "notes": i[7],
                    "phone": i[8],
                    "school_id": i[9],
                    "schoolname": i[10],
                    "avg": "-" if i[12] is None else float(i[12])
                })
                print(result)
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def get_all_pupils_learn(self, data):
        surname = check_for_null(data, 'surname')
        if surname == 'NULL':
            return json.dumps({"error": "Недостатньо данних"}), 400
        try:
            sql = "SELECT student_id, surname, name, email, class, school_id FROM pupils WHERE NOT EXISTS (SELECT * FROM studying AS A WHERE subject_id IN (SELECT " \
                  "sub_id FROM subjects WHERE teacher_id IN (SELECT teacher_id FROM teachers WHERE surname=%s)) AND " \
                  "NOT EXISTS (SELECT * FROM studying WHERE studying.student_id=pupils.student_id AND " \
                  "A.subject_id=studying.subject_id));" % surname
            res = self.db.execute(sql)
            sql2 = "SELECT teacher_id FROM teachers WHERE surname=%s;" % surname
            res2 = self.db.execute(sql2)
            if len(res2) < 1:
                return json.dumps([]), 200
            result = []
            for pupil in res:
                result.append({
                    "id": pupil[0],
                    "name": pupil[1] + " " + pupil[2],
                    "email": pupil[3],
                    "class": pupil[4],
                    "school_id": pupil[5]
                })
            print(result)
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)
