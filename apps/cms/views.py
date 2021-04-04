from flask import Blueprint,views,render_template,request,session,redirect,url_for,g
from .forms import LoginForm,ResetForm,ResetEmailForm,AddBannerForm,UpdateBannerForm,AddBoardForm,UpdateBoardForm,DeleteBoardForm
from .models import CMSUser,CMSPermission
from .decorators import login_required,permission_required
import config
from exts import db,mail
from utils import restful,zlcache
from flask_mail import Message
import string,random,re
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel
from flask_paginate import get_page_parameter,Pagination


bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email/')
def send_email():
    message = Message('邮件发送测试',recipients=['yanchicharles@gmail.com'],body='测试')
    mail.send(message)
    return 'success'


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if re.match('\w+@\w+\.[a-zA-Z\.]+', email) == None:
        return restful.params_error("请输入正确格式邮箱！")
    if email == g.cms_user.email:
        return restful.params_error('修改邮箱与当前邮箱相同！')

    source = list(string.ascii_letters)
    # source.extend(map(lambda x:str(x),range(0,10)))
    source.extend(['0','1','2','3','4','5','6','7','8','9'])
    captcha = "".join(random.sample(source,6))
    message = Message('BBS论坛验证码',recipients=[email],body='您的验证码是： %s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    zlcache.set(email,captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'posts':PostModel.query.order_by(PostModel.create_time.desc()).slice(start, end),
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html',**context)


#后台加精
@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


#后台取消加精
@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    boards_ = BoardModel.query.all()
    context = {
        'boards':boards_
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/fsuers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_roles.html')


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


#新增轮播图
@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

#修改轮播图
@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


#删除轮播图
@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请输入正确轮播图id！')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()

#新增板块
@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

#修改板块
@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())

#删除板块
@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    form = DeleteBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        if board_id:
            board = BoardModel.query.get(board_id)
            if board:
                db.session.delete(board)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='没有这个板块！')
        else:
            return restful.params_error(message='请输入正确板块id')
    else:
        return restful.params_error(message=form.get_error())




class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #默认过期时间31天
                    session.permanent = True
                # return redirect(url_for('cms.index'))
                return restful.success()
            else:
                return restful.params_error(message='邮箱或密码错误')
        else:
            return restful.params_error(message=form.get_error())

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误!")
        else:
            return restful.params_error(form.get_error())


class ResetEmail(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))
