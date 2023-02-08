import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


with app.app_context():
    db.create_all()

db.session.add_all(utils.add_info_to_user(User))
db.session.commit()

db.session.add_all(utils.add_info_to_order(Order))
db.session.commit()

db.session.add_all(utils.add_info_to_offer(Offer))
db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def page_api_all_users():
    if request.method == 'GET':
        result = []
        users = User.query.all()
        for user in users:
            result.append(user.to_dict())
            return jsonify(result)

    elif request.method == 'POST':
        new_user = json.loads(request.data)
        user = utils.add_new_user(User, new_user)
        db.session.add(user)
        db.session.commit()
        return '201 Created', 201


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def page_api_user_by_id(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        update_user = json.loads(request.data)
        user = Order.query.get(id)

        user.id = update_user['id']
        user.first_name = update_user["first_name"]
        user.last_name = update_user["last_name"]
        user.age = update_user['age']
        user.email = update_user['email']
        user.role = update_user['role']
        user.phone = update_user['phone']

        db.session.add(user)
        db.session.commit()

        return '201 Updated', 201

    elif request.method == 'DELETE':
        user_to_delete = User.query.get(id)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Removed', 201


@app.route('/orders', methods=['GET', 'POST'])
def page_api_all_orders():
    if request.method == 'GET':
        result = []
        orders = Order.query.all()
        for order in orders:
            result.append(order.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        new_order = json.loads(request.data)
        order = utils.add_new_user(User, new_order)
        db.session.add(order)
        db.session.commit()
        return '201 Created', 201


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def page_api_order_by_id(id):
    if request.method == 'GET':
        order = Order.query.get(id)
        return jsonify(order.to_dict())
    elif request.method == 'PUT':
        update_order = json.loads(request.data)
        order = Order.query.get(id)

        order.id = update_order['id']
        order.name = update_order["name"]
        order.description = update_order["description"]
        order.start_date = update_order['start_date']
        order.end_date = update_order['end_date']
        order.address = update_order['address']
        order.price = update_order['price']
        order.customer_id = update_order['customer_id']
        order.executor_id = update_order['executor_id']

        db.session.add(order)
        db.session.commit()

        return '201 Updated', 201

    elif request.method == 'DELETE':
        order_to_delete = Order.query.get(id)
        db.session.delete(order_to_delete)
        db.session.commit()
        return 'Removed', 201


@app.route('/offers', methods=['GET', 'POST'])
def page_api_all_offers():
    if request.method == 'GET':
        result = []
        offers = Offer.query.all()
        for offer in offers:
            result.append(offer.to_dict())
        return jsonify(result)

    elif request.method == 'POST':
        new_offer = json.loads(request.data)
        offer = utils.add_new_user(User, new_offer)
        db.session.add(offer)
        db.session.commit()
        return '201 Created', 201


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def page_api_offer_by_id(id):
    if request.method == 'GET':
        offer = Offer.query.get(id)
        return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        update_offer = json.loads(request.data)
        offer = Offer.query.get(id)

        offer.id = update_offer['id']
        offer.order_id = update_offer["order_id"]
        offer.executor_id = update_offer["executor_id"]

        db.session.add(offer)
        db.session.commit()

        return '201 Updated', 201

    elif request.method == 'DELETE':
        offer_to_delete = Offer.query.get(id)
        db.session.delete(offer_to_delete)
        db.session.commit()
        return 'Removed', 201


if __name__ == '__main__':
    app.run(debug=True)
