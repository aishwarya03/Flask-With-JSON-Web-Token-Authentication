from flask import Flask, request, json, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'HIHIUHIUHIni' 
    # file_path = os.path.abspath(os.getcwd())+"\todos.db"
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoo.db'
    db.init_app(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True)
        name = db.Column(db.String(50))
        password = db.Column(db.String(50))
        admin = db.Column(db.Boolean)

    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(50))
        complete = db.Column(db.Boolean)
        user_id = db.Column(db.Integer,)

    with app.app_context():
        db.create_all()

    @app.route('/user', methods=['GET'])
    def get_all_users():
        users = User.query.all()
        output = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'user': output})
    
    @app.route('/user/<public_id>', methods=['GET'])
    def get_one_user(public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message' : 'No user found'})
        else:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            return jsonify({'user' : user_data})
    
    @app.route('/user', methods=['POST'])
    def create_user():
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message' : 'New User Created'})

    @app.route('/user/<public_id>', methods=['PUT'])
    def update_user_promotion(public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message' : 'No user found'})
        
        user.admin = True
        db.session.commit()
        return jsonify({'message' : 'User Created has been promoted'})
    
    @app.route('/user/<public_id>', methods=['DELETE'])
    def delete_user(public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message' : 'No user found'})
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message' : 'User Created has been Deleted'})

    return app

app = create_app()

if __name__ =='__main__':
    app.run(debug=True)