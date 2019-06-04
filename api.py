from pymongo import MongoClient
from flask import Flask, request, jsonify, json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['data_peace']

#
# with open("data.dat", mode="r") as f:
#     data_string = f.readline()

# data_json = json.loads(data_string)
post = db.post


# db.post.updateMany(doc, doc, {upsert:true})


@app.route('/')
def home():
    return "hello world"


@app.route('/api/users', methods=['GET'])
def get():
    list = []
    page = int(request.args.get('page', 1)) - 1
    limit = int(request.args.get('limit', 5))
    name = request.args.get('name', None)
    sort = request.args.get('sort', None)
    post = db.post
    if sort is not None:
        if name is not None:
            name = "^" + name

        if sort[0] == '-':
            results = post.find({'$or': [{'first_name': {"$regex": name}}, {'last_name': {"$regex": name}}]},
                                {'_id': 0}).skip(page * limit).limit(
                limit).sort(sort[1:], -1)
        else:
            results = post.find({'$or': [{'first_name': {"$regex": name}}, {'last_name': {"$regex": name}}]},
                                {'_id': 0}).skip(page * limit).limit(limit).sort(sort)
    else:
        results = post.find({}, {'_id': 0}).skip(page * limit).limit(limit)

    for result in results:
        list.append(result)

    return jsonify(list), 200


@app.route('/api/users', methods=['POST'])
def post():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    if 'id' not in values:
        response = {
            'message': 'some data not found'
        }
        return jsonify(response), 400
    print(values)
    post = db.post
    result = post.insert_one(values)
    print(result)
    return "Succesfullu uploaded", 201


@app.route('/api/users/<id>', methods=['PUT'])
def update(id):
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    post = db.post
    result = post.update_one({'id': int(id)}, {'$set': values})
    print(result)

    return "succesfully updated", 200


@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    post = db.post
    result = post.find_one({'id': int(id)}, {'_id': 0})
    return jsonify(str(result)), 200


@app.route('/api/users/<id>', methods=['DELETE'])
def delete(id):
    post = db.post
    result = post.remove({'id': int(id)})
    return jsonify(str(result)), 200


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
