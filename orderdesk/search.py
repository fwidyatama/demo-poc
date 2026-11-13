from flask import Blueprint, render_template, request

from .auth import login_required
from .db import get_db

bp = Blueprint("search", __name__)


@bp.get("/search")
@login_required
def search():
    """Products whose name contains q, or whose SKU is q (case-insensitive)."""
    q = request.args.get("q", "").strip()
    products = []
    if q:
        products = get_db().execute(
            "SELECT id, name, sku, price_cents FROM product WHERE name LIKE ? OR sku = ? ORDER BY name LIMIT 50",
            (f"%{q}%", q.upper())).fetchall()
    return render_template("search.html", q=q, products=products)
