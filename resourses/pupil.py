from flask import jsonify


# data = {'name': 'nabin khadka'}
#     return jsonify(data)

class Pupil():
    def __init__(self, database):
        self.db = database

    def register(self, json):
        # check all fields
        if ((not 'name' in json) or (not 'surname' in json) or (not 'class' in json) or (not 'email' in json) or
                (not 'school_id' in json)):
            return jsonify({
                "error": "Недостатньо данних"
            }), 400

        #check fields that can be NULL
        if not 'patronymic' in json:
            json['patronymic'] = 'NULL'
        else:
            json['patronymic'] = "'"+json['patronymic']+"'"
        if not 'phone' in json:
            json['phone'] = 'NULL'
        else:
            json['phone'] = "'"+json['phone']+"'"
        if not 'birth_date' in json:
            json['birth_date'] = 'NULL'
        else:
            json['birth_date'] = "'"+json['birth_date']+"'"

        # try to add to db
        try:
            sql = "INSERT INTO pupils (name, surname, patronymic, class, email, phone, birth_date, school_id) " \
                  "VALUES ('%s', '%s', %s, '%s', '%s', %s, %s, '%s')" % (json['name'], json['surname'],
                                        json['patronymic'], json['class'], json['email'], json['phone'],
                                        json['birth_date'], json['school_id'])
            self.db.execute(sql)
        except Exception as e:
            code = str(e)[:4]
            if code == '1062':
                return jsonify({
                    "error": "Користувач з такою поштою вже є в базі даних"
                }), 409
            elif code == '1452':
                return jsonify({
                    "error": "Школи з таким кодом не існує"
                }), 406
            else:
                return jsonify({
                    "error": str(e)
                }), 406
        return "ok", 201
