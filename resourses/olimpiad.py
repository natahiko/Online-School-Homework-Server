from datetime import datetime
from utils import get_error, check_parameter, check_for_null, check_all_parameters
import json
import random


class Olimpiad():

    def __init__(self, database):
        self.db = database

    def get_teacher_olympiads(self, id):
        try:
            sql = "SELECT * FROM olimpiads WHERE teach_id='%s' ORDER BY title" % id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "title": i[1],
                    "con_id": i[3],
                    "notes": "" if i[6] is None else i[6],
                    "discipline": i[4],
                    "class_num": i[5]
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def delete_olimp(self, id):
        try:
            sql = "DELETE FROM olimpiads WHERE olimp_id='%s'" % id
            res = self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def add_olimp(self, data):
        # check all fields
        if not check_all_parameters(data, ['title', 'discipline', 'teacher_id']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        # check fields that can be NULL
        data['notes'] = check_for_null(data, 'notes')
        data['class_num'] = check_for_null(data, 'class_num')
        # generate code
        code = None
        while code is None:
            arr = [str(random.randint(0, 9)) for _ in range(10)]
            code = "".join(arr)
            res = self.db.execute("SELECT * FROM olimpiads WHERE olimp_id='%s';" % code)
            if len(res) > 0:
                code = None

        if not check_parameter(data, 'con_id'):
            sql = "INSERT INTO competition (name_id, ev_date, place, stage, notes) " \
                  "VALUES ('%s', '%s','%s', '%s', %s);" % (
                  data['name_id'], datetime.strptime(data['ev-date'], "%Y-%m-%dT%H:%M"),
                  data['place'], data['stage'], data['con_notes'])
            res0 = self.db.execute(sql)
            data['con_id'] = res0
        # try to add to db
        try:
            sql = "INSERT INTO olimpiads (olimp_id, title, teach_id, con_id, discipline, class_num, notes) " \
                  "VALUES ('%s', '%s','%s','%s','%s', %s, %s);" % (code, data['title'], data['teacher_id'],
                                                                   data['con_id'], data['discipline'],
                                                                   data['class_num'], data['notes'])
            self.db.execute(sql)
            return json.dumps({"code": code}), 200
        except Exception as e:
            return get_error(e)

    def get_competition_names(self):
        try:
            sql = "SELECT * FROM competition_names"
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "name": i[1]
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def edit_olimp(self, data):
        if not check_all_parameters(data, ['title', 'discipline']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        # check fields that can be NULL
        data['notes'] = check_for_null(data, 'notes')
        data['class_num'] = check_for_null(data, 'class_num')

        # try to add to db
        try:
            sql = "UPDATE olimpiads SET title='%s', discipline='%s', class_num=%s, notes=%s" \
                  " WHERE olimp_id='%s';" % (
                  data['title'], data['discipline'], data['class_num'], data['notes'], data['id'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)
