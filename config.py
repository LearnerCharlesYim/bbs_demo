import os


DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'bbs_demo'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(24)


CMS_USER_ID = 'USER_ID'
FRONT_USER_ID = 'USER_ID'
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "409322382@qq.com"
MAIL_PASSWORD = "dmhslemhtwdpbjcj"
MAIL_DEFAULT_SENDER = "409322382@qq.com"


# 阿里大于相关配置
ALIDAYU_APP_KEY = ''
ALIDAYU_APP_SECRET = ''
ALIDAYU_SIGN_NAME = ''
ALIDAYU_TEMPLATE_CODE = ''


#配置Ueditor
# UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "YPLYi40Ha-xVI90-Q-co1l1AE2ybS_7EHKyZ6TRe"
UEDITOR_QINIU_SECRET_KEY = "nwTHAsUQJUlm5fiq7ejNJTSXB7wCREox85sCYkb1"
UEDITOR_QINIU_BUCKET_NAME = "charlesyim"
UEDITOR_QINIU_DOMAIN = "http://qqrkbrkwg.hd-bkt.clouddn.com/"



# flask-paginate的相关配置
PER_PAGE = 10