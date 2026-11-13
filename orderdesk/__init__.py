"""Order Desk: a small Flask app where customers track their orders and download invoices."""
import os

from flask import Flask, redirect, url_for

from . import auth, db, files, orders, search, users


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="orderdesk-2023-session-key",
        DATABASE=os.path.join(app.instance_path, "orderdesk.sqlite"),
        INVOICE_DIR=os.path.join(app.instance_path, "invoices"),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.config["INVOICE_DIR"], exist_ok=True)

    db.init_app(app)
    for blueprint in (auth.bp, users.bp, orders.bp, search.bp, files.bp):
        app.register_blueprint(blueprint)

    @app.template_filter("money")
    def money(cents):
        return f"${(cents or 0) / 100:,.2f}"

    @app.get("/")
    def index():
        return redirect(url_for("orders.list_orders"))

    return app
