from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    height = db.Column(db.String(80))
    birth_year = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    homeworld = db.Column(db.String(120))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250))
    gravity = db.Column(db.String(120))
    population = db.Column(db.String(120))
    climate = db.Column(db.String(120))

    def __repr__(self):
        return '<Planet %r>' % self.planet_name
    
    def serialize(self):
        return{
            "id": self.id,
            "planet_name": self.planet_name,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(250))
    model = db.Column(db.String(120))
    vehicle_class = db.Column(db.String(80))
    manufacturer = db.Column(db.String(120))

    def __repr__(self):
        return '<Vehicle %r>' % self.vehicle_name
    
    def serialize(self):
        return{
            "id": self.id,
            "vehicle_name": self.vehicle_name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer
        }


class CharacterFavorites(db.Model):
    __tablename__ = 'fav_character'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the relationships
    character = db.relationship('Character', backref='favorites')
    user = db.relationship('User', backref='favorite_characters')

class PlanetFavorites(db.Model):
    __tablename__ = 'fav_planet'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the relationships
    planet = db.relationship('Planet', backref='favorites')
    user = db.relationship('User', backref='favorite_planets')

class VehicleFavorites(db.Model):
    __tablename__ = 'fav_vehicle'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define the relationships
    vehicle = db.relationship('Vehicle', backref='favorites')
    user = db.relationship('User', backref='favorite_vehicles')