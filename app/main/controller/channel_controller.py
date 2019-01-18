from flask_restplus import Resource
from flask import request
from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import ChannelDto
from ..service.channel_service import get_all_channels, add_channel, get_channel_state, update_channel

api = ChannelDto.api
_channel = ChannelDto.channel_state


@api.route('/')
class ChannelList(Resource):
    @api.doc('List of channels')
    @admin_token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.marshal_list_with(_channel, envelope='data')
    def get(self):
        """List all channels"""
        return get_all_channels()

    @api.doc('Create a new channel')
    @admin_token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.response(201, 'Channel successfully created.')
    @api.expect(_channel, validate=True)
    def post(self):
        """Create channel"""
        data = request.json
        return add_channel(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'Channel identifier')
@api.response(404, 'Channel not found.')
class Channel(Resource):

    @api.doc('Get channel by id')
    @token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.marshal_with(_channel)
    def get(self, public_id):
        """Get channel by public_id"""
        channel = get_channel_state(public_id)
        if not channel:
            api.abort(404)
        else:
            return channel

    @api.doc('Update channel state')
    @admin_token_required
    @api.param('Authorization', 'Authorization token', _in='header')
    @api.marshal_with(_channel)
    @api.expect(_channel, validate=True)
    def put(self, public_id):
        """Update channel state"""
        data = request.json
        return update_channel(public_id=public_id, data=data)
