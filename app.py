import os

from flask import (
    Flask, 
    redirect,
    render_template,
    url_for
)

from scr.controllers.db import init_app
from scr.blueprints import (
    auth,
    index
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'teste.db'),
    )

    app.config['EXPLAIN_TEMPLATE_LOADING'] = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def base():
        return redirect(url_for("auth.login"))

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/repassword')
    def repassword():
        return render_template("repassword.html")

    init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(index.bp)

    return app
