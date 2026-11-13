import os

from flask import Blueprint, abort, current_app, request, send_file

from .auth import login_required

bp = Blueprint("files", __name__, url_prefix="/files")


@bp.get("/invoice")
@login_required
def invoice():
    """Download an invoice PDF; the billing job writes them as <order id>-<yyyymmdd>.pdf."""
    name = request.args.get("name", "")
    path = os.path.join(current_app.config["INVOICE_DIR"], name)
    if not name or not os.path.isfile(path):
        abort(404)
    return send_file(path, as_attachment=True)
