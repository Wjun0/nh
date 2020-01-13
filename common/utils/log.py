import logging,os


def create_logger(app):
    logging_file_dir = app.config['LOGGING_FILE_DIR']

    flask_app_log = logging.getLogger('flask.app')

    flask_app_log.setLevel(logging.INFO)


    console_log_handler = logging.StreamHandler()  # 控制台处理器

    console_log_formatter = logging.Formatter(
        fmt='%(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s ')

    console_log_handler.setFormatter(console_log_formatter)

    flask_app_log.addHandler(console_log_handler)

    from logging.handlers import RotatingFileHandler

    file_log_handler = RotatingFileHandler(
        filename=os.path.join(logging_file_dir,'chat.log'),
        maxBytes=100 * 1024 * 1024,
        backupCount=10)


    file_log_format = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s  %(lineno)d %(message)s ')

    file_log_handler.setFormatter(file_log_format)

    # 单独设置文件日志的级别
    # file_log_handler.setLevel(logging.INFO)
    flask_app_log.addHandler(file_log_handler)