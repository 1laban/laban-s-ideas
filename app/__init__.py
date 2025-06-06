from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp # Changed import and alias
    app.register_blueprint(main_bp)

    # The import of models here is fine for now, it makes User model available when 'app' package is imported.
    from app import models

    @app.shell_context_processor
    def make_shell_context():
        # models are already imported as 'models'
        return {'db': db,
                'User': models.User,
                'Event': models.Event,
                'Ticket': models.Ticket,
                'Order': models.Order}

    return app
