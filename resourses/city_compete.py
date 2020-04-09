import json

from utils import get_error, check_for_null, check_parameter, check_all_parameters


class CityCompete():

    def __init__(self, database):
        self.db = database

    def get_competition_names_and_stages(self):
        try:
            sql = "SELECT * FROM competition_names"
            res = self.db.execute(sql)
            names = []
            for i in res:
                names.append({
                    "id": i[0],
                    "name": i[1]
                })
            sql = "SELECT * FROM stages"
            res = self.db.execute(sql)
            stages = []
            for i in res:
                stages.append({
                    "id": i[0],
                    "name": i[1]
                })
            return json.dumps({
                "names": names,
                "stages": stages
            }), 200
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

    def add_competition(self, data):
        if not check_all_parameters(data, ['stage_id', 'name_id', 'date', 'place']):
            return json.dumps({"error": "Недостатньо данних"}), 400
        data['notes'] = check_for_null(data, 'notes')
        try:
            sql = "INSERT INTO competition (name_id, ev_date, place, stage, notes) VALUE ('%s','%s','%s','%s',%s)" % \
                  (data['name_id'], data['date'], data['place'], data['stage_id'], data['notes'])
            self.db.execute(sql)
            return json.dumps({"data": True}), 200
        except Exception as e:
            return get_error(e)

    def get_cities(self):
        try:
            res = self.db.execute("SELECT id, city FROM cities;")
            return json.dumps(res), 200
        except Exception as e:
            return get_error(e)

    def add_city(self, data):
        if check_parameter(data, 'city'):
            return json.dumps({"error": "Недостатньо данних"}), 400
        notes = check_for_null(data, 'notes')
        # try to add to db
        try:
            sql = "INSERT INTO cities (city, notes) VALUES ('%s','%s');" % (data['city'], notes)
            self.db.execute(sql)
            return {}, 200
        except Exception as e:
            return get_error(e)
