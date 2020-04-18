import json
import random
from datetime import datetime

from utils import get_error, check_parameter, check_for_null, check_all_parameters


class Olimpiad():

    def __init__(self, database):
        self.db = database

    def get_teacher_olympiads(self, id):
        try:
            sql = "SELECT * FROM olimpiads INNER JOIN competition ON olimpiads.con_id = competition.con_id " \
                  "INNER JOIN competition_names ON competition.name_id = competition_names.name_id " \
                  "WHERE teach_id='%s' ORDER BY title;" % id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "title": i[1],
                    "con_id": i[3],
                    "notes": "" if i[6] is None else i[6],
                    "discipline": i[4],
                    "class_num": i[5],
                    "ev_date": i[9].strftime("%Y.%m.%d %H:%M"),
                    "place": i[10],
                    "stage": i[11],
                    "name": i[14],
                    "remain_time": str(abs(datetime.now() - i[9]))
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

    def get_pupil_olimpiad(self, id):
        try:
            sql = "SELECT * FROM compete INNER JOIN olimpiads ON compete.olimp_id = olimpiads.olimp_id " \
                  "INNER JOIN competition ON olimpiads.con_id = competition.con_id INNER JOIN competition_names " \
                  "ON competition_names.name_id=competition.name_id " \
                  "WHERE student_id='%s' ORDER BY title;" % id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "olimp_id": i[0],
                    "title": i[3],
                    "discipline": i[5],
                    "class_num": "" if i[6] is None else i[6],
                    "notes": "" if i[7] is None else i[7],
                    "ev_date": i[11].strftime("%Y.%m.%d %H:%M"),
                    "place": i[12],
                    "stage": i[13],
                    "name": i[16],
                    "remain_time": str(abs(datetime.now() - i[11]))
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def get_tasks_and_sources(self, id):
        try:
            sql = "SELECT * FROM competition_tasks WHERE olimp_id='%s' ORDER BY deadline;" % id
            res = self.db.execute(sql)
            tasks = []
            for i in res:
                sql0 = "SELECT * FROM tasks_hyperlinks WHERE task_id='%s';" % i[0]
                res0 = self.db.execute(sql0)
                print(res0)
                links = []
                for link in res0:
                    links.append(link[1])
                date = str(i[4])[:-3].replace(" ", 'T')
                tasks.append({
                    "id": i[0],
                    "task_caption": i[1],
                    "deadline": i[4].strftime("%Y.%m.%d %H:%M"),
                    "deadline_iso": date,
                    "content": i[2],
                    "notes": "" if i[3] is None else i[3],
                    "active": datetime.now() <= i[4],
                    "hyperlinks": links,
                    "remaining_time": str(abs(datetime.now() - i[4]))
                })
            sql = "SELECT * FROM additional_sources WHERE olimp_id='%s' ORDER BY caption;" % id
            res2 = self.db.execute(sql)
            sources = []
            for i in res2:
                id0 = i[0]
                sql0 = "SELECT * FROM additional_hyperlinks WHERE source_id='%s';" % id0
                res0 = self.db.execute(sql0)
                links = []
                for link in res0:
                    links.append(link[1])
                sources.append({
                    "id": id0,
                    "caption": i[1],
                    "content": i[2],
                    "notes": "" if i[4] is None else i[4],
                    "links": links
                })
            return json.dumps({
                "tasks": tasks,
                "sources": sources
            }), 200
        except Exception as e:
            return get_error(e)

    def delete_task(self, id):
        try:
            sql = "DELETE FROM competition_tasks WHERE task_id='%s';" % id
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def add_task(self, data):
        if not check_all_parameters(data, ['source_id', 'deadline', 'content', 'task_caption']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "INSERT INTO competition_tasks (task_caption, content, notes, deadline, olimp_id) VALUES " \
                  "('%s','%s',%s,'%s','%s');" % (data['task_caption'], data['content'], data['notes'],
                                                 data['deadline'], data['source_id'])
            res = self.db.execute(sql)
            for i in data['hyperlinks']:
                sql0 = "INSERT INTO tasks_hyperlinks (link, task_id) VALUES ('%s', '%s');" % (i, res)
                self.db.execute(sql0)
            return json.dumps({"id": res}), 200
        except Exception as e:
            return get_error(e)

    def edit_task(self, data):
        if not check_all_parameters(data, ['id', 'deadline', 'content', 'task_caption']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            task_id = data['id']
            sql = "UPDATE competition_tasks SET task_caption='%s', content='%s', notes=%s, deadline='%s' WHERE " \
                  "task_id='%s';" % (data['task_caption'], data['content'], data['notes'], data['deadline'], task_id)
            self.db.execute(sql)
            sql = "DELETE FROM tasks_hyperlinks WHERE task_id='%s';" % task_id
            self.db.execute(sql)
            for i in data['hyperlinks']:
                sql0 = "INSERT INTO tasks_hyperlinks (link, task_id) VALUES ('%s', '%s');" % (i, task_id)
                self.db.execute(sql0)
            return json.dumps({"id": task_id}), 200
        except Exception as e:
            return get_error(e)

    def get_all_pupils(self, id):
        try:
            sql = "SELECT p.student_id, p.name, p.surname, p.patronymic, p.birth_date, p.class, p.email, p.notes," \
                  " p.phone, school_id, schools.name, YEAR(CURDATE()) - YEAR(birth_date) - If(Month(birth_date)<Month" \
                  "(CURDate()),0,If(Month(birth_date)>Month(CURDate()),1,If(Day(birth_date)>Day(CURDate()),1,0))) AS age, AVG(mark) " \
                  "FROM compete INNER JOIN pupils p on compete.student_id = p.student_id INNER JOIN schools" \
                  " ON p.school_id = schools.code LEFT OUTER JOIN answers ON " \
                  "p.student_id = answers.student_id WHERE compete.olimp_id='%s' GROUP BY student_id ;" % id
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "id": i[0],
                    "name": i[1] + " " + i[2] + " " + ("" if i[3] is None else i[3]),
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
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def add_additional_source(self, data):
        if not check_all_parameters(data, ['source_id', 'caption', 'content']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "INSERT INTO additional_sources (caption, content, olimp_id, notes) VALUES ('%s','%s','%s',%s);" % \
                  (data['caption'], data['content'], data['source_id'], data['notes'])
            id = self.db.execute(sql)
            for i in data['hyperlinks']:
                sql0 = "INSERT INTO additional_hyperlinks (hyperlink, source_id) VALUES ('%s', '%s');" % (i, id)
                self.db.execute(sql0)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)
