from flask import jsonify
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
            res = self.db.execute("SELECT * FROM teachers WHERE teacher_id='%s';" % code)
            if len(res) > 0:
                code = None

        # try to add to db
        try:
            sql = "INSERT INTO subjects (subject_id, title, class_num, notes, teacher_id) " \
                  "VALUES ('%s', '%s','%s', %s, '%s');" % (code, data['title'], data['class_num'], data['notes'],
                                                           data['teacher_id'])
            self.db.execute(sql)
            return json.dumps({"code": code}), 200
        except Exception as e:
            return get_error(e)

    def get_teacher_subjects(self, teacher_id):
        try:
            sql = "SELECT * FROM subjects WHERE teacher_id='%s' ORDER BY title" % teacher_id
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