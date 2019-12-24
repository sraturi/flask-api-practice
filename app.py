from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required , create_access_token
from flask_mail import Mail, Message
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'planets.db')
app.config['JWT_SECRET_KEY']= 'SECRET!!' #should change it
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 1234#port from mailtrap.io
app.config['MAIL_USERNAME'] = 'from mailtrap.io'
app.config['MAIL_PASSWORD'] = 'from mailtrap.io'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt  =JWTManager(app)
mail = Mail(app)
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
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                         planet_type='Class K',
                         home_star='Sol',
                         mass=4.867e24,
                         radius=3760,
                         distance=67.24e6)

    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
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


@app.route('/planets',methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register',methods=['POST'])
def register():
    #this email is in the body
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='the email already exist'),409
    else:
        first_name = request.form['first_name']
        last_name  = request.form['last_name']
        password  = request.form['password']
        user = User(first_name= first_name, last_name=last_name, email= email,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message = "new User created!"), 201


@app.route('/login',methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email= email, password = password).first()
    if test:
        access_token = create_access_token(identity= email)
        return jsonify(message = "Login successful!", access_token = access_token)
    else:
        return jsonify(message="Invalid email or password"), 401

@app.route('/retreive_password/<string:email>',methods = ['GET'])
def retrieve_password(email:str):
    user = User.query.filter_by(email=email).first()
    if user: 
        msg = Message('your password is '+ user.password,sender= "admin@training.com",recipients=[email])
        mail.send(msg)
        return jsonify(Message = "password sent to "+email)
    else:
        return jsonify(Message = "account does not exist:  "+email),401


@app.route('/planet/<int:planet_id>',methods=['GET'])
def planet_detail(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else: 
        return jsonify(message = 'the planet does not exist'),404
    
@app.route('/add_planet',methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    planet = Planet.query.filter_by(planet_name=planet_name).first()
    if planet:
        return jsonify(message = "This planet already exists!"),409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance =float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name,planet_type=planet_type
        ,home_star=home_star,
        mass=mass,radius=radius,distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message="New planet added!"),201


@app.route('/update_planet',methods=['PUT'])
@jwt_required
def update_planet():
        planet_id = request.form['planet_id']
        planet  = Planet.query.filter_by(planet_id=planet_id).first()
        if planet:
            planet.planet_name = request.form['planet_name']
            planet.planet_type = request.form['planet_type']
            planet.home_star  = request.form['home_star']
            planet.mass  = float(request.form['mass'])
            planet.radius = float(request.form['radius'])
            planet.distance = float(request.form['distance'])
            db.session.commit()
            return jsonify(message='planet updated successfully!'),202
        else:
            return jsonify(message= 'planet does not exist'),404


@app.route('/delete_planet/<int:planet_id>',methods=['DELETE'])
@jwt_required
def delete_planet(planet_id:int):
        planet = Planet.query.filter_by(planet_id=planet_id).first()
        if planet:
            db.session.delete(planet)
            db.session.commit()
            return jsonify(message="the planet "+planet.planet_name+ " is deleted"),201


        else:
            return jsonify(message="the planet does not exist"),404


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
    planet_id = Column(Integer,primary_key = True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','email','password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id','planet_name','planet_type','home_star','mass','radius','distance')


user_schema  = UserSchema()
users_schema = UserSchema(many = True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)











if __name__ == '__main__':
    app.run()