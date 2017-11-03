import os
import json
from flask import Blueprint, render_template, send_file

pages_blueprint = Blueprint('pages_api', __name__)

@pages_blueprint.route("/")
def index():
    return render_template("index.html")

@pages_blueprint.route('/js/<path:path>')
def send_js(path):
    # $CONDA_PREFIX/lib/node_modules/jquery/dist/
    pathparts = os.path.normpath(path).split(os.sep)
    filepath = os.path.join(os.getenv("CONDA_PREFIX"), "lib", "node_modules", path)
    if not os.path.exists(filepath):
        filepath = os.path.join(os.getenv("CONDA_PREFIX"), "lib", "node_modules", pathparts[0], "dist", *pathparts[1:])
    return send_file(filepath)



@pages_blueprint.route("/experiments/<instrument_id>", methods=["GET"])
def batch_tabs(instrument_id):
    return render_template("experiments.html", instrument_id=instrument_id)

