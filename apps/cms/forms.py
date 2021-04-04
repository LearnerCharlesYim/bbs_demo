from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式密码(6-20位字符)')])
    remember = IntegerField()

class ResetForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式密码(6-20位字符)')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式新密码(6-20位字符)')])
    newpwd2 = StringField(validators=[Length(6,20,message='请输入正确格式新密码(6-20位字符)'),EqualTo("newpwd",message='请确认两次输入密码一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度验证码')])
    def validate_captcha(self,field):
        captcha = field.data
        if self.email.data != '':
            email = self.email.data
            captcha_cache = zlcache.get(email)
            if not captcha_cache or captcha.lower() != captcha_cache.lower():
                raise ValidationError('邮箱验证码错误！')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图id！')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])

class UpdateBoardForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id!')])
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])

class DeleteBoardForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id!')])
