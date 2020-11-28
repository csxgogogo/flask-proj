from flask import Flask, jsonify, request
from celery_tasks.main import celery_app

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok"})


@app.route('/add')
def tow_sum():
    a = request.args.get('a')
    b = request.args.get('b')
    celery_app.send_task('tow-sum-task', [int(a), int(b)])
    return jsonify({"stat": 0, "msg": 'send task successful'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
