def log(logger, s, beginning=False):
    log_info(logger, s, beginning)


def log_info(logger, s, beginning=False):
    s = "\b\b\b\b\b\b\b\b\b\b" + s
    if beginning:
        s = "\b" + s
    logger.info(s)