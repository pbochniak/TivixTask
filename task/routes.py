from flask import current_app as app


@app.route("/<path:path>", methods=["GET"])
def anyPath(path):
    return f"Path: '{path}'"
