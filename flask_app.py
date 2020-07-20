from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
import os


def create_app():
    """
    Construct core Flask application
    with embedded Dash app.
    """
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import Flask routes
        import routes

        # Import Dash application
        # from dash.convolution import create_dashboard
        from dashapps.convolution import signal_kernel_dashboard
        from dashapps.convolution import convolution_dashboard

        convolution_dashboard(app)
        signal_kernel_dashboard(app)

        # Compile CSS
        # from application.assets import compile_assets
        # compile_assets(app)

        return app


app = create_app()


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    """
    Adds time stamp to url, to counteract
    CSS reload issues due to the browser cache.
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.run()
