# from redis import Redis
from core.utils.flask_extended import Flask


app = Flask(__name__)
# redis = Redis(host='redis', port=6379)

from core import app_setup


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)