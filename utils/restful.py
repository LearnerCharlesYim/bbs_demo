from flask import jsonify

class HttpCode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    methoderror = 405
    servererror = 500

def restful_result(code,message,data):
    return jsonify({"code":code,"message":message,"data":data or {}})

def success(message="",data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)

def params_error(message=""):
    """
        请求参数错误
    """
    return restful_result(code=HttpCode.paramserror, message=message,data=None)

def unauth_error(message=""):
    """
        没有权限访问
    """
    return restful_result(code=HttpCode.unautherror,message=message,data=None)

def method_error(message=""):
    """
        请求方法错误
    """
    return restful_result(code=HttpCode.unautherror, message=message,data=None)

def server_error(message=""):
    """
        服务器内部错误
    """
    return restful_result(code=HttpCode.servererror, message=message or "服务器内部错误", data=None)
