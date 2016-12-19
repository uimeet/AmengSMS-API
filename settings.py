# coding=utf-8

import web
from web.utils import storage

web.config.debug = True

# ====== 数据库相关配置 ======
DATABASES = storage(
    # 核心库
    core=storage(
        master=storage(
            db='amengsms',
            user='root',
            pw='163888',
            host='127.0.0.1',
            port=3306,
        ),
        slaves=[
        ],
    ),
)


# ====== 缓存配置 ======
CACHED = storage(
    # 使用的缓存驱动
    DRIVER='File',
    # 缓存驱动的选项
    OPTIONS=storage(
        # 文件缓存使用的缓存目录
        ROOT = 'runtime/cache',
        # 缓存使用的主机地址
        HOSTS=['hls.mydomain.com:11211', ],
        # sasl 用户名
        SASL_NAME='7ed3364ad62946cc',
        # sasl 密码
        SASL_PASSWORD='PAP6eim64mmwBw3M',
    ),
    # 是否启用页面缓存
    ENABLE_PAGE_CACHED=False,
)


# ############# 网站相关配置 ##############
# ====== 网站名称 ======
SITE_NAME = u'AmengSMS'
# 网站公司名
SITE_COMPANY = u'白鹿社'
# 网站口号
SITE_SLOGAN = u'Ameng Steaming Media System'
# 网站实例前缀
SITE_PREFIX = 'SM'

# ====== 域名 ======
# 主域名
SITE_DOMAIN = '127.0.0.1:8000'
# 接口域名
API_DOMAIN = '127.0.0.1:8080'
# 站点url前缀
SITE_URL_PREFIX = 'http://'


# ====== 服务器推相关配置 ======
COMET = storage(
    # 主机地址
    HOST = 'p.test.com',
    # 是否启用推送
    PUSH_ENABLED = True,
    # 管理端口
    ADMIN_PORT = 80,
    # 用户端口
    USER_PORT = 80,
)

# ====== 跨域域名配置 ======
CORS_DOMAINS = ('http://localhost:8000', 'http://127.0.0.1:8000',)

# ====== 聚合数据相关 ======
JUHE = storage(
    # IP 接口
    IP = storage(
        URL = 'http://apis.juhe.cn/ip/ip2addr?key=%s&dtype=json&ip=%s',
        KEY = '0f35ebef7ece58d65f98c80a8e0baebd',
    ),
)