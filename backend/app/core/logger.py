import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger("gitbrain")


logger = setup_logger()