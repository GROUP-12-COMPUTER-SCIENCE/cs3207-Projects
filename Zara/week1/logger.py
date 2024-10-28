# logger.py

import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

def log_symbols(symbol_table):
    logger.info("Symbol Table Entries:")
    for name, symbol in symbol_table.symbols.items():
        logger.info(f"{name}: {symbol}")
