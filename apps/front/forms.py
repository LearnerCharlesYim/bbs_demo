from ..forms import BaseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,Length,InputRequired,URL
from utils import zlcache
import memcache
from .models import FrontUser



class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式的手机号码！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式的短信验证码！'),InputRequired(message='请输入验证码！')])
    username = StringField(validators=[Regexp(r".{2,20}",message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1",message='两次输入的密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式验证码！'),InputRequired(message='请输入验证码！')])

    def validate_telephone(self,field):
        telephone = field.data
        # try:
        if FrontUser.query.filter_by(telephone=telephone).first():
            print(telephone)
            raise ValidationError(message='此手机号已经注册！')
        # except sqlalchemy.exc.IntegrityError:
            # raise ValidationError(message='此手机号已经注册！')


    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        # print(sms_captcha)
        telephone = self.telephone.data
        try:
            sms_captcha_mumber = zlcache.get(telephone)
            if not sms_captcha_mumber or sms_captcha_mumber.lower() != sms_captcha.lower():
                raise ValidationError(message='短信验证码错误！')
        except memcache.Client.MemcachedKeyCharacterError:
            raise ValidationError(message='短信验证码错误！')


    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        try:
            graph_captcha_number = zlcache.get(graph_captcha.lower())
            if not graph_captcha_number:
                raise ValidationError(message='图形验证码错误！')
        except memcache.Client.MemcachedKeyCharacterError:
            raise ValidationError(message='图形验证码错误！')


class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式验证码！'),InputRequired(message='请输入验证码！')])
    remember = StringField()

    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        try:
            graph_captcha_number = zlcache.get(graph_captcha.lower())
            if not graph_captcha_number:
                raise ValidationError(message='图形验证码错误！')
        except memcache.Client.MemcachedKeyCharacterError:
            raise ValidationError(message='图形验证码错误！')


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])
    author_id = StringField(validators=[InputRequired()])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])

class SettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    realname = StringField()
    avatar = StringField(validators=[URL(message=u'头像格式不对！')])
    signature = StringField()


