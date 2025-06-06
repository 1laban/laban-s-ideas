from app import create_app, db # db import is not strictly needed here anymore but harmless
from app.models import User, Event, Ticket, Order # model imports are not strictly needed here but harmless

app = create_app()

# The shell context processor is now defined within create_app in app/__init__.py

if __name__ == '__main__':
    app.run(debug=True)
