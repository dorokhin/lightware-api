from .. import db


class Channel(db.Model):
    """ Channel Model for storing channel state"""
    __tablename__ = "channel_state"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    last_change = db.Column(db.DateTime, nullable=False)
    channel_type = db.Column(db.Boolean)
    state = db.Column(db.Boolean, nullable=False, default=False)
    dimmer_state = db.Column(db.SmallInteger)
    public_id = db.Column(db.String(100), unique=True)
