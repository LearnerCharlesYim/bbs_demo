from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db,mail,alidayu
from flask_wtf import CSRFProtect
from datetime import datetime
import re

#配置文件config.py /exts.py /models.py/manage.py
#前台 后台 公共

def create_app():
    app = Flask(__name__)

    @app.template_filter('comment_sum')
    def comments_sum(post):
        comments = post.comments
        index = 0
        for comment in comments:
            index += 1
        return index

    @app.template_filter('handle_time')
    def handle_time(time):
        """
        time距离现在的时间间隔
        1. 如果时间间隔小于1分钟以内，那么就显示“刚刚”
        2. 如果是大于1分钟小于1小时，那么就显示“xx分钟前”
        3. 如果是大于1小时小于24小时，那么就显示“xx小时前”
        4. 如果是大于24小时小于30天以内，那么就显示“xx天前”
        5. 否则就是显示具体的时间 2017/10/20 16:15
        """
        if isinstance(time, datetime):
            now = datetime.now()
            timestamp = (now - time).total_seconds()
            if timestamp < 60:
                return "刚刚"
            elif timestamp >= 60 and timestamp < 60 * 60:
                minutes = timestamp / 60
                return "%s分钟前" % int(minutes)
            elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
                hours = timestamp / (60 * 60)
                return '%s小时前' % int(hours)
            # elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
            #     days = timestamp / (60 * 60 * 24)
            #     return "%s天前" % int(days)
            else:
                # return time.strftime('%Y/%m/%d %H:%M')
                return time.strftime('%m-%d %H:%M')
        else:
            return time

    @app.template_filter('stars')
    def stars(star_author_ids):
        index = 0
        for star_author_id in star_author_ids:
            index += 1
        return index

    @app.template_filter('likes')
    def likes(post):
        sum = 0
        for star in post.stars:
            sum += 1
        return sum

    #过滤html字符以及限制长度
    @app.template_filter('simple')
    def simple(text):
        if re.search(r'<img.*?>', text):
            text = re.sub(r'<img.*?>','[图片]',text)
        ret = re.sub(r'<.*?>','',text)
        if len(ret) >= 50:
            ret = ret[:50] + '...'
        return ret


    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    alidayu.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()





