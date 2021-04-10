from flask import Blueprint,request,make_response,jsonify
from exts import alidayu
from utils import restful,zlcache
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils.captcha import Captcha
from io import BytesIO
import qiniu


bp = Blueprint("common",__name__,url_prefix='/c')

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # ?telephone=xxx
#     # /c/sms_captcha/xxx
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码！')
#
#     captcha = Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         # return restful.params_error(message='短信验证码发送失败！')
#         return restful.success()


#阿里云短信服务接口
@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('发送的短信验证码是：',captcha)
        # 阿里云短信服务
        # if alidayu.send_sms(telephone,code=captcha):
        #     zlcache.set(telephone,captcha)
        #     return restful.success()
        # else:
        #     # return restful.params_error()
        #     zlcache.set(telephone,captcha)
        #     return restful.success()
        zlcache.set(telephone, captcha)
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = 'YPLYi40Ha-xVI90-Q-co1l1AE2ybS_7EHKyZ6TRe'
    secret_key = 'nwTHAsUQJUlm5fiq7ejNJTSXB7wCREox85sCYkb1'
    q = qiniu.Auth(access_key,secret_key)

    bucket = 'charlesyim'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})