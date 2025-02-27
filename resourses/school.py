from utils import get_error, check_parameter, check_for_null, check_all_parameters
import json
import random


class School():

    def __init__(self, database):
        self.db = database

    def edit(self, data):
        if not check_all_parameters(data, ['name', 'street', 'house', 'phone', 'code']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        data['region'] = check_for_null(data, 'region')

        try:
            sql = "UPDATE schools SET name='%s',  region=%s, street='%s', house_number='%s', phone='%s', " \
                  "notes=%s WHERE code='%s';" % (data['name'], data['region'], data['street'], data['house'],
                                                 data['phone'], data['notes'], data['code'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def add(self, data):
        # check all fields
        if not check_all_parameters(data, ['cityid', 'name', 'street', 'house', 'phone']):
            return json.dumps({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL

        data['notes'] = check_for_null(data, 'notes')
        data['region'] = check_for_null(data, 'region')

        # generate school code
        code = None
        while code is None:
            arr = [str(random.randint(0, 9)) for _ in range(10)]
            code = "".join(arr)
            res = self.db.execute("SELECT code FROM schools WHERE code='%s';" % code)
            if len(res) > 0:
                code = None

        # try to add to db
        try:
            sql = "INSERT INTO schools (code, name, city, region, street, house_number, phone, notes) " \
                  "VALUES ('%s', '%s','%s', %s, '%s', '%s', '%s', %s);" % (code, data['name'],
                                                                           data['cityid'], data['region'],
                                                                           data['street'], data['house'],
                                                                           data['phone'], data['notes'])
            self.db.execute(sql)
            return json.dumps({"code": code}), 200
        except Exception as e:
            return get_error(e)

    def get_info(self, id: str):
        try:
            sql = "SELECT schools.name, region, street, house_number, schools.phone, schools.notes, cities.city, " \
                  "COUNT(pupils.student_id) FROM schools INNER JOIN cities ON schools.city = cities.id " \
                  "INNER JOIN pupils ON schools.code = pupils.school_id WHERE code='%s' GROUP BY pupils.school_id ;" % id
            res = self.db.execute(sql)[0]
            print(res)
            if len(res) < 1:
                return json.dumps({"err": "Не знайдено школу в базі даних"}), 400
            return json.dumps({
                "name": res[0],
                "city": res[6],
                "region": "" if res[1] is None else res[1],
                "street": res[2],
                "house": res[3],
                "phone": res[4],
                "notes": "" if res[5] is None else res[5],
                "school_pupils_num": res[7]
            }), 200
        except Exception as e:
            return get_error(e)

    def get_all_schools(self):
        try:
            sql = "SELECT * FROM schools INNER JOIN cities ON schools.city = cities.id ORDER BY name;"
            res = self.db.execute(sql)
            result = []
            for i in res:
                result.append({
                    "code": i[0],
                    "name": i[1],
                    "address": i[9] + ", " + ("" if (i[3] is None or i[3] == "") else (i[3] + ", ")) + i[4] + " " + i[
                        5],
                    "phone": i[6],
                    "region": "" if i[3] is None else i[3],
                    "street": i[4],
                    "house": i[5]
                })
            return json.dumps(result), 200
        except Exception as e:
            return get_error(e)

    def delete_school(self, id):
        try:
            sql = "DELETE FROM schools WHERE code='%s';" % id
            res = self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)
