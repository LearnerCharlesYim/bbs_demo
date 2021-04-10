from flask import Blueprint,views,render_template,request,session,redirect,url_for,g
from .forms import LoginForm,ResetForm,ResetEmailForm,AddBannerForm,UpdateBannerForm,AddBoardForm,UpdateBoardForm,DeleteBoardForm,AddCMSUser,AddRoleForm,EditRoleForm
from .models import CMSUser,CMSPermission,CMSRole
from .decorators import login_required,permission_required
import config
from exts import db,mail
from utils import restful,zlcache
from flask_mail import Message
import string,random,re
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel,PostStarModel,CommentModel,CommentStarModel
from flask_paginate import get_page_parameter,Pagination
from apps.front.models import FrontUser
from sqlalchemy.sql import func
from functools import reduce

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
    sort = request.args.get('sort',type=int,default=1)
    board_id = request.args.get('board',type=int,default=0)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(PostStarModel).group_by(PostModel.id).order_by(func.count(PostStarModel.id).desc(), PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()


    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'boards':BoardModel.query.all(),
        'posts':posts,
        'pagination': pagination,
        'c_sort':sort,
        'c_board':board_id
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


#删帖
@bp.route('/dpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")
    db.session.delete(post)
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

#评论
@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    sort = request.args.get('sort', type=int, default=1)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = None
    if sort == 1:
        query_obj = CommentModel.query.order_by(CommentModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(CommentModel).outerjoin(CommentStarModel).group_by(CommentModel.id).order_by(func.count(CommentStarModel.id).desc(),CommentModel.create_time.desc())

    start = (page - 1) * config.PER_PAGE
    total = query_obj.count()
    comments = query_obj.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'comments': comments,
        'pagination': pagination,
        'c_sort':sort
    }
    return render_template('cms/cms_comments.html', **context)


#删除评论
@bp.route('/dcomment/',methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def dcomment():
    comment_id = request.form.get('comment_id')
    comment = CommentModel.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='没有此评论！')

#搜索评论
@bp.route('/comments/search/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def search_c():
    kw = request.args.get('kw',default='').strip()
    print(kw)
    comments = CommentModel.query.filter(CommentModel.content.contains(f'{kw}')).order_by(CommentModel.create_time.desc()).all()
    users = FrontUser.query.filter(FrontUser.username.contains(f'{kw}')).order_by(FrontUser.join_time.desc()).all()

    context = {
        'comments':comments,
        'users':users,
        'kw':kw
    }
    return render_template('cms/cms_search_comments.html',**context)


#板块信息
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    boards_ = BoardModel.query.all()
    context = {
        'boards':boards_
    }
    return render_template('cms/cms_boards.html',**context)


#前台用户列表
@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    sort = request.args.get('sort', type=int, default=1)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = None
    if sort == 1:
        query_obj = FrontUser.query.order_by(FrontUser.join_time.desc())
    elif sort == 2:
        query_obj = db.session.query(FrontUser).outerjoin(PostModel).group_by(FrontUser.id).order_by(func.count(PostModel.id).desc(),FrontUser.join_time.desc())

    elif sort ==3:
        query_obj = db.session.query(FrontUser).outerjoin(CommentModel).group_by(FrontUser.id).order_by(func.count(CommentModel.id).desc(),FrontUser.join_time.desc())
    start = (page - 1) * config.PER_PAGE
    total = query_obj.count()
    front_users = query_obj.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'front_users': front_users,
        'pagination': pagination,
        'c_sort':sort
    }
    return render_template('cms/cms_fusers.html', **context)


#操作前台用户
@bp.route('/fusers/edit/<id>',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fuser_edit(id):
    if request.method == 'GET':
        front_user = FrontUser.query.get(id)
        return render_template('cms/cms_edit_fusers.html',front_user=front_user)


#拉黑前台用户
@bp.route('/black_front_user/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def black_front_user():
    user_id = request.form.get('user_id')
    user_status = request.form.get('user_status')
    user = FrontUser.query.get(user_id)
    if user:
        if int(user_status):
            user.status = False
            db.session.commit()
            return restful.success()
        else:
            user.status = True
            db.session.commit()
            return restful.success()
    else:
        return restful.params_error('没有这个用户！')


#后台用户列表
@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = CMSUser.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'users': CMSUser.query.order_by(CMSUser.join_time.desc()).slice(start, end),
        'pagination': pagination
    }


    return render_template('cms/cms_cmsusers.html',**context)


#后台用户详细页面
@bp.route('/cusers/<id>')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cuser_detail(id):
    user = CMSUser.query.get(id)
    roles = CMSRole.query.all()
    return render_template('cms/cms_editcmsuser.html',user=user,roles=roles)


#修改后台用户信息权限
@bp.route('/cusers/edit/',methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def edit_cuser():
    user_id = request.form.get('user_id')
    roles = request.values.getlist('roles[]')
    user = CMSUser.query.get(user_id)
    if user:
        user.roles = []
        for item in roles:
            role = CMSRole.query.filter_by(id=int(item)).first()
            role.users.append(user)
            # user.roles.append(role)
        print(user.roles)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('没有此用户！')


#新增后台管理用户
@bp.route('/cuser/add/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def add_cuser():
    if request.method == 'GET':
        roles = CMSRole.query.all()
        return render_template('cms/cms_addcmsuser.html',roles=roles)
    else:
        form = AddCMSUser(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            roles = request.values.getlist('roles[]')
            user = CMSUser(email=email,username=username,password=password)
            db.session.add(user)
            if roles:
                for item in roles:
                    role = CMSRole.query.filter_by(id=int(item)).first()
                    user.roles.append(role)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


#拉黑后台用户
@bp.route('/cusers/black_cuser/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def black_cuser():
    user_id = request.form.get('user_id')
    status = request.form.get('status')
    user = CMSUser.query.get(user_id)
    if user:
        if int(status):
            user.status = False
            db.session.commit()
            return restful.success()
        else:
            user.status = True
            db.session.commit()
            return restful.success()
    else:
        return restful.params_error('没有这个用户！')


#新增角色用户组
@bp.route('/croles/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    if request.method =='GET':
        roles = CMSRole.query.order_by(CMSRole.permissions.desc()).all()
        return render_template('cms/cms_roles.html',roles=roles)
    else:
        form = AddRoleForm(request.form)
        if form.validate():
            name = form.name.data
            desc = form.desc.data
            permissions = request.values.getlist('permissions[]')
            if permissions:
                results = map(int, permissions)
                permissions = reduce(lambda x, y: x + y, results)
                role = CMSRole(name=name, desc=desc, permissions=permissions)
                db.session.add(role)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='请至少选择一项权限！')
        else:
            return restful.params_error(form.get_error())

#修改角色用户组
@bp.route('/roles/edit',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def roles_edit():
    form = EditRoleForm(request.form)
    if form.validate():
        name = form.name.data
        desc = form.desc.data
        id = request.form.get('id')
        permissions = request.values.getlist('permissions[]')
        if permissions:
            results = map(int, permissions)
            permissions = reduce(lambda x, y: x + y, results)
            role = CMSRole.query.get(id)
            if role:
                role.name = name
                role.desc = desc
                role.permissions = permissions
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='没有这个角色!')
        else:
            return restful.params_error(message='请至少选择一项权限')
    else:
        return restful.params_error(message=form.get_error())


#删除角色用户组
@bp.route('/croles/delete/',methods=['GET','POST'])
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def crole_delete():
    role_id = request.form.get('role_id')
    role = CMSRole.query.get(role_id)
    db.session.delete(role)
    db.session.commit()

    return restful.success()


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
                if user.status:
                    session[config.CMS_USER_ID] = user.id
                    if remember:
                        #默认过期时间31天
                        session.permanent = True
                    return restful.success()
                else:
                    return restful.params_error(message='您已被禁止登入，请于管理员联系！')
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
