from flask import Flask
from flask_cors import CORS
from common.extensions import cache

from routes.routes import routes_list

app = Flask(__name__)
cors = CORS(app)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

app.config['CORS_HEADERS'] = 'Content-Type'

for (url, method, allowed_methods) in routes_list:
    app.add_url_rule(url, view_func=method, methods=allowed_methods)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=False)
