import datetime
import uuid
from datetime import timezone

from app.main import db
from app.main.model.channel import Channel

norilsk_time = timezone(datetime.timedelta(0, 25200), 'Asia/Krasnoyarsk')


def add_channel(data):
    channel = None
    if data.get('public_id'):
        channel = Channel.query.filter_by(public_id=data['public_id']).first()
    if not channel:
        new_channel = Channel(
            name=data['name'],
            last_change=datetime.datetime.now(tz=norilsk_time),
            channel_type=data['channel_type'],
            state=data['state'],
            dimmer_state=data['dimmer_state'],
            public_id=str(uuid.uuid4()),

        )
        channel_id = save_obj(new_channel)
        response_object = {
            'status': 'success',
            'message': 'Successfully created.',
            'public_id': channel_id,
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Channel already exists',
        }
        return response_object, 409


def update_channel(public_id, data):
    channel = None
    if public_id:
        # channel = Channel.query.filter_by(public_id=public_id).first()
        channel = Channel.query.filter_by(public_id=public_id).update(
            dict(
                name=data['name'],
                dimmer_state=data['dimmer_state'],
                last_change=datetime.datetime.now(tz=norilsk_time),
                channel_type=data['channel_type'],
                state=data['state']
            )
        )

    if not bool(channel):
        response_object = {
            'status': 'fail',
            'message': 'Channel not found',
        }
        return response_object, 404
    else:
        db.session.commit()
        return channel, 204


def get_all_channels():
    return Channel.query.all()


def get_channel_state(channel_id: object) -> object:
    return Channel.query.filter_by(public_id=channel_id).first()


def save_obj(data):
    db.session.add(data)
    db.session.commit()
    return data.get_public_id
