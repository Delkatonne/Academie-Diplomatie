from flask import current_app, render_template, send_from_directory

from app.routes.public import bp


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/formations")
def formations():
    return render_template("formations.html")


# Fichiers CSS, JavaScript et images du frontend
@bp.get("/css/<path:filename>")
def frontend_css(filename):
    return send_from_directory(current_app.config["FRONTEND_DIR"] / "css", filename)


@bp.get("/js/<path:filename>")
def frontend_js(filename):
    return send_from_directory(current_app.config["FRONTEND_DIR"] / "js", filename)


@bp.get("/images/<path:filename>")
def frontend_images(filename):
    return send_from_directory(current_app.config["FRONTEND_DIR"] / "images", filename)
