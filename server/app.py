#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, Pizza, RestaurantPizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return '<h1>Pizza Restaurant API</h1>'


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants], 200


class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        return restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas.id', 
                                       'restaurant_pizzas.price', 'restaurant_pizzas.pizza_id', 
                                       'restaurant_pizzas.restaurant_id', 'restaurant_pizzas.pizza.id',
                                       'restaurant_pizzas.pizza.name', 'restaurant_pizzas.pizza.ingredients')), 200
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204


class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas], 200


class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            # Validate required fields
            if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
                return {'errors': ['Missing required fields']}, 400
            
            # Check if restaurant and pizza exist
            restaurant = Restaurant.query.get(data['restaurant_id'])
            pizza = Pizza.query.get(data['pizza_id'])
            
            if not restaurant:
                return {'errors': ['Restaurant not found']}, 400
            if not pizza:
                return {'errors': ['Pizza not found']}, 400
            
            # Create new RestaurantPizza
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            return restaurant_pizza.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id',
                                                 'pizza.id', 'pizza.name', 'pizza.ingredients',
                                                 'restaurant.id', 'restaurant.name', 'restaurant.address')), 201
            
        except ValueError as e:
            return {'errors': [str(e)]}, 400
        except Exception as e:
            return {'errors': ['Failed to create restaurant pizza']}, 400


# Add resources to API
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantByID, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)