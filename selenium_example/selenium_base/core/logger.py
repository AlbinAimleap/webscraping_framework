import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


def setup_logger(name, level=logging.DEBUG):
    date_fmt = "%Y-%m-%d-%H-%M-%S"
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=date_fmt,
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    logs_dir = Path(__file__).resolve().parent.parent.parent  / "logs"
    logs_dir.mkdir(exist_ok=True) 
       
    file_handler = logging.handlers.TimedRotatingFileHandler(
        logs_dir / f"{name}-{datetime.now().strftime('%Y-%m-%d')}.log",
        when='midnight',
        interval=1,
        backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=date_fmt
        )
    )
    logger.addHandler(file_handler)
    return logger

logger = setup_logger("selenium_logger")
    