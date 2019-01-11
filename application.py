import os
from app import blueprint
from app.main import create_app


app = create_app(os.getenv('LIGHTWARE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

app.run()
