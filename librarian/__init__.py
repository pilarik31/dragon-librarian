import os

from flask import Flask
# from sassutils.wsgi import SassMiddleware


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'librarian.sqlite'),
    )

    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'librarian': ('static/sass', 'static/css', '/static/css')
    # })

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import scenes
    app.register_blueprint(scenes.bp)
    app.add_url_rule('/', endpoint='index')

    return app
