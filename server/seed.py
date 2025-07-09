#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():
    print("Starting seed...")
    
    # Clear existing data
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
    
    # Create restaurants
    restaurants = []
    restaurant_names = [
        "Karen's Pizza Shack",
        "Sanjay's Pizza",
        "Kiki's Pizza",
        "Gino's Italian",
        "Mario's Pizzeria"
    ]
    
    for name in restaurant_names:
        restaurant = Restaurant(
            name=name,
            address=fake.address()
        )
        restaurants.append(restaurant)
    
    db.session.add_all(restaurants)
    
    # Create pizzas
    pizzas = []
    pizza_data = [
        ("Emma", "Dough, Tomato Sauce, Cheese"),
        ("Geri", "Dough, Tomato Sauce, Cheese, Pepperoni"),
        ("Melanie", "Dough, Sauce, Ricotta, Red peppers, Mustard"),
        ("Margherita", "Dough, Tomato Sauce, Mozzarella, Basil"),
        ("Hawaiian", "Dough, Tomato Sauce, Cheese, Ham, Pineapple"),
        ("Meat Lovers", "Dough, Tomato Sauce, Cheese, Pepperoni, Sausage, Ham"),
        ("Veggie Supreme", "Dough, Tomato Sauce, Cheese, Peppers, Mushrooms, Onions")
    ]
    
    for name, ingredients in pizza_data:
        pizza = Pizza(
            name=name,
            ingredients=ingredients
        )
        pizzas.append(pizza)
    
    db.session.add_all(pizzas)
    db.session.commit()
    
    # Create restaurant pizzas (associations)
    restaurant_pizzas = []
    for restaurant in restaurants:
        # Each restaurant will have 2-4 pizzas
        num_pizzas = randint(2, 4)
        selected_pizzas = fake.random_elements(elements=pizzas, length=num_pizzas, unique=True)
        
        for pizza in selected_pizzas:
            restaurant_pizza = RestaurantPizza(
                price=randint(1, 30),
                restaurant_id=restaurant.id,
                pizza_id=pizza.id
            )
            restaurant_pizzas.append(restaurant_pizza)
    
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    
    print(f"Seeded {len(restaurants)} restaurants")
    print(f"Seeded {len(pizzas)} pizzas")
    print(f"Seeded {len(restaurant_pizzas)} restaurant-pizza associations")
    print("Seed completed!")