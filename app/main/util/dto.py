from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user management')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication management')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class ChannelDto:
    api = Namespace('channel', description='channel switch management')
    resource_fields = {
        'name': fields.String(required=False, description='Channel name'),
        'channel_type': fields.Boolean(required=True, description='Channel type'),
        'state': fields.Boolean(required=False, description='Channel state'),
        'dimmer_state': fields.Integer(required=False, description='Channel dimmer  value'),
        'public_id': fields.String(description='Public channel identifier'),
        'last_change': fields.DateTime(required=False, description='Last change time'),

    }

    channel_state = api.model('channel', resource_fields)
