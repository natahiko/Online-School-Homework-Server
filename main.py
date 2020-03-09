import os
from flask import Flask, request
from utils import Database, ParserConfig
from resourses import *

path = os.path.dirname(os.path.abspath(__file__))

# load config with all dispatchers
config = ParserConfig(os.path.join(path, 'config', 'conf.json'))
# create application
app = Flask(__name__)

# init configuration and db
with app.app_context():
    app.configuration = config
    app.database = Database(**config['database'])

# initialise all resourses
pupil = Pupil(app.database)


@app.route('/registerpupil', methods=['POST'])
def hello_world():
    return pupil.register(request.get_json())

@app.route('/loginpupil', methods=['POST'])
def hello_world():
    return pupil.login(request.get_json())


if __name__ == '__main__':
    app.run(port=2303, debug=True)
