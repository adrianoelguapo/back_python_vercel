from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS  # Importar CORS
from bson import ObjectId

app = Flask(__name__)

# Configurar CORS
CORS(app)

# Configurar conexión a MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://admin:123@cluster0.tz018.mongodb.net/despliegue_vercel_express?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

@app.route('/api/users', methods=['GET'])
def get_users():
    users = []
    for user in db.users.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "apellido": user["apellido"],
            "tlf": user["tlf"]
        })
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    user_data = {
        "name": new_user["name"],
        "apellido": new_user["apellido"],
        "tlf": new_user["tlf"]
    }
    user_id = db.users.insert_one(user_data).inserted_id
    user_data["_id"] = str(user_id)
    return jsonify(user_data), 201

@app.route('/api/users/<string:name>', methods=['GET'])
def search_user(name):
    try:
        users = db.users.find({"name": name})
        results = []
        for user in users:
            results.append({
                "id": str(user["_id"]),
                "name": user["name"],
                "apellido": user["apellido"],
                "tlf": user["tlf"]
            })
        if results:
            return jsonify(results), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def home():
    return 'Hello, World!'

#app.run()