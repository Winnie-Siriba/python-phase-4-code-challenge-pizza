# Pizza Restaurant API

Flask API for managing pizza restaurants with many-to-many relationships.

## Setup

```bash
pipenv install && pipenv shell
export FLASK_APP=server/app.py
flask db init && flask db migrate && flask db upgrade head
python seed.py
```

## Run

```bash
python app.py
```

Server runs on `localhost:5555`

## API Endpoints

- `GET /restaurants` - All restaurants
- `GET /restaurants/<id>` - Restaurant details
- `DELETE /restaurants/<id>` - Delete restaurant
- `GET /pizzas` - All pizzas
- `POST /restaurant_pizzas` - Create restaurant-pizza association

## Models

- **Restaurant**: id, name, address
- **Pizza**: id, name, ingredients  
- **RestaurantPizza**: price (1-30), restaurant_id, pizza_id

## Test

```bash
pytest -x
```