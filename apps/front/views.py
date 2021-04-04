from flask import Blueprint,render_template,views,request,session,url_for,abort,g,redirect
from exts import alidayu,db
from .forms import SignupForm,LoginForm,AddPostForm,AddCommentForm,SettingsForm
from utils import restful,safeutils
from .models import FrontUser
import config,time
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel,PostStarModel,CommentStarModel
from .decorators import login_required
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func
from utils import profile_defs



bp = Blueprint("front",__name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get('st',type=int,default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards_ = BoardModel.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = None
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = db.session.query(PostModel).outerjoin(PostStarModel).group_by(PostModel.id).order_by(func.count(PostStarModel.id).desc(),PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()

    pagination = Pagination( bs_version=3,page=page,total=total,outer_window=0,inner_window=2)

    context = {
        'banners': banners,
        'boards': boards_,
        'posts':posts,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html',**context)

@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.login'))

@bp.route('/profile/')
@login_required
def profile():
    user = g.front_user
    context = {
        'user':user
    }
    return render_template('front/front_profile.html',**context)


@bp.route('/profile/posts')
@login_required
def profile_posts():
    user = g.front_user
    context = profile_defs.user_post_details(user)
    return render_template('front/front_profile_posts.html',**context)


@bp.route('/profile/posts/r')
@login_required
def profile_posts_r():
    user = g.front_user
    context = profile_defs.user_comments_detail(user)
    return render_template('front/front_profile_posts.html',**context)


@bp.route('/profile/posts/s')
@login_required
def profile_posts_s():
    user = g.front_user
    context = profile_defs.user_poststars_detail(user)
    return render_template('front/front_profile_posts.html',**context)


@bp.route('/u/<id>')
def user_profile(id):
    user = FrontUser.query.get(id)
    context = {
        'user':user
    }
    return render_template('front/front_profile.html',**context)


@bp.route('/u/<id>/posts')
def user_profile_posts(id):
    current_user = FrontUser.query.get(id)
    context = profile_defs.user_post_details(current_user)
    return render_template('front/front_profile_posts.html',**context)


@bp.route('/u/<id>/r')
def user_profile_comments(id):
    current_user = FrontUser.query.get(id)
    context = profile_defs.user_comments_detail(current_user)
    return render_template('front/front_profile_posts.html',**context)


@bp.route('/u/<id>/s')
def user_profile_stars(id):
    current_user = FrontUser.query.get(id)
    context = profile_defs.user_poststars_detail(current_user)
    return render_template('front/front_profile_posts.html',**context)

@bp.route('/profile/replies')
def replies():
    user = g.front_user
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE

    #用户所有的评论
    comment_replies = []
    comments = user.comments
    for comment in comments:
        replies = comment.replies
        for reply in replies:
            comment_replies.append(reply)
    results = []
    index = 0
    for comment_reply in comment_replies:
        index += 1
        comment_post_id = comment_reply.post_id
        comment_id = comment_reply.id
        content = comment_reply.content
        create_time = comment_reply.create_time
        tup_reply = (comment_id,content, create_time,comment_post_id)
        results.append(tup_reply)


    def takeTime(elem):
        return elem[1]

    results.sort(key=takeTime,reverse=True)

    pagination = Pagination(bs_version=3, page=page, total=index, outer_window=0, inner_window=2)
    context = {
        'user':user,
        'replies':results[start:end],
        'pagination':pagination
    }
    return render_template('front/front_reply_me.html',**context)



@bp.route('/profile/replies/p')
def p_replies():
    user = g.front_user
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE

    # 用户所有的帖子评论
    post_replies = []
    posts = user.posts
    for post in posts:
        comments = post.comments
        for comment in comments:
            post_replies.append(comment)
    results = []
    index = 0
    for post_reply in post_replies:
        index += 1
        id = post_reply.id
        comment_post_id = post_reply.post_id
        content = post_reply.content
        create_time = post_reply.create_time
        tup_reply = (id,content, create_time,comment_post_id)
        results.append(tup_reply)

    def takeTime(elem):
        return elem[1]

    results.sort(key=takeTime, reverse=True)
    pagination = Pagination(bs_version=3, page=page, total=index, outer_window=0, inner_window=2)

    context = {
        'user':user,
        'p_replies':results[start:end],
        'pagination':pagination
    }
    return render_template('front/front_reply_me.html',**context)


@bp.route('/settings/',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingsForm(request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            avatar = form.avatar.data
            signature = form.signature.data
            user = FrontUser.query.get(g.front_user.id)
            user.username = username
            user.realname = realname
            user.avatar = avatar
            user.signature = signature
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())





#帖子详情
@bp.route('/post/<int:post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    post.read_count += 1
    db.session.commit()

    count = 0

    for comment in post.comments:
        count += 1
    if count > 5:
        comments = CommentModel.query.with_parent(post).order_by(CommentModel.create_time.desc())[:5]
        # comments = post.comments[:5]
    else:
        comments = CommentModel.query.with_parent(post).order_by(CommentModel.create_time.desc())[:count]
        # comments = post.comments[:count]

    star_author_ids = []
    # 获取这篇帖子所有点赞的作者id
    for star in post.stars:
        star_author_ids.append(star.author_id)
    #获取所有评论所有点赞作者id
    comments_infos = []
    for comment in comments:
        b = {}
        b['comment_id'] = comment.id
        b['comment_content'] = comment.content
        b['comment_createtime'] = comment.create_time
        b['comment_author_avatar'] = comment.author.avatar
        b['comment_author_username'] = comment.author.username
        if comment.father_comment:
            b['comment_father_comment_content'] = comment.father_comment.content
            b['comment_father_comment_author'] = comment.father_comment.author.username
        index = 0
        a = []
        for commentstar in comment.stars:
            index += 1
            a.append(commentstar.author_id)
        b['sum_stars'] = index
        b['star_author_id'] = a
        comments_infos.append(b)


    #测试
    # for comments_info in comments_infos:
    #     print(comments_info['star_author_id'])
    #     print('='*30)

    context = {
        'post':post,
        # 'comments':comments,
        'star_author_ids':star_author_ids,
        'comment_count':count,
        'comments_infos':comments_infos
    }
    #测试
    # names = []
    # for star_author_id in star_author_ids:
    #     name = FrontUser.query.get(star_author_id).username
    #     names.append(name)
    # print(names)
    return render_template('front/front_pdetail.html',**context)


#异步加载评论
@bp.route('/load_comment/')
def load_comment():
    global comment_father_author_name, comment_father_comment_content
    post_id = request.args.get('post_id')
    index = int(request.args.get('index'))
    post = PostModel.query.get(post_id)
    comments = CommentModel.query.with_parent(post).order_by(CommentModel.create_time.desc())
    sum = 0
    for comment in comments:
        sum += 1
    if index > sum - 1:
        return restful.params_error(message='没有更多了...')
    if index + 5 > sum - 1:
        comments = comments[index:sum]
    else:
        comments = comments[index:index+5]

    comments_info = []
    for comment in comments:
        comment_id = comment.id
        content = comment.content
        avatar = comment.author.avatar
        username = comment.author.username
        create_time = comment.create_time
        a = []
        for star in comment.stars:
            a.append(star.author_id)

        # timeArray = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(create_time.timetuple())
        sum = 0
        for star in comment.stars:
            sum += 1
        if comment.father_comment:
            comment_father_author_name = comment.father_comment.author.username
            comment_father_comment_content = comment.father_comment.content
            comment1 = {
                'comment_id':comment_id,
                'content':content,
                'avatar':avatar,
                'username':username,
                'create_time':timestamp,
                'comment_stars':sum,
                'conmment_like_authors':a,
                'comment_father_author_name':comment_father_author_name,
                'comment_father_comment_content':comment_father_comment_content

            }
        else:
            comment1 = {
                'comment_id': comment_id,
                'content': content,
                'avatar': avatar,
                'username': username,
                'create_time': timestamp,
                'comment_stars': sum,
                'conmment_like_authors': a,
            }
        comments_info.append(comment1)


    data = {
        'comments_info':comments_info,
        'logo_img':url_for('static',filename='common/images/logo.jpg')
        }
    return restful.success(data=data)


#写评论
@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            # 判断是否时子评论
            if (request.form.get('comment_id')):
                comment_id = request.form.get('comment_id')
                comment = CommentModel(content=content,father_comment_id=comment_id)
            else:
                comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这篇帖子')

    else:
        return restful.params_error(message=form.get_error())


#发帖
@bp.route('/add_post/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            author_id = form.author_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title,content=content,author_id=author_id)
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


#帖子点赞
@bp.route('/astar/',methods=['GET','POST'])
@login_required
def astar():
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        post_id = request.form.get("post_id")
        poststar = PostStarModel(author_id=user_id,post_id=post_id)
        db.session.add(poststar)
        db.session.commit()
        post = PostModel.query.get(post_id)
        sum = 0
        for star in post.stars:
            sum += 1
        data={
            "sum":sum
        }
        return restful.success(data=data)


#取消帖子点赞
@bp.route('/dstar/',methods=['GET','POST'])
@login_required
def dstar():
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        post_id = request.form.get("post_id")
        poststar = PostStarModel.query.filter_by(post_id=post_id,author_id=user_id).first()
        db.session.delete(poststar)
        db.session.commit()
        post = PostModel.query.get(post_id)
        sum = 0
        for star in post.stars:
            sum += 1
        data = {
            "sum": sum
        }
        return restful.success(data=data)


#评论点赞
@bp.route('/like_comment/',methods=['GET','POST'])
@login_required
def like_comment():
    if request.method == 'POST':
        author_id = request.form.get("user_id")
        comment_id = request.form.get("comment_id")
        commentstar = CommentStarModel(author_id=author_id,comment_id=comment_id)
        db.session.add(commentstar)
        db.session.commit()
        comment = CommentModel.query.get(comment_id)
        sum = 0
        for star in comment.stars:
            sum += 1
        data = {
            "sum":sum
        }
        return restful.success(data=data)



#取消评论点赞
@bp.route('/dislike_comment/',methods=['GET','POST'])
@login_required
def dislike_comment():
    if request.method == 'POST':
        author_id = request.form.get("user_id")
        comment_id = request.form.get("comment_id")
        commentstar = CommentStarModel.query.filter_by(author_id=author_id,comment_id=comment_id).first()
        db.session.delete(commentstar)
        db.session.commit()
        comment = CommentModel.query.get(comment_id)
        sum = 0
        # print(comment.stars)
        for star in comment.stars:
            sum += 1
        data = {
            "sum":sum
        }
        return restful.success(data=data)


@bp.route('/load_reply/')
@login_required
def load_reply():
    comment_id = request.args.get('comment_id',type=int)
    comment = CommentModel.query.get(comment_id)
    comment_author = comment.author.username
    comment_content = comment.content
    data = {
        'comment_author' : comment_author,
        'comment_content'  : comment_content
    }

    return restful.success(data=data)




# @bp.route('/sms_captcha/')
# def sms_captcha():
#     result = alidayu.send_sms('17107807634',code='test')
#     if result:
#         return '发送成功!'
#     else:
#         return '发送失败!'

class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')


    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            session[config.FRONT_USER_ID] = user.id
            return_to = request.referrer
            if return_to and return_to != request.url and return_to != url_for('front.login') and safeutils.is_safe_url(return_to):
                referrer = return_to
                data = {
                    'referrer': referrer
                }
                return restful.success(data=data)
            else:
                return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

class LoginView(views.MethodView):
    def get(self):
        if config.FRONT_USER_ID in session:
            return redirect(url_for('front.index'))
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
            return render_template('front/front_login.html', return_to=return_to)
        else:
            return render_template('front/front_login.html')


    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
