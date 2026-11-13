import click
from flask import Blueprint, abort, g, jsonify, request
from werkzeug.security import generate_password_hash

from .auth import login_required
from .db import get_db

bp = Blueprint("users", __name__, url_prefix="/users")


def public(user):
    """A user as the API shows it: never the password hash."""
    return {"id": user["id"], "username": user["username"], "email": user["email"], "is_admin": bool(user["is_admin"])}


@bp.get("/me")
@login_required
def me():
    return jsonify(public(g.user))


@bp.patch("/me")
@login_required
def update_me():
    email = (request.get_json(silent=True) or {}).get("email", "").strip()
    if "@" not in email:
        return jsonify(error="a valid email address is required"), 422
    db = get_db()
    db.execute("UPDATE user SET email = ? WHERE id = ?", (email, g.user["id"]))
    db.commit()
    return jsonify(public(db.execute("SELECT * FROM user WHERE id = ?", (g.user["id"],)).fetchone()))


@bp.get("/")
@login_required
def list_users():
    if not g.user["is_admin"]:
        abort(403)
    return jsonify([public(u) for u in get_db().execute("SELECT * FROM user ORDER BY username")])


@bp.cli.command("create")
@click.argument("username")
@click.argument("email")
@click.password_option()
@click.option("--admin", is_flag=True)
def create_user(username, email, password, admin):
    """Create a user: flask --app orderdesk users create alice alice@example.com"""
    db = get_db()
    db.execute("INSERT INTO user (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
               (username, generate_password_hash(password), email, int(admin)))
    db.commit()
    click.echo(f"Created {username}.")
