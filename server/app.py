#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.to_dict())
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.all()
    baked_goods_list = [good.to_dict() for good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict())
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)