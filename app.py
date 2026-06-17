from flask import Flask, render_template
from database import get_db_connection

app = Flask(__name__)

from controller.routes import api_routes
app.register_blueprint(api_routes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)