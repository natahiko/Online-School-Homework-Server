import os
from flask import Flask
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
user = User(app.database)

@app.route('/')
def hello_world():
    return user.addUser()

if __name__ == '__main__':
    app.run(debug=True)
