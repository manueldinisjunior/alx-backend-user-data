#!/usr/bin/env python3
"""This module showcases industry standards for handling personal data/PII"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates/redacts a log message to filter out specified PII fields"""
    for field in fields:
        message = re.sub(rf'{field}=([^{separator}]+)',
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialises an instance of this class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact values in log record using filter_datum and format method of
        super class configured on this instance creation in __init__
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates a custom Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connection to a secure MySQL database"""
    # Fetch values from environment variables or use included defaults
    kwargs = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME', ''),
    }
    return mysql.connector.connect(**kwargs)


def main() -> None:
    """Retrieves data from db, redacts PII, then pretty prints each row"""
    # Fetch data from database then close connection
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    column_names = [val[0] for val in cursor.description]
    cursor.close()
    db.close()

    # Create Logger object then loop through users in data and log each
    logger = get_logger()
    for user in users:
        message = ''.join([f'{x}={y};' for x, y in zip(column_names, user)])
        logger.info(message)


if __name__ == '__main__':
    """Tests the code in this module"""
    main()
