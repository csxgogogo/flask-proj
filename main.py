from flask import Flask, jsonify, request

from celery_tasks.main import celery_app

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok"})


@app.route('/add')
def tow_sum():
    a = request.args.get('a')
    b = request.args.get('b')
    try:
        celery_app.send_task("tow-sum-task", [a, b])
    except :
        return jsonify({'status': '1', 'errmsg': "celery err"})

    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(port="8888", debug=True)
