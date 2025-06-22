from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(body=data['body'], username=data['username'])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = db.session.get(Message, id) 
        if not message:
            return jsonify({"error": "Message not found"}), 404
        message.body = request.json['body']
        db.session.commit()
        return jsonify(message.to_dict())

    elif request.method == 'DELETE':
        message = db.session.get(Message, id)  
        if not message:
            return jsonify({"error": "Message not found"}), 404
        db.session.delete(message)
        db.session.commit()
        return jsonify(message.to_dict())

if __name__ == '__main__':
    app.run(port=5000)
