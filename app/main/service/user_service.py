import uuid
import datetime

from app.main import db
from app.main.model.user import User


def create_new_user(user_data, is_admin):
    return User(
            public_id=str(uuid.uuid4()),
            email=user_data['email'],
            admin=True if is_admin else False,
            username=user_data['username'],
            password=user_data['password'],
            registered_on=datetime.datetime.utcnow()
        )


def process_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = create_new_user(data, False)
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
