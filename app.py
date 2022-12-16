import datetime
from flask import Flask, render_template, jsonify, request, json
import requests
from pymongo import MongoClient

app = Flask(__name__)

def get_database():
    CONNECTION_STRING = "mongodb+srv://vip:vip123@vip.lef3vva.mongodb.net/?retryWrites=true&w=majority"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['Reflection']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.get('/getpost')
def getpost():
    messages = []
    db = (get_database())['message']
    cursor = db.find()
    list(map(lambda v: messages.append({'message': v['message'], 'timestamp': (v['timestamp'])},), cursor))
    return jsonify({'data':messages})
    
@app.post('/post')
def post():
    data = json.loads(request.data)
    collection = {
        'message' : data['message'],
        'timestamp' : datetime.datetime.utcnow()
    }
    db = (get_database())['message']
    db.insert_one(collection)
    return jsonify({'message': 'Data Added!'})

if __name__ == "__main__":
    app.run(debug=True, port=3005)
