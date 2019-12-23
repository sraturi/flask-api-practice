from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'planets.db')

db = SQLAlchemy(app)

# script for database init destroy and seed

@app.cli.command('db_create')
def db_create():
    db.create_all()


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=2.258e23,
                     radius=1516,
                     planet_id = "qwerty",
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                         planet_type='Class K',
                         home_star='Sol',
                         mass=4.867e24,
                         planet_id = "sdfg",
                         radius=3760,
                         distance=67.24e6)

    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
                     planet_id="dfghgf",
                     radius=3959,
                     distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='Sachin',
                     last_name='Raturi',
                     email='test@test.com',
                     password='qwerty')

    db.session.add(test_user)
    db.session.commit()
    print('Database is seeded!')


@app.route('/')
def hello_world():
    return jsonify(message='jhgyfvb vyghbjn'),404



@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name, age):
    if age < 18:
        return jsonify(message= name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


# database modules 
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer,primary_key =True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = "planets"
    planet_id = Column(String,primary_key = True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)













if __name__ == '__main__':
    app.run()