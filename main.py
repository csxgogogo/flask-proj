from flask import Flask, jsonify, request, session, g, make_response

from celery_tasks.main import celery_app
# create a flask app object
app = Flask(__name__)
# set development mode
app.debug = True
# session key
app.secret_key = '65696038ed97afcbf8552a1939ca846e5e6a92f5cf6f7f639688596a49f53476'


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok"})


@app.route("/get-validation-code")
def get_code():
    try:
        code = session['validation_code']
    except:
        return 'get code err'
    return jsonify(validation_code=code)


@app.route('/add')
def tow_sum():
    a = request.args.get('a')
    b = request.args.get('b')
    celery_app.send_task('tow-sum-task', [int(a), int(b)])
    return jsonify({"stat": 0, "msg": 'send task successful'})


from api import api
# register blueprint
app.register_blueprint(api, url_prefix='/api')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
