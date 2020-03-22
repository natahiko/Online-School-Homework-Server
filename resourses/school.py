from flask import jsonify
from utils import get_error
from utils import get_hash
import json
import random


class School():

    def __init__(self, database):
        self.db = database

    def add(self, data):
        # check all fields
        if ((not 'cityid' in data) or (not 'name' in data) or (not 'street' in data) or
                (not 'house' in data) or (not 'phone' in data)):
            return jsonify({"error": "Недостатньо данних"}), 400

        # check fields that can be NULL
        if not 'notes' in data:
            data['notes'] = 'NULL'
        else:
            data['notes'] = "'" + data['notes'] + "'"
        if not 'region' in data:
            data['region'] = 'NULL'
        else:
            data['region'] = "'" + data['region'] + "'"

        # generate school code
        code = None
        while code is None:
            arr = [str(random.randint(0, 9)) for _ in range(10)]
            code = "".join(arr)
            print(code)
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
