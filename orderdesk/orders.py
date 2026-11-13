from flask import Blueprint, abort, flash, g, redirect, render_template, url_for

from .auth import login_required
from .db import get_db

bp = Blueprint("orders", __name__, url_prefix="/orders")


def get_order(order_id):
    """The order, if the signed-in user owns it (or is an admin)."""
    order = get_db().execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        abort(404)
    if order["user_id"] != g.user["id"] and not g.user["is_admin"]:
        abort(403)
    return order


@bp.get("/")
@login_required
def list_orders():
    orders = get_db().execute(
        "SELECT o.id, o.status, o.created, SUM(i.quantity * p.price_cents) AS total_cents FROM orders o"
        " LEFT JOIN order_item i ON i.order_id = o.id LEFT JOIN product p ON p.id = i.product_id"
        " WHERE o.user_id = ? GROUP BY o.id ORDER BY o.created DESC", (g.user["id"],)).fetchall()
    return render_template("orders.html", orders=orders)


@bp.get("/<int:order_id>")
@login_required
def show(order_id):
    order = get_order(order_id)
    items = get_db().execute(
        "SELECT p.name, p.sku, p.price_cents, i.quantity FROM order_item i JOIN product p ON p.id = i.product_id"
        " WHERE i.order_id = ?", (order_id,)).fetchall()
    return render_template("order.html", order=order, items=items)


@bp.post("/<int:order_id>/cancel")
@login_required
def cancel(order_id):
    order = get_order(order_id)
    if order["status"] != "open":
        flash("Only open orders can be cancelled.")
    else:
        db = get_db()
        db.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
        db.commit()
        flash(f"Order #{order_id} cancelled.")
    return redirect(url_for("orders.show", order_id=order_id))
