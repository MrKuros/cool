import os
from flask import Flask, render_template

import pulumi.automation as auto
import pandas as pd

key = pd.read_csv("../keys/key.csv")

def ensure_plugins():
    ws = auto.LocalWorkspace()
    ws.install_plugin("aws", "v4.0.0")


def create_app():
    ensure_plugins()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= key.columns[1],
        PROJECT_NAME="cool",
        PULUMI_ORG=os.environ.get("PULUMI_ORG"),
    )

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    import sites

    app.register_blueprint(sites.bp)

    import virtual_machines

    app.register_blueprint(virtual_machines.bp)

    return app
