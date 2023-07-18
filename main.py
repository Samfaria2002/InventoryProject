from flask import Flask
from flask_restful import Api
from extensions import db, migrate
from routes.agBp import agBp
from model.agModel import Desktop, Agenda
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desktop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'agenda':        'sqlite:///agenda.db',
    'desktop':      'sqlite:///desktop.db'
}


@app.route('/agendac')
def agenda_list():
    db.create_all(Agenda.__tablename__)

@app.route('/desktopc')
def desk_list():
    db.create_all(Desktop.__tablename__)


db.init_app(app)
migrate.init_app(app)
app.register_blueprint(agBp)

if __name__ == '__main__':
    app.run()