from flask import request, g, jsonify, make_response

from . import api


def query_db():
    """
    test g object
    :return:
    """
    user_id = g.user_id
    user_name = g.user_name
    print({"user": {"id": user_id, "name": user_name}})


@api.route('/user_profile')
def user_profile():
    g.user_id = request.args.get('user_id')
    g.user_name = request.args.get('user_name')
    query_db()
    rsp = make_response({'stat': 0})
    # rsp = make_response()
    rsp.headers['Server'] = 'csx'
    return rsp
