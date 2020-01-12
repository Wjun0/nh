class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/test'  # 数据库地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 不追究数据库变化
    SQLALCHEMY_ECHO = False  # 是否打印底层SQL语句

    # redis配置
    REDIS_HOST = '192.168.59.128'
    REDIS_PORT = 6379

    #日志文件路径
    # LOGGING_FILE_DIR = 'flask\logs'


config_dict = {
    'dev': DefaultConfig
}
