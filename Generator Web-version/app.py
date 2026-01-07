from flask import Flask, render_template, jsonify
import threading

from mission_service import run_mission

app = Flask(__name__)

# --------------------------------------------------
# Globaler Run-State (für 1 User ausreichend)
# --------------------------------------------------

LOG_BUFFER = []
IS_RUNNING = False


def log(message: str):
    """Sammelt Logs aus mission_service"""
    LOG_BUFFER.append(message)


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global IS_RUNNING, LOG_BUFFER

    if IS_RUNNING:
        return jsonify({"status": "already running"})

    LOG_BUFFER = []
    IS_RUNNING = True

    def task():
        global IS_RUNNING
        try:
            result = run_mission(log)
            log(result)
        finally:
            IS_RUNNING = False

    threading.Thread(target=task, daemon=True).start()

    return jsonify({"status": "started"})


@app.route("/logs")
def logs():
    return jsonify({
        "logs": "".join(LOG_BUFFER),
        "running": IS_RUNNING
    })


# --------------------------------------------------
# Local Dev Entry Point
# (wird von Render/Gunicorn ignoriert)
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
