from exts import db
from datetime import datetime


#轮播图模型
class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)


#板块模型
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


#帖子模型
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    read_count = db.Column(db.Integer,default=0)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)


    board = db.relationship("BoardModel",backref="posts")
    author = db.relationship("FrontUser",backref='posts')



#加精模型
class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    create_time = db.Column(db.DateTime,default=datetime.now)
    post = db.relationship("PostModel",backref=db.backref("highlight",cascade='all'))


#评论模型
class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"),nullable=False)
    father_comment_id = db.Column(db.Integer,db.ForeignKey("comment.id"))

    post = db.relationship("PostModel",backref=db.backref('comments',cascade='all'))
    author = db.relationship("FrontUser",backref='comments')

    father_comment = db.relationship("CommentModel",backref=db.backref("replies",cascade='all'),remote_side=[id])


#帖子点赞模型
class PostStarModel(db.Model):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

    author_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    author = db.relationship('FrontUser',backref='stars')
    post = db.relationship('PostModel',backref=db.backref('stars',cascade='all'))



#评论点赞模型
class CommentStarModel(db.Model):
    __tablename__ = 'comment_star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    author = db.relationship('FrontUser', backref=db.backref('comment_stars',cascade='all'))
    comment = db.relationship('CommentModel', backref=db.backref('stars',cascade='all'))

