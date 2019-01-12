from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.channel_controller import api as channel_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='LightWare RESTful API',
          version='1.0.0',
          description='LightWare RESTful API server'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(channel_ns, path='/channel')
api.add_namespace(auth_ns)
