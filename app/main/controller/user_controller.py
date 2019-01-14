from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto
from ..service.user_service import process_new_user, get_all_users, get_a_user, delete_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created')
    @api.doc('Create a new user')
    def post(self):
        data = request.json
        return process_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
class User(Resource):
    @api.doc('Get user by id')
    @api.response(404, 'User not found')
    @token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.marshal_with(_user)
    def get(self, public_id):
        user = get_a_user(public_id)
        if not user:
            return 'abort', 404
        else:
            return user

    @api.doc('Delete user by id')
    @api.response(404, 'User not found')
    @api.response(204, 'User was deleted')
    @admin_token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    def delete(self, public_id):
        return delete_user(public_id)
