from io import BytesIO

from flask import session, make_response

from . import api
from utils.validation_code import create_validation_code


@api.route("/validation-code", methods=['GET'])
def get_validation_code():
    """
    获取图片验证码接口
    :return:图片文件和验证码
    """
    code_img, code_str = create_validation_code()
    print(code_str)
    session['validation_code'] = code_str
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality=50)
    buf_str = buf.getvalue()
    rsp = make_response(buf_str)
    rsp.headers['Content_Type'] = 'image/jpeg'
    return rsp
