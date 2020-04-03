from flask import jsonify
from utils import get_error, check_for_null, check_parameter
import json


class City():

    def __init__(self, database):
        self.db = database

    def get_cities(self):
        try:
            res = self.db.execute("SELECT id, city FROM cities;")
            return json.dumps(res), 200
        except Exception as e:
            return get_error(e)

    def add_city(self, data):
        if check_parameter(data, 'city'):
            return jsonify({"error": "Недостатньо данних"}), 400
        notes = check_for_null(data, 'notes')
        # try to add to db
        try:
            sql = "INSERT INTO cities (city, notes) VALUES ('%s','%s');" % (data['city'], notes)
            self.db.execute(sql)
            return {}, 200
        except Exception as e:
            return get_error(e)
