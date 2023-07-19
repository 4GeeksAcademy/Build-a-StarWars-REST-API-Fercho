"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, CharacterFavorites, PlanetFavorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    
    user_list = [user.serialize() for user in users]
    return jsonify(user_list), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    character_list = [character.serialize() for character in characters]
    return jsonify(character_list), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    
    planet_list = [planet.serialize() for planet in planets]
    return jsonify(planet_list), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = User.query.get_or_404(user_id)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

    return jsonify(user_data), 200

def get_user_by_id():
    user_id = request.args.get('user_id')
    if user_id is None:
        return None
    return int(user_id) 

@app.route('/characters/<int:character_id>', methods=['GET'])
def getCharacter(character_id):
    character = Character.query.get_or_404(character_id)

    character_data = {
        "id": character.id,
        "name": character.name,
        "height": character.height,
        "birth_year": character.birth_year,
        "gender": character.gender,
        "homeworld": character.homeworld
    }

    return jsonify(character_data), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    planet_data = {
        "id": planet.id,
        "planet_name": planet.planet_name,
        "gravity": planet.gravity,
        "population": planet.population,
        "climate": planet.climate
    }

    return jsonify(planet_data), 200


@app.route('/users', methods=['POST'])
def post_new_user():
    user_data = request.json
    user = User(username=user_data['username'], email=user_data['email'], password=user_data['password'])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "username": user.username,
        "email": user.email,
        "password":user.password
    }
    return jsonify(response_body), 200

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def addCharacterFavorite(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404

    existing_favorite = CharacterFavorites.query.filter_by(char_id=character_id).first()
    if existing_favorite:
        return jsonify({"error": "Character already a favorite"}), 400

    character_favorite = CharacterFavorites(char_id=character_id)
    db.session.add(character_favorite)
    db.session.commit()

    return jsonify({"message": "Character favorite added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addPlanetFavorite(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    existing_favorite = PlanetFavorites.query.filter_by(planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Planet already a favorite"}), 400

    planet_favorite = PlanetFavorites(planet_id=planet_id)
    db.session.add(planet_favorite)
    db.session.commit()

    return jsonify({"message": "Planet favorite added successfully"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deletePlanetFavorite(planet_id):
    favorite = PlanetFavorites.query.filter_by(planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Planet favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Planet favorite deleted successfully"}), 200


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def deleteCharacterFavorite(character_id):
    favorite = CharacterFavorites.query.filter_by(char_id=character_id).first()
    if favorite is None:
        return jsonify({"error": "Character favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Character favorite deleted successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
