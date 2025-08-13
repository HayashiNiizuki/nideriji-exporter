import logging


def init():
    logger = logging.getLogger("exporter")
    logger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("./exporter.log", encoding="utf-8")
    streamhandler = logging.StreamHandler(stream=None)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fileHandler.setFormatter(formatter)
    streamhandler.setFormatter(formatter)

    # 添加处理器到 logger
    logger.addHandler(fileHandler)
    logger.addHandler(streamhandler)

    # 记录日志
    logger.info("Copyright (c) 2025 hayashi")

    return logger


LOG = init()
